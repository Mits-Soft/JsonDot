import json
from typing import Optional, Union, Any

class Dot(object):
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        self.translation = {}
        self.file_path = file_path
        pass

    def __str__(self) -> str:
        return self.__dict__.__str__()
    
    def __setattr__(self, name: str, value: Any) -> None:
        # if not (hasattr(value, "check") and getattr(value, "check") == "true"):
        #     attr_obj = self.create_attr_obj(name, value)
        #     attr_obj["check"] = "true"
        #     super().__setattr__(attr_obj["name"], attr_obj["value"])
        # else:
        super().__setattr__(name, value)
        
    def create_attr_obj(self, name: str, value: Any):
        # name = self.format_param(name)
        if isinstance(value, list):
            ao = {"name": name, "value": self.process_list(value), "check": "true"}
        else:
            ao = {"name": name, "value": value, "check": "true"}
        return ao
    
    def loads(self, s: str):
        return JsonDot().loads(str, self)
        
    def load(self, path):
        return JsonDot().load(path)
        
    def __load_data(self, data: Union[dict,list]):
        return JsonDot().load_data(data, Dot())    
    
    def load_field(self, name, value):
        name = self.format_param(name)
        setattr(self, name, value)
        return self

    def add_field(self, name, value):
        name = self.format_param(name)
        if isinstance(value, list):
            blist = self.process_list(value)
            setattr(self, name, blist)
        else: 
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
    
    @staticmethod
    def process_list_static(l: list, file_path: Optional[str] = None):
        return Dot._shared_process_list(l, file_path)
    
    def process_list(self, l: list):
        return self._shared_process_list(l, self.file_path)
    
    @staticmethod
    def _shared_process_list(l: list, file_path: Optional[str]):
        blist = []
        for elem in l:            
            if isinstance(elem, dict):
                bdot = Dot(file_path)
                d = JsonDot()._JsonDot__load_data(elem, bdot)
            elif isinstance(elem, list):
                d = Dot._shared_process_list(elem, file_path)
            else:
                d = elem
            blist.append(d)
        return blist
    
    def process_list_for_dumps(self, l: list):
        blist = []
        e = None
        d = None
        for elem in l:            
            if isinstance(elem, Dot):
                e = elem
                d = elem.__dumps()               
            if isinstance(elem, list):
                e = elem
                d = self.process_list_for_dumps(e)
            blist.append(d)
        return blist
    
    def dumps(self):
        data = self.__dumps()
        return self.format_json(data)

    def __dumps(self):
        items = self.__dict__.items()
        s = ''
        d1 = {}
        for k, v in items:
            if isinstance(v, Dot):
                v = v.__dumps()
                if self.translation and k in self.translation:
                    k = self.translation[k]
                d1[k] = v
            elif isinstance(v, list):
                blist = list()
                for i, elem in enumerate(v):
                    if isinstance(elem, Dot):
                        d = elem.__dumps()
                        blist.append(d)
                    if isinstance(elem, list):
                        clist = self.process_list_for_dumps(elem)
                        blist.append(clist)
                if self.translation and k in self.translation:
                    k = self.translation[k]
                d1[k] = blist                       
            elif k != 'translation' and k != 'file_path':
                if self.translation and k in self.translation:
                    k = self.translation[k]
                d1[k] = v
        s = d1.__str__()
        return s
        pass

    def dump(self, path):
        self.file_path = path
        data = self.__dumps()
        data = self.format_json(data)
        with open(path, 'w') as file:
            file.write(data)
        
    def format_json(self, s: str):
        output = ''
        for char in s:
            if char == "'":
                output += '"'
            elif char == '"':
                output += " "
            else:
                output += char
        return output

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

class JsonDot():

    def __init__(self) -> None:
        self.file_path = ""
        self.data = None
        self.dot = None
        pass

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
    
    def load_data(self, data: Union[dict,list], dot: Union[Dot,list]):
        return self.__load_data(data, dot)

    def __load_data(self, data: Union[dict,list], dot: Union[Dot,list]):
        for k, v in data.items():
            if isinstance(v, dict):
                bdot = Dot(self.file_path)
                dot.load_field(k, self.__load_data(v, bdot))
            elif isinstance(v, list):
                blist = self.process_list_for_load(v)
                dot.load_field(k, blist)
            else:
                dot.load_field(k, v)
        return dot
            
    def process_list_for_load(self, l: list):
        return Dot.process_list_static(l, self.file_path)
    
    def dumps(self):
        return self.__dumps()

    def __dumps(self):
        formated_json = self.format_json(self.data)
        return formated_json

    def dump(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.__dumps())

    def format_json(self, s: str):
        output = ''
        for char in s:
            if char == "'":
                output += '"'
            elif char == '"':
                output += " "
            else:
                output += char
        return output

