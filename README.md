# Laboratorio 3: MQTT hacia Azure IoT Central (Protocolo Visible)

**Estudiante:** Juan Camilo Rojas Guerrero  
**Materia:** IoT + Cloud + Sistemas Distribuidos  
**Universidad Autónoma de Bucaramanga (UNAB)**

## Contenido
- `python-vm/device_sdk.py`: Baseline con SDK oficial del Lab 2.
- `python-vm/device_mqtt_explicit.py`: Cliente MQTT puro con `paho-mqtt` y generación programática de SAS Token.
- `wokwi/`: Firmware C++ y circuito ESP32.

## Cómo generar el SAS Token manualmente
El script `device_mqtt_explicit.py` implementa el cálculo RFC 2104 HMAC-SHA256:
1. Recurso URI: `{HubHost}/devices/{DeviceId}`
2. Firma: `Base64(HMAC-SHA256(DecodedPrimaryKey, UTF8(URI + "\n" + ExpiryTime)))`
3. Password MQTT: `SharedAccessSignature sr={URI}&sig={Signature}&se={ExpiryTime}`
