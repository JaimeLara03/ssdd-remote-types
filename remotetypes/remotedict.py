import RemoteTypes as rt
from typing import Optional
import Ice

from remotetypes.iterable import Iterable  # Importa la clase personalizada Iterable

class RemoteDict(rt.RDict):
    """Implementation of the RDict type."""

    def __init__(self, identifier: str):
        """Initialize the dictionary with a unique identifier."""
        super().__init__()
        self._identifier = identifier
        self._data = {}  # Diccionario interno para almacenar los datos
        self._hash_cache = None  # Caché para el hash del diccionario

    def remove(self, key: str, current: Optional[Ice.Current] = None) -> None:
        """Remove a key from the dictionary."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        del self._data[key]
        self._hash_cache = None  # Reset hash cache

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of items in the dictionary."""
        return len(self._data)

    def contains(self, key: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the dictionary contains a specific key."""
        return key in self._data

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Return a hash value for the dictionary."""
        if self._hash_cache is None:
            self._hash_cache = hash(frozenset(self._data.items()))
        return self._hash_cache

    def setItem(self, key: str, value: str, current: Optional[Ice.Current] = None) -> None:
        """Set a value for a specific key in the dictionary."""
        self._data[key] = value
        self._hash_cache = None  # Reset hash cache

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Get the value associated with a specific key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        return self._data[key]

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Remove and return the value for a specific key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        value = self._data.pop(key)
        self._hash_cache = None  # Reset hash cache
        return value

    def getIdentifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the RemoteDict."""
        return self._identifier

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        hash_cache = hash(tuple(self._data.items()))  # Asegúrate de usar items() si necesitas pares clave-valor
        iterable = Iterable(list(self._data.keys()), hash_cache)  # Solo claves si es necesario
        proxy = current.adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)

