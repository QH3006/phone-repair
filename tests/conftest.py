import os
import sys
import pytest

# Ensure backend can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Point to an isolated test database so tests NEVER pollute production phone_repair.db
TEST_DB_PATH = os.path.join(PROJECT_ROOT, "phone_repair_test.db").replace("\\", "/")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

from backend.app.db.database import Base, engine, SessionLocal
from backend.app.db.init_db import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_isolated_test_db():
    """Tự động khởi tạo database test riêng biệt cho mọi bài test."""
    Base.metadata.create_all(bind=engine)
    init_db()
    yield
