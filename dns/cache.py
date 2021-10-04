import time


class Cache:
    def __init__(self, filename):
        self.filename = filename
        self.data = dict()

    def init(self):
        with open(self.filename) as f:
            for line in f.readlines():
                line = line.rstrip("\n").split(" ")
                name = line[0]
                if name not in self.data:
                    self.data[name] = dict()
                self.data[name][int(line[1])] = line[2:]

    def update(self):
        new_data = dict()
        with open(self.filename, 'w') as f:
            for key, value in self.data.items():
                for kkey, vvalue in value.items():
                    if float(vvalue[2]) > time.time():
                        f.write(f'{key} {kkey} {" ".join(map(str, vvalue))}\n')
                        if key not in new_data.keys():
                            new_data[key] = dict()
                        new_data[key][int(kkey)] = vvalue
        self.data = new_data

    def add_record(self, name, rtype, data):
        if name not in self.data.keys():
            self.data[name] = dict()
        self.data[name][rtype] = data
        self.update()
