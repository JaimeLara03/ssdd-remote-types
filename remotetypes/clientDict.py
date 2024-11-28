import sys
import logging
from typing import List
import Ice
import RemoteTypes as rt

from remotetypes.iterable import CancelIteration, StopIteration

class Client(Ice.Application):
    def run(self, argv: List[str]) -> int:
        try:
            # Recibir el proxy del servidor desde la línea de comandos
            proxy = self.communicator().stringToProxy("factory:default -p 10000")
        except IndexError:
            logging.error('¡Se requiere un proxy como argumento!')
            return -1

        # Convertir el proxy en un FactoryPrx
        factory = rt.FactoryPrx.checkedCast(proxy)
        if not factory:
            logging.error('El proxy dado no es un objeto Factory.')
            return -1

        print("Conectado al servidor.")

        # Obtener un diccionario remoto desde la fábrica
        remote_dict = factory.get(rt.TypeName.RDict, "miDiccionario")
        rdict = rt.RDictPrx.checkedCast(remote_dict)

        if not rdict:
            logging.error('No se pudo obtener un RDict remoto.')
            return -1

        print("Diccionario remoto obtenido.")

        # Operaciones con el diccionario remoto
        try:
            # 1. setItem
            print("Añadiendo clave1 -> valor1 al diccionario remoto.")
            rdict.setItem("clave1", "valor1")

            print("Añadiendo clave2 -> valor2 al diccionario remoto.")
            rdict.setItem("clave2", "valor2")

            # 8. iter
            print("Iterando sobre el diccionario remoto.")
            iterator = rdict.iter()
            while True:
                try:
                    key = iterator.next()
                    print(f"Clave: {key}")
                except rt.StopIteration:
                    print("Iteración completada (final del diccionario alcanzado).")
                    break
        except Exception as e:
            print(f"Error inesperado durante la iteración: {e}")

        print("Todas las operaciones completadas exitosamente.")
        return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = Client()
    sys.exit(client.main(sys.argv))
