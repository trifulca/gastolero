all:
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  instalar      Instala todas las dependencias."
	@echo "  migrar        Ejecuta las migraciones de datos."
	@echo "  ejecutar      Levanta la aplicacion en localhost:8000"
	@echo "  test          Ejecuta todas las pruebas."
	@echo "  test_live     Ejecuta las pruebas en modo contínuo."
	@echo ""
	@echo ""

ejecutar:
	cd gastolero/; pipenv run python manage.py runserver

migrar:
	cd gastolero/; pipenv run python manage.py migrate

test:
	cd gastolero/; pipenv run python manage.py test web

test_live: test
	cd gastolero/; pipenv run watchmedo shell-command --patterns="*.py;*.txt" --recursive --command='clear; python manage.py test web' .
