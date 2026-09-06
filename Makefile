.PHONY: build check test up

build:
	cd frontend && npm ci --include=dev --no-audit && npm run build

check: build
	python3 -m py_compile backend/app.py backend/init_db.py

test:
	python3 -m backend.init_db
	pytest -q

up:
	docker compose up --build
