import serial


while True:
    try:
        arduino = serial.Serial('/COM5', 9600)
        print('Arduino conectado')
        break
    except:
        pass

while True:

    # arduino.write(input().encode())
    msg = str(arduino.readline())
    msg = msg[2:-5]
    print(msg)
    arduino.flush()
