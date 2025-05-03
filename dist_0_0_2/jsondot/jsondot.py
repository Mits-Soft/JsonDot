import os
import json
from typing import Optional, Union, Any


class Dot(object):

    def __init__(self, file_path: Optional[str] = None, data: Optional[dict] = None) -> None:
        self.translation = {}
        self.file_path = file_path
        if data == None:
            self.data = {}
        else:
            self.data = data
        pass

    def __str__(self) -> str:
        return self.__dict__.__str__()
    
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
    
    def process_list(self, l: list):
        return JsonDot().process_list_for_load(l)
    
    # def items(self):
    #     d = self.__dict__.items()
    #     d1 = self.pack_items(d, self.translation)
    #     return d1.items()   
    
    def process_list_for_bumps(self, l: list):
        blist = []
        e = None
        d = None
        for elem in l:            
            if isinstance(elem, Dot):
                e = elem
                d = elem.__dumps()               
            if isinstance(elem, list):
                e = elem
                d = self.process_list_for_bumps(e)
            blist.append(d)
        return blist
    
    def dumps_in_list(self, format: bool = False):
        data = self.__dumps()
        if format == True:
            return self.format_json(data)
        else:
            return data
        
    def dumps(self):
        return json.dumps(self.data, indent = 4, ensure_ascii=False)
    
    # def dumps(self, dot = None):
    #     if dot == None: dot = self
    #     for key, value in self.data:
    #         if isinstance(value, Dot):
    #             dot.set_field(key, self.dumps(value))
    #     return json.dumps(dot.data, indent = 4)

    def __dumps(self):
        items = self.__dict__.items()
        s = ''
        d1 = {}
        for k, v in items:
            if isinstance(v, Dot):
                v = v.__dumps()
                d1[k] = v
            elif isinstance(v, list):
                blist = list()
                for i, elem in enumerate(v):
                    if isinstance(elem, Dot):
                        d = elem.__dumps()
                        blist.append(d)
                    if isinstance(elem, list):
                        clist = self.process_list_for_bumps(elem)
                        blist.append(clist)
                d1[k] = blist                       
            elif k != 'file_path' and k != 'translation' and k != 'data':
                k = self.translation[k]
                d1[k] = v
        # s = d1.__str__()
        # s = str(d1)
        s = json.dumps(d1)
        return s

    def dump(self, path = None):
        if path == None:
            path = self.file_path
        path = os.path.normpath(path)
        data = self.dumps()
        # data = self.format_json(data)
        # with open(path, 'w', encoding="utf-8") as file:
        #     file.write(data)
            
        try:
            with open(path, "w") as f:
                f.write(data)
        except Exception as e:
            raise e
        
    def format_json(self, s: str):
        output = ''
        for char in s:
            if char == "'":
                output += '"'
            # elif char == '"':
            #     output += " "
            else:
                output += char
        output = output.replace('True', '"true"')
        output = output.replace('False', '"false"')
        return output
    
    def load_data_from_dot(self, data, dot):
        return JsonDot().load_data(data.data, dot)
    
    def __load_data(self, data: Union[dict,list]):
        return JsonDot().load_data(data, Dot())
        
    def load(self, path):
        return JsonDot().load(path)
    
    def loads(self, s: str):
        return JsonDot().loads(str, self)

    def items(self):
        d = self.__dict__.items()
        d1 = self.pack_items(d, self.translation)
        return d1.items()

    def pack_items(self, dictionary: dict, translation):
        d1 = {}
        for k, v in dictionary:
            if isinstance(v, Dot):
                bd = {}
                # bd[k] = v
                bd[k] = self.pack_items(v.__dict__.items(), v.translation)
                d1[k] = bd[k]
            # elif k != 'file_path':
            elif k != 'translation' and k != 'file_path' and k != 'data':
                # key = translation[k]
                d1[k] = v
        return d1
    
    # def pack_items(self, dictionary: dict, translation):
    #     d1 = {}
    #     for k, v in dictionary:
    #         if isinstance(v, Dot):
    #             bd = {}
    #             bd[k] = self.translate(v.__dict__.items(), v.translation)
    #             d1[k] = bd[k]
    #         elif k != 'translation' and k != 'file_path':
    #             key = translation[k]
    #             d1[key] = v
    #     return d1

    def add_field(self, name, value):
        name = self.format_param(name)
        fname = self.format_field_name_for_dict(name)
        if fname not in self.data:
            if isinstance(value, Dot):
                self.data[fname] = value.data
            else:
                self.data[fname] = value
        setattr(self, name, value)
        return self

    def add_field_to_data(self, name, value):
        fname = self.format_field_name_for_dict(name)
        self.data[fname] = value
        return self

    def set_field(self, name, value):
        lname = self.format_param(name)
        fname = self.format_field_name_for_dict(name)
        if isinstance(value, Dot):
            self.data[fname] = value.data
        else:
            self.data[fname] = value
        setattr(self, lname, value)        
        return self
    
    def add_element_to_list(self, name, elem):
        self.__dict__[name].append(elem)
        if len(self.data[self.format_field_name_for_dict(name)]) != 0 and isinstance(self.data[self.format_field_name_for_dict(name)][len(self.data[self.format_field_name_for_dict(name)]) - 1], Dot):
            l = self.data[self.format_field_name_for_dict(name)].copy()
            l.pop()
            l.append(elem.data)
            self.data[self.format_field_name_for_dict(name)] = l
        else:
            self.data[self.format_field_name_for_dict(name)].append(elem.data)
            
    def add_list_of_elements(self, name, elems_list):
        for elem in elems_list:
            self.add_element_to_list(name, elem)
            

    def get_field(self, key):
        value = self.__dict__[key]
        return value
        # return self[key]
        
    def get_dot_by_name(self, s: str):
        l = s.split(".")
        dot = self.retrieve_dot(l)
        return dot
    
    def retrieve_dot(self, l: list, dot = None):
        if dot == None:
            dot = self
        for j, n in enumerate(l):
            l[j] = self.format_param(n)
                    
        for i, dot_name in enumerate(l):
            node = dot.__dict__[dot_name]
            if i + 1 > len(l):
                return node
            is_dot = isinstance(node, Dot)
            is_in_node = i + 1 < len(l) and l[i + 1] in node.__dict__
            is_not_node_in_dot = i + 1 < len(l) and not isinstance(node.__dict__[l[i + 1]], Dot)
            if is_dot and is_in_node and is_not_node_in_dot:
                ndot = Dot(self.file_path)
                ndot.add_field(l[i + 1], node.get_field(l[i + 1]))   
                return node               
            else:
                dotn = l.pop(i)
                dotb = dot.__dict__[dotn]
                node = self.retrieve_dot(l, dotb)
                return node
            

    def format_field_name_for_dict(self, param):
        new_param = ""
        for char in param:
            if char == "_" or char == " ":
                new_param += "-"
            else:
                new_param += char
        new_param = new_param.lower()
        # self.translation[new_param] = param
        return new_param
    
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


class JsonDot():

    def __init__(self) -> None:
        self.file_path = ""
        self.data = None
        self.dot = None
        pass

    def loads(self, s: str):
        self.data = json.loads(s)
        dot = Dot(self.file_path, self.data)
        dot = self.__load_data(self.data, dot)
        self.dot = dot
        return self.dot

    def load(self, path: str) -> Dot:
        self.file_path = path
        with open(path, 'r') as f:
            self.data = json.load(f)
        dot = Dot(self.file_path, self.data)
        dot = self.__load_data(self.data, dot)
        self.dot = dot
        return self.dot
    
    def dumps(self):
        return self.__dumps()

    def __dumps(self):
        formated_json = self.format_json(self.data)
        return formated_json

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

    def dump(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.__dumps())
            
    def process_list_for_load(self, l: list):
        blist = []
        e = None
        d = None
        for elem in l:            
            if isinstance(elem, dict):
                e = elem
                bdot = Dot(self.file_path)
                d = self.__load_data(e, bdot)
                
            elif isinstance(elem, list):
                e = elem
                d = self.process_list_for_load(e)
            blist.append(d)
        return blist
    
    def load_data(self, data: Union[dict,list], dot: Union[Dot,list]):
        return self.__load_data(data, dot)

    def __load_data(self, data: Union[dict,list], dot: Union[Dot,list]):
        for k, v in data.items():
            if isinstance(v, dict):
                bdot = Dot(self.file_path, v)
                dot.add_field(k, self.__load_data(v, bdot))
            elif isinstance(v, list):
                blist = self.process_list_for_load(v)
                dot.add_field(k, blist)
            else:
                dot.add_field(k, v)
        return dot

