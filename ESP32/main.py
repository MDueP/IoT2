from neopixel import NeoPixel
from machine import Pin, UART, ADC
from time import sleep
from dht import DHT11
from gps_simple import MQ135V2

dht11 = DHT11(Pin(26))
mq135 = MQ135V2(14)
mq135.__adc.atten(ADC.ATTN_11DB)
mq135.__adc.width(ADC.WIDTH_11BIT)

np = NeoPixel(Pin(2, Pin.OUT), 12)
uart = UART(2, 9600)

def movePixel(f, l, r, g, b):
    for i in range(f, l):
        np[i] = (r, g, b)
        
def movePixel2(f, l, r, g, b):
    for i in range(f, l, -1):
        np[i] = (r, g, b)

while True:
    sleep(1)
        
    dht11.measure()
    temperature = dht11.temperature()
    humidity = dht11.humidity()
    rzero = mq135.get_rzero()
    corrected_rzero = mq135.get_corrected_rzero(temperature, humidity)
    resistance = mq135.get_resistance()
    ppm = mq135.get_ppm()
    corrected_ppm = mq135.get_corrected_ppm(temperature, humidity)

    print("RZero:                ", rzero)
    print("Corrected RZero:      ", corrected_rzero)
    print("Resistance:           ", resistance)
    print("PPM:                  ", ppm)
    print("Corrected PPM:        ", corrected_ppm)
    print("Temperature:          ", temperature)
    print("Humidity:             ", humidity)
    print()
    
    data = str(temperature) + " " + str(humidity) + " " + str(corrected_ppm) + "\n"
    uart.write(data)
    uartLight = uart.readline()
    if uartLight != b'1' and uartLight != b'0':
        uartLight = b'1'
    print(uartLight)
        
    if uartLight == b'1':
        np[0] = (0, 0, 0)
        np[6] = (0, 0, 0)
    
        if humidity < 25:
            movePixel(1, 2, 255, 40, 0)
            movePixel(2, 5, 0, 0, 0)
        elif 25 < humidity < 40:
            movePixel(1, 3, 30, 40, 0)
            movePixel(3, 5, 0, 0, 0)
        elif 40 < humidity < 50:
            movePixel(1, 4, 40, 40, 0)
            movePixel(4, 5, 0, 0, 0)
        elif 50 < humidity < 65:
            movePixel(1, 5, 50, 30, 0)
            movePixel(5, 6, 0, 0, 0)
        elif humidity > 65:
            movePixel(1, 6, 255, 40, 0)
            
        if corrected_ppm < 400:
            movePixel2(11, 10, 20, 20, 50)
            movePixel(7, 11, 0, 0, 0)
        elif 400 < corrected_ppm < 600:
            movePixel2(11, 9, 20, 20, 50)
            movePixel(7, 10, 0, 0, 0)
        elif 600 < corrected_ppm < 700:
            movePixel2(11, 8, 20, 20, 50)
            movePixel(7, 9, 0, 0, 0)
        elif 700 < corrected_ppm < 900:
            movePixel2(11, 7, 20, 20, 50)
            movePixel(7, 8, 0, 0, 0)
        elif 900 < corrected_ppm:
            movePixel2(11, 6, 255, 40, 0)
        np.write()
    else:
        for i in range(12):
            np[i] = (0,0,0)
        np.write()