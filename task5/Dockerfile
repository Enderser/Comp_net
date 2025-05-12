FROM python:3.8-slim

WORKDIR /task5

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "task5.py"]