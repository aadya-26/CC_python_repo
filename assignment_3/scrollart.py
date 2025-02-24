import random, os, shutil, time

os.system('cls | clear')  # Clear the screen


WIDTH = shutil.get_terminal_size()[0] - 2
DELAY = 0.2
SIZE = 3
EMPTY_CHAR = ' : '

CHARS = list('/\_/\-')

def slashblank():
    while True:
        columns = []
        for i in range(WIDTH // (SIZE * 3)):
            random_char = random.choice(CHARS + [' '])
            for j in range(SIZE):
                columns.append(random_char)
                columns.append #(EMPTY_CHAR)

        for j in range(SIZE):
            yield ''.join(columns)


try:
    scroll_iterator = slashblank()
    while True:
        for i in range(SIZE):
            print(next(scroll_iterator))
        time.sleep(DELAY)

except KeyboardInterrupt:
    print('Slashblank, by Aadya Singh')
    print('Reference Code: Pacwall, by Al Sweigart al@inventwithpython.com 2024')