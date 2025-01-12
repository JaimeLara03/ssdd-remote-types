#!/bin/bash

# Nombre del entorno virtual
ENV_NAME=".venv"

# Crear el entorno virtual
echo "Creando el entorno virtual..."
python3 -m venv $ENV_NAME

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source $ENV_NAME/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar las dependencias principales
echo "Instalando la dependencia principal: zeroc-ice..."
pip install zeroc-ice
pip install confluent_kafka
pip install six
pip install -e .

# Instalar dependencias adicionales
echo "¿Deseas instalar dependencias opcionales para pruebas y linters? (s/n)"
read INSTALL_EXTRAS

if [[ $INSTALL_EXTRAS == "s" ]]; then
    echo "Instalando dependencias opcionales..."
    pip install pytest mypy pylint ruff
else
    echo "Saltando la instalación de dependencias opcionales."
fi

# Verificar si slice2py está disponible
if ! command -v slice2py &> /dev/null; then
    echo "El comando slice2py no está instalado. Por favor, instala Ice antes de continuar."
    echo "Puedes instalarlo siguiendo las instrucciones en: https://zeroc.com/downloads"
    exit 1
fi

# Ejecutar slice2py para descomprimir el archivo Slice
echo "Generando archivos Python desde remotetypes.ice..."
if [[ -f "remotetypes/remotetypes.ice" ]]; then
    slice2py remotetypes/remotetypes.ice
    echo "Generación completada."
else
    echo "Error: El archivo remotetypes/remotetypes.ice no existe."
    exit 1
fi

# Instrucciones para ejecutar el servidor
echo "Para ejecutar el servidor, usa el siguiente comando:"
echo "remotetypes --Ice.Config=config/remotetypes.config"

echo "¡Configuración completada!"

