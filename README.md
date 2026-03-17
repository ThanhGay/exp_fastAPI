# FastAPI Sample: Login, Logout, View Items

A minimal FastAPI project to learn **authentication** (login/logout) and **protected routes** (view items).

## Setup

```bash
git clone 

# create virtural environment to run fastAPI
python -m venv venv 

# active venv
source venv/bin/activate

# install requirement package
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

## Run migrations (alembic)

Generate migration
```bash
python -m alembic revision --autogenerate -m "<migration_name>"
```

Apply migration into database
```bash
python -m alembic upgrade head
```
# exp_fastAPI
route -> service -> repository
