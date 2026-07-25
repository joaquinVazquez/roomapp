from app.db.connection import SessionLocal
from app.db.seed import seed_roles, seed_dias_semana


def run():

    db = SessionLocal()

    try:
        seed_roles(db)
        seed_dias_semana(db)

    finally:
        db.close()


if __name__ == "__main__":
    run()