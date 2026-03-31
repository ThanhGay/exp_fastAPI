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
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    ALGORITHM = os.getenv("ALGORITHM")      
    SECRET_KEY :str = os.getenv("SECRET_KEY")

    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(", ")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")

    # Configuration for fastapi-mail
    MAIL_TLS: bool = os.getenv("MAIL_TLS")
    MAIL_SSL: bool = os.getenv("MAIL_SSL")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS")

    TEMPLATE_DIR = os.path.join(os.getcwd(), "app/templates/")

    @property
    def database_url(self) -> str:
        return (
            f"mariadb+pymysql://{self.MARIADB_USER}:{self.MARIADB_PASSWORD}"
            f"@{self.MARIADB_HOST}:{self.MARIADB_PORT}/{self.MARIADB_DATABASE}"
        )
       
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")

settings = Settings()
    