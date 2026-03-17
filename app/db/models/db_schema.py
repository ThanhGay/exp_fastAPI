from enum import Enum

class DbSchema(str,Enum):
    AUTH="auth"
    PRODUCT="prod"
    ORDER="ord"
