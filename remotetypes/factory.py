"""Needed classes to implement the Factory interface."""

import RemoteTypes as rt
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet

import logging

import Ice
from typing import Optional, Dict

class Factory(rt.Factory):
    """Skeleton for the Factory implementation."""

    def __init__(self, adapter: Ice.ObjectAdapter) -> None:
        """Initialise the Factory object."""
        self.adapter = adapter  # Adaptador para publicar objetos
        self.instances: Dict[str, Ice.Object] = {}  # Almacenar instancias registradas

    def get(self, typeName: rt.TypeName, identifier: Optional[str] = None, current: Optional[Ice.Current] = None) -> rt.RType:
        """Obtener un objeto remoto según el tipo solicitado."""
        print("Empieza el get")

        # Si el objeto ya existe, devolver su proxy
        if identifier and identifier in self.instances:
            print(f"El objeto '{identifier}' ya existe, devolviendo proxy existente.")
            return self.adapter.createProxy(self.communicator().stringToIdentity(identifier))

        # Crear un nuevo objeto basado en el tipo solicitado
        if typeName == rt.TypeName.RList:
            instance = RemoteList(identifier)
        elif typeName == rt.TypeName.RSet:
            instance = RemoteSet(identifier)
            print("Se creó el RemoteSet")
        elif typeName == rt.TypeName.RDict:
            instance = RemoteDict(identifier)
        else:
            raise ValueError("Unknown type name")

        # Registrar el objeto en el adaptador con una identidad única
        identity = Ice.Identity(name=identifier, category="")
        current.adapter.add(instance, identity)
        self.instances[identifier] = instance  # Almacenar la instancia localmente

        # Generar el proxy remoto y devolverlo
        proxy = current.adapter.createProxy(identity)
        print(f"Proxy generado: {proxy}.")
        
        return rt.RTypePrx.checkedCast(proxy)
