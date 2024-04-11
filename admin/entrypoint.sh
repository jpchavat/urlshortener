#CMD ["python", "common/generate_db.py", "&&", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "--access-logfile=-", "admin.app:create_app()"]
pyhton3 common/generate_db.py;
gunicorn -w 2 -b 0.0.0.0:8000 --access-logfile=- admin.app:create_app\(\);

