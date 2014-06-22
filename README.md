It's my *first* web project and also my *first* Python project, strange things can happen. :P

Important
=========

Some dependencies you need to install manually.

- Python **2.7.x**
- SQLite **3.x**
- Py-SQLite3 **x**

Installing from ports is pretty easy and I assume that you can do it all by yourself.

I also assume that you have your IPFW up and running. ;)

Now you can use pip to install the others dependencies.
You can install it inside a Python virtual env.
To satisfy the list of dependencies you can just run:

- pip install -r deps.txt

Or install by hand the main packages with:

- pip install Flask
- pip install Flask-Login
- pip install Flask-SQLAlchemy
- pip install Flask-WTF

Try to keep it working with the most recent version of each package.

After installing everything, you can run the tests and see if it passes:
python benicio_tests.py

The default login/password is:

- Login: Admin (case sensitive)
- Password: bendmin

Important:
========
In the 'config.py' file there's a DEBUG variable, set it to False only when you start to send commands directly to IPFW, if it's set to True, all commands will only be written in a file named 'file'.

Caution:
=======
While I don't create a daemon to execute the commands from the web interface, I recommend you to run this project inside a BSD Jail.
For security sake.
