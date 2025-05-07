from jsondot.jsondot import JsonDot, Dot


class JsonDotExample():

    def __init__(self) -> None:
        self.d1 = Dot()
        
        self.d1 = self.d1.load(".\\examples\\d1.json")
        
        self.s1 = self.d1.dumps()
        
        self.d1.dump()
        
        print("Dumped string: \n" + self.s1)
        self.json = JsonDot.load('.\\examples\\example.json')

        print("Loaded json")
        print(self.json.dumps())

        self.json.add_field("list_one", [
            "Juan",
            "Pablo",
            "Pedro",
            "Maria",
            "Jose"
        ])

        self.json.lista_nombres = [
            "Ana",
            "Luis",
            "Carlos",
            "Sofia",
            "Elena"
        ]
        self.json.lista_nueva = [
            {
                "Equipo": "McLaren",
                "Pilotos": [
                    {"Nombre": "Lando", "Apellido": "Norris"},
                    {"Nombre": "Oscar", "Apellido": "Piastri"}
                ]
            },
            {
                "Equipo": "Red Bull",
                "Pilotos": [
                    {"Nombre": "Max", "Apellido": "Verstappen"},
                    {"Nombre": "Sergio", "Apellido": "Pérez"}
                ]
            }
        ]

        s = self.json.dumps()
        print("Dumped string: \n" + s)

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
        ])
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

        self.json.diccionario = {
            "Nombre": "Juan",
            "Apellido": "Perez",
            "Edad": 30,
            "Gustos": [
                {"Nombre": "música", "Tipo": "rock"},
                {"Nombre": "deporte", "Tipo": "fútbol"}
            ]
        }

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
