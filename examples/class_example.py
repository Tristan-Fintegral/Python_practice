import numpy as np


class Gender:
    MALE = 'Male'
    FEMALE = 'Female'
    GENDERS = [MALE, FEMALE]

class Animal:

    def __init__(self, name):
        self.name = name

    def __eq__(self, value):
        return self.__repr__() == value.__repr__()

    def __len__(self):
        return len(self.name)


class Duck(Animal):

    def __init__(self, name, material, gender):
        super().__init__(name=name)
        self.material = material
        if gender not in Gender.GENDERS:
            raise TypeError(
                f'Expected gender {gender} to be '
                f'in list of genders {Gender.GENDERS}'
            )
        self.gender = gender

    def quack(self):
        print(f'Quack, I am a {self.material} duck called {self.name}.')

    def __repr__(self):
        return f'Duck - Name: {self.name}, ' \
               f'Material: {self.material}, ' \
               f'Gender: {self.gender}'

    def have_baby_with(self, other):
        if self.gender == other.gender:
            return None
        else:
            rand_gender = np.random.choice(Gender.GENDERS)
            return Duck(
                name=f'{self.name}-{other.name}',
                material=self.material,
                gender=rand_gender
            )

class Wolf(Animal):
    def __init__(self, name, material, gender):
        super().__init__(name=name)
        self.material = material
        if gender not in Gender.GENDERS:
            raise TypeError(
                f'Expected gender {gender} to be '
                f'in list of genders {Gender.GENDERS}'
            )
        self.gender = gender

    def howl(self):
        print(f'HAWOOOOO, I am a {self.material} wolf called {self.name}.')

    def __repr__(self):
        return f'Wolf - Name: {self.name}, ' \
               f'Material: {self.material}, ' \
               f'Gender: {self.gender}'


def main():
    alex = Duck(name='Alex', material='flesh', gender=Gender.MALE)
    angela_m = Wolf(name='Angie', material='iron', gender=Gender.FEMALE)
    baby_duck = alex.have_baby_with(angela_m)
    temp = 1


if __name__=='__main__':
    main()