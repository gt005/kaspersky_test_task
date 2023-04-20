### Тестовое задание в kaspersky на "Python разработку".

Я тут сделал небольшой отчет, чтобы было проще разобраться что происходит. 

Для запуска всего проекта, в корневой директории проекта нужно выполнить команду `docker-compose up`. Все сервисы будут запущены в контейнерах и ничего дополнительно делать не надо.

Я использовал django rest framework, sqlite, Redis Queue.

Решил использовать sqlite и не подключать стороннюю субд так как тут задача не требует сверх нагрузки и специфичных запросов. Насчет Redis Queue: изначально была идея использовать celery, но он показался мне тяжеловесным для этой задачи и я нашел Redis Queue как решение.

Redis worker настроен в файле `kaspersky_file_api/worker.py`

Все API лежат в `kaspersky_file_api/main/views.py`

Логика поиска файлов и работы с бд лежит в `kaspersky_file_api/main/api_addons/search_handlers.py`

Файлы для тестов (тесты запускать в той же директории что и файл) лежат в:
* Функций поиска: `kaspersky_file_api/main/api_addons/test_search_functions.py` (запуск `python3 -m unittest`)