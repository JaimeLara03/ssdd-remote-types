import RemoteTypes as rt
from typing import Optional
import Ice

from remotetypes.iterable import IterableRDict  # Importa la clase personalizada Iterable

class RemoteDict(rt.RDict):
    """Implementación de la interfaz RDict."""

    def __init__(self, identifier: str):
        """Inicializa el diccionario remoto con un identificador único."""
        super().__init__()
        self._identifier = identifier
        self._data = {}  # Diccionario interno para almacenar los datos

    def remove(self, key: str, current: Optional[Ice.Current] = None) -> None:
        """Elimina una clave del diccionario."""
        if key not in self._data:
            raise rt.KeyError(key=key)
        del self._data[key]

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Devuelve el número de elementos en el diccionario."""
        return len(self._data)

    def contains(self, key: str, current: Optional[Ice.Current] = None) -> bool:
        """Verifica si el diccionario contiene una clave específica."""
        return key in self._data

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Devuelve un valor hash para el diccionario."""
        return hash(frozenset(self._data.items()))

    def setItem(self, key: str, value: str, current: Optional[Ice.Current] = None) -> None:
        """Establece un valor para una clave específica en el diccionario."""
        self._data[key] = value

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Obtiene el valor asociado a una clave específica."""
        if key not in self._data:
            raise rt.KeyError(key=key)
        return self._data[key]

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Elimina y devuelve el valor para una clave específica."""
        if key not in self._data:
            raise rt.KeyError(key=key)
        return self._data.pop(key)

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Devuelve el identificador del RemoteDict."""
        return self._identifier

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """
        Devuelve un proxy para un iterador del diccionario.
        """
        adapter = current.adapter
        if not adapter:
            raise RuntimeError("El adaptador no está disponible.")

        # Pasar una referencia al RemoteDict y su hash actual al iterador
        iterable = IterableRDict(self)

        # Registrar el iterador en el adaptador de objetos
        proxy = adapter.addWithUUID(iterable)

        # Obtener el proxy como un objeto de tipo IterablePrx
        iterable_proxy = rt.IterablePrx.checkedCast(proxy)
        if not iterable_proxy:
            raise RuntimeError("No se pudo crear un proxy válido para el iterador.")

        print(f"Iterador creado para el diccionario con {len(self._data)} elementos.")
        return iterable_proxy




