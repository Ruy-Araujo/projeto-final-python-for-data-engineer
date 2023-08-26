FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

ENTRYPOINT [ "python","./main.py" ]
CMD ["--coin-id", "1", "--date-start", "2023-01-01", "--date-end", "2023-02-01", "--interval", "1d", "--convert", "BRL"]