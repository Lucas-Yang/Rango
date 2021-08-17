from app.common.db import MySQLClient, MyMongoClient
from app.common.logger import LogManager

logger = LogManager().logger
mongodb_client = MyMongoClient().db

