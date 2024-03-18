import serial
from time import sleep
from socket import *

serverName = ""
serverPort = ""
clientSocket = socket(AF_INET, SOCK_DGRAM)

ser = serial.Serial("/dev/ttyS0", 9600)
LED_status = b'0'

print("Online.")
while True:
    sleep(0.5)
    data_send = ser.readline()
    print("ESP data = ", data_send)
    message_send = data_send
    clientSocket.sendto(message_send.encode(), (serverName, serverPort))
    
    data_receive, client = serverSocket.recvfrom(2048)
    print("LED status = ", data_receive)
    ser.write(data_receive)
    