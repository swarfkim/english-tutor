import reflex as rx
from py_pglite import PGliteManager, PGliteConfig
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)


class DBManager:
    _manager = None

    @classmethod
    def start(cls):
        if cls._manager is not None:
            return

        data_dir = Path("pgdata")
        data_dir.mkdir(exist_ok=True)

        config = PGliteConfig(
            work_dir=data_dir,
            cleanup_on_exit=False,
            use_tcp=True,
            tcp_port=5432,
            timeout=60,
        )

        # Check if the socket already exists. PGlite handles this usually,
        # but we want to be safe across reloads.
        cls._manager = PGliteManager(config)
        try:
            logger.info("Starting PGlite server...")
            cls._manager.start()

            # Custom wait loop since manager.wait_for_ready() defaults to 'postgres' user
            # and we are running as 'swarf'.
            import time
            import psycopg

            logger.info("Waiting for database to be ready...")
            for i in range(30):
                try:
                    # Connect as swarf
                    with psycopg.connect(
                        "postgresql://swarf@localhost:5432/postgres", connect_timeout=1
                    ) as conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT 1")
                    logger.info("PGlite server is ready (connection verified).")
                    break
                except Exception:
                    time.sleep(0.5)
            else:
                logger.error("Failed to connect to PGlite after retries.")
        except Exception as e:
            logger.error(f"Failed to start PGlite: {e}")
            # If it failed because it's already running, we might be okay
            pass

    @classmethod
    def stop(cls):
        if cls._manager:
            cls._manager.stop()
            cls._manager = None
