FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
WORKDIR /app
COPY ./quiz/ /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
