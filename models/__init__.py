#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

storage_t = getenv("AGRO_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
storage.reload()
