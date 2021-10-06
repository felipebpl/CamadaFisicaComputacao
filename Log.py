from datetime import datetime

class Log():
    def __init__(self, info, alteration): #alteration = Receb/Envia
        self.msg_type = info[0]
        self.size = len(info)
        self.alteration = alteration
        self.time = datetime.now()
        self.all = []

        if self.msg_type == 3:
            self.pkg_id = info[4]
            self.total_pkg = info[3]
            self.crc = str(info[8:10]).upper()
            self.crc = self.crc[4:6] + self.crc[8:10]

        else:
            self.pkg_id = ''
            self.total_pkg = ''
            self.crc = ''

    def create_log(self):
        if self.msg_type == 3:
            info = f'{self.time} / {self.alteration} / {self.msg_type} / {self.size} / {self.pkg_id} / {self.total_pkg} / {self.crc}'
        else:
            info = f'{self.time} / {self.alteration} / {self.msg_type} / {self.size}'
        return info

    def write_logs(self, info, filename):
        # quando passar o atributo filename, ja definir o path, server ou client, e a teste que for Ex: write_logs(Log, 'Client1.txt')
        self.all.append(info)
        file = open(filename, "a")
        for info in self.all:
            file.write(info)
            file.write('\n')
            file.close()