## Getting started (placed in backend dir):

### Installing everything (to run locally or to have editor support otherwise use docker):
    - Create virtual env: python -m venv .venv
    - Activate virtual env: source .venv/bin/activate
    - Upgrade pip if necessary: pip install --upgrade pip
    - Install requirements: pip install -r ./requirements.txt


### To update the requirements.txt with installed dependency: 
- pip freeze > ./requirements.txt


### Run the api:
- fastapi dev app/main.py


### Database Migrations:

- Always check the generated file and look at constraints, indexes, etc. to add names to them if they are not part of the naming dictionary.

## Inside the api container (if its being run with docker):
- create a revision (./src/alembic/versions/): alembic revision --autogenerate -m "migration name"
- make the migration: alembic upgrade head


## Using Docker compose:

### To run all the services with docker compose (using down to stop deletes everything):
- start: docker compose -f compose.yml up
- stop: docker compose -f compose.yml down

### Add the --build flag to rebuild images with latest code
docker compose -f compose.yml up --build

### Add the --project-name flag to give a custom name
- start: docker compose --project-name expense-app -f compose.yml up --build
- stop: docker compose --project-name expense-app -f compose.yml down


### When the container is running enter it with:
- docker exec -it expense-app bash


