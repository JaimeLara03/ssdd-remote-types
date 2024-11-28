"""Needed classes to implement and serve the RList type."""

import RemoteTypes as rt 
from typing import Optional
import Ice, IcePy

from remotetypes.iterable import IterableRList  # Importa la clase personalizada Iterable

class RemoteList(rt.RList):
    """Implementation of the RList type."""

    def __init__(self, identifier: str):
        """
        Initialize the RemoteList.
        :param identifier: Unique identifier for the list.
        :param adapter: Ice ObjectAdapter to register iterators.
        """
        super().__init__()
        self._identifier = identifier  # Identificador único de la lista
        self._data = []  # Datos de la lista
        self._hash_cache = None  # Caché para el hash de la lista

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Return a proxy to an iterator for the list."""
        # Crear un iterador basado en la lista actual
        iterator = IterableRList(self)

        # Obtener el adaptador del servidor desde el contexto actual
        adapter = current.adapter
        if not adapter:
            raise RuntimeError("El adaptador no está disponible.")

        # Registrar el iterador en el adaptador de objetos
        proxy = adapter.addWithUUID(iterator)

        # Registrar el proxy como un tipo específico de iterador
        iterable_proxy = rt.IterablePrx.checkedCast(proxy)
        if not iterable_proxy:
            raise RuntimeError("No se pudo crear un proxy válido para el iterador.")

        print(f"Iterador creado para la lista con {len(self._data)} elementos.")
        return iterable_proxy


    def remove(self, value: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an element by value."""
        if value not in self._data:
            raise rt.KeyError(f"Value '{value}' not found.")
        self._data.remove(value)
        self._hash_cache = None  # Reset hash cache
        print(f"Removed value: {value}")

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the length of the list."""
        return len(self._data)

    def contains(self, value: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the list contains a specific value."""
        return value in self._data

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Return a hash value for the list."""
        if self._hash_cache is None:
            self._hash_cache = hash(tuple(self._data))
        return self._hash_cache

    def append(self, value: str, current: Optional[Ice.Current] = None) -> None:
        """Append an element to the end of the list."""
        self._data.append(value)
        self._hash_cache = None  # Reset hash cache
        print(f"Appended value: {value}")

    def pop(self, index=None, current: Optional[Ice.Current] = None) -> str:
        """Remove and return the element at the given position or the last element."""
        try:
            index = int(index) if index is not None else -1
        except (ValueError, TypeError):
            index = -1

        if not self._data:
            raise rt.IndexError("Cannot pop from an empty list.")

        if index >= len(self._data):
            raise rt.IndexError(f"Index '{index}' out of range.")

        value = self._data.pop(index)
        self._hash_cache = None  # Reset hash cache
        print(f"Popped value at index {index}: {value}")
        return value

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Return the element at the given position."""
        if index < 0 or index >= len(self._data):
            raise rt.IndexError(f"Index '{index}' out of range.")
        value = self._data[index]
        print(f"Retrieved item at index {index}: {value}")
        return value

    def getIdentifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the RemoteList."""
        return self._identifier
