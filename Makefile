runserver:
	python3 backend/manage.py runserver --settings backend.settings.development 5000

test:
	python3 backend/manage.py test --settings backend.settings.development --pattern tests_*.py