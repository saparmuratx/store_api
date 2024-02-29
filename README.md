# Inventory API - techstart_test

Test assignment for Backend developer 

Simple product inventory management system API built with Python and FastAPI

## Local Deployment With Docker

Deploying and testing made easy with use of Docker containerization.

### Before building

Create .env file

`cp .env.example .env`  

and set own environment variables.

### Building Docker Containers
- Build containers defined in `Dockerfile` and `docker-compose.yaml`:
```shell
docker compose up -d --build
```

### Tests
All tests are integrational and require DB connection. 

Tests will run on `postgres` default database instead of `app` database.

Defined in `.env`:

```shell
TEST_DATABASE_URL=postgresql://app:app@app_db:5432/postgres
```

### Run Tests
- All tests are defined in `src/tests/test_inventory.py`
```shell
docker compose exec api pytest
```

## Rebuild API after changes
- Destroy running containers
```shell
docker compose down
# and rebuild it
docker compose up -d --build
```


## Structure
```
├── src
│   ├── inventory               
│   │   ├── crud.py     # CRUD functions
│   │   ├── models.py   # SQLAlchemy models
│   │   ├── schemas.py  # Pydantic models
│   │   └── router.py   # router
|   |
│   ├── tests
│   │   └── test_inventory.py   # unit tests 
│   │ 
│   ├── main.py         # projects main file 
│   ├── database.py     # db connection and session
│   └── config.py       # global configs
│  
├── .env                # Environment variables
├── Dockerfile                 
└── docker-compose.yaml         
```

## API

#### /inventory/establishments/
* `GET` : get all establishments
* `POST` : create a new establishment

#### /inventory/establishments/{establishment_id}/
* `GET` : Get establishment
* `PUT` : Update establishment
* `DELETE` : Delete establishment
