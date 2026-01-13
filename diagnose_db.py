import psycopg
import time

try:
    # Try multiple common users
    for user in ["postgres", "swarf", "root"]:
        try:
            print(f"Trying to connect as '{user}'...")
            with psycopg.connect(
                f"postgresql://{user}@localhost:5432/postgres", connect_timeout=2
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT current_user;")
                    result = cur.fetchone()
                    if result:
                        print(
                            f"Connected successfully as '{user}'! Current user in DB: {result[0]}"
                        )
                    else:
                        print(
                            f"Connected successfully as '{user}'! But could not fetch current user."
                        )
                    break
        except Exception as e:
            print(f"Failed for '{user}': {e}")
except Exception as e:
    print(f"Connection test failed: {e}")
