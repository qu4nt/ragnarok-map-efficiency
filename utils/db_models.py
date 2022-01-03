from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean

BASE_DIR = Path.cwd()

engine = create_engine('sqlite:///data/originsro.sqlite3', echo=True)
Base = declarative_base()
session = Session(bind=engine)

class Item(Base):
    __tablename__ = 'items'

    # Basic Info
    name = Column(String)
    item_id = Column(Integer, primary_key=True)
    type = Column(String)
    # Details
    weight = Column(Integer)
    npc_buy = Column(Integer)
    npc_sell = Column(Integer)
    refineable = Column(Boolean)
    equip_locations = Column(String)
    # Stats
    range = Column(Integer)
    defense = Column(Integer)
    attack = Column(Integer)
    weapon_level = Column(Integer)
    slots = Column(Integer)
    # Restrictions
    level_range = Column(String)
    usage = Column(String)
    trade = Column(String)
    job_class_types = Column(String)
    job_classes = Column(String)
    gender = Column(String)
    # Scripts
    use_script = Column(String)
    equip_script = Column(String)
    unequip_script = Column(String)


    def __repr__(self):
       return f"<Item(ID={self.item_id}, name={self.name}>"

# Base.metadata.create_all(engine)