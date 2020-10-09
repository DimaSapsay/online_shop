1. Создать virtualenv

	```
	python3 -m venv /path/to/your/venv
	```
2. Активировать окружение и установить зависимости

	```
	source /path/to/your/venv/bin/activate
	pip install -r requirements.txt
	```
	
3. Переименовать файл confog_.py в config.py и установить настройки.

4. Установить БД

    ```
    flask db init
    flask db migrate -m "your comment"
    flask db upgrade
    ```
   
5. Запустить проект

    ```
   export FLASK_APP=online_store.py
   flask run
   ```
