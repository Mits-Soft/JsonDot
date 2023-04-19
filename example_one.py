from jsondot import JsonDot


class JsonDotExample():

    def __init__(self) -> None:
        self.json = JsonDot().load('.\examples\example.json')
        
        print("Loaded json")
        print(self.json.dumps())
        
        print("Value got from json using dot")
        print("Nombre: " + self.json.nombre)        
        print("Apellido: " + self.json.apellido)        
        print("Edad: " + str(self.json.edad))        
        
        print("Change name to Pinocho Geppetto") 
        self.json.nombre = "Pinocho"
        self.json.apellido = "Geppetto"
        self.json.edad = 6
        
        print("Nombre: " + self.json.nombre)        
        print("Apellido: " + self.json.apellido)        
        print("Edad: " + str(self.json.edad))
        
        print("Loaded json")
        print(self.json.dumps())
        
        s = self.json.dumps()
        
        self.j = JsonDot().loads(s)
        
        self.j.dump('.\examples\example.json')
             
        s = self.json.dumps()
        print("Dumped string: \n" + s)
        
        
        pass
    
if __name__ == "__main__":
    json_dot_example = JsonDotExample()
