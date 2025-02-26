import json
import uuid
import urllib
import joblib
import numpy as np
import pandas as pd
import ast
from flask import Flask, request, jsonify, render_template
import pymysql
pymysql.install_as_MySQLdb()
from models import db, UserAccount, UserDietRecommendation, UserProfile

app = Flask(__name__)
# 🔹 Set a secret key for sessions and security
app.secret_key = "!@#$%QWER^&*()POIYTREWQ"  # Change this to a secure, random key

# Open and read the config file
with open('config.json', 'r') as file:
    data = json.load(file)
dbUserName = urllib.parse.quote_plus(data['username'])
dbPassword = urllib.parse.quote_plus(data['password'])
dbHost = data['host']
dbName = data['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUserName}:{dbPassword}@{dbHost}/{dbName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

label_encoders_path = "dataset_model_training/label_encoders.pkl"
# Open the file in binary mode and load the data
with open(label_encoders_path, 'rb') as file:
    label_encoders = joblib.load(file)

diet_recommendation_model_path = "dataset_model_training/diet_recommendation_model.pkl"
# Open the file in binary mode and load the data
with open(diet_recommendation_model_path, 'rb') as file:
    model = joblib.load(file)

reverse_mapping_path = "dataset_model_training/reverse_mapping.pkl"
# Open the file in binary mode and load the data
with open(reverse_mapping_path, 'rb') as file:
    reverse_mapping = joblib.load(file)

diet_plans = pd.read_csv("dataset_model_training/diet_plans_goal_based.csv")

def saveInDatabase(inputJson, recommended_diet):
    # Capture User Input
    email = inputJson["email"]
    name = inputJson["name"]
    age = int(inputJson["age"])
    gender = inputJson["gender"]
    weight = float(inputJson["weight"])
    height = float(inputJson["height"])
    activityLevel = inputJson["activityLevel"]
    goal = inputJson["goal"]

    # Create new user
    new_user = UserAccount(
        userId=str(uuid.uuid4()), email=email#, passwordHash=password
    )
    db.session.add(new_user)
    db.session.commit()

    # Create user profile
    new_profile = UserProfile(
        profileId=str(uuid.uuid4()),
        userId=new_user.userId,
        name=name,
        age=age,
        gender=gender,
        weight=weight,
        height=height,
        activityLevel=activityLevel,
        goal=goal
    )
    db.session.add(new_profile)
    db.session.commit()

    # Store Recommendation
    new_recommendation = UserDietRecommendation(
        recommendationId=str(uuid.uuid4()),
        userId=new_user.userId,
        dietPlanId=recommended_diet['dietPlanId']
    )
    db.session.add(new_recommendation)
    db.session.commit()


@app.route('/')
def home():

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form

        # Validate required fields
        required_fields = ['age', 'weight', 'height', 'activityLevel', 'goal']
        for field in required_fields:
            if field not in data:
                return f"Missing input field: {field}", 400

        # Convert numerical fields
        try:
            age = int(data['age'])
            weight = float(data['weight'])
            height = float(data['height'])
        except ValueError:
            return "Invalid input: Age must be an integer, Weight and Height must be numbers.", 400

        # Validate categorical fields
        if data['activityLevel'] not in label_encoders['activityLevel'].classes_:
            return f"Invalid activity level: {data['activityLevel']}", 400

        if data['goal'] not in label_encoders['goal'].classes_:
            return f"Invalid goal: {data['goal']}", 400

        # Encode categorical values
        activity_level_encoded = label_encoders['activityLevel'].transform([data['activityLevel']])[0]
        goal_encoded = label_encoders['goal'].transform([data['goal']])[0]

        # Create input array
        user_input = np.array([[age, weight, height, activity_level_encoded, goal_encoded]])

        # Make prediction
        predicted_idx = model.predict(user_input)[0]
        
        predicted_diet_id = str(reverse_mapping.get(predicted_idx))
        
        if predicted_diet_id is None:
            return "No suitable diet plan found", 404

        # Ensure dietPlanId is a string for matching
        diet_plans['dietPlanId'] = diet_plans['dietPlanId'].astype(str)

        # Retrieve matching diet plan
        matching_diet = diet_plans[diet_plans['dietPlanId'] == predicted_diet_id]

        if matching_diet.empty:
            return "No matching diet plan found", 404

        recommended_diet = matching_diet.iloc[0]
        # print("Raw meal plan data:", recommended_diet['mealPlan'])  # Debugging

        # Try parsing the meal plan
        meal_plan_str = recommended_diet['mealPlan'].strip()
        try:
            meal_plan = json.loads(meal_plan_str.replace("'", '"'))  # Convert single quotes to double quotes
        except json.JSONDecodeError:
            try:
                meal_plan = ast.literal_eval(meal_plan_str)  # Try as Python dict
            except (ValueError, SyntaxError) as e:
                return f"Error parsing meal plan data: {str(e)}", 500

        saveInDatabase(data, recommended_diet)

        return render_template('result.html', 
                               name=recommended_diet['name'], 
                               description=recommended_diet['description'], 
                               recommendedCalories=recommended_diet['recommendedCalories'], 
                               mealPlan=meal_plan)

    except Exception as e:
        print("Error occurred:", str(e))  # Log error
        return f"An unexpected error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
