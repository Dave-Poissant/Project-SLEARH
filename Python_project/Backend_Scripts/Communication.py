import sys
import glob
import serial
import serial.tools.list_ports
import time
import json


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
        self.__stream__ = {}
        self.__port_name__ = None
        self.__port__ = None
        self.connect_port()

    def update_stream(self, value):
        self.__stream__ = {
            "command": value
        }

    def read_stream(self):
        try:
            encoded_message = self.__port__.readline().decode("utf-8")
            encoded_message = encoded_message.split(":")
            first_part_encoded_message = encoded_message[0].split('"')
            second_part_encoded_message = encoded_message[1].split('}')
            dict_encoded_message = {first_part_encoded_message[1]: second_part_encoded_message[0]}
            message = json.dumps(dict_encoded_message)
            incoming_message = json.loads(message)
            return incoming_message["com_state"]
        except serial.SerialException or FileNotFoundError:
            self.connect_port()
            return self.read_stream()

    def send_stream(self):
        encoded_message = json.dumps(self.__stream__)
        print(encoded_message)
        try:
            self.__port__.write(bytes(str(encoded_message), "utf-8"))
        except serial.SerialException or FileNotFoundError:
            self.connect_port()
            self.send_stream()

    def find_port(self):
        all_port = serial_ports()
        if len(all_port) < 1:
            print("No Arduino found !")
        elif len(all_port) > 1:
            print("More than one Arduino found, using first at: " + all_port[0])
            self.__port_name__ = all_port[0]
        else:
            print("Arduino found at: " + all_port[0])
            self.__port_name__ = all_port[0]

    def connect_port(self):
        self.find_port()
        while self.__port_name__ is None:
            self.find_port()

        self.__port__ = serial.Serial(self.__port_name__, baudrate=9600)


Instance = Communication()
# msg = 1

# if __name__ == "__main__":
#     while True:
#         # if msg == 0:
#         #     msg = 1
#         # else:
#         #     msg = 0
#
#         try:
#             incoming = Instance.read_stream()
#             print(str(type(incoming)))
#             print("Im printin this: " + incoming)
#         except Exception as e:
#             print(e)
#
#         # try:
#         #     ser.write(bytes(str(msg), "utf-8"))
#         # except Exception as e:
#         #     print(e)
#
#         # ser.close()
#         # time.sleep(1)
