from sqlalchemy import create_engine, text
from .config import DATABASE_URL
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=1800, future=True)
def query(sql, params=None):
    with engine.connect() as conn:
        return conn.execute(text(sql), params or {}).mappings().all()
def execute(sql, params=None):
    with engine.begin() as conn:
        return conn.execute(text(sql), params or {})
def init_wait():
    import time
    for _ in range(40):
        try:
            with engine.connect() as c: c.execute(text('SELECT 1'))
            return
        except Exception: time.sleep(2)
    raise RuntimeError('MySQL did not become ready')