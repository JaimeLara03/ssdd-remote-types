from confluent_kafka import Consumer, Producer
import json

# Configuraciones iniciales
TOPIC_INPUT = "operations"  # Cambia según la configuración
TOPIC_OUTPUT = "results"      # Cambia según la configuración
BROKER_KAFKA = "localhost:9092"
ID_GRUPO = "remotetypes_grupo"

configuracion_consumidor = {
    'bootstrap.servers': BROKER_KAFKA,
    'group.id': ID_GRUPO,
    'auto.offset.reset': 'earliest'
}
consumidor = Consumer(configuracion_consumidor)

configuracion_productor = {
    'bootstrap.servers': BROKER_KAFKA
}
productor = Producer(configuracion_productor)

consumidor.subscribe([TOPIC_INPUT])

def procesar_mensaje(mensaje):
    """Procesa un mensaje y devuelve una respuesta"""
    respuesta = {"id": mensaje.get("id"), "estado": "error"}
    try:
        identificador_objeto = mensaje["object_identifier"]
        tipo_objeto = mensaje["object_type"]
        operacion = mensaje["operation"]
        argumentos = mensaje.get("args", {})

        if operacion == "iter":
            respuesta["error"] = "OperacionNoSoportada"
        else:
            resultado = invocar_operacion_remota(identificador_objeto, tipo_objeto, operacion, argumentos)
            respuesta["estado"] = "ok"
            respuesta["resultado"] = resultado
    except KeyError as e:
        respuesta["error"] = f"Clave faltante: {str(e)}"
    except Exception as e:
        respuesta["error"] = str(e)

    return respuesta

def invocar_operacion_remota(identificador_objeto, tipo_objeto, operacion, argumentos):
    """Lógica para realizar la operación en el servidor remoto"""

    if tipo_objeto == "RSet":
        return f"Procesado {operacion} en {identificador_objeto}"
    elif tipo_objeto == "RList":
        return f"Procesado {operacion} en {identificador_objeto}"
    elif tipo_objeto == "RDict":
        return f"Procesado {operacion} en {identificador_objeto}"
    else:
        raise ValueError(f"Tipo de objeto desconocido: {tipo_objeto}")

try:
    while True:
        msg = consumidor.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error al consumir mensaje: {msg.error()}")
            continue

        mensaje_entrada = json.loads(msg.value().decode('utf-8'))
        print(f"Mensaje recibido: {mensaje_entrada}")

        respuesta = procesar_mensaje(mensaje_entrada)
        print(f"Respuesta: {respuesta}")

        productor.produce(
            TOPIC_OUTPUT,
            key=str(respuesta["id"]),
            value=json.dumps(respuesta)
        )
        productor.flush()

except KeyboardInterrupt:
    print("Finalizando cliente...")

finally:
    consumidor.close()
