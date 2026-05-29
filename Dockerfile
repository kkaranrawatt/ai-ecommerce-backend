FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .
ENV SECRET_KEY=dummy-secret-key-for-build
ENV DEBUG=False
ENV ALLOWED_HOSTS=*
ENV DATABASE_URL=sqlite:///tmp/db.sqlite3


RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]
