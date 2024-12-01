1.Flask install 
pip3 install flask

2.venv install 
python3 -m venv pyenv
source pyenv/bin/activate
pip3 install flask bcrypt

3.cd to app.py
4.python3 test.py
5.http://127.0.0.1:5000/ in web 
6.open anotehr terminal
7.create account
curl -X POST http://127.0.0.1:5000/create-account -H "Content-Type: application/json" -d '{"username": "test", "password": "123456"}'
8.log in 
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "test", "password": "123456"}'
9.update password
curl -X POST http://127.0.0.1:5000/update-password -H "Content-Type: application/json" -d '{"username": "test", "old_password": "123456", "new_password": "654321"}'

