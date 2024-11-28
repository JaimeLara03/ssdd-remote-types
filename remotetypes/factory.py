import RemoteTypes as rt
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet

import logging
import json
import os
import atexit

import Ice
from typing import Optional, Dict

class Factory(rt.Factory):
    """Implementación de la Factory con persistencia."""

    def __init__(self, adapter: Ice.ObjectAdapter) -> None:
        """Inicializa el objeto Factory."""
        self.adapter = adapter  # Adaptador para publicar objetos
        self.instances: Dict[str, Ice.Object] = {}  # Almacenar instancias registradas
        self.load_data()  # Cargar datos al iniciar
        atexit.register(self.save_data)  # Registrar función para guardar datos al salir

    def load_data(self):
        """Carga los datos de las estructuras remotas desde un archivo JSON."""
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                # Cargar RDicts
                for identifier, obj_data in data.get('RDict', {}).items():
                    instance = RemoteDict(identifier)
                    instance._data = obj_data
                    self.instances[identifier] = instance
                    self.adapter.add(instance, Ice.Identity(name=identifier, category=""))
                # Cargar RLists
                for identifier, obj_data in data.get('RList', {}).items():
                    instance = RemoteList(identifier)
                    instance._data = obj_data
                    self.instances[identifier] = instance
                    self.adapter.add(instance, Ice.Identity(name=identifier, category=""))
                # Cargar RSets
                for identifier, obj_data in data.get('RSet', {}).items():
                    instance = RemoteSet(identifier)
                    instance._storage_._data = set(obj_data)
                    self.instances[identifier] = instance
                    self.adapter.add(instance, Ice.Identity(name=identifier, category=""))
            print("Datos cargados desde data.json")
        else:
            print("No se encontró data.json, iniciando con datos vacíos")

    def save_data(self):
        """Guarda los datos de las estructuras remotas en un archivo JSON."""
        data = {'RDict': {}, 'RList': {}, 'RSet': {}}
        for identifier, instance in self.instances.items():
            if isinstance(instance, RemoteDict):
                data['RDict'][identifier] = instance._data
            elif isinstance(instance, RemoteList):
                data['RList'][identifier] = instance._data
            elif isinstance(instance, RemoteSet):
                data['RSet'][identifier] = list(instance._storage_)
        with open('data.json', 'w') as f:
            json.dump(data, f)
        print("Datos guardados en data.json")

    def get(self, typeName: rt.TypeName, identifier: Optional[str] = None, current: Optional[Ice.Current] = None) -> rt.RType:
        """Obtiene un objeto remoto según el tipo solicitado."""
        # Si el objeto ya existe, devolver su proxy
        if identifier and identifier in self.instances:
            identity = Ice.Identity(name=identifier, category="")
            return rt.RTypePrx.checkedCast(self.adapter.createProxy(identity))

        # Crear un nuevo objeto basado en el tipo solicitado
        if typeName == rt.TypeName.RList:
            instance = RemoteList(identifier)
        elif typeName == rt.TypeName.RSet:
            instance = RemoteSet(identifier)
        elif typeName == rt.TypeName.RDict:
            instance = RemoteDict(identifier)
        else:
            raise ValueError("Unknown type name")

        # Registrar el objeto en el adaptador con una identidad única
        identity = Ice.Identity(name=identifier, category="")
        self.adapter.add(instance, identity)
        self.instances[identifier] = instance  # Almacenar la instancia localmente

        # Generar el proxy remoto y devolverlo
        proxy = self.adapter.createProxy(identity)
        return rt.RTypePrx.checkedCast(proxy)
