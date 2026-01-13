import reflex as rx
import os
from pathlib import Path

# Data directory for PGLite
data_dir = Path("pgdata")
data_dir.mkdir(exist_ok=True)

# Connection string for PGLite
# Note: We expect the PGlite manager to be managed via a separate lifecycle or simply start it if needed.
# For Reflex, we can use a local sqlite for easier dev, or a fixed pglite path.
# py-pglite provides a way to get the DSN.

# To keep it simple and ensure reflex run works, we'll use TCP on 5432
db_url = "postgresql+psycopg://swarf@localhost:5432/postgres"

config = rx.Config(
    app_name="english_tutor",
    db_url=db_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
