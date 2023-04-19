import json


class Dot(object):

    def __init__(self, file_path) -> None:
        self.translation = {}
        self.file_path = file_path
        pass

    # def __getitem__(self, key):
    #     return getattr(self, key)

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
            elif k != 'translation' and k != 'file_path':
                k = self.translation[k]
                d1[k] = v
                # s += d1.__str__()
        s = d1.__str__()
        return s
        pass

    def dump(self, path):
        data = ""
        s = self.dumps()
        jd = JsonDot().loads(s)
        jd.dump(path)
        # with open(path, 'w') as file:
        #     file.write(data)

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
        return self

    def load(self, path: str):
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

    def __load_data(self, data: dict, dot: Dot):
        for k, v in data.items():
            if isinstance(v, dict):
                bdot = Dot(self.file_path)
                dot.add_field(k, self.__load_data(v, bdot))
            else:
                dot.add_field(k, v)
        return dot
