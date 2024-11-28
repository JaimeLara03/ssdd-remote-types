"""Needed classes to implement and serve the RSet type."""

from typing import Optional

import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

from remotetypes.customset import StringSet
from remotetypes.iterable import IterableRSet

class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier) -> None:
        """Initialise a RemoteSet with an empty StringSet."""
        self._storage_ = StringSet()
        self.id_ = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self._storage_.remove(item)
        except KeyError as error:
            raise rt.KeyError(item) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self._storage_)
        contents.sort()
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Crea un objeto iterable para el conjunto remoto."""
        adapter = current.adapter
        if not adapter:
            raise RuntimeError("El adaptador no está disponible.")

        # Crear el iterador y pasar una referencia al RemoteSet
        iterable = IterableRSet(self)

        # Registrar el iterador en el adaptador de objetos
        proxy = adapter.addWithUUID(iterable)

        # Obtener el proxy como un objeto de tipo IterablePrx
        iterable_proxy = rt.IterablePrx.checkedCast(proxy)
        if not iterable_proxy:
            raise RuntimeError("No se pudo crear un proxy válido para el iterador.")

        print(f"Iterador creado para el conjunto con {len(self._storage_)} elementos.")
        return iterable_proxy

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new string to the StringSet."""
        self._storage_.add(item)

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            return self._storage_.pop()

        except KeyError as exc:
            raise rt.KeyError() from exc
