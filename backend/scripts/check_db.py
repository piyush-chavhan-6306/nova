from sqlalchemy import text
from app.core.database import engine

def check_db():
    try:
        conn = engine.connect()
        tables = [
            r[0] for r in conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            )
        ]
        print("Connected: True")
        print(f"Database URL: {engine.url}")
        print("PostgreSQL Tables and Record Counts:")
        for t in sorted(tables):
            cnt = conn.execute(text(f'SELECT count(*) FROM "{t}"')).scalar()
            print(f"  - {t}: {cnt} records")
        conn.close()
    except Exception as e:
        print("Connected: False")
        print("Error:", str(e))

if __name__ == "__main__":
    check_db()
