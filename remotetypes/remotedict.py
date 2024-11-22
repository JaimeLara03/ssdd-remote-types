"""Needed classes to implement and serve the RDict type."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error


class RemoteDict(rt.RDict):
    """Implementation of the RDict type."""

    def __init__(self):
        """Initialize the dictionary."""
        self._data = {}
        self._hash_cache = None  # To store the hash value

    def remove(self, key):
        """Remove a key from the dictionary."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        del self._data[key]
        self._hash_cache = None  # Reset hash cache

    def length(self):
        """Return the number of items in the dictionary."""
        return len(self._data)

    def contains(self, key):
        """Check if the dictionary contains a specific key."""
        return key in self._data

    def hash(self):
        """Return a hash value for the dictionary."""
        if self._hash_cache is None:
            self._hash_cache = hash(frozenset(self._data.items()))
        return self._hash_cache

    def setItem(self, key, value):
        """Set a value for a specific key in the dictionary."""
        self._data[key] = value
        self._hash_cache = None  # Reset hash cache

    def getItem(self, key):
        """Get the value associated with a specific key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        return self._data[key]

    def pop(self, key):
        """Remove and return the value for a specific key."""
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found.")
        value = self._data.pop(key)
        self._hash_cache = None  # Reset hash cache
        return value
