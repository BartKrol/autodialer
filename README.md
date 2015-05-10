Autodialer
==========

About
-----
This is a simple customer managing tool for sales developed as an interview task (developed in 12 hours).

Usage & Features
----------------
* Basic functionality:
    1. Agent is able to login to his account with given username and password
    2. Agent is given a number to call
    3. Agent is able to see current status of the call.
    3. Twilio creates a conference (_a bridge_) and agent is the only person inside
    4. Agent is given a list of clients to call

* Special cases:
    1. Every time new agent is logged in, he is given a number from database and this number is marked as used.
    2. For the session duration he will be given the same number
    3. After the end of conference, agent may start a new one by calling the same number
    4. It is possible to call any client once again

Possible Improvements
---------------------

* Use Twisted or Tornado to handle asynchronous tasks
* Use Celery to handle long running tasks
* Add administration panel
* Remove code from __init__.py

Setup
-----
- create virtual environment for development

```sh
$ virtualenv env
```
- activate virtual environment

```sh
$ source env/bin/activate
```

- install python necessary packages

```sh
$ pip install -r requirments.txt
```

- initiate database

```sh
$ ./manage.py db init
```

- create first migration

```sh
$ ./manage.py db migrate
```

- upgrade database and create tables

```sh
$ ./manage.py db upgrade
```

- populates database with fake data

```sh
$ ./manage.py populate
```

- Run _Autodialer_ Server

```sh
$ ./manage.py runserver
```

- Login as _username_: Test _password_: TEST


