"""Needed classes for implementing the Iterable interface for different types of objects."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import Ice
from typing import List, Optional

from RemoteTypes import StopIteration

# TODO: It's very likely that the same Iterable implementation doesn't fit
# for the 3 needed types. It is valid to implement 3 different classes implementing
# the same interface and use an object from different implementations when needed.

class StopIteration(Ice.UserException):
    """Exception raised when iteration is completed."""
    pass


class CancelIteration(Ice.UserException):
    """Exception raised when the iterable object is modified."""
    pass


class IterableRList(rt.Iterable):
    """Implementation for the Iterable interface."""

    def __init__(self, data: List[str], hash_cache: int):
        """
        Initialize the Iterable object.
        :param data: The data to iterate over.
        :param hash_cache: Cached hash value of the data to detect modifications.
        """
        self._data = data  # Datos del objeto iterado
        self._index = 0  # Índice actual en la iteración
        self._hash_cache = hash_cache  # Caché del hash inicial para detectar modificaciones

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Obtiene el siguiente elemento en el iterador."""
        # Verificar si el objeto iterado fue modificado
        if self._hash_cache != hash(tuple(self._data)):
            raise rt.CancelIteration()

        # Verificar si ya no hay más elementos en la lista
        if self._index >= len(self._data):
            raise rt.StopIteration()

        # Devolver el elemento actual y avanzar el índice
        element = self._data[self._index]
        self._index += 1
        return element

    def cancel(self, hash_cache: int, current: Optional[Ice.Current] = None) -> None:
        """Cancel the iteration if the object has been modified."""
        if hash_cache != self._hash_cache:
            raise CancelIteration()
        
class IterableRDict(rt.Iterable):
    """Iterador para RemoteDict."""

    def __init__(self, data: dict, hash_cache: int):
        """
        Inicializar el iterador del diccionario remoto.
        :param data: Diccionario de pares clave-valor o lista de pares clave-valor.
        :param hash_cache: Caché de hash inicial para detectar modificaciones.
        """
        if isinstance(data, dict):
            self._data = data # Convierte el diccionario a una lista de pares clave-valor
        elif isinstance(data, list):
            self._data = list(data.items())  # Asume que ya es una lista de pares clave-valor
        else:
            raise TypeError("El parámetro 'data' debe ser un diccionario o una lista de pares clave-valor.")

        self._index = 0  # Índice actual en la iteración
        self._hash_cache = hash_cache  # Hash inicial del diccionario

    def next(self, current: Optional[Ice.Current] = None) -> tuple:
        """
        Obtiene el siguiente par clave-valor en el iterador.
        :raises StopIteration: Si se alcanza el final de la iteración.
        :raises CancelIteration: Si el objeto iterado fue modificado.
        """
        # Verificar si el objeto iterado fue modificado
        if self._hash_cache != hash(frozenset(self._data.items())):
            raise rt.CancelIteration("El diccionario fue modificado.")

        # Verificar si ya no hay más elementos en el diccionario
        if self._index >= len(self._data):
            raise rt.StopIteration("No hay más elementos para iterar.")

        # Obtener las claves del diccionario como una lista ordenada
        keys = list(self._data.keys())

        # Devolver el par clave-valor actual y avanzar el índice
        current_key = keys[self._index]
        current_value = self._data[current_key]
        self._index += 1
        return current_key, current_value



