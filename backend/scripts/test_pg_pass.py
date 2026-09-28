import psycopg2

passwords = ["postgres", "admin", "root", "password", "123456", "1234", "", "nova", "nova_db"]
found = False

for p in passwords:
    try:
        conn = psycopg2.connect(user="postgres", password=p, host="localhost", port=5432, dbname="postgres")
        print(f"SUCCESS: PostgreSQL connected with password: '{p}'")
        found = True
        conn.close()
        break
    except Exception as e:
        pass

if not found:
    print("Could not connect to local PostgreSQL with common default passwords.")
