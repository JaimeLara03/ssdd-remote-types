import sys
import logging
from typing import List
import Ice
import RemoteTypes as rt

class RListClient(Ice.Application):
    def run(self, argv: List[str]) -> int:
        # Conectar al servidor
        proxy_str = "factory:default -p 10000"
        proxy = self.communicator().stringToProxy(proxy_str)

        # Convertir el proxy en un FactoryPrx
        factory = rt.FactoryPrx.checkedCast(proxy)
        if not factory:
            logging.error('El proxy dado no es un objeto Factory.')
            return -1

        print("Conectado al servidor.")

        # Obtener un RList remoto desde la fábrica
        remote_list = factory.get(rt.TypeName.RList, "miLista")
        rlist = rt.RListPrx.checkedCast(remote_list)

        if not rlist:
            logging.error('No se pudo obtener un RList remoto.')
            return -1

        print("Lista remota obtenida.")

        # Limpiar la lista remota antes de las pruebas
        print("Limpiando la lista remota.")
        try:
            while True:
                rlist.pop()
        except rt.IndexError:
            pass  # La lista está vacía

        try:
            # 2.8 RList.append añade un elemento al final
            print("Añadiendo 'elemento1' a la lista remota.")
            rlist.append("elemento1")
            print("Añadiendo 'elemento2' a la lista remota.")
            rlist.append("elemento2")

            # 2.3 RList.length devuelve la longitud
            length = rlist.length()
            print(f"Longitud actual de la lista: {length}")

            # 2.5 RList.contains devuelve True
            contains_elemento1 = rlist.contains("elemento1")
            print(f"¿Contiene 'elemento1'? {contains_elemento1}")

            # 2.4 RList.contains devuelve False
            contains_inexistente = rlist.contains("elemento_inexistente")
            print(f"¿Contiene 'elemento_inexistente'? {contains_inexistente}")

            # 2.12.1 RList.getItem devuelve el elemento indicado
            elemento_pos0 = rlist.getItem(0)
            print(f"Elemento en posición 0: {elemento_pos0}")

            # 2.12.2 RList.getItem mantiene el elemento indicado
            elemento_pos0_post = rlist.getItem(0)
            print(f"Elemento en posición 0 después de getItem: {elemento_pos0_post}")

            # 2.13 RList.getItem lanza IndexError
            print("Intentando obtener elemento en posición inválida.")
            try:
                rlist.getItem(10)
            except rt.IndexError as e:
                print(f"Se lanzó IndexError al intentar obtener una posición inválida.")

            # 2.6 RList.hash devuelve enteros iguales
            hash1 = rlist.hash()
            print(f"Hash actual de la lista: {hash1}")

            # 2.7 RList.hash devuelve enteros diferentes
            print("Modificando la lista y verificando el hash.")
            rlist.append("elemento3")
            hash2 = rlist.hash()
            print(f"Hash después de modificación: {hash2}")
            if hash1 != hash2:
                print("El hash ha cambiado después de la modificación.")

            # 2.10.1 y 2.10.2 RList.pop devuelve y elimina el elemento indicado
            print("Haciendo pop en posición 1.")
            elemento_popped = rlist.pop(-4)
            print(f"Elemento obtenido: {elemento_popped}")
            length_post_pop = rlist.length()
            print(f"Longitud de la lista después de pop: {length_post_pop}")

            # 2.11 RList.pop lanza IndexError
            print("Intentando hacer pop en posición inválida.")
            try:
                rlist.pop(10)
            except rt.IndexError as e:
                print("Se lanzó IndexError al intentar hacer pop en una posición inválida.")

            # 2.9.1 y 2.9.2 RList.pop devuelve y elimina el elemento del final
            print("Haciendo pop del último elemento.")
            elemento_popped_final = rlist.pop()
            print(f"Elemento obtenido: {elemento_popped_final}")
            length_final = rlist.length()
            print(f"Longitud final de la lista: {length_final}")

            # 2.2 RList.remove devuelve excepción
            print("Intentando eliminar 'elemento_inexistente'.")
            try:
                rlist.remove("elemento_inexistente")
            except rt.KeyError as e:
                print(f"Se lanzó KeyError al intentar eliminar un elemento que no existe: {e.key}")

            # 2.1 RList.remove borra un elemento por valor
            print("Eliminando 'elemento1' de la lista.")
            rlist.remove("elemento1")
            length_after_remove = rlist.length()
            print(f"Longitud de la lista después de eliminar 'elemento1': {length_after_remove}")

            # Verificar que la lista está vacía
            if length_after_remove == 0:
                print("La lista está vacía después de eliminar todos los elementos.")

            # Iteración sobre la lista
            print("Iterando sobre la lista remota:")
            try:
                iterator = rlist.iter()
                while True:
                    try:
                        item = iterator.next()
                        print(f"Elemento: {item}")
                    except rt.StopIteration:
                        print("Iteración completada.")
                        break
                    except rt.CancelIteration:
                        print("Iteración cancelada debido a modificaciones en la lista.")
                        break
            except Exception as e:
                print(f"Error durante la iteración: {e}")

        except Exception as e:
            print(f"Error durante las operaciones: {e}")
            return -1

        print("Pruebas de RList completadas exitosamente.")
        return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = RListClient()
    sys.exit(client.main(sys.argv))
