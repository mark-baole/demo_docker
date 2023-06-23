# run inference app
uvicorn app:app --workers 4 --host 0.0.0.0 --port 8080 --reload