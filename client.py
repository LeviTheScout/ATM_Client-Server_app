from socket import *
cli=socket(AF_INET,SOCK_STREAM) #crating socket
cli.connect(('localhost',11846)) #connecting with server

print(cli.recv(1024).decode()) #message for entering pin

cli.send(input().encode())   #accepted pin from user and passed it to server
a=cli.recv(1024).decode()     #response of server to enterd pin

while a=='False':   #if pin is wrong
    print('Wrong Pin! Try again.')
    cli.send(input().encode())
    a=cli.recv(1024).decode()
if a=='True': #if pin is correct
    print('Welcome!')
    menu={1:'Change Pin',2:'Check Balance',3:'Withdraw Money',4:'Add Money to your Account',5:'Exit'} #Menu
    print('----------------------------------')
    for i in menu:
        print(i,':',menu[i])
    print('----------------------------------')
    a=int(input('Enter number corresponding to operation you want to perform: '))
    while a!=5:
        if a in [1,2,3,4]:
            cli.send(str(a).encode())  #sending request to client about particular operation to be performed
            
            if a==1: #changing pin
                print('Enter New pin:')
                cli.send(input().encode())  #new pin sent to server
                print('New Pin is',cli.recv(1024).decode())  #pin changed and verfication response
                print('----------------------------------')
            
            if a==2: #checking balance
                print('----------------------------------')
                print('Your current Balance is : ',cli.recv(1024).decode()) #recieced balance of user from server
                print('----------------------------------')
            
            if a==3: #Withdraw money
                print('----------------------------------')
                cli.send(input('Enter Amount :').encode())   #sent 'amount to be deducted' to server
                print('----------------------------------')
                if cli.recv(1024).decode()=='0': #server will verify if user has sufficient balance to perform this operation
                    print('Insufficient balance!')
                    print('----------------------------------')
                else:
                    print('Please Collect your money!')
                    print('----------------------------------')
            
            if a==4: #adding money to the account 
                cli.send(input('Enter Amount to be credited :').encode())
                print('Place money notes in proper order inside ATM Machine!')
                print(cli.recv(1024).decode())
                print('----------------------------------')
        else:
            print('wrong choice')
        for i in menu:
            print(i,':',menu[i])
        print('----------------------------------')
        a=int(input())
    
    if a==5: #connection closing request
        cli.send(str(a).encode())