import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load datasets
user_profiles = pd.read_csv("dataset_model_training/user_profiles.csv")
diet_plans = pd.read_csv("dataset_model_training/diet_plans_goal_based.csv")

# Print unique values before mapping (Debugging Step)
print("Unique goals in user_profiles:", user_profiles['goal'].unique())
print("Unique goals in diet_plans:", diet_plans['goal'].unique())

# Initialize label encoders
label_encoders = {
    'activityLevel': LabelEncoder(),
    'goal': LabelEncoder()
}

# Fit encoders with actual dataset values
user_profiles['activityLevel'] = label_encoders['activityLevel'].fit_transform(user_profiles['activityLevel'])
user_profiles['goal'] = label_encoders['goal'].fit_transform(user_profiles['goal'])
diet_plans['goal'] = label_encoders['goal'].transform(diet_plans['goal'])  # Encode goals in diet plans

# Verify encoding success
print("Encoded activityLevel:", user_profiles['activityLevel'].unique())
print("Encoded goal:", user_profiles['goal'].unique())

# Create a mapping from goal (encoded) to dietPlanId
diet_plan_mapping = diet_plans.set_index("goal")["dietPlanId"].to_dict()

# Ensure all goals in `user_profiles` exist in `diet_plans`
missing_goals = set(user_profiles['goal'].unique()) - set(diet_plans['goal'].unique())
if missing_goals:
    print(f"Warning: Missing goal mappings in diet_plans for {missing_goals}")

# Map goal to dietPlanId
user_profiles['dietPlanId'] = user_profiles['goal'].map(diet_plan_mapping)

# Handle missing values (Assign default dietPlanId)
default_diet_id = diet_plans['dietPlanId'].iloc[0]  # Assign first available diet plan
user_profiles['dietPlanId'] = user_profiles['dietPlanId'].fillna(default_diet_id)

# Encode dietPlanId as integers
diet_plan_ids = user_profiles['dietPlanId'].unique()
diet_plan_id_mapping = {diet_id: idx for idx, diet_id in enumerate(diet_plan_ids)}
reverse_mapping = {idx: diet_id for diet_id, idx in diet_plan_id_mapping.items()}

# Replace dietPlanId with mapped integer values
user_profiles['dietPlanId'] = user_profiles['dietPlanId'].map(diet_plan_id_mapping)

# Features and target
X = user_profiles[['age', 'weight', 'height', 'activityLevel', 'goal']].values.astype(float)  # Ensure numeric
y = user_profiles['dietPlanId'].astype(int)  # Ensure integer

# Scale numerical features (improves model generalization)
scaler = StandardScaler()
X[:, :3] = scaler.fit_transform(X[:, :3])  # Normalize age, weight, height

# Ensure dataset is not empty
if len(X) == 0 or len(y) == 0:
    raise ValueError("Dataset is empty after processing. Please check input files.")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Check class distribution
print("Class distribution in training data:")
print(pd.Series(y_train).value_counts())  # Ensure balanced classes

# Train model with class balancing
model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced', max_depth=10)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "dataset_model_training/diet_recommendation_model.pkl")
joblib.dump(label_encoders, "dataset_model_training/label_encoders.pkl")
joblib.dump(reverse_mapping, "dataset_model_training/reverse_mapping.pkl")  # Save reverse mapping
joblib.dump(scaler, "dataset_model_training/scaler.pkl")  # Save scaler

print("Model training completed successfully!")
