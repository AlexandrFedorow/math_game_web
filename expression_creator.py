from random import randint
import config


class Expression:
    def __init__(self):
        self.a = randint(1, 100)
        self.b = randint(1, 100)
        self.c = randint(1, 100)

        self.action = ['+', '-', '*', '/']

    def decision(self, task):
        a1 = int(eval(task))
        a2 = int(a1 - 1)
        a3 = int(self.c - self.b + 4)
        if self.a == self.c:
            a4 = int(34 - self.a)
        else:
            a4 = int(self.b - self.c)

        t = task.split()

        if len(t) == 3:
            if t[1] == '-':
                a3 = int(eval(t[2] + t[1] + t[0]))

        elif len(t) == 5:
            if '*' in t:
                a3 = int(eval(t[0] + t[3] + t[2] + t[1] + t[4]))

                if t.index('*') == 1:
                    a4 = int(eval(t[0] + t[1] + '(' + t[2] + t[3] + t[4] + ')'))

                else:
                    a4 = int(eval('(' + t[0] + t[1] + t[2] + ')' + t[3] + t[4]))

        return a1, a2, a3, a4

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
        exeption = config.game.create_task_with_one_action()
        return exeption
    else:
        exeption = config.game.create_task_with_two_actions()
        return exeption



def descision(task):
    ans = list(config.game.decision(task))
    return ans, ans[0]



