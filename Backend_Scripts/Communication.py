import sys
import glob
import serial
import serial.tools.list_ports

good_com_port = "COM7"


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = list(serial.tools.list_ports.comports())
        # ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        if "Arduino" in port[1]:
            try:
                s = serial.Serial(port[0])
                s.close()
                result.append(port[0])
            except (OSError, serial.SerialException):
                pass
    return result


class Communication:
    def __init__(self):
        self.__port__ = None
        self.__stream__ = {}

    def update_stream(self, key, value):
        self.__stream__[key] = value

    def read_stream(self, key):
        if key in self.__stream__:
            return self.__stream__[key]
        return None

    def send_stream(self, key, message):
        if key in self.__stream__:
            all_ports = self.find_port()
            for port in all_ports:
                s = serial.Serial(port)
                if s.name == good_com_port:
                    s.write(bytes(message, "utf-8"))
                s.close()


if __name__ == "__main__":
    com = Communication()
    ser = None
    while True:
        ports = serial_ports()
        if len(ports) < 1:
            print("No Arduino found !")
        elif len(ports) > 1:
            print("More than one Arduino found, using first at: " + ports[0])
        else:
            print("Arduino found at: " + ports[0])
            ser = serial.Serial(ports[0], baudrate=9600)
        msg = 'b'

        try:
            incoming = ser.readline().decode("utf-8")
            print(incoming)
        except Exception as e:
            print(e)

        try:
            ser.write(bytes(msg, "utf-8"))
        except Exception as e:
            print(e)

        ser.close()
