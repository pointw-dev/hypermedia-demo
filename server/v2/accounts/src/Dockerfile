FROM python:3.11.4-slim

ENV HY_API_PORT=80
EXPOSE $HY_API_PORT

WORKDIR /api
COPY accounts-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY accounts-service .

CMD ["python", "run.py"]
