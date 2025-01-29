from confluent_kafka import Consumer, Producer
import json

# Configuraciones de Kafka
TOPIC_INPUT = "operations"     # Ajusta según tu configuración
TOPIC_OUTPUT = "results"       # Ajusta según tu configuración
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

# Suscribimos el consumidor al tópico de entrada
consumidor.subscribe([TOPIC_INPUT])


def procesar_mensaje(mensaje):
    """
    Procesa un solo mensaje (un diccionario con la petición)
    y devuelve una respuesta.
    """
    respuesta = {"id": mensaje.get("id"), "estado": "error"}
    try:
        identificador_objeto = mensaje["object_identifier"]
        tipo_objeto = mensaje["object_type"]
        operacion = mensaje["operation"]
        argumentos = mensaje.get("args", {})

        if operacion == "iter":
            respuesta["error"] = "OperacionNoSoportada"
        else:
            resultado = invocar_operacion_remota(
                identificador_objeto,
                tipo_objeto,
                operacion,
                argumentos
            )
            respuesta["estado"] = "ok"
            respuesta["resultado"] = resultado

    except KeyError as e:
        respuesta["error"] = f"Clave faltante: {str(e)}"
    except Exception as e:
        respuesta["error"] = str(e)

    return respuesta


def invocar_operacion_remota(identificador_objeto, tipo_objeto, operacion, argumentos):
    """
    Lógica para realizar la operación en el servidor remoto.
    Ajusta esta parte con la lógica específica de tu aplicación.
    """
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
        # Espera (poll) por mensajes de Kafka
        msg = consumidor.poll(1.0)

        # Si no llega nada, sigue esperando
        if msg is None:
            continue

        # Si hay error en el mensaje, lo notificamos y continuamos
        if msg.error():
            print(f"Error al consumir mensaje: {msg.error()}")
            continue

        # Decodificamos el contenido del mensaje de Kafka a string
        raw_value = msg.value().decode('utf-8')

        # Intentamos convertirlo a JSON
        try:
            datos = json.loads(raw_value)
        except json.JSONDecodeError:
            print(f"Mensaje no es un JSON válido: {raw_value}")
            # Continuamos con el siguiente mensaje sin interrumpir el programa
            continue

        # 'datos' puede ser una lista o un diccionario
        if isinstance(datos, list):
            print(f"Mensaje recibido (lista de peticiones): {datos}")

            for peticion in datos:
                respuesta = procesar_mensaje(peticion)
                print(f"Respuesta generada: {respuesta}")

                productor.produce(
                    TOPIC_OUTPUT,
                    key=str(respuesta["id"]),          # clave del mensaje (opcional, útil para particiones)
                    value=json.dumps(respuesta)        # convertimos la respuesta a JSON
                )

            productor.flush()

        elif isinstance(datos, dict):
            print(f"Mensaje recibido (petición única): {datos}")

            respuesta = procesar_mensaje(datos)
            print(f"Respuesta generada: {respuesta}")

            productor.produce(
                TOPIC_OUTPUT,
                key=str(respuesta["id"]),
                value=json.dumps(respuesta)
            )
            productor.flush()

        else:
            # Si no es ni lista ni dict, es un formato inesperado
            print("Mensaje recibido con formato inesperado (ni lista ni diccionario).")

except KeyboardInterrupt:
    print("Finalizando cliente...")

finally:
    consumidor.close()
