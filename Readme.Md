1. Clone the repository 
2. create virtual environment file using commond python -m venv venv or env
3. activate the virtual environment on your os 
4. Now install requirements file using commond pip install -r requirements.txt
5. When all required package installed then you will run project using uvicorn main:app --relaod
6. for celery use commond    celery -A main.celery worker --logleve=info
