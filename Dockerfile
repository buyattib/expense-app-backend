FROM python:3.9

# set the working directory inside the container
WORKDIR /code

# copy the requirements file inside the container
COPY ./requirements.txt /code/requirements.txt
COPY ./alembic.ini /code/alembic.ini

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy the app code in the container
COPY ./app /code/app

# run in production mode
# CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

CMD ["fastapi", "dev", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]

