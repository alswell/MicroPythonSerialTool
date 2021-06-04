import os
import serial
import threading

mpys = '''
def mpys_read(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print('-', line, end='')

def mpys_write(path, content, origin_name=None):
    try:
        if uos.stat(path)[0] == 16384:
            path = "/".join([path, origin_name])
    except Exception:
        pass
    with open(path, 'w') as f:
        f.write(content)

def mpys_del(path):
    if uos.stat(path)[0] == 16384:
        for f in uos.listdir(path):
            mpys_del('/'.join([path, f]))
        uos.rmdir(path)
    else:
        uos.remove(path)
'''


class SendBlock(object):
    def __init__(self, ser):
        self.ser = ser

    def __enter__(self):
        self.ser.write(b'\x05')

    def __exit__(self, _type, value, trace):
        self.ser.write(b'\x04')


class SerialHelper(threading.Thread):
    def __init__(self, port="/dev/ttyUSB0", baud_rate=115200):
        super(SerialHelper, self).__init__()
        self.ser = serial.Serial(port, baud_rate, timeout=0.5)
        self.send_block_helper = SendBlock(self.ser)

        self._recv()
        self.cmd("dir()")
        data = self.ser.readline()
        data = self.ser.readline()
        if data.decode('utf8').find("mpys") == -1:
            self.script("from machine import Pin, PWM", mpys)
            self._recv()

        self.start()

    def _recv(self, output=True):
        while True:
            data = self.ser.readline()
            if output:
                print(data.decode('utf8'), end='')
                # print(data)
            if len(data) == 0:
                break

    def run(self):
        self._recv()
        print(" -*- finish -*- ")

    def cmd(self, s):
        self.ser.write(bytes(s + '\r', encoding='utf8'))

    def script(self, *ss):
        with self.send_block_helper:
            for s in ss:
                self.cmd(s)

    def touch(self, file, content=None):
        with self.send_block_helper:
            self.cmd("with open('" + file + "', 'w') as f:")
            if content is None:
                self.cmd("    pass")
            else:
                self.cmd("    f.write('''" + content)
                self.cmd("''')")

    def log_to_file(self, log, file):
        with self.send_block_helper:
            self.cmd("with open('" + file + "', 'a') as f:")
            self.cmd("    f.write('''" + log)
            self.cmd("''')")

    def ls(self, path='/'):
        self.cmd("uos.listdir('%s')" % path)

    def cat(self, file):
        self.cmd("mpys_read('%s')" % file)

    def mkdir(self, name):
        self.cmd("uos.mkdir('%s')" % name)

    def cp(self, src_file, des_file=None):
        name = os.path.basename(src_file)
        with open(src_file) as f:
            c = f.read()
            c = c.replace('\\', '\\\\')
            self.script("mpys_write('%s', '''%s''', '%s')" % (name if des_file is None else des_file, c, name))

    def rm(self, file):
        self.cmd("mpys_del('%s')" % file)

    def pin(self, n, mode, value=None):
        if mode == "out":
            self.cmd("Pin(%s, Pin.OUT, value=%s)" % (n, value))
        elif mode == "in":
            self.cmd("Pin(%s, Pin.IN).value()" % n)

    def pwm(self, n, freq, duty):
        self.cmd("PWM(Pin(%s), freq=%s, duty=%s)" % (n, freq, duty))

    def cancel(self):
        self.ser.write(b'\x03')

    def reset(self):
        self.ser.write(b'\x04')

    def close(self):
        self.ser.close()
