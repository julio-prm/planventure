from app import app, db
# Import all models so they are registered with SQLAlchemy
from models.user import User
from models.trip import Trip
with app.app_context():
    db.create_all()
    print("Database tables created.")
