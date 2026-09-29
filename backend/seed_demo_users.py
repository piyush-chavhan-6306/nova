import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal, engine, Base
import app.models
Base.metadata.create_all(bind=engine)

from app.models.user import User
from app.core.security import get_password_hash
from app.utils.enums import UserRole

db = SessionLocal()

demo_data = [
    ("usr_admin_001", "admin@nova.dev", "Platform Administrator", UserRole.ADMIN, "nova2026!"),
    ("usr_org_001", "organizer@nova.dev", "Alex Organizer", UserRole.ORGANIZER, "nova2026!"),
    ("usr_judge_001", "judge@nova.dev", "Dr. Ada Okonkwo", UserRole.JUDGE, "nova2026!"),
    ("usr_participant_001", "participant@nova.dev", "Priya Sharma", UserRole.PARTICIPANT, "nova2026!"),
]

for uid, email, name, role, password in demo_data:
    existing = db.query(User).filter(User.id == uid).first()
    if not existing:
        user = User(
            id=uid,
            email=email,
            name=name,
            role=role,
            hashed_password=get_password_hash(password)
        )
        db.add(user)
        print(f"Created: {email}")
    else:
        existing.hashed_password = get_password_hash(password)
        existing.name = name
        existing.role = role
        print(f"Updated password: {email}")

db.commit()
db.close()
print("Seed complete!")
