pip install --upgrade pip
pip install virtualenv
virtualenv env
source env/bin/activate
pip install --upgrade pip
pip install flask

python3 init_db.py
python3 app.py