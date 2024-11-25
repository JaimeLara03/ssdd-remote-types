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


class Iterable(rt.Iterable):
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
