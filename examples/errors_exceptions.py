import numpy as np

def get_icecream(flavour):

    random_error(chance_of_error=0)

    icecream_lookup = {
        'CHOCOLATE': 'Tasty Choco',
        'Strawberry': 'Tangy Strawbs',
        'Vanilla': 'Boring vanilla'
    }

    return icecream_lookup[flavour]


def random_error(chance_of_error=0.3):
    rand_num = np.random.uniform(0, 1)
    if rand_num < chance_of_error:
        raise RuntimeError('Random interruption.')


def main():

    list_of_flavs = ['Strawberry', 'Banana', 'Chocolate', 'Vanilla', 'Berry']
    ice_cream_depository = []

    for flavour in list_of_flavs:
        try:
            ice_cream = get_icecream(flavour)
            print(f'Ice cream is {ice_cream}.')
        except KeyError:
            ice_cream = flavour
            print(f'Error in get_icecream, ice cream set to {ice_cream}.')

        ice_cream_depository.append(ice_cream)
    print(ice_cream_depository)
    temp = 1


if __name__ == '__main__':
    main()