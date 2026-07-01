from database import engine, SessionLocal
from models import Base, User
from auth import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin)
        db.commit()
        print("Admin user created: username=admin, password=admin123")
    
    db.close()

if __name__ == "__main__":
    init_db()