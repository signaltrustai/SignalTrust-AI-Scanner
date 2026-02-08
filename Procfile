web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 3 --worker-class gthread --threads 2 --timeout 60 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 --preload --log-level info
