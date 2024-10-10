from time import sleep
from machine import Pin

LED = 0

def setup():
    global LED
    LED = Pin('LED', Pin.OUT)

def loop():
    timer = 0
    while True:
        timer += 1
        print(f'Testing: {str(timer)}')
        
        sleep(1)

        if timer == 5:
            timer = 0
            print_devider()

        LED.toggle()

def print_devider():
    print('')
    print('#################')
    print('#               #')
    print('#  Start again  #')
    print('#               #')
    print('#################')
    print('')

try:
    setup()
    loop()
except (Exception, KeyboardInterrupt) as e:
    print(f'\nError was caught:{e}')
finally:
    print('Program Done...')