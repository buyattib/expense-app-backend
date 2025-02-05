# Getting started (in backend dir):


## Installing everything (to have editor support):
    - Create virtual env: python -m venv .venv
    - Activate virtual env: source .venv/bin/activate
    - Upgrade pip if necessary: pip install --upgrade pip
    - Install requirements: pip install -r ./requirements.txt



## Run the app (need to install docker and docker compose):
- start: docker compose --project-name expense-app -f compose.yml up --build
- stop: docker compose --project-name expense-app -f compose.yml down

To test:
- start with watch: docker compose --project-name expense-app -f compose.yml up --build --watch



## Update the requirements.txt when installing dependencies: 
- pip freeze > ./requirements.txt



## Database Migrations:
- Migrations are controlled sets of changes developed to modify the structure of the objects within a relational database. They help transition database schemas from their current state to a new desired state. This means
that a migration handles the changes on the code (the schema) and applies it to the database.

- Always check the generated file and look at constraints, indexes, etc. to add names to them if they are not part of the naming dictionary.

### Inside the api container:
- create a revision (a new file is going to be created at ./app/alembic/versions/): alembic revision --autogenerate -m "migration name"
- make the migration: alembic upgrade head



## PgAdmin:

### To connect to the db in pgadmin (containerized and running in localhost:5050):
- hostname: expense-app-pg (container name)
- port: 5432 (container port)
- database: db name
- username: (pg username)
- password: (pg password)

### To connect to the db in pgadmin (external):
- hostname: localhost
- port: 5432
- database: db name
- username: (pg username)
- password: (pg password)



## Docker:
When using docker compose, an internal network for the containers is created.
If not stoping the containers with down command, the containers, images, networks and volumes are not deleted.

- When the container is running enter it with: docker exec -it expense-app bash
- List running containers: docker container ls
- List all containers: docker container ls -a
- Remove a container: docker container rm <container_id>
- List images: docker image ls
- Remove an image: docker image rm <image_id>
- List networks: docker network ls
- Remove network: docker network rm <network_id>
- List volumes: docker volume ls
- Remove volume: docker volume rm <volume_id>
