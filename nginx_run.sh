gunicorn --bind localhost:8080 --timeout 1000 --keep-alive 1000 --workers=8 'app:init()'
celery -A tasks worker --loglevel=INFO -D