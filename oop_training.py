#create a class for cars

class Car(object):
    def __init__(self, manufacturer, color, capacity, max_speed):
        self.manufacturer = manufacturer
        self.color = color
        self.capacity = capacity
        self.max_speed = max_speed
        self.position = 0
    def steps(self, steps):
        self.position += steps


'George'_car = Car('Jeep', 'black', 5,220)
'George'_car.manufacturer
'George'_car.color
'George'_car.max_speed
'George'_car.capacity
'George'_car.position
dir('George'_car)

'George'_car.steps(89)
'George'_car.position

# create a class for a human being

class HumanBeing(object):
    def __init__(self, name, eye_color):
        self.name = name
        self.eye_color = eye_color

'George' = HumanBeing('Nikolas', 'brown')
'George'.name
'George'.eye_color

class Man(HumanBeing):
    pass


John = Man('John', 'blue')
John.name
John.eye_color


class Woman(HumanBeing):
    pass

Maria = Woman('Maria', 'blue')
Maria.name
Maria.eye_color

type(Maria)

Andre = HumanBeing('Andre', 'blue')
type(Andre)

Andre.price = 100
Andre.price

Andre.gender = 'male'

Andre.gender

dir(Andre)
Andre.__str__()

# create a class for financial instruments

class FinancialInstrument(object):
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

class FinancialInstrument(FinancialInstrument):
    def get_price(self):
        return self.price


aapl = FinancialInstrument('aapl',100)
aapl.get_price()


################################################################

class FinancialInstruments(object):
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price


class Stocks(FinancialInstruments):
    def get_price(self):
        return self.price


aapl = Stocks('aapl', 100)
aapl.get_price()


##########################################################################

# make a class to store (ie database) students' names and students grades

class GradeBook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def add_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


book = GradeBook()

book.add_student('Nikolas')
book.add_grade('Nikolas', 80)
book.add_grade('Nikolas', 70)
book.add_grade('Nikolas', 60)

book.add_student('George')
book.add_grade('George', 90)
book.add_grade('George', 95)
book.add_grade('George', 100)

book.average_grade('Nikolas')
book.average_grade('George')

from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        self._grade = {}

    def add_student(self,name):
        self._grade[name] = defaultdict()

    def add_subject(self,name,subject):
        self._grade[name][subject] = []

    def add_score(self,name, subject, score):
        self._grade[name][subject].append(score)



del(book2)

book2 = BySubjectGradebook()

book2.add_student('Nikolas')
book2.add_subject('Nikolas', 'Geography')
book2.add_subject('Nikolas', 'Maths')
book2.add_subject('Nikolas', 'History')

book2.add_score('Nikolas', 'Geography', 80)
book2.add_score('Nikolas', 'Maths', 90)
book2.add_score('Nikolas', 'History', 70)

import random
random.seed(123456)
random.random()


######################################################




#####################################################

class Employee:
    def __init__(self, name, company, retired='NO'):
        self._name = name
        self.__company = company
        self.__retired = retired

    def get_company(self):
        return self.__company

    def set_company(self,value):
        self.__company = value


e = Employee('Prayad', 'Amazon')
print(f'{e._name}\'s company is {e.get_company()}')
e.set_company('Google')
print('='*25)
print(f'{e._name}\'s company is {e.get_company()}')

######################################################


class Employee:

    def __init__(self, name, company, retired='NO'):
        self._name = name
        self.__company = company
        self.__retired = retired

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self,value):
        self.__company = value



e = Employee('Prayad', 'Google')
print(f'The company name is {e.company}')
print('='*35)
e.company = 'Amazon'
print(f'The company name is {e.company}')
print('='*35)
Employee.company = 'Microsoft'
print(f'The company name is {e.company}')
print(f'The company name is {Employee.company}')


###################################

import numpy as np
from abc import abstractmethod

class BaseGenerator:
    _generator = np.random.RandomState()
    __seed = 10

    def __init__(self):
        self._generator.seed(self.__seed)























