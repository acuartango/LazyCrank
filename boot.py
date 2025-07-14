import network
import time
import webrepl

def connect_wifi():
    ssid = 'SID'
    password = 'SECRET'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a WiFi...")
        wlan.connect(ssid, password)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("WiFi conectado. IP:", wlan.ifconfig()[0])
    else:
        print("No se pudo conectar a WiFi.")
# Conecta a tu red
connect_wifi()
# Inicia WebREPL (requiere configuración previa)
webrepl.start()
