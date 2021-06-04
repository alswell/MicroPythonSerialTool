import os
import sys
from mpys import SerialHelper

CMD = ["reset", "cancel", "ls", "cat", "mkdir", "cp", "rm", "pin", "pwm"]


def main():
    if sys.argv[1] == "help":
        print("supported commands:", CMD)
        return
    if sys.argv[1] not in CMD:
        print("unsupported command:", sys.argv[1])
        return
    port = os.environ.get("mpys_port", "/dev/ttyUSB0")
    baud = os.environ.get("mpys_baud", "115200")
    print("using port: %s, baud rate: %s" % (port, baud))
    s = SerialHelper(port, int(baud))
    f = s.__getattribute__(sys.argv[1])
    f(*sys.argv[2:])
    s.join()
    s.close()


if __name__ == '__main__':
    main()
