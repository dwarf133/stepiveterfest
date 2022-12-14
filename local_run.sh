pkill -9 -f 'tasks worker'
fuser -k 8080/tcp
gunicorn --bind localhost:8080 --timeout 1000 --keep-alive 1000 --workers=2 'app:init()'
celery -A tasks worker --loglevel=INFO -D