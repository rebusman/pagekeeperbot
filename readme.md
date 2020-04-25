## Запуск

### Установить wkhtmltopdf

https://wkhtmltopdf.org/

### Разрешить зависимости 
```sh
pip install -r requirements.txt
```
### Пример конфигурационного файла config.ini
```sh
[DEFAULT]
Token = # токен бота
Proxy = # url прокси
Filepath = # папка для временного хранения страниц
```
### Запустить бота
```sh
python -m pagekeeperbot.py
```