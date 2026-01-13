from py_pglite import PGliteManager, PGliteConfig
from pathlib import Path
import psycopg

data_dir = Path("pgdata_diag")
data_dir.mkdir(exist_ok=True)
config = PGliteConfig(work_dir=data_dir, cleanup_on_exit=True)
manager = PGliteManager(config)

print("Starting PGlite...")
manager.start()
if manager.wait_for_ready():
    print("PGlite is ready!")
    dsn = config.get_connection_string(driver="psycopg")
    print("DSN:", dsn)
    standard_dsn = dsn.replace("+psycopg", "")
    try:
        with psycopg.connect(standard_dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_user, session_user;")
                result = cur.fetchone()
                if result:
                    u1, u2 = result
                    print(f"Current user: {u1}, Session user: {u2}")
                else:
                    print("Could not fetch current and session users.")
                cur.execute("SELECT usename FROM pg_user;")
                users = [r[0] for r in cur.fetchall()]
                print(f"All users: {users}")
    except Exception as e:
        print(f"Failed to query users: {e}")
    manager.stop()
else:
    print("PGlite failed to start.")
