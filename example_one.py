from jsondot.jsondot import JsonDot, Dot


class JsonDotExample():

    def __init__(self) -> None:
        self.json = JsonDot().load('.\\examples\\example.json')

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
        self.json.gustos[1].nombre = "F1"
        self.json.add_field("list_two", [
            {
                "Tipo": "música",
                "Nombre": "rock"
            },
            {
                "Tipo": "deporte",
                "Nombre": "F1"
            }
        ] )
        self.json.list_three = [
            {
                "Tipo": "música",
                "Nombre": "rock"
            },
            {
                "Tipo": "deporte",
                "Nombre": "F1"
            }
        ]

        print("Nombre: " + self.json.nombre)
        print("Apellido: " + self.json.apellido)
        print("Edad: " + str(self.json.edad))

        print("Loaded json")
        print(self.json.dumps())

        s = self.json.dumps()
        print("Dumped string: \n" + s)

        self.json.dump('.\\examples\\example.json')

        pass


if __name__ == "__main__":
    json_dot_example = JsonDotExample()
