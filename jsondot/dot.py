import json
    
# class Box(object):
    
#     def __init__(self):
#         # self.__dict__.update(data)
#         pass

#     def __getitem__(self, key):
#         return getattr(self, key)

#     def __setitem__(self, key, value):
#         setattr(self, key, value)
    
class Box(object):
    
    def __init__(self) -> None:
        self.translation = {}
        pass
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    # def items(self):
    #     items_list = []
    #     for key, value in self.__dict__.items():
    #         items_list.append((self.translation.get(key, key), value))
    #         if isinstance(value, Box):
    #             items_list.extend([(f"{self.translation.get(key, key)}.{nested_key}", nested_value) 
    #                                for nested_key, nested_value in value.items()])
    #     return items_list
    def items(self):
        d = self.__dict__.items()
        d1 = self.translate(d, self.translation)
        return d1.items()
    
    def translate(self, dictionary: dict, translation):
        d1 = {}
        for k,v in dictionary:
            if isinstance(v, Box):
                bd = {}
                bd[k] =  self.translate(v.__dict__.items(), v.translation)
                d1[k] = bd[k]
            elif k != 'translation':
                key = translation[k]
                d1[key] = v
        return d1
    
    def add_field(self, name, value):
        name = self.format_param(name)
        setattr(self, name, value)
        return self
    
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
        # self.box = Box()
        pass
    
    def from_json(self, path: str):
        with open(path, 'r') as f:
            self.data = json.load(f)            
        box = Box()
        box = self.load_data(self.data, box)
        return box
            
    def load_data(self, data: dict, box: Box):
        for k,v in data.items():
            if isinstance(v, dict):
                bbox = Box()
                box.add_field(k, self.load_data(v, bbox))
            else:
                box.add_field(k, v)
        return box
    # def load_data(self):
    #     for key, value in self.data.items():
    #         self.box.add_field(key, value)
    #     pass
