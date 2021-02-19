import random
import config
import expression_creator
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    lvl = db.Column(db.Integer(), default=1)

    def __repr__(self):
        return '<Users %r' % self.id


def mixing():
    config.mix_des = config.des
    random.shuffle(config.mix_des)


def check(c):
    line = Users.query.filter_by(name=session['user']).all()

    if config.a == config.mix_des[c]:
        session['lvl'] += 1

    else:
        if session['lvl'] > 1:
            session['lvl'] -= 1

    line[0].lvl = str(session['lvl'])
    db.session.commit()


@app.route('/', methods=['post', 'get'])
def login():
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

    elif len(line) != 0:
        return render_template('checkin.html', message='Nickname is already in use')

    elif len(line) == 0 and username != '' and password != '' and password_again != '' and password == password_again:
        session['user'] = username
        session['lvl'] = 1
        user = Users(name=username, password=password)

        try:
            db.session.add(user)
            db.session.commit()
        except:
            return 'error'

        config.e = expression_creator.create_level(1)
        config.des, config.a = expression_creator.descision(config.e)
        mixing()
        return render_template('main.html', ctr1=config.mix_des[0],
                                        ctr2=config.mix_des[1],
                                        ctr3=config.mix_des[2],
                                        ctr4=config.mix_des[3],
                                        exp=config.e,
                                        lvl=1)

    return render_template('checkin.html')


@app.route('/sing_in', methods=['post', 'get'])
def sing_in():
    username = ''
    password = ''
    line = []
    if request.method == 'POST':

        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        line = Users.query.filter_by(name=username).all()

        if len(line) != 1 or line[0].password != password or username == '' or password == '':
            return render_template('sing_in.html', message='Error')
        else:

            session['lvl'] = int(line[0].lvl)
            session['user'] = username

            config.e = expression_creator.create_level(session['lvl'])
            config.des, config.a = expression_creator.descision(config.e)
            mixing()

            return render_template('main.html', ctr1=config.mix_des[0],
                                   ctr2=config.mix_des[1],
                                   ctr3=config.mix_des[2],
                                   ctr4=config.mix_des[3],
                                   exp=config.e,
                                   lvl=session['lvl'])

    return render_template('sing_in.html')


@app.route('/main', methods=['GET'])
def main():

    line = line = Users.query.filter_by(name='jaja').all()
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    return render_template('main.html', ctr1=config.mix_des[0],
                                        ctr2=config.mix_des[1],
                                        ctr3=config.mix_des[2],
                                        ctr4=config.mix_des[3],
                                        exp=config.e,
                                        lvl=session['lvl'],
                                        lider_list=line)


@app.route('/add_ans1', methods=['POST'])
def give_ans1():
    check(0)
    config.e = expression_creator.create_level(session['lvl'])
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans2', methods=['POST'])
def give_ans2():
    check(1)
    config.e = expression_creator.create_level(session['lvl'])
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans3', methods=['POST'])
def give_ans3():
    check(2)
    config.e = expression_creator.create_level(session['lvl'])
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans4', methods=['POST'])
def give_ans4():
    check(3)
    config.e = expression_creator.create_level(session['lvl'])
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


app.run()