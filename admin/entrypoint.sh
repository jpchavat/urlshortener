#CMD ["python", "common/generate_db.py", "&&", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "--access-logfile=-", "admin.app:create_app()"]
pyhton common/generate_db.py;
gunicorn -w 2 -b 0.0.0.0:8000 --access-logfile=- admin.app:create_app\(\);

