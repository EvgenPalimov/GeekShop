## Проект "Интернет-магазин GeekShop!"

### Базовая документация к проекту

Основные системные требования:

* Ubuntu 20.04 LTS
* Python 3.9
* Django 3.2.9
* Зависимости (Python) из requirements.txt

Интернет-магазин одежды GeekShop, разработан на платформе Django. Реализован 
механизм регистрации и авторизации, в т.ч. авторизацию через ВКонтакте. 
Имеется личный кабинет с возможностью оформлением заказов. Реализована
административная панель для управления данными и заказами.

### Установка необходимого ПО

#### Обновляем информацию о репозиториях

```
apt update
```

#### Установка nginx, Git, virtualenv, gunicorn

```
apt install nginx
```

Git

```
apt install git-core
```

virtualenv

```
apt install python3-venv
```

gunicorn

```
apt install gunicorn
```

#### Настраиваем виртуальное окружение

При необходимости, для установки менеджера пакетов pip выполняем команду:

```
apt install python3-pip
```

Создаем и активируем виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Ставим зависимости:

```
pip3 install -r requirements.txt
```

#### Суперпользователь

```
python3 manage.py createsuperuser
```

к примеру (логин/пароль): admin:admin

#### Выполнение миграций и сбор статических файлов проекта

Выполняем миграции:

```
python3 manage.py migrate
```

#### Заполнить базу данных тестовыми данными (необязательно)

```
python3 manage.py fill_db
```

#### Тест запуска

```
python3 manage.py runserver
```

Настроим параметры службы «gunicorn»

```
sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/GeekShop
ExecStart=/home/django/GeekShop/env/bin/gunicorn --error-logfile 
"/var/log/gunicorn/error.log" --access-logfile "/var/log/gunicorn/access.log" 
--workers 3 --bind unix:/home/django/GeekShop/GeekShop.sock GeekShop.wsgi

[Install]
WantedBy=multi-user.target

```

Активирование и запуск сервиса

```
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

Настройки параметров для nginx

```
sudo nano /etc/nginx/sites-available/GeekShop

server {
  listen 80;
  server_name 81.200.145.185;
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
    root /home/django/GeekShop;
  }
  location /media/ {
    root /home/django/GeekShop;
  }
  location / {
    include proxy_params;
    proxy_pass http://unix:/home/django/GeekShop/GeekShop.sock;
  }
}
```

Перезапускаем службу «nginx»

```
sudo systemctl restart nginx
```

#### Активируем сайт

```
sudo ln -s /etc/nginx/sites-available/GeekShop /etc/nginx/sites-enabled
```

### После этого в браузере можно ввести ip-адрес сервера и откроется проект.
