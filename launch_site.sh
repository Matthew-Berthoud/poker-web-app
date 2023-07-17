pip install --upgrade pip
pip install virtualenv
virtualenv env
source env/bin/activate
pip install --upgrade pip
pip install flask
pip install cs50

python3 init_db.py
python3 app.py


# RUNNING THIS FILE WILL WIPE ALL DATABASE TABLES CLEAN