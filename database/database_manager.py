from typing import Optional
from common.config import config
from common.log import log
from database.mongodb import MongoDB

class Database:
    """
    Database factory class that manages the initialization of the database engine.
    Currently only supports MongoDB.
    """
    def __init__(self, database_type: str):
        self.database: Optional[MongoDB] = None

        if database_type in ["mongo", "mongodb"]:
            self.database = MongoDB(
                host=config.mongodb_host,
                port=config.mongodb_port,
                username=config.mongodb_user,
                password=config.mongodb_password,
                database_name=config.mongodb_database,
                tls=config.mongodb_tls,
                srv=config.mongodb_srv,
                auth_source=config.mongodb_auth_source
            )
        else:
            log.error(f"The database {database_type} could not be found.")

    def get_database(self) -> Optional[MongoDB]:
        if not self.database:
            log.error(
                "[Database] No database is currently present. It is advised against proceeding in this state."
            )
        return self.database
