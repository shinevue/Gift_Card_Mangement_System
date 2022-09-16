FROM python:3.10.4-slim-bullseye
RUN apt-get update
RUN apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"
ENV APP_ENV=PROD
COPY ./ /app/
WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install
ENTRYPOINT ["gunicorn", "-w", "1", "--bind", "0.0.0.0:8000" , "gcmanager.app:create_app()"]
