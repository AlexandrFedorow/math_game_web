import random
import re
import expression_creator
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'hello'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
valid_pattern = re.compile(r"^[0-9a-zA-Z]{5,20}$", re.I)
db = SQLAlchemy(app)




class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    lvl = db.Column(db.Integer(), default=1)

    def __repr__(self):
        return '<Users %r' % self.id


#admin = Admin(app)
#admin.add_view(ModelView(Users, db.session))


def validate(name):
    return bool(valid_pattern.match(name))


def mixing():
    random.shuffle(session['description'])


def check(c):
    line = Users.query.filter_by(name=session['user']).all()

    if session['answer'] == session['description'][c]:
        session['lvl'] += 1

    else:
        if session['lvl'] > 1:
            session['lvl'] -= 1

    line[0].lvl = str(session['lvl'])
    db.session.commit()


@app.route('/', methods=['post', 'get'])
def login():# тут происходит регистрация пользователя
    username = ''
    password = ''
    password_again = ''
    line = []

    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        password_again = request.form.get('password_again')
        line = Users.query.filter_by(name=username).all()

    if password != password_again:
        return render_template('checkin.html', message='Passwords do not match')

    elif len(password) < 5 and len(password) != 0:
        return render_template('checkin.html', message='Password is too short')

    elif ' ' in password:
        return render_template('checkin.html', message='Must be no spaces in the password')

    elif len(line) != 0:
        return render_template('checkin.html', message='Nickname is already in use')

    elif not validate(username) and len(username) != 0:
        return render_template('checkin.html', message='Incorrect nickname')

    elif len(line) == 0 and username != '' and password != '' and password_again != '' and password == password_again:
        session['user'] = username
        session['lvl'] = 1
        user = Users(name=username, password=generate_password_hash(password))

        try:
            db.session.add(user)
            db.session.commit()
        except:
            return 'error'

        session['expression'] = expression_creator.create_level(session['lvl'])
        session['description'], session['answer'] = expression_creator.descision(session['expression'])
        mixing()
        line = Users.query.order_by(Users.lvl.desc()).limit(5)

        return render_template('main.html', ctr1=session['description'][0],
                               ctr2=session['description'][1],
                               ctr3=session['description'][2],
                               ctr4=session['description'][3],
                               exp=session['expression'],
                               lvl=session['lvl'],
                               lider_list=line)

    return render_template('checkin.html')


@app.route('/sing_in', methods=['post', 'get'])
def sing_in():#тут происходит вход поьзователя

    if request.method == 'POST':

        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        line = Users.query.filter_by(name=username).all()

        if len(line) != 1 or not(check_password_hash(line[0].password, password)) or username == '' or password == '':#check_password_hash(self.password_hash, password)
            return render_template('login.html', message='Error')
        else:

            session['lvl'] = int(line[0].lvl)
            session['user'] = username

            session['expression'] = expression_creator.create_level(session['lvl'])
            session['description'], session['answer'] = expression_creator.descision(session['expression'])
            mixing()
            line = Users.query.order_by(Users.lvl.desc()).limit(5)

            return render_template('main.html', ctr1=session['description'][0],
                                   ctr2=session['description'][1],
                                   ctr3=session['description'][2],
                                   ctr4=session['description'][3],
                                   exp=session['expression'],
                                   lvl=session['lvl'],
                                   lider_list=line)

    return render_template('login.html')


@app.route('/main', methods=['GET'])
def main():
    line = Users.query.order_by(Users.lvl.desc()).limit(5)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    return render_template('main.html', ctr1=session['description'][0],
                           ctr2=session['description'][1],
                           ctr3=session['description'][2],
                           ctr4=session['description'][3],
                           exp=session['expression'],
                           lvl=session['lvl'],
                           lider_list=line)


@app.route('/add_ans1', methods=['POST'])
def give_ans1():
    check(0)
    session['expression'] = expression_creator.create_level(session['lvl'])
    session['description'], session['answer'] = expression_creator.descision(session['expression'])
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans2', methods=['POST'])
def give_ans2():
    check(1)
    session['expression'] = expression_creator.create_level(session['lvl'])
    session['description'], session['answer'] = expression_creator.descision(session['expression'])
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans3', methods=['POST'])
def give_ans3():
    check(2)
    session['expression'] = expression_creator.create_level(session['lvl'])
    session['description'], session['answer'] = expression_creator.descision(session['expression'])
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans4', methods=['POST'])
def give_ans4():
    check(3)
    session['expression'] = expression_creator.create_level(session['lvl'])
    session['description'], session['answer'] = expression_creator.descision(session['expression'])
    mixing()
    return redirect(url_for('main'))


app.run()
