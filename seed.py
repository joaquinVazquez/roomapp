from app.db.session import SessionLocal
from app.db.seed import seed_roles

def run():
    db = SessionLocal()
    try:
        seed_roles(db)
        print("Roles creados correctamente")
    finally:
        db.close()

if __name__ == "__main__":
    run()