#CMD ["python", "common/generate_db.py", "&&", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "--access-logfile=-", "admin.app:create_app()"]
sleep 5;
/usr/local/bin/python common/generate_db.py;
gunicorn -w 2 -b 0.0.0.0:8000 --access-logfile=- admin.app:create_app\(\);

