import sys
import logging
from typing import List
import Ice
import RemoteTypes as rt


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
            # 1.8 RDict.setItem invocado correctamente
            print("Añadiendo clave1 -> valor1 al diccionario remoto.")
            rdict.setItem("clave1", "valor1")

            print("Añadiendo clave2 -> valor2 al diccionario remoto.")
            rdict.setItem("clave2", "valor2")

            # 1.3 RDict.length devuelve la longitud
            print(f"Longitud actual del diccionario: {rdict.length()}")

            # 1.5 RDict.contains devuelve True
            print(f"¿Contiene clave1? {rdict.contains('clave1')}")

            # 1.4 RDict.contains devuelve False
            print(f"¿Contiene clave_inexistente? {rdict.contains('clave_inexistente')}")

            # 1.10.1 RDict.getItem devuelve el valor
            print(f"Valor asociado a clave1: {rdict.getItem('clave1')}")

            # 1.6 RDict.hash devuelve enteros iguales
            hash1 = rdict.hash()
            print(f"Hash actual del diccionario: {hash1}")
            hash2 = rdict.hash()
            print(f"Hash actual del diccionario sin modificaciones: {hash2}")
            if hash1 == hash2:
                print("El hash del diccionario no ha cambiado sin modificaciones.")

            # 1.7 RDict.hash devuelve enteros diferentes
            rdict.setItem("clave3", "valor3")
            hash3 = rdict.hash()
            print(f"Hash del diccionario después de modificación: {hash3}")
            if hash1 != hash3:
                print("El hash del diccionario ha cambiado después de una modificación.")

            # 1.9 RDict.getItem lanza KeyError
            try:
                print("Intentando obtener valor de clave_inexistente.")
                valor_inexistente = rdict.getItem("clave_inexistente")
            except rt.KeyError:
                print("Se lanzó KeyError al intentar obtener una clave que no existe.")

            # 1.10.2 RDict.getItem mantiene el valor
            valor = rdict.getItem("clave3")
            print(f"Valor asociado a clave3: {valor}")
            print(f"¿Contiene clave3 después de getItem? {rdict.contains('clave3')}")

            # 1.11 RDict.pop lanza KeyError
            try:
                print("Intentando hacer pop de clave_inexistente.")
                valor = rdict.pop("clave_inexistente")
            except rt.KeyError:
                print("Se lanzó KeyError al intentar hacer pop de una clave que no existe.")

            # 1.12.1 RDict.pop devuelve el valor y 1.12.2 RDict.pop elimina el valor
            print("Eliminando y obteniendo clave3.")
            value = rdict.pop("clave3")
            print(f"Valor eliminado: {value}")
            print(f"¿Contiene clave3 después de pop? {rdict.contains('clave3')}")

            # 1.1 RDict.remove borra un elemento por clave
            print("Eliminando clave2 del diccionario remoto usando remove.")
            rdict.remove("clave2")
            print("Clave2 eliminada.")

            # 1.2 RDict.remove devuelve excepción
            try:
                print("Intentando eliminar clave_inexistente usando remove.")
                rdict.remove("clave_inexistente")
            except rt.KeyError:
                print("Se lanzó KeyError al intentar eliminar una clave que no existe.")

            # 1.3 RDict.length devuelve la longitud (después de eliminaciones)
            print(f"Longitud actual del diccionario después de eliminaciones: {rdict.length()}")

            # 4.1 iter devuelve un objeto de tipo Iterable
            print("Obteniendo un iterador del diccionario remoto.")
            iterator = rdict.iter()
            if iterator:
                print("El método iter devolvió un objeto de tipo Iterable.")
            else:
                print("El método iter no devolvió un objeto válido.")

            # 4.2 next devuelve el elemento siguiente y 4.3 next lanza StopIteration
            print("Iterando sobre el diccionario remoto:")
            try:
                while True:
                    try:
                        key = iterator.next()
                        print(f"Clave: {key}")
                    except rt.StopIteration:
                        print("Iteración completada.")
                        break
                    except rt.CancelIteration:
                        print("Iteración cancelada debido a modificaciones en el diccionario.")
                        break
            except Exception as e:
                print(f"Error inesperado durante la iteración: {e}")

            # 4.4 next lanza CancelIteration
            print("Iterando sobre el diccionario remoto con modificación durante la iteración:")
            try:
                iterator = rdict.iter()
                # Modificar el diccionario después de obtener el iterador
                rdict.setItem("clave4", "valor4")
                while True:
                    try:
                        key = iterator.next()
                        print(f"Clave: {key}")
                    except rt.StopIteration:
                        print("Iteración completada.")
                        break
                    except rt.CancelIteration:
                        print("Iteración cancelada debido a modificaciones en el diccionario.")
                        break
            except Exception as e:
                print(f"Error inesperado durante la iteración: {e}")

            # Verificación final de longitud
            print(f"Longitud final del diccionario: {rdict.length()}")

        except Exception as e:
            print(f"Error durante las operaciones: {e}")
            return -1


        print("\nLista \n.")
        
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
            elemento_popped = rlist.pop(1)
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
        
        
    
        print("\nSET \n.")

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
    client = Client()
    sys.exit(client.main(sys.argv))
