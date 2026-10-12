FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]