# Use an official Python image as base
FROM python:3.12.3-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app"]
