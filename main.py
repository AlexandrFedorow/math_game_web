import random
import config
import expression_creator
from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)


def mixing():
    config.mix_des = config.des
    random.shuffle(config.mix_des)


def check(c):
    if config.a == config.mix_des[c]:
        config.lvl += 1
    else:
        if config.lvl > 1:
            config.lvl -= 1


@app.route('/', methods=['GET'])
def hello_world():
    config.e = expression_creator.create_level(1)
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', ctr1=config.mix_des[0],
                                        ctr2=config.mix_des[1],
                                        ctr3=config.mix_des[2],
                                        ctr4=config.mix_des[3],
                                        exp=config.e,
                                        lvl=config.lvl)


@app.route('/add_ans1', methods=['POST'])
def give_ans1():
    check(0)
    config.e = expression_creator.create_level(config.lvl)
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans2', methods=['POST'])
def give_ans2():
    check(1)
    config.e = expression_creator.create_level(config.lvl)
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans3', methods=['POST'])
def give_ans3():
    check(2)
    config.e = expression_creator.create_level(config.lvl)
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


@app.route('/add_ans4', methods=['POST'])
def give_ans4():
    check(3)
    config.e = expression_creator.create_level(config.lvl)
    config.des, config.a = expression_creator.descision(config.e)
    mixing()
    return redirect(url_for('main'))


app.run()