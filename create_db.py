from flask import Flask
import sshtunnel
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

tunnel = sshtunnel.SSHTunnelForwarder(
	('ssh.pythonanywhere.com'), 
	ssh_username='', 
	ssh_password='',
	remote_bind_address=('', 3306))

tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = ''.format(tunnel.local_bind_port)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

'''
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(50))
	class_var = db.Column(db.String(50))


class PreClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class FirstClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class SecondClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class ThirdClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class FourthClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class IndiClass(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))
'''

# создать таблицы
# db.create_all()

'''
# создать ссылки в бд,меняя модели
week = ['Понедельник','Вторник','Среда','Четверг','Пятница']
for den in week:
	# сменить модель
	dob = IndiClass(day=den,videolink1='https://www.youtube.com/watch?v=jhuVvggyz58',
									pdflink1='http://flask.pocoo.org/',
									videolink2='https://www.youtube.com/watch?v=jhuVvggyz58',
									pdflink2='http://flask.pocoo.org/',
									videolink3='https://www.youtube.com/watch?v=jhuVvggyz58',
									pdflink3='http://flask.pocoo.org/')
	db.session.add(dob)
	db.session.commit()
'''