# Smart Diet Planner  

## Project Description  

The **Smart Diet Planner** helps users find personalized diet suggestions based on their **age, gender, weight, height, activity level, and goal**. The model utilizes data collected from the web to provide recommendations.  

This web application is built using **Flask** and features a user-friendly form where users can input their information. Based on the input, the system suggests **recommended calorie intake and meal plans** for **breakfast, lunch, and dinner**.  

### Features  

- **User Input Form**: Users can enter their **name, email, age, gender, weight, height, activity level, and goal**.  
- **Diet Recommendation**: The system provides **calorie intake suggestions** and a **personalized meal plan**.  
- **Database Integration**: Data is stored in **MySQL**, using tables such as `UserAccount`, `UserProfile`, `DietPlan`, and `UserDietRecommendation` to manage user information and recommendations.  

## Tech Stack  

- **Flask** – Web framework for handling requests and rendering HTML templates.  
- **MySQL** – Database for storing and retrieving user data.  
- **Jinja2** – Templating engine for rendering dynamic HTML in Flask.  
- **Python** – The primary language for backend logic.  
- **HTML/CSS** – Used for designing the front-end interface and user input form.  

## Setup Instructions  

### Prerequisites  

Ensure you have the following installed:  

- **Python 3.12.3**  
- **MySQL Server**  

#### [Python 3.12 Setup Guide](https://www.python.org/downloads/release/python-3123/)  

- Follow the link for installation instructions.  
- Ensure **Python is added to your system's PATH** during installation.  

#### [MySQL Setup Guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html)  

- Follow the link to install and set up **MySQL Server** on your system.  

### Create a Python Virtual Environment & Install Flask  

1. Open the command line and navigate to the project folder.  
2. Create a virtual environment:  
   ```bash
   python -m venv env
   ```  
3. Activate the virtual environment:  
   - On **Windows**:  
     ```bash
     env\Scripts\activate
     ```  
4. Install the required Python packages:  
   ```bash
   pip install -r requirements.txt
   ```  

### Database Setup in MySQL  

1. Open **MySQL Workbench**.  
2. In the **Menu bar**, click on **Database** → **Connect to Database**, then click **OK**.  
3. In the **Schemas** panel (left side), click the **+** button to create a new schema.  
4. Enter the desired **database name** and click **Apply**.  
5. Once created, **right-click** on the schema and select **Set as Default Schema**.  

### Update Database Credentials  

1. Open the `config.json` file in the project folder.  
2. Update the database credentials with your MySQL details:  

   ```json
   {
       "username": "your-mysql-username",
       "password": "your-mysql-password",
       "host": "localhost",
       "database": "diet_planner"
   }
   ```  

### Create Database Tables  

1. Ensure the **Python virtual environment** is activated:  
   ```bash
   env\Scripts\activate
   ```  
2. Run the following script to create the necessary tables:  
   ```bash
   python create_tables.py
   ```  

### Running the Project  

Once the setup is complete, start the Flask application:  

1. Ensure the **virtual environment** is activated.  
2. Run the application:  
   ```bash
   python app.py
   ```  
3. Open your browser and go to `http://127.0.0.1:5000` to access the **Smart Diet Planner**.  

## Usage  

1. Enter your details: **name, email, age, gender, weight, height, activity level, and goal**.  
2. Submit the form.  
3. The system will generate **recommended calorie intake** and a **meal plan** for **breakfast, lunch, and dinner** based on the provided information.  

## Future Enhancements  

- Improve the **recommendation model** with more advanced machine learning algorithms.  
- Add a feature to **save user recommendations** for more personalized suggestions.  
- Implement an **exercise recommendation system**.  

## Contributing  

We welcome contributions! Feel free to **fork the repository**, submit **issues**, and open **pull requests** with any improvements or features.  

## License  

This project is licensed under the **MIT License**.  

## Acknowledgments  

- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)  
- **MySQL Documentation**: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)  
