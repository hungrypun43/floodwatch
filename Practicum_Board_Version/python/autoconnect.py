'''send to api'''
import request
import time

'''mcu board'''
from practicum import find_mcu_boards,McuBoard,PeriBoard

def working():
    devices = find_mcu_boards()
    mcu = McuBoard(devices[0])
    peri = PeriBoard(mcu)
    res = int(peri.get_value()[1])
    print(res)
    status = request.update(res, '7a2b463d-b450-432e-a69c-1a14efa7d428', 'toofasttoawake')
    status = int(status)
    print(status)
    peri.set_status(status)

while True:
    working()
    time.sleep(15)
