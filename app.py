from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user ,login_required, current_user
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length
import random
import sshtunnel

app = Flask(__name__)

# для подключения к pythonanywhere бд с помощью ssh
tunnel = sshtunnel.SSHTunnelForwarder(
	('ssh.pythonanywhere.com'),
	ssh_username='',
	ssh_password='',
	remote_bind_address=('', 3306))

tunnel.start()

app.config['SQLALCHEMY_DATABASE_URI'] = ''.format(tunnel.local_bind_port)
# для хорошего соединения с pythonanywhere бд
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
mail = Mail(app)

app.config['SECRET_KEY'] = ''
app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] = ''
#app.config['TESTING'] = True # чтобы не вводить капчу каждый раз

login_manager = LoginManager()
login_manager.init_app(app)
# роут для редиректа
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
	'''пользователь'''
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(50))
	class_var = db.Column(db.String(50))
	
class PreClass(db.Model):
	'''индивидуальная программа'''
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class FirstClass(db.Model):
	'''1 класс'''
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class SecondClass(db.Model):
	'''2 класс'''
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class ThirdClass(db.Model):
	'''3 класс'''
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class FourthClass(db.Model):
	'''4 класс'''
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class IndiClass(db.Model):
	'''Индвивидуальная программа'''
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50))
	videolink1 = db.Column(db.String(50))
	pdflink1 = db.Column(db.String(50))
	videolink2 = db.Column(db.String(50))
	pdflink2 = db.Column(db.String(50))
	videolink3 = db.Column(db.String(50))
	pdflink3 = db.Column(db.String(50))

class LessonForm(FlaskForm):
	'''форма бесплатного урока'''
	email = StringField('Введите e-mail', validators=[InputRequired('Введите e-mail'),Email('Некорректный e-mail адрес')])

class QuestionForm(FlaskForm):
	'''форма вопроса'''
	question = TextAreaField('Введите вопрос и получите ответ на ваш адрес', validators=[InputRequired('Введите ваш вопрос'),
				Length(min=5, message='Слишком короткий вопрос')])
	email = StringField('Введите e-mail', validators=[InputRequired('Введите e-mail'),Email('Некорректный e-mail адрес')])
	recaptcha = RecaptchaField()

class QuestionaryForm(FlaskForm):
	'''форма анкеты'''
	parent_name = StringField('введите имя')
	phone = StringField('введите номер')
	email = StringField('введите e-mail', validators=[InputRequired('Введите e-mail'),Email('Некорректный e-mail адрес')])
	pupil_name = StringField('введите имя')
	class_var = SelectField('класс', choices=[('Подготовка к школе','Подготовка к школе'),
													('1','1'),('2','2'),('3','3'),('4','4')])
	subject = StringField('введите название учебных предметов')
	programm = TextAreaField('ваш УМК или автор учебной программы ( учебника )')
	wishes = TextAreaField('Ваш комментарий')

class VideoLessonForm(FlaskForm):
	'''форма видеоурока'''
	videolink = StringField('ссылка на видео')

class PdfLessonForm(FlaskForm):
	'''форма pdf урока'''
	pdflink = StringField('ссылка на приложение')

class LoginForm(FlaskForm):
	'''форма входа'''
	password = StringField('Введите код', validators=[InputRequired('Введите код в поле')])

class CreateUserForm(FlaskForm):
	'''форма создания пользователя'''
	username = StringField('имя пользователя')
	class_var = SelectField('класс', choices=[('pre_class','Подготовка к школе'),('first_class','1 класс'),
							('second_class','2 класс'),('third_class','3 класс'),('fourth_class','4 класс'),
							('indi_class','Индивидуальная программа')])


@login_manager.user_loader
def load_user(user_id):
	'''функция для flask-login'''
	return User.query.get(int(user_id))

@app.route('/login', methods=['GET','POST'])
def login():
	'''вход на сайт'''
	login_form = LoginForm()

	if login_form.validate_on_submit():
		user = User.query.filter_by(password=login_form.password.data).first()
		if user:
			if user.class_var == 'Admin':
				login_user(user)
				return redirect(url_for('admin', table='third_class'))
			else:
				login_user(user)
				return redirect(url_for('schedule'))

		flash('флешка', 'error')
		return render_template('login.html', login_form=login_form)

	flash('флешка', 'unlogged')
	return render_template('login.html', login_form=login_form)

@app.route('/logout')
@login_required
def logout():
	'''выход с сайта'''
	logout_user()
	return redirect(url_for('login'))

@app.route('/')
def index():
	return render_template('index.html')

# делал письмо для подписи
@app.route('/mail')
def mail():
	return render_template('mail.html')

@app.route('/courses')
def courses():
	'''курсы и цены'''
	return render_template('courses.html')

@app.route('/payment/<int:price>')
def payment(price):
	'''форма оплаты'''
	return render_template('payment.html', price=price)

@app.route('/event')
def event():
	'''ивент'''
	return render_template('event.html')

@app.route('/admin/<string:table>')
@login_required
def admin(table):
	'''таблица ссылок на уроки'''
	if current_user.class_var != 'Admin':
		return redirect('error')
	else:
		if table == 'pre_class':
			lessons = PreClass.query.all()
		elif table == 'first_class':
			lessons = FirstClass.query.all()
		elif table == 'second_class':
			lessons = SecondClass.query.all()
		elif table == 'third_class':
			lessons = ThirdClass.query.all()
		elif table == 'fourth_class':
			lessons = FourthClass.query.all()
		elif table == 'indi_class':
			lessons = IndiClass.query.all()
		else:
			return redirect('error')

	return render_template('admin.html', lessons=lessons, table=table)

@app.route('/users')
@login_required
def users():
	'''управление пользователями'''
	if current_user.class_var != 'Admin':
		return redirect('error')
	else:
		user_form = CreateUserForm()
		users = User.query.all()

	return render_template('users.html',user_form=user_form,users=users)

@app.route('/createuser', methods=['POST'])
def createuser():
	'''создать пользователя'''
	user_form = CreateUserForm()

	if user_form.validate_on_submit:
		# генерируем код\пароль для пользователя
		user_code = ''
		for x in range(16):
			user_code += random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))

		new_user = User(password=user_code,username=user_form.username.data,
						class_var=user_form.class_var.data)
		db.session.add(new_user)
		db.session.commit()

		return redirect(url_for('users'))

@app.route('/deleteuser/<string:user_code>', methods=['GET'])
def deleteuser(user_code):
	'''удалить пользователя'''
	user = User.query.filter_by(password=user_code).one()
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('users'))

@app.route('/linkchange/<string:table>/<string:day>/<string:linktype>/<string:link>')
@login_required
def linkchange(table,day,linktype,link):
	'''форма для изменения ссылки'''
	videolessonform = VideoLessonForm()
	pdflessonform = PdfLessonForm()

	return render_template('linkchange.html',table=table,day=day,linktype=linktype,link=link,
								videolessonform=videolessonform,pdflessonform=pdflessonform)

def changevideolinkdry(result,link,videolessonform):
	'''выбор номера videolink'''
	if link == 'videolink1':
		result.videolink1 = videolessonform.videolink.data
		db.session.commit()
	elif link == 'videolink2':
		result.videolink2 = videolessonform.videolink.data
		db.session.commit()
	elif link == 'videolink3':
		result.videolink3 = videolessonform.videolink.data
		db.session.commit()

@app.route('/changevideolink/<string:table>/<string:day>/<string:link>', methods=['POST'])
@login_required
def changevideolink(table,day,link):
	'''изменить ссылку видео'''
	videolessonform = VideoLessonForm()

	if videolessonform.validate_on_submit():
		
		if table == 'pre_class':
			result = PreClass.query.filter_by(day=day).first()
			changevideolinkdry(result,link,videolessonform)
		elif table == 'first_class':
			result = FirstClass.query.filter_by(day=day).first()
			changevideolinkdry(result,link,videolessonform)
		elif table == 'second_class':
			result = SecondClass.query.filter_by(day=day).first()
			changevideolinkdry(result,link,videolessonform)
		elif table == 'third_class':
			result = ThirdClass.query.filter_by(day=day).first()
			changevideolinkdry(result,link,videolessonform)
		elif table == 'fourth_class':
			result = FourthClass.query.filter_by(day=day).first()
			changevideolinkdry(result,link,videolessonform)
		elif table == 'indi_class':
			result = IndiClass.query.filter_by(day=day).first()
			changevideolinkdry(result,link,videolessonform)

	return redirect(url_for('admin', table=table))
		
def changepdflinkdry(result,link,pdflessonform):
	'''выбор номера pdflink'''
	if link == 'pdflink1':
		result.pdflink1 = pdflessonform.pdflink.data
		db.session.commit()
	elif link == 'pdflink2':
		result.pdflink2 = pdflessonform.pdflink.data
		db.session.commit()
	elif link == 'pdflink3':
		result.pdflink3 = pdflessonform.pdflink.data
		db.session.commit()

@app.route('/changepdflink/<string:table>/<string:day>/<string:link>', methods=['POST'])
@login_required
def changepdflink(table,day,link):
	'''изменить ссылку на приложение'''
	pdflessonform = PdfLessonForm()

	if pdflessonform.validate_on_submit():

		if table == 'pre_class':
			result = PreClass.query.filter_by(day=day).first()
			changepdflinkdry(result,link,pdflessonform)
		elif table == 'first_class':
			result = FirstClass.query.filter_by(day=day).first()
			changepdflinkdry(result,link,pdflessonform)
		elif table == 'second_class':
			result = SecondClass.query.filter_by(day=day).first()
			changepdflinkdry(result,link,pdflessonform)
		elif table == 'third_class':
			result = ThirdClass.query.filter_by(day=day).first()
			changepdflinkdry(result,link,pdflessonform)
		elif table == 'fourth_class':
			result = FourthClass.query.filter_by(day=day).first()
			changepdflinkdry(result,link,pdflessonform)
		elif table == 'indi_class':
			result = IndiClass.query.filter_by(day=day).first()
			changepdflinkdry(result,link,pdflessonform)

	return redirect(url_for('admin', table=table))

@app.route('/schedule')
@login_required
def schedule():
	'''уроки'''
	if current_user.class_var == 'pre_class':
		monday = PreClass.query.filter_by(day='Понедельник').first()
		tuesday = PreClass.query.filter_by(day='Вторник').first()
		wednesday = PreClass.query.filter_by(day='Среда').first()
		thursday = PreClass.query.filter_by(day='Четверг').first()
		friday = PreClass.query.filter_by(day='Пятница').first()
	elif current_user.class_var == 'first_class':
		monday = FirstClass.query.filter_by(day='Понедельник').first()
		tuesday = FirstClass.query.filter_by(day='Вторник').first()
		wednesday = FirstClass.query.filter_by(day='Среда').first()
		thursday = FirstClass.query.filter_by(day='Четверг').first()
		friday = FirstClass.query.filter_by(day='Пятница').first()
	elif current_user.class_var == 'second_class':
		monday = SecondClass.query.filter_by(day='Понедельник').first()
		tuesday = SecondClass.query.filter_by(day='Вторник').first()
		wednesday = SecondClass.query.filter_by(day='Среда').first()
		thursday = SecondClass.query.filter_by(day='Четверг').first()
		friday = SecondClass.query.filter_by(day='Пятница').first()
	elif current_user.class_var == 'third_class':
		monday = ThirdClass.query.filter_by(day='Понедельник').first()
		tuesday = ThirdClass.query.filter_by(day='Вторник').first()
		wednesday = ThirdClass.query.filter_by(day='Среда').first()
		thursday = ThirdClass.query.filter_by(day='Четверг').first()
		friday = ThirdClass.query.filter_by(day='Пятница').first()
	elif current_user.class_var == 'fourth_class':
		monday = FourthClass.query.filter_by(day='Понедельник').first()
		tuesday = FourthClass.query.filter_by(day='Вторник').first()
		wednesday = FourthClass.query.filter_by(day='Среда').first()
		thursday = FourthClass.query.filter_by(day='Четверг').first()
		friday = FourthClass.query.filter_by(day='Пятница').first()
	elif current_user.class_var == 'indi_class':
		monday = IndiClass.query.filter_by(day='Понедельник').first()
		tuesday = IndiClass.query.filter_by(day='Вторник').first()
		wednesday = IndiClass.query.filter_by(day='Среда').first()
		thursday = IndiClass.query.filter_by(day='Четверг').first()
		friday = IndiClass.query.filter_by(day='Пятница').first()

	return render_template('schedule.html',monday=monday,tuesday=tuesday,
					wednesday=wednesday,thursday=thursday,friday=friday)


@app.route('/questionary', methods=['GET', 'POST'])
def questionary():
	'''анкета для индивидуальной программы'''
	questionary_form = QuestionaryForm()

	if questionary_form.validate_on_submit():
		# анкета пользователя на почту
		msg = Message(sender='', recipients=[''])
		msg.subject = 'Анкета от пользователя'
		msg.html = 'Родитель : <strong>{}</strong><br>Телефон: <strong>{}</strong>\
		<br>e-mail: <strong>{}</strong><br>Имя ученика: <strong>{}</strong>\
		<br>Класс: <strong>{}</strong><br>Предметы: <strong>{}</strong>\
		<br>Программа: <strong>{}</strong><br>Пожелания: <strong>{}</strong>'.\
		format(questionary_form.parent_name.data,questionary_form.phone.data,
			questionary_form.email.data,questionary_form.pupil_name.data,
			questionary_form.class_var.data,questionary_form.subject.data,
			questionary_form.programm.data,questionary_form.wishes.data)

		mail.send(msg)

		flash('флешка')
		return redirect(url_for('questionary'))

	return render_template('questionary.html', questionary_form=questionary_form)

@app.route('/lesson', methods=['GET', 'POST'])
def lesson():
	'''отправка бесплатного урока'''
	lesson_form = LessonForm()
	question_form = QuestionForm()

	if lesson_form.validate_on_submit():
		# бесплатный урок пользователю
		msg = Message(sender='', recipients=[lesson_form.email.data])
		msg.subject = 'Ваш пробный урок'
		msg.html = '<h1>Ваш урок находится по <a href="">ссылке</a></h1>'

		# отчет о доставке бесплатного урока
		msg_report = Message(sender='', recipients=[''])
		msg_report.subject = 'Отчёт'
		msg_report.html = '<h1>Бесплатный урок отправлен пользователю {}</h1>'.format(lesson_form.email.data)

		# отправка обоих
		mail.send(msg)
		mail.send(msg_report)

		flash('флешка')
		return redirect(url_for('lesson'))

	return render_template('lesson.html', lesson_form=lesson_form, question_form=question_form)

@app.route('/question', methods=['GET', 'POST'])
def question():
	'''задать вопрос'''
	lesson_form = LessonForm()
	question_form = QuestionForm()

	if question_form.validate_on_submit():
		
		msg = Message(sender='', recipients=[''])
		msg.subject = 'Вопрос от пользователя'
		msg.html = 'Пользователь : <strong>{0}</strong><br>Задал вопрос: <strong>{1}</strong>'.\
					format(question_form.email.data, question_form.question.data)
		
		mail.send(msg)

		flash('флешка')
		return redirect(url_for('question'))

	return render_template('question.html', lesson_form=lesson_form, question_form=question_form)

@app.route('/freelesson')
def freelesson():
	'''страница бесплатного урока'''
	return render_template('freelesson.html')

@app.errorhandler(404)
def error(error):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=False)