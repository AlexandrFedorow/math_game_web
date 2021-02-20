from random import randint
import config


class Expression:
    def __init__(self):
        self.a = randint(1, 100)
        self.b = randint(1, 100)
        self.c = randint(1, 100)

        self.action = ['+', '-', '*', '/']
        self.trig = ['sin', 'cos', 'tg', 'ctg']
        self.angle = ['30', '45', '60']

    def decision(self, task):
        a1 = int(eval(task))
        a2 = int(a1 - 1)
        a3 = int(self.c - self.b + 4)
        a4 = int(randint(a1-20, a1-1))

        return a1, a2, a3, a4

    def trigonometry_decision(self, task):
        may = ['1/2', '√2/2', '√3/2', '1', '√3', '√3/3']
        ans = []
        if 'sin' in task:
            if '30' in task:
                ans.append('1/2')
            elif '45' in task:
                ans.append('√2/2')
            elif '60' in task:
                ans.append('√3/2')

        elif 'cos' in task:
            if '30' in task:
                ans.append('√3/2')
            elif '45' in task:
                ans.append('√2/2')
            elif '60' in task:
                ans.append('1/2')

        elif 'tg' in task:
            if '30' in task:
                ans.append('√3/3')
            elif '45' in task:
                ans.append('1')
            elif '60' in task:
                ans.append('√3')

        elif 'ctg' in task:
            if '30' in task:
                ans.append('√3')
            elif '45' in task:
                ans.append('1')
            elif '60' in task:
                ans.append('√3/3')

        while len(ans) <= 3:
            a = may[randint(0, len(may)-1)]
            if a not in ans:
                ans.append(a)

        return ans

    def trigonometry_task(self):
        ex = self.trig[randint(0, 3)] + '(' + self.angle[randint(0, 2)] + ')'
        return ex

    def create_task_with_one_action(self):
        self.a = randint(1, 100)
        self.b = randint(1, 100)
        self.c = randint(1, 100)

        act = self.action[randint(0, 3)]

        if act == '/':
            while self.a % self.b != 0:
                self.b = randint(1, 100)

        if act == '*':
            while self.a >= 10 or self.b >= 10:
                self.a = randint(1, 10)
                self.b = randint(1, 10)

        ex = str(self.a) + ' ' + act + ' ' + str(self.b)
        return ex

    def create_task_with_two_actions(self):
        self.a = randint(1, 100)
        self.b = randint(1, 100)
        self.c = randint(1, 100)

        acts = ['', '']
        while acts[0] == acts[1] or acts[0] == '*' and acts[1] == '/' or acts[0] == '/' and acts[0] == '*':
            acts[0] = self.action[randint(0, 3)]
            acts[1] = self.action[randint(0, 3)]

        if '*' in acts:
            if acts.index('*') == 0:
                if self.a >= 10 or self.b >= 10:
                    self.a = randint(1, 10)
                    self.b = randint(1, 10)
            else:
                if self.b >= 10 or self.c >= 10:
                    self.b = randint(1, 10)
                    self.c = randint(1, 10)

        if '/' in acts:
            if acts.index('/') == 0:
                while self.a % self.b != 0:
                    self.b = randint(1, 100)
            else:
                while self.b % self.c != 0:
                    self.c = randint(1, 100)

        ex = str(self.a) + ' ' + acts[0] + ' ' + str(self.b) + ' ' + acts[1] + ' ' + str(self.c)
        return ex


def create_level(game_lvl):
    config.game = Expression()

    if game_lvl <= 10:
        check = randint(0, 1)

        if check == 0 or game_lvl < 10:
            exeption = config.game.create_task_with_one_action()
            config.trig_chek = 0
        elif check == 1 and game_lvl >= 10:
            exeption = config.game.trigonometry_task()
            config.trig_chek = 1

        return exeption
    else:
        config.trig_chek = 0
        exeption = config.game.create_task_with_two_actions()
        return exeption


def descision(task):
    if config.trig_chek == 0:
        ans = list(config.game.decision(task))
    else:
        ans = config.game.trigonometry_decision(task)
    return ans, ans[0]



