"""Needed classes to implement the Factory interface."""

import RemoteTypes as rt
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet
from RemoteTypes import TypeName, RTypePrx


class Factory(rt.Factory):
    """Skeleton for the Factory implementation."""

    def __init__(self):
        """Initialize the Factory with an empty object registry."""
        self._objects = {}  # Dictionary to store objects by their identifier

    def get(self, type_name, identifier=None):
        """Create or retrieve a remote object."""
        if identifier and identifier in self._objects:
            return self._objects[identifier]  # Reuse existing object

        # Create a new object based on type_name
        if type_name == TypeName.RDict:
            new_object = RemoteDict()
        elif type_name == TypeName.RList:
            new_object = RemoteList()
        elif type_name == TypeName.RSet:
            new_object = RemoteSet()
        else:
            raise ValueError(f"Unknown type: {type_name}")

        # Store the object in the registry if identifier is provided
        if identifier:
            self._objects[identifier] = new_object

        return new_object
