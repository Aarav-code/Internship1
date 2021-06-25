import json
import re
import datetime

class Main:
    def __init__(self):
        self.user = None
        self.roles = []
        self.c = None
        self.doj_after = None

    def getCategories(self, user):
        f = open(user)
        self.user= dict(json.load(f))

        f = open('nittio/sample.json')
        a = dict(json.load(f))
        positions = list(a.keys())
        self.c = a
        self.change(positions)
        self.check(positions)
        return self.roles
    
    def change(self, a):
        for i in a:
            for j in self.c[i]:
                if j == 'doj_after': continue
                if len(self.c[i][j]) == 1:
                    self.c[i][j] = self.c[i][j][0]
                else:
                    temp = ''
                    for k in self.c[i][j]:  
                       temp += k + '|'
                    self.c[i][j] = temp[0:-1]
                    temp = ''

    def check(self, a):
        doj_condition = False
        for i in a:
            if 'doj_after' not in self.c[i]: doj_condition = True
            conditions = True
            for j in self.c[i]:
                if not doj_condition and j == 'doj_after':
                    doj_after = self.c[i][j]
                if j == 'doj_after': continue
                if not re.match(self.c[i][j], self.user[j]):
                    conditions = False
            if not doj_condition:
                try:
                    if self.calculate_doj(doj_after, self.user['doj_after']) is True and conditions is True:
                        self.roles.append(i)
                except:
                    continue
            elif conditions:
                self.roles.append(i)
        
    def calculate_doj(self, doj, user_doj):
        doj_split = doj.split('-')
        day1 = int(doj_split[2])
        month1 = int(doj_split[1])
        year1 = int(doj_split[0])
        doj_after = datetime.datetime(year1, month1, day1)

        doj_split2 = user_doj.split('-')
        day = int(doj_split2[2])
        month = int(doj_split2[1])
        year = int(doj_split2[0])
        user_doj = datetime.datetime(year, month, day)

        return (doj_after < user_doj)


a = Main()
print(a.getCategories('nittio/user.json'))
