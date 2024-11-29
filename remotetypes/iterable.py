"""Needed classes for implementing the Iterable interface for different types of objects."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import Ice
from typing import List, Optional

# TODO: It's very likely that the same Iterable implementation doesn't fit
# for the 3 needed types. It is valid to implement 3 different classes implementing
# the same interface and use an object from different implementations when needed.

import Ice

class StopIteration(Ice.UserException):
    def __init__(self, reason=""):
        Ice.UserException.__init__(self)
        self.reason = reason

    def __str__(self):
        return self.reason

class CancelIteration(Ice.UserException):
    def __init__(self, reason=""):
        Ice.UserException.__init__(self)
        self.reason = reason

    def __str__(self):
        return self.reason



class IterableRList(rt.Iterable):
    """Implementation for the Iterable interface."""

    def __init__(self, remote_list):
        self._remote_list = remote_list  # Referencia al RemoteList original
        self._hash_cache = remote_list.hash()  # Hash inicial de la lista
        self._data = list(remote_list._data)  # Copia de los datos de la lista
        self._index = 0  # Índice para iterar sobre los elementos

    def next(self, current=None):
        # Verificar si la lista fue modificada
        current_hash = self._remote_list.hash()
        if self._hash_cache != current_hash:
            raise rt.CancelIteration()

        if self._index >= len(self._data):
            raise rt.StopIteration()

        item = self._data[self._index]
        self._index += 1
        return item
    
class IterableRDict(rt.Iterable):
    def __init__(self, remote_dict):
        self._remote_dict = remote_dict  # Referencia al RemoteDict original
        self._hash_cache = remote_dict.hash()  # Hash inicial del diccionario
        self._keys = list(remote_dict._data.keys())  # Capturar las claves actuales del diccionario
        self._index = 0  # Índice para iterar sobre las claves

    def next(self, current: Optional[Ice.Current] = None):
        # Verificar si el diccionario fue modificado
        current_hash = self._remote_dict.hash()
        if self._hash_cache != current_hash:
            raise rt.CancelIteration()

        if self._index >= len(self._keys):
            raise rt.StopIteration()

        key = self._keys[self._index]
        self._index += 1
        return key


class IterableRSet(rt.Iterable):
    def __init__(self, remote_set):
        self._remote_set = remote_set  # Referencia al RemoteSet original
        self._hash_cache = remote_set.hash()  # Hash inicial del conjunto
        self._items = list(remote_set._storage_)  # Capturar los elementos actuales del conjunto
        self._index = 0  # Índice para iterar sobre los elementos

    def next(self, current=None):
        # Verificar si el conjunto fue modificado
        current_hash = self._remote_set.hash()
        if self._hash_cache != current_hash:
            raise rt.CancelIteration()

        if self._index >= len(self._items):
            raise rt.StopIteration()

        item = self._items[self._index]
        self._index += 1
        return item

