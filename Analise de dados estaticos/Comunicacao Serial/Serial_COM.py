import serial

# def get_data(amonunt):
while True: #Loop para a conexão com o Arduino
    try:  #Tenta se conectar, se conseguir, o loop se encerra
        arduino = serial.Serial('/dev/ttyUSB0', 9600)
        print('Arduino conectado')
        break
    except:
        pass

while True: #Loop principal
    msg = str(arduino.readline()) #Lê os dados em formato de string
    msg = msg[2:-5] #Fatia a string
    print(msg) #Imprime a mensagem
    arq = open("dados.txt",'a') 
    arq.write(msg+'\n')
    arq.close()
    arduino.flush() #Limpa a comunicação

    # return None