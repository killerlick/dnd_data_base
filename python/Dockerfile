FROM python:3.12-slim

WORKDIR /app 

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python3 spell_database.py

CMD ["python3", "insert_spells_database.py"]