from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from askue_rs.settings import default

engine = create_engine(default)
base_test = declarative_base(bind=engine)
