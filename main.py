from machine import Pin, PWM
from time import sleep
import uasyncio as asyncio
import socket

# Pines conectados al L298N
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
ENA = PWM(Pin(4), freq=1000)
ENA.duty(0)  # velocidad 0

# Pines botones ESP32
btn_forward = Pin(5, Pin.IN, Pin.PULL_UP)
btn_backward = Pin(6, Pin.IN, Pin.PULL_UP)
btn_stop = Pin(7, Pin.IN, Pin.PULL_UP)

# Pines fines de carrera ESP32
limit_1 = Pin(8, Pin.IN, Pin.PULL_UP)
limit_2 = Pin(9, Pin.IN, Pin.PULL_UP)

# Estado
state = "STOP"
velocidad = 1023  # Velocidad por defecto
velocidad = 512  # Velocidad por defecto

async def motor_soft_start(direction_func, target_speed=velocidad, duration=2):
    steps = 10
    delay = duration / steps
    for i in range(1, steps+1):
        speed = int(target_speed * i / steps)
        direction_func(speed)
        await asyncio.sleep(delay)

def motor_forward(speed=velocidad):
    if limit_1.value() == 0:
        print("⚠️ Fin de carrera 1 activado")
        motor_stop()
        return
    IN1.on()
    IN2.off()
    ENA.duty(speed)

def motor_backward(speed=velocidad):
    if limit_2.value() == 0:
        print("⚠️ Fin de carrera 2 activado")
        motor_stop()
        return
    IN1.off()
    IN2.on()
    ENA.duty(speed)

def motor_stop():
    ENA.duty(0)
    IN1.off()
    IN2.off()

# Función para manejar los botones conectados al ESP32 y a GND (Están en PullUp a 3v3)
async def check_buttons():
    global state
    while True:
        if btn_forward.value() == 0:
            state = "UP"
            print("Pulsador: SUBIR")
            await motor_soft_start(motor_forward)
        elif btn_backward.value() == 0:
            state = "DOWN"
            print("Pulsador: BAJAR")
            await motor_soft_start(motor_backward)
        elif btn_stop.value() == 0:
            state = "STOP"
            print("Pulsador: PARAR")
            motor_stop()
        await asyncio.sleep(0.1)

# Webserver API
async def web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print('Servidor Web escuchando en puerto 80')

    while True:
        cl, addr = s.accept()
        request = cl.recv(1024).decode()
        response = ""

        if "GET /up" in request:
            print("Web: SUBIR")
            await motor_soft_start(motor_forward)
            response = "HTTP/1.1 200 OK\r\n\r\nSubiendo"
        elif "GET /down" in request:
            print("Web: BAJAR")
            await motor_soft_start(motor_backward)
            response = "HTTP/1.1 200 OK\r\n\r\nBajando"
        elif "GET /stop" in request:
            print("Web: PARAR")
            motor_stop()
            response = "HTTP/1.1 200 OK\r\n\r\nParado"
        elif "GET / " in request or "GET /index.html" in request:
            with open("index.html") as f:
                html = f.read()
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        cl.send(response)
        cl.close()

async def main():
    await asyncio.gather(
        check_buttons(),
        web_server()
    )

asyncio.run(main())
