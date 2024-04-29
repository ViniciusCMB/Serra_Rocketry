import serial #Importa a biblioteca

while True: #Loop para a conexão com o Arduino
    try:  #Tenta se conectar, se conseguir, o loop se encerra
        com = serial.Serial('COM5', 9600)
        print('Arduino conectado')
        break
    except:
        pass

while True: #Loop principal
    msg = str(com.readline()) #Lê os dados em formato de string
    msg = msg[2:-5] #Fatia a string
    print(msg) #Imprime a mensagem
    com.flush() #Limpa a comunicação