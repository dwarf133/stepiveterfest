pkill -9 -f 'tasks worker'
fuser -k 443/tcp
gunicorn --bind fest.stepiveter.ru:443 --timeout 1000 --keep-alive 1000 --keyfile /etc/letsencrypt/live/fest.stepiveter.ru/privkey.pem --certfile /etc/letsencrypt/live/fest.stepiveter.ru/fullchain.pem --workers=8 'app:init()' -D
celery -A tasks worker --loglevel=INFO -D