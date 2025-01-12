
# Repositorio de herramientas de Kafka para la sesión de laboratorio

Este documento ha sido realizado por **Jaime Lara Contento**. La clase del cliente Kafka se encuentra dentro de `remotetypes/clientekafka.py`.

## Despliegue del servicio Kafka

Para desplegar el servicio Kafka, se puede utilizar **Docker Compose**:

```bash
docker compose up -d
```

## Herramientas de CLI

Las herramientas de línea de comandos de Kafka permiten interactuar con un servidor Kafka. **Todos los comandos deben ejecutarse dentro de un contenedor Docker que tenga Kafka instalado.**

Para acceder al contenedor Docker, utiliza:

```bash
docker exec -it <nombre_del_contenedor_kafka> /bin/bash
```

### Listar topics en un broker de Kafka

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

**Ejemplo de salida:**

```
example
```

### Producir un mensaje

```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic example
```

Después de ejecutar el comando, escribe tu mensaje y pulsa **Enter**. Para terminar de escribir el mensaje, presiona **Control+D**. Para finalizar la ejecución sin enviar más mensajes, presiona **Control+D** nuevamente.

### Consumir mensajes desde el principio

```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic example --from-beginning
```

Si se quieren consumir sólo mensajes nuevos, se puede ajustar la opción `--offset` según sea necesario.

Para imprimir metadatos además de los mensajes, se pueden usar las propiedades `--property`. Por ejemplo, para imprimir el número de partición y offset de cada mensaje:

```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic example --from-beginning --property print.partition=true --property print.offset=true
```

Para detener el consumidor, se puede pulsar **Control+C** o usar la opción `--timeout-ms` para que finalice automáticamente después de un período de inactividad.

## Enviar y recibir mensajes

### Enviar mensajes al topic

Para enviar mensajes de petición de operación, sigue los pasos:

1. Accede al contenedor de Docker con Kafka:

   ```bash
   docker exec -it <nombre_del_contenedor_kafka> /bin/bash
   ```

2. Usa el siguiente comando para enviar mensajes JSON al topic configurado:

   ```bash
   kafka-console-producer.sh --bootstrap-server localhost:9092 --topic <nombre_del_topic>
   ```

3. Escribe el mensaje en formato JSON. Ejemplo:

```json
{"id": "12345", "object_identifier": "obj1", "object_type": "RSet", "operation": "add", "args": {"value": "elemento"}}
```

4. Pulsa **Control+D** para enviar el mensaje.

**Nota:** Si los mensajes no respetan el formato, asegúrate de manejar los errores como se define en el enunciado.

### Recibir mensajes del topic de respuesta

Para verificar las respuestas desde otro topic:

```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <nombre_del_topic_respuesta> --from-beginning
```

Esto mostrará las respuestas en el siguiente formato JSON:

```json
{"id": "12345", "status": "ok", "result": "Operación completada correctamente"}
```

## Solución de problemas con Docker

Si experimentas problemas con Docker o el cliente de Kafka, puedes limpiar todos los contenedores, volúmenes y datos usando el siguiente comando:

```bash
docker system prune -a --volumes
```

> **Advertencia:** Este comando eliminará **todos** los contenedores, redes, volúmenes y datos asociados en tu sistema Docker. Utilízalo con precaución.
