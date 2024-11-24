import sys
import logging
from typing import List
import Ice
import RemoteTypes as rt
from remotetypes.iterable import StopIteration, CancelIteration

class Client(Ice.Application):
    def run(self, argv: List[str]) -> int:
        try:
            # Recibir el proxy del servidor desde la línea de comandos
            proxy = self.communicator().stringToProxy("factory:default -p 10000")
        except IndexError:
            logging.error("¡Se requiere un proxy como argumento!")
            return -1

        # Convertir el proxy en un FactoryPrx
        factory = rt.FactoryPrx.checkedCast(proxy)
        if not factory:
            logging.error("El proxy dado no es un objeto Factory.")
            return -1

        print("Conectado al servidor.")

        # Obtener una lista remota desde la fábrica
        remote_list = factory.get(rt.TypeName.RList, "miLista")
        rlist = rt.RListPrx.checkedCast(remote_list)

        if not rlist:
            logging.error("No se pudo obtener un RList remoto.")
            return -1

        print("Lista remota obtenida.")

        try:
            # Probar append
            print("Añadiendo elementos a la lista.")
            rlist.append("valor1")
            rlist.append("valor2")
            rlist.append("valor3")
            print("Elementos añadidos: valor1, valor2, valor3.")

            # Probar iterador
            print("Iterando a través de la lista remota:")
            iterator = rlist.iter()
            try:
                while True:
                    element = iterator.next()
                    print(f"Elemento: {element}")
            except Exception as e:
                print("Iteración completada.")
            except CancelIteration:
                print("Iteración cancelada debido a modificaciones.")

            # Probar getItem
            print("Recuperando elementos de la lista.")
            print(f"Elemento en posición 0: {rlist.getItem(0)}")
            print(f"Elemento en posición 1: {rlist.getItem(1)}")
            print(f"Elemento en posición 2: {rlist.getItem(2)}")

            # Probar contains
            print("Verificando si la lista contiene ciertos valores.")
            print(f"¿Contiene 'valor2'? {rlist.contains('valor2')}")
            print(f"¿Contiene 'valor4'? {rlist.contains('valor4')}")

            # Probar remove
            print("Eliminando 'valor2' de la lista.")
            rlist.remove("valor2")
            print("'valor2' eliminado.")

            # Probar length
            print(f"Longitud de la lista: {rlist.length()}")

            # Probar hash
            print("Calculando el hash de la lista.")
            hash1 = rlist.hash()
            print(f"Hash actual: {hash1}")

            # Probar pop
            print("Eliminando y recuperando el último elemento de la lista.")
            ultimo = rlist.pop()
            print(f"Último elemento eliminado: {ultimo}")

            print("Eliminando y recuperando el primer elemento de la lista.")
            primero = rlist.pop(0)
            print(f"Primer elemento eliminado: {primero}")

            # Manejo explícito de excepciones para remove
            print("Intentando eliminar un elemento inexistente.")
            try:
                rlist.remove("valorNoExistente")
            except Exception as e:
                print(f"Excepción capturada: {e}")

            print("Intentando acceder a un índice fuera de rango.")
            try:
                rlist.getItem(10)
            except Exception as e:
                print(f"Excepción capturada: {e}")

            print("Intentando hacer pop de un índice fuera de rango.")
            try:
                rlist.pop(10)
            except Exception as e:
                print(f"Excepción capturada: {e}")

        except Exception as e:
            logging.error(f"Error durante las operaciones: {e}")
            return -1

        print("Todas las operaciones completadas exitosamente.")
        return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = Client()
    sys.exit(client.main(sys.argv))
