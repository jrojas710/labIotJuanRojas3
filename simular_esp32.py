import time
import json
import random
import hmac
import hashlib
import base64
import urllib.parse
import ssl
import paho.mqtt.client as mqtt

# ==========================================
# CREDENCIALES
# ==========================================
IOT_HUB_HOSTNAME = "iotc-20ba21f7-4249-41e6-bb9c-55e4a8891e49.azure-devices.net"
DEVICE_ID = "Vacuna-ESP32-Wokwi"
PRIMARY_KEY = "kMVZcf/Ihj0ahCfgq/3xnAl+TxTjceGuF+Zjxu76itE="

# Generador manual de SAS Token (RFC 2104 HMAC-SHA256)
def generate_sas_token(uri, key, expiry=3600):
    ttl = int(time.time()) + expiry
    uri_enc = urllib.parse.quote_plus(uri)
    sig_raw = f"{uri_enc}\n{ttl}"
    key_bytes = base64.b64decode(key)
    sig = hmac.new(key_bytes, sig_raw.encode('utf-8'), hashlib.sha256).digest()
    sig_enc = urllib.parse.quote_plus(base64.b64encode(sig))
    return f"SharedAccessSignature sr={uri_enc}&sig={sig_enc}&se={ttl}"

uri = f"{IOT_HUB_HOSTNAME}/devices/{DEVICE_ID}"
sas_token = generate_sas_token(uri, PRIMARY_KEY)
username = f"{IOT_HUB_HOSTNAME}/{DEVICE_ID}/?api-version=2021-04-12"
telemetry_topic = f"devices/{DEVICE_ID}/messages/events/"

print("\n" + "="*60)
print(f"[*] Conectando Cliente MQTT Puro a Azure IoT Central")
print(f"[*] Broker / Host : {IOT_HUB_HOSTNAME}:8883")
print(f"[*] Client ID     : {DEVICE_ID}")
print(f"[*] SAS Token     : {sas_token[:35]}...")
print(f"[*] Topic Envío   : {telemetry_topic}")
print("="*60 + "\n")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+] Conexión MQTT sobre TLS establecida exitosamente!")
    else:
        print(f"[-] Falló conexión rc={rc}")

def on_publish(client, userdata, mid):
    print(f"    -> [ACK RECIBIDO] Broker confirmó mensaje mid={mid}")

client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=username, password=sas_token)
client.tls_set_context(ssl.create_default_context())

client.on_connect = on_connect
client.on_publish = on_publish

client.connect(IOT_HUB_HOSTNAME, 8883, keepalive=60)
client.loop_start()
time.sleep(2)

temp = 4.2
hum = 52.0
bat = 97.0
qos_probado = 2  # Cambiado a QoS 2

try:
    for i in range(1, 11):
        temp += random.uniform(-0.15, 0.15)
        hum += random.uniform(-0.3, 0.3)
        bat = max(0.0, bat - 0.05)

        data = {
            "temperatura": round(temp, 2),
            "humedad": round(hum, 2),
            "nivel_bateria": round(bat, 1)
        }
        payload = json.dumps(data)
        bytes_size = len(payload.encode('utf-8'))

        t0 = time.time()
        res = client.publish(telemetry_topic, payload, qos=qos_probado)
        res.wait_for_publish()
        lat = round((time.time() - t0) * 1000, 2)

        print(f"[Msg #{i:02d}] {payload} | Tamaño: {bytes_size} B | QoS: {qos_probado} | Latencia: {lat} ms")
        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    print("[*] Desconectado.")
