import sys
import logging
from typing import List
import Ice
import RemoteTypes as rt

class ClientSet(Ice.Application):
    def run(self, argv: List[str]) -> int:
        try:
            # Conectar al servidor
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

        # Obtener un conjunto remoto desde la fábrica
        remote_set = factory.get(rt.TypeName.RSet, "miConjunto")
        rset = rt.RSetPrx.checkedCast(remote_set)

        if not rset:
            logging.error('No se pudo obtener un RSet remoto.')
            return -1

        print("Conjunto remoto obtenido.")

        # Operaciones con el conjunto remoto
        try:
            # Añadir elementos
            print("Añadiendo elemento1 al conjunto remoto.")
            rset.add("elemento1")

            print("Añadiendo elemento2 al conjunto remoto.")
            rset.add("elemento2")

            # length
            print(f"Longitud actual del conjunto: {rset.length()}")

            # contains
            print(f"¿Contiene elemento1? {rset.contains('elemento1')}")
            print(f"¿Contiene elemento_inexistente? {rset.contains('elemento_inexistente')}")

            # hash
            hash1 = rset.hash()
            print(f"Hash actual del conjunto: {hash1}")

            # Iteración
            print("Iterando sobre el conjunto remoto:")
            try:
                iterator = rset.iter()
                while True:
                    try:
                        item = iterator.next()
                        print(f"Elemento: {item}")
                    except rt.StopIteration:
                        print("Iteración completada.")
                        break
                    except rt.CancelIteration:
                        print("Iteración cancelada debido a modificaciones en el conjunto.")
                        break
            except Exception as e:
                print(f"Error inesperado durante la iteración: {e}")

            # Modificar durante la iteración
            print("Iterando sobre el conjunto remoto con modificación durante la iteración:")
            try:
                iterator = rset.iter()
                # Modificar el conjunto después de obtener el iterador
                rset.add("elemento3")
                while True:
                    try:
                        item = iterator.next()
                        print(f"Elemento: {item}")
                    except rt.StopIteration:
                        print("Iteración completada.")
                        break
                    except rt.CancelIteration:
                        print("Iteración cancelada debido a modificaciones en el conjunto.")
                        break
            except Exception as e:
                print(f"Error inesperado durante la iteración: {e}")

            # Verificación final de longitud
            print(f"Longitud final del conjunto: {rset.length()}")

        except Exception as e:
            print(f"Error durante las operaciones: {e}")
            return -1

        print("Todas las operaciones completadas exitosamente.")
        return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = ClientSet()
    sys.exit(client.main(sys.argv))
