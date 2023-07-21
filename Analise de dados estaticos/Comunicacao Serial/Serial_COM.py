import serial
from datetime import datetime

while True: #Loop para a conexão com o Arduino
    try:  #Tenta se conectar, se conseguir, o loop se encerra
        arduino = serial.Serial('/dev/ttyUSB0', 9600)
        print('Arduino conectado')
        break
    except:
        pass

while True: #Loop principal
    msg = str(arduino.readline()) #Lê os dados em formato de string
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = msg[2:-5] #Fatia a string
    print(msg) #Imprime a mensagem
    arq = open("dados.txt",'a') 
    arq.write(current_time+';')
    arq.write(msg+'\n')
    arq.close()
    arduino.flush() #Limpa a comunicação