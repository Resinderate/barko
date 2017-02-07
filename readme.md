# Barko To-Do List App
![](http://i.imgur.com/IYQzBtM.png =800x)

### Tech
* Python 2.7
* Django
* Bootstrap
* (A little bit of) jQuery

### Install Requirements
Preferably inside a virtualenv:
```sh
$ pip install -r requirements.txt
```

### Run Dev Server
```sh
$ python manage.py runserver
```
Running at default:
```sh
127.0.0.1:8000
```
Sample logins in test db:
```sh
User : Pass
admin : adminadmin
ronan : ronanronan
```

### Run Tests
```sh
$ python manage.py test
```

### Time
* **Roughly 20~ hrs total**
* Planning: 2~ hrs
* Django Hello World and Environment: 3~ hrs
* Backend: 6~ hrs
* Frontend: 6~ hrs
* Writing Tests: 3~ hrs

### Todo
Stuff next on the list if it was taken further:
* Ajax for data requests, avoid refreshing the page after every action.
* Server side Forms.
* Fix task details formatting on small devices.
* System to handle really long titles.