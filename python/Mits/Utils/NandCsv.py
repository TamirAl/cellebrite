import csv
FILE_PATH = r"R:\Research\Wiki\Chipsets\Qualcomm\NAND_LIST.csv"


class NandCsv(object):
    def __init__(self, file_path = None):
        if (None == file_path):
            file_path = FILE_PATH
        self.file_path = file_path
        self.csv_data = self.read_csv_file()
        self.names = self.csv_data[0]
        self.dic = self.build_dic()
        
    def read_csv_file(self):
        res = []
        f = open(self.file_path)
        reader = csv.reader(f)
        for i in reader:
            all_empty = True
            for x in i:
                if x != "":
                    all_empty = False
                    break
            if all_empty == False:
                res.append(i)
        f.close()
        return res


    def build_dic(self):
        res = {}
        for line in self.csv_data[1:]:
            res[(eval(line[0]), eval(line[1]))] = zip(self.names, line)
        return res
        


    def get_digits(self, data):
        return int(filter(lambda x:x.isdigit(),data ))
        
    def handle_width(self, data):
        width = self.get_digits(data)
        if (width == 8):
            return 0
        if (width == 16):
            return 1
        print "Unknown device width: %s", data
        raise
        
    def parse_entry(self, entry):
        d = {"page" : ("PageSize",   lambda x: eval(x)),
             "oob"  : ("SpareSize",  lambda x: eval(x)),
             "block": ("BlockSize",  lambda x: self.get_digits(x)*1024 / self.result["PageSize"]),
             "bus"  : ("Width",      lambda x: self.handle_width(x)),
             "mb"   : ("BlockCount", lambda x: (self.get_digits(x) * 1024 * 1024) / self.result["PageSize"] / self.result["BlockSize"])
             }
        
        if (d.has_key(entry[0].lower())):
             new_entry = d[entry[0].lower()]
             return new_entry[0], new_entry[1](entry[1])
        return entry
        
    def handle_data(self, data):
        self.result = {}
        for entry in data:
            if ((len(entry[0]) > 0) and (len(entry[1]) > 0)):
                rec = self.parse_entry(entry)
                self.result[rec[0]] = rec[1]
        return self.result


    def get_data(self, makeId, deviceId):
        data = self.search_data(makeId, deviceId)
        return self.handle_data(data)


    def search_data(self, makerId, deviceId):
        if (self.dic.has_key( (makerId, deviceId))):
            return self.dic[(makerId, deviceId)]
        else:
            raise Exception("Device Not Found")
