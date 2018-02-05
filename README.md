# flask-app

## Description:

Web based build your own multiple path story app.

## Requirments:

Python 2.7+

## How to run:

- Clone github repo
- run `cd flask-app`
- run `pip install .`
- run `./run_app.sh`
    - NOTE: running this script will drop the database table!
    - to prevent this run command `export FLASK_APP=flask_app;export DEBUG=true;flask run`
- navigate to `http://127.0.0.1:5000` in a browser

NOTE: Debug mode will be active.

## Testing the app:

- from flask-app
- run `python setup.py test` to test the app
- or run `coverage run -m pytest` for test coverage
- code test coverage at 96%
