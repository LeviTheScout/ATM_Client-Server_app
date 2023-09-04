from socket import *

s=socket(AF_INET,SOCK_STREAM) # making socket with TCP connection 
s.bind(('',11846))            # connecting client and server via particular port 
s.listen(1)                   # allowed number of client 

#getting pin of the client from external file
with open(r'\client server\pin.txt', 'r') as f: #be sure to change this location of the file.
    lines = f.read().splitlines()
    last_line = lines[-1]
    pin=int(last_line)

#getiing balance of the user from external file
with open(r'\client server\bal.txt', 'r') as f:
    lines = f.read().splitlines()
    last_line = lines[-1]
    bal=int(last_line)

print('server is  ready')

while True:
    conne,addr=s.accept()
    conne.send('hey client! Please enter your Pin!'.encode())
    
    p=int(conne.recv(1024).decode()) #pin recieved from client machine
    
    #verification of pin
    while int(p)!=pin:
        conne.send('False'.encode())
        p=conne.recv(1024).decode()
    if int(p)==pin:
        conne.send('True'.encode())  
    
    #operation to be performed
    m=int(conne.recv(1024).decode())
    
    while m!=5: #this loop will make sure that connection will be open till client demands to close it.
        if m==1:   #changing pin
            pin=int(conne.recv(1024).decode()) #recieved new pin from client machine
            conne.send(str(pin).encode()) 
        with open(r'\client server\pin.txt','w') as f: #updating pin in external file
            f.write(str(pin)+'\n')
            f.close()
        
        if m==2: #check balance operation 
            conne.send(str(bal).encode())
        
        if m==3: #Money withdrawal operation
            money=int(conne.recv(1024).decode())  #client request of particular amount to be deducted 
            
            if money>bal:    #if requested money is more than current balance
                conne.send('0'.encode())
            else:            # if requested money is less than current balance---will be able to debit money
                conne.send('1'.encode())
                bal=abs(money-bal)
        
        
        if m==4: #adding money to account
            ad=int(conne.recv(1024).decode())
            bal+=ad
            conne.send('Money successfully credited into your account!'.encode())
        with open(r'\client server\bal.txt','w') as f: #updating balance to the external file
            f.write(str(bal)+'\n')
            f.close()
        m=int(conne.recv(1024).decode())
    
    conne.close() #connection will be closed when m==5