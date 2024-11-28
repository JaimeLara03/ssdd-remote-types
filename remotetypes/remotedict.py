import RemoteTypes as rt
from typing import Optional
import Ice

from remotetypes.iterable import IterableRDict  # Importa la clase personalizada Iterable

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
        """
        Devuelve un proxy para un iterador del diccionario.
        """
        if not self._data:
            raise rt.StopIteration()

        # Crear un iterador basado en las claves del diccionario
        hash_cache = hash(frozenset(self._data.items()))
        iterable = IterableRDict(list(self._data.keys()), hash_cache)

        # Obtener el adaptador del servidor desde el contexto actual
        adapter = current.adapter
        if not adapter:
            raise RuntimeError("El adaptador no está disponible.")

        # Registrar el iterador en el adaptador de objetos
        proxy = adapter.addWithUUID(iterable)

        # Registrar el proxy como un tipo específico de iterador
        iterable_proxy = rt.IterablePrx.checkedCast(proxy)
        if not iterable_proxy:
            raise RuntimeError("No se pudo crear un proxy válido para el iterador.")

        print(f"Iterador creado para el diccionario con {len(self._data)} claves.")
        return iterable_proxy


