# gesassos-web
Gestion des comptes assos pour le SiMDE et les bureaux d'assos

## Installation
* [Installer Django](https://docs.djangoproject.com/en/1.11/topics/install/#installing-official-release)
* Installer MySQL
	* `sudo apt-get install mysql-server libmysqlclient-dev`
	* lancer le promt `mysql -u root -p`
	* créer une base de données `CREATE DATABASE gesassos CHARACTER SET utf8;`
* Installer mysqlclient `sudo pip install mysqlclient` (et `sudo apt-get install python-dev python3-dev` si besoin)
* `sudo pip install django-cas-client==1.3.0`
* Lancer le serveur local
```
cd gesassos-web
python manage.py runserver
```

## Production
* Penser à changer `SECRET_KEY`, `DEBUG` et `DATABASES` dans `/gesassos/settings.py`