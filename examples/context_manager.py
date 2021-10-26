import time
from examples import errors_exceptions


class DataWrite:

    def __init__(self, filename, mode='w'):
        self.filename = filename
        self.mode = mode
        print('Initiating data write context.\n')

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        self.file.write('Entering data write context.\n')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.file:
            self.file.write('Exiting data write context.\n')
            self.file.close()


class Timer:

    def __init__(self):
        print('Creating timer.\n')

    def __enter__(self):
        self.start_time = time.time()
        print(f'Start time is {self.start_time}.')

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.end_time = time.time()
        print(f'End time is {self.end_time} seconds.')
        self.elapsed_time = self.end_time - self.start_time
        print(f'In with statement for {self.elapsed_time} seconds.')



def my_custom_context():
    data_to_insert = [1, 2, 3, 4, 5]
    with Timer():
        with DataWrite("result_output.txt", mode="w") as file:
            file.write(f"Data is {data_to_insert}.\n")
            #errors_exceptions.random_error(1)


def using_with():

    with open("result_output.txt", mode="w") as file:
        file.write(f"Starting data write.\n")
        errors_exceptions.random_error(1)

    file.write(f"Can we write data now?\n")

def unclosed_file():

    file = open("result_output.txt", "w")
    file.write(f"Starting data write.\n")
    errors_exceptions.random_error(1)
    data_to_insert = [1, 2, 3, 4, 5]
    file.write(f"Data: {data_to_insert}.\n")
    file.close()

def using_try_except_else_finally():
    file = open("result_output.txt", "w")
    file.write(f"Starting data write.\n")

    try:
        errors_exceptions.random_error(1)
        data_to_insert = [1,2,3,4,5]
        file.write(f"Data: {data_to_insert}.\n")
    except:
        file.write(f"There was an error.\n")
    else:
        file.write(f"There was not an error.\n")
    finally:
        file.write(f"Finishing data write.\n")
        file.close()

if __name__ == '__main__':
    my_custom_context()
