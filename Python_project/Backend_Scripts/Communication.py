import sys
import glob
import serial
import serial.tools.list_ports
import time
import json
import threading
from Ui_Main_Script import Ui_Connection_Listener


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
            result.append(port[0])

    return result


class Communication:

    def __init__(self):
        self.__stream__ = {}
        self.should_run = True
        self.__port_name__ = None
        self.__port__ = None
        self.ui_adress = None
        self.__private_thread__ = threading.Thread(target=self.__communication_thread__)
        self.__private_thread__.setDaemon(True)

    def set_ui_adress(self, adress):
        self.ui_adress = adress

    def __change_connected_state__(self, state):
        pass
        # self.connection_observer.change_connected_state(state)

    def start_thread(self):
        self.__private_thread__.start()

    def end_thread(self):
        self.should_run = False
        self.__private_thread__.join()
        print("Communication thread joined")

    def update_stream(self, value):
        self.__stream__ = {
            "command": value
        }

    def read_stream(self):
        try:
            print("yo")
            encoded_message = self.__port__.readline().decode("utf-8")
            print("yo2")
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

        try:
            print(str(encoded_message) + " on port " + str(self.__port__.name))
        except:
            print(str(encoded_message) + " on port None")

        try:
            self.__port__.write(bytes(str(encoded_message), "utf-8"))
            print("Write success")
        except serial.SerialException or FileNotFoundError as e:
            # print(str(e) + "\nReconnecting...")
            # self.connect_port()
            # self.send_stream()
            print("Could not send.")

    def find_port(self):
        all_port = serial_ports()
        if len(all_port) < 1:
            if self.__port__ is not None:
                print("No Arduino found !")
                self.__port_name__ = None
                self.__port__ = None
            return False

        elif len(all_port) > 1:
            if self.__port__ is None or str(self.__port__.name) != str(all_port[0]):
                print("More than one Arduino found, using first at: " + all_port[0])
                self.__port_name__ = all_port[0]
        else:
            if self.__port__ is None or not str(self.__port__.name) == str(all_port[0]):
                print("Arduino found at: " + all_port[0])
                self.__port_name__ = all_port[0]

        if self.__port__ is None and self.__port_name__ is not None:
            self.connect_port()
        return True

    def connect_port(self):
        try:
            self.__port__ = serial.Serial(self.__port_name__, baudrate=9600)
        except serial.SerialException or FileNotFoundError:
            self.find_port()
            self.connect_port()
        print("Connected to " + str(self.__port__.name))

    def __communication_thread__(self):
        was_connected = None
        while self.should_run:

            if self.find_port():
                if self.__port__.isOpen():
                    if not was_connected:
                        self.ui_adress.change_connected_state(True)
                        # pass
                        # self.__change_connected_state__(True)
                    else:
                        pass
                    was_connected = True
                else:
                    self.ui_adress.change_connected_state(False)
                    # self.__change_connected_state__(False)
                    was_connected = False
                # print("exist: " + str(port_exists))

            else:
                self.ui_adress.change_connected_state(False)
                # self.__change_connected_state__(False)
                was_connected = False
                print("Exist: False")

            time.sleep(0.5)


class Connection_Observer:

    def change_connected_state(self, state):
        pass


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
