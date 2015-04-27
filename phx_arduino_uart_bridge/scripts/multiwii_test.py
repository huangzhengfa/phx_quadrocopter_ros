__author__ = 'manuelviermetz'

import pyCopter
import time

mw = pyCopter.serial_com.multiwii_protocol('/dev/multiwii')
mw.startup_delay = 15.0

last_time = time.time()

while True:
    last_time = time.time()
    mw.receive(debug=False)
    time.sleep(0.01)
    #mw.get_msg(cmd_list=[105], debug=False)
    mw.get_msg(cmd_list=[101, 102, 104, 105, 106, 108, 109], debug=False)
    mw.receive(debug=False)
    #print mw.attitude
    print time.time()-last_time#, mw.status, mw.raw_imu, mw.rc
