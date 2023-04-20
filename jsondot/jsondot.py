import json
from typing import Optional, Union


class Dot(object):

    def __init__(self, file_path: Optional[str] = None) -> None:
        self.translation = {}
        self.file_path = file_path
        pass

    def __str__(self) -> str:
        return self.__dict__.__str__()

    def dumps(self):
        items = self.__dict__.items()
        s = ""
        d1 = {}
        for k, v in items:
            if isinstance(v, Dot):
                # v = v.translate(v.__dict__.items(), v.translation)
                v = v.dumps()
                d1[k] = v
            elif isinstance(v, list):
                blist = list()
                for i, elem in enumerate(v):
                    if isinstance(elem, Dot):
                        d = elem.dumps()
                        blist.append(d)
                d1[k] = blist                       
            elif k != 'translation' and k != 'file_path':
                k = self.translation[k]
                d1[k] = v
                # s += d1.__str__()
        s = d1.__str__()
        return s
        pass

    def dump(self, path):
        data = self.dumps()
        data = self.format_json(data)
        with open(path, 'w') as file:
            file.write(data)
        
    def format_json(self, s: str):
        output = ""
        for char in s:
            if char == "'":
                output += '"'
            elif char == '"':
                output += " "
            else:
                output += char
        return output
        
    def load(self, path):
        return JsonDot().load(path)
    
    def loads(self, s: str):
        return JsonDot().loads(str, self)

    def items(self):
        d = self.__dict__.items()
        d1 = self.translate(d, self.translation)
        return d1.items()

    def translate(self, dictionary: dict, translation):
        d1 = {}
        for k, v in dictionary:
            if isinstance(v, Dot):
                bd = {}
                bd[k] = self.translate(v.__dict__.items(), v.translation)
                d1[k] = bd[k]
            elif k != 'translation':
                key = translation[k]
                d1[key] = v
        return d1

    def add_field(self, name, value):
        name = self.format_param(name)
        setattr(self, name, value)
        return self

    def get_field(self, key):
        return self[key]

    def format_param(self, param):
        new_param = ""
        for char in param:
            if char == "-" or char == " ":
                new_param += "_"
            else:
                new_param += char
        new_param = new_param.lower()
        self.translation[new_param] = param
        return new_param


class JsonDot(Dot):

    def __init__(self) -> None:
        self.file_path = ""
        self.data = None
        self.dot = None
        # self.dot = Dot()
        pass

    # def __getattribute__(self, key):
    #     return super().get_field(key)

    def loads(self, s: str):
        self.data = s
        dot = Dot(self.file_path)
        dot = self.__load_data(self.data, dot)
        self.dot = dot
        return self.dot

    def load(self, path: str) -> Dot:
        self.file_path = path
        with open(path, 'r') as f:
            self.data = json.load(f)
        dot = Dot(self.file_path)
        dot = self.__load_data(self.data, dot)
        self.dot = dot
        return self.dot

    def dumps(self):
        formated_json = self.format_json(self.data)
        return formated_json

    def format_json(self, s: str):
        output = ""
        for char in s:
            if char == "'":
                output += '"'
            elif char == '"':
                output += " "
            else:
                output += char
        return output

    def dump(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.dumps())
            
    def process_list_for_load(self, list: list):
        blist = []
        e = None
        d = None
        for elem in list:            
            if isinstance(elem, dict):
                e = elem
                bdot = Dot(self.file_path)
                d = self.__load_data(e, bdot)
                
            elif isinstance(elem, list):
                blist.append(self.__load_data(elem, self.file_path))
            blist.append(d)
        return blist

    def __load_data(self, data: Union[dict,list], dot: Union[Dot,list]):
        # if isinstance(dot, list):
        #     dot.append(Dot(self.file_path))
        #     dot = dot[-1]

        for k, v in data.items():
            if isinstance(v, dict):
                bdot = Dot(self.file_path)
                dot.add_field(k, self.__load_data(v, bdot))
            elif isinstance(v, list):
                blist = self.process_list_for_load(v)
                dot.add_field(k, blist)
            else:
                dot.add_field(k, v)
        return dot
            
    # def process_list_for_load(self, list: list):
    #     blist = []                             
    #     for elem in list:
    #         bdot = Dot(self.file_path)
    #         if isinstance(elem, dict):
    #             blist.append(self.__load_data(elem, bdot))
    #         elif isinstance(elem, list):
    #             blist.append(self.__load_data(elem, bdot))
    #     return blist

    # def __load_data(self, data: dict, dot: Union[Dot, list]):        
    #     for k, v in data.items():
    #         if isinstance(v, dict):
    #             bdot = Dot(self.file_path)
    #             dot.add_field(k, self.__load_data(v, bdot))
    #         elif isinstance(v, list):
    #             blist = self.process_list_for_load(v)
    #             dot.add_field(k, blist)       
    #         else:
    #             dot.add_field(k, v)
    #     return dot
