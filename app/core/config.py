import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env từ thư mục gốc project (cạnh main.py / pyproject.toml)
env_path = Path(__file__).resolve().parents[2] / ".env"


load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "QLY Ban Hang"
    PROJECT_VERSION: str = "1.0.0"

    # Database config (MariaDB)
    MARIADB_USER: str = os.getenv("MARIADB_USER", "root")
    MARIADB_PASSWORD: str = os.getenv("MARIADB_PASSWORD", "")
    MARIADB_HOST: str = os.getenv("MARIADB_HOST", "localhost")
    MARIADB_PORT: str = os.getenv("MARIADB_PORT", "3306")
    MARIADB_DATABASE: str = os.getenv("MARIADB_DATABASE", "ecommerce")
    
    # Token config
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    ALGORITHM = os.getenv("ALGORITHM")      
    SECRET_KEY :str = os.getenv("SECRET_KEY")

    @property
    def database_url(self) -> str:
        return (
            f"mariadb+pymysql://{self.MARIADB_USER}:{self.MARIADB_PASSWORD}"
            f"@{self.MARIADB_HOST}:{self.MARIADB_PORT}/{self.MARIADB_DATABASE}"
        )
       
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")

settings = Settings()
    