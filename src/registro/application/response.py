


class RegistroResponse():

    @staticmethod
    def Registro(listaRegistro, type):
        if type == "Pred":
            counts = {
                'N': 0,
                'V': 0,
                '!': 0,
                'F': 0,
                'f': 0
            }
            for item in listaRegistro:
                if item in counts:
                    counts[item] += 1
            data = counts
        elif type == "BPM":
            data = listaRegistro

        elif type == "ECG":
            data = listaRegistro
        return data
