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

Build containers defined in `Dockerfile` and `docker-compose.yaml`:

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

```shell
docker compose exec api pytest
```

All test cases are defined in `src/tests/test_inventory.py`

### Rebuilding API after changes

```shell
# Destroy running containers
docker compose down
# and rebuild them
docker compose up -d --build
```

### Project Structure

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

## Documentation and Request Examples

Documentation with **Swagger UI** is located in `http://localhost:8000/docs` 

alternatively **ReDoc** `http://localhost:8000/redoc`

### Establishments

#### Create Establishment

`POST` : `http://localhost:8000/inventory/establishments`

Body

```json
{
    "name": "Galata headquarters",
    "description": "Ottoman Brotherhood main quarters",
    "location": "Constantinople",
    "opening_hours": "09:30:00",
}
```

Response

```json
{
    "name": "Galata headquarters",
    "description": "Ottoman Brotherhoods main quarters",
    "location": "Constantinople",
    "opening_hours": "09:30:00",
    "id": 1
}
```

#### List Establishments

`GET` : `/inventory/establishments/?skip=0&limit=100`

Use path parameters for pagination:

`skip` : number of establishments to skip, starting from the beginning

`limit` : number of establishments to retrieve

Response

```json
[
    {
        "name": "Galata headquarters",
        "description": "Ottoman Brotherhood main quarters",
        "location": "Constantinople",
        "opening_hours": "09:30:00",
        "id": 1,
        "items": []
    },
    {
        "name": "Alamut",
        "description": "Assasin's Global HQ",
        "location": "Qazvin Plain",
        "opening_hours": "09:00:00",
        "id": 2,
        "items": []
    }
]
```

#### Read Establishment

`GET` : `/inventory/establishments/{establishment_id}/`

Response

```json
{
    "name": "Baghdad HQ",
    "description": "Baghdad Brotherhood office",
    "location": "Baghdad City",
    "opening_hours": "10:00:00",
    "id": 1,
    "items": [
        {
            "name": "Hidden Blade Baghdad Steel",
            "description": "Deadly Assasin's weapon with faster retractor",
            "price": 250.0,
            "quantity": 420,
            "id": 1,
            "establishment_id": 6
        },
        {
            "name": "Mamluk Armour",
            "description": "Heavy armour",
            "price": 420.0,
            "quantity": 69,
            "id": 2,
            "establishment_id": 6
        }
    ]
}
```

#### Update Establishment

`PUT` : `/inventory/establishments/{establishment_id}/`

Body

```json
{
    "description": "Isntanbul Brotherhood main quarters",
    "location": "Istanbul city",
}
```

Response

```json
{
    "name": "Galata headquarters",
    "description": "Isntanbul Brotherhood main quarters",
    "location": "Istanbul city",
    "opening_hours": "09:30:00",
    "id": 1
}
```

#### Delete Establishment

`DELETE` : `/inventory/establishments/{establishment_id}/`

```json
returns 204 No Content
```

### Products aka Items

#### Create Item

`POST` : `http://localhost:8000/inventory/establishments/{establishment_id}/items/`

Body

```json
{
    "name": "Hidden Blade Damascus",
    "description": "Deadly Assasin's weapon",
    "price": 150.0,
    "quantity": 69
}
```

Response

```json
{
    "name": "Hidden Blade Damascus",
    "description": "Deadly Assasin's weapon",
    "price": 150.0,
    "quantity": 69,
    "id": 1,
    "establishment_id": 1
}
```

#### List Items

`GET` : `/inventory/items/?skip=0&limit=100`

Use path parameters for pagination:

`skip` : number of items to skip, starting from the beginning

`limit` : number of items to retrieve

Response:

```json
[
    {
        "name": "Hidden Blade Baghdad Steel",
        "description": "Forged by master Assasins",
        "price": 430.0,
        "quantity": 420,
        "id": 3,
        "establishment_id": 2
    },
    {
        "name": "Hidden Blade Damascus",
        "description": "Deadly weapon of Assasin's",
        "price": 150.0,
        "quantity": 69,
        "id": 4,
        "establishment_id": 2
    }
]
```

#### Read Item

`GET` : `/inventory/items/{item_id}/`

Response

```json
{
    "name": "Hidden Blade Baghdad Steel",
    "description": "Deadly Assasin's weapon with faster retractor",
    "price": 250.0,
    "quantity": 420,
    "id": 3,
    "establishment_id": 2
}
```

#### Update Item

`PUT` : `/inventory/items/{item_id}/`

Body

```json
{
    "price": 430.0,
    "description": "Forged by master Assasin's"
}
```

Response

```json
{
    "name": "Hidden Blade Baghdad Steel",
    "description": "Forged by master Assasin's",
    "price": 430.0,
    "quantity": 420,
    "id": 3,
    "establishment_id": 2
}
```

#### Delete Item

`DELETE` : `/inventory/items/{item_id}/`

```json
returns 204 No Content
```
