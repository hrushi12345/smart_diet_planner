from app import app, db

# Creates the tables defined in models
with app.app_context():
    db.create_all()
