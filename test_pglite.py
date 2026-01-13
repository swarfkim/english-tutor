from py_pglite import PGliteManager, PGliteConfig
from pathlib import Path
import time

data_dir = Path("pgdata_test")
data_dir.mkdir(exist_ok=True)
config = PGliteConfig(
    work_dir=data_dir, cleanup_on_exit=True, timeout=60, use_tcp=True, tcp_port=5432
)
manager = PGliteManager(config)

print("Starting PGlite...")
manager.start()
if manager.wait_for_ready():
    print("PGlite is ready!")
    print("DSN:", config.get_connection_string())
    print("Keeping server alive for diagnosis... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop()
else:
    print("PGlite failed to start.")
