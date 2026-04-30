install:
	pip install -r requirements.txt

api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

ui:
	streamlit run ui/app.py

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .
