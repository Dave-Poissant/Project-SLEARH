import json

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

    def find_port(self):
        pass

if __name__ == "__main__":
    com = Communication()
    com.update_stream('char', 'a')

    print(str(com.read_stream('char')))


    #ports = serial.tools.list_ports.comports()
    #print("number of ports: " + str(len(ports)))

    