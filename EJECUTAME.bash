#!/bin/bash

# Nombre del entorno virtual
ENV_NAME="env"

# Crear el entorno virtual
echo "Creando el entorno virtual..."
python3 -m venv $ENV_NAME

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source $ENV_NAME/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar la dependencia principal
echo "Instalando la dependencia principal..."
pip install .

# Instalar dependencias para pruebas y linters
echo "¿Deseas instalar las dependencias para pruebas y linters? (s/n)"
read INSTALL_EXTRAS

if [[ $INSTALL_EXTRAS == "s" ]]; then
    echo "Instalando dependencias para pruebas..."
    pip install .[tests]

    echo "Instalando dependencias para linters..."
    pip install .[linters]
else
    echo "Saltando la instalación de dependencias adicionales."
fi

# Verificar si slice2py está instalado
if ! command -v slice2py &> /dev/null; then
    echo "El comando slice2py no está instalado. Por favor, instala Ice antes de continuar."
    echo "Puedes instalarlo siguiendo las instrucciones en: https://zeroc.com/downloads"
    exit 1
fi

# Ejecutar slice2py para descomprimir el archivo Slice
echo "Descomprimiendo el archivo Slice..."
if [[ -f "remotetypes/remotetypes.ice" ]]; then
    slice2py remotetypes/remotetypes.ice
    echo "Descompresión completada."
else
    echo "Error: El archivo remotetypes/remotetypes.ice no existe."
    exit 1
fi

# Instrucciones para ejecutar el servidor
echo "Para ejecutar el servidor, usa el siguiente comando:"
echo "remotetypes --Ice.Config=config/remotetypes.config"

echo "¡Configuración completada!"
