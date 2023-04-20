### Тестовое задание в kaspersky на "Python разработку".

Я тут сделал небольшой отчет, чтобы было проще разобраться что происходит. 

Для запуска всего проекта, в корневой директории проекта нужно выполнить команду `docker-compose up`. Все сервисы будут запущены в контейнерах и ничего дополнительно делать не надо.

Я использовал django rest framework, PostgreSQL, Redis Queue.

Использовал PostgreSQL и docker volumes, чтобы не удалялись данные. Насчет Redis Queue: изначально была идея использовать celery, но он показался мне тяжеловесным для этой задачи и я нашел Redis Queue как решение.

Redis worker настроен в файле `kaspersky_file_api/worker.py`

Все API лежат в `kaspersky_file_api/main/views.py`

Логика поиска файлов и работы с бд лежит в `kaspersky_file_api/main/api_addons/search_handlers.py`

Файлы для тестов лежат в:
* Функций поиска: `kaspersky_file_api/main/api_addons/test_search_functions.py` (запуск `python -m unittest` рядом с файлом `test_search_functions.py`)
* API: `kaspersky_file_api/main/tests.py` (Запуск `python manage.py test`)

Итог: Сделал также работу с zip архивами. Но есть один нюанс в `tests.py`, я не могу разобраться почему функция поиска не начинает поиск при тестировании, но проверил через Postman - все работает как надо. Также проверил unittest функции и все корректно. !При пустых фильтрах выводится все записи, что считаю правильным. 