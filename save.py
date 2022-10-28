#! /usr/bin/env python

import struct
import atexit
from datetime import datetime
from time import sleep
import numpy as np
from tcp import Tcp

def main():
    Timeout_default = 1 # sec.
    sampling_time = 0.2 # sec.
    n_channels = 20

    ip_address = '10.241.47.98'
    port = 8023
    tcp = Tcp(Timeout_default)
    if not tcp.open(ip_address, port):
        print('Connection Error')
        return
    atexit.register(tcp.close)

    command = "MEAS:OUTP:ONE?"

    while True:
        msg = tcp.send_read_command(command, Timeout_default)
        data_list = struct.unpack_from('>{}h'.format(n_channels), msg, 8)
        data = np.array(data_list, dtype='float')
        # For Pt1000, val = bin / 10.
        # For Voltage, val = bin / 2000.
        data[0:10] = data[0:10] / 10.
        data[10:] = data[10:] / 2000.

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        str_line = now
        for d in data:
            str_line += (','+str(d))
        str_line += '\n'

        with open('data.csv', mode='a') as f:
            f.write(str_line)
        sleep(sampling_time)

    return

if __name__ == '__main__':
    main()
