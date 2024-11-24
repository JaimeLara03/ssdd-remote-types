import RemoteTypes as rt
from typing import Optional
import Ice


class RemoteDict(rt.RDict):
    """Implementation of the RDict type."""

    def __init__(self, identifier: str):
        """Initialize the dictionary with a unique identifier."""
        super().__init__()  # Inicializar la clase base de Ice
        self._identifier = identifier  # Identificador único del diccionario
        self._data = {}  # Diccionario interno para almacenar los datos
        self._hash_cache = None  # Caché para el valor hash del diccionario

    def remove(self, key: str, current: Optional[Ice.Current] = None) -> None:
        """Remove a key from the dictionary."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        del self._data[key]
        self._hash_cache = None  # Reset hash cache
        print(f"Removed key: {key}")

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
        print(f"Set item: {key} -> {value}")

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Get the value associated with a specific key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        value = self._data[key]
        print(f"Get item: {key} -> {value}")
        return value

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Remove and return the value for a specific key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        value = self._data.pop(key)
        self._hash_cache = None  # Reset hash cache
        print(f"Popped item: {key} -> {value}")
        return value

    def getIdentifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the RemoteDict."""
        return self._identifier
