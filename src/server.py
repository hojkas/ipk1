import sys
import socket
import re

def break_by_space(data):
    data = data.split()
    return data

def extract_request(data):
    data = re.sub(r"^/resolve\?name=", '', data)
    data = re.split(r"&type=", data)
    return data[0], data[1]

# vytvoreni socketu
try:
    s = socket.socket()
    print("Socket successfully created.")
except:
    print("Socket creation ended with error.")
    exit()

# nahrani port cisla z argumentu
port = int(sys.argv[1])

# bind socketu s portem
try:
    s.bind(('', port))
    print('Socket bound to', port)
except:
    print('Socket binding failed.')
    exit()

# zacatek naslouchani socketu
s.listen()
print('Socket listening.')

try:
    # nekonecna smycka, dokud nenastane chyba nebo se neukonc
    while True:
        # cekani na spojeni a navazani
        print('Waiting for connection...')
        (connection, address) = s.accept()
        print('Connected to:', address)

        # cekani na data od klienta
        data = connection.recv(1024)
        data = data.decode()
        print('Got data: ', data)

        # funkce zpracovani dat a vytvoreni pozadovane odpovedi
        test = break_by_space(data)
        answer = ""
        if test[0] == 'GET':
            #zpracovani GET pozadavku
            data = test
            if data[2] == 'HTTP/1.1':
                if re.match(r"^/resolve\?name=\S*&type=(A|PTR)$", data[1]) is not None:
                    #format v poradku, muze zacit preklad
                    name, type = extract_request(data[1])
                    #v name je jmeno/ip adresa pro preklad, v type A nebo PTR
                    if type == 'A':
                        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", name):
                            answer = 'HTTP/1.1 400 Bad Request'
                        else:
                            #bude prekladat adresu na ip
                            try:
                                res = socket.gethostbyname(name)
                                answer = 'HTTP/1.1 200 OK \r\n\r\n'
                                answer += name
                                answer += ':A='
                                answer += res
                            except:
                                answer = 'HTTP/1.1 404 Not found'

                    elif type == 'PTR':
                        #preklad na adresu z ip
                        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", name):
                            try:
                                res = socket.gethostbyaddr(name)
                                answer = 'HTTP/1.1 200 OK \r\n\r\n'
                                answer += name
                                answer += ':PTR='
                                answer += res[0]
                            except:
                                answer = 'HTTP/1.1 404 Not found'
                        else:
                            answer = 'HTTP/1.1 400 Bad Request'
                    else:
                        #shouldn't happen
                        print('Something went wrong with extracting request type.')
                else:
                    answer = 'HTTP/1.1 400 Bad Request'
            else:
                answer = 'HTTP/1.1 400 Bad Request'


            #konec zpracovani GET pozadavku
        elif test[0] == 'POST':
            #zpracovani POST pozadavku
            if re.match(r"^POST /dns-query HTTP/1.1", data) is not None:
                #ok post pozadavek

                #oseknuti hlavicky
                data_parts = re.split(r"(\n\n|\r\n\r\n)", data)
                if len(data_parts) <= 3:
                    lines = data_parts[2]
                    lines = lines.splitlines()
                    found = False #na kontrolu, zda nahodou vse nebylo spatne, tudiz treba vypsat not found
                    empty_line = False

                    #cyklus na kontroly vsech dotazu a provedeni
                    for line in lines:
                        if empty_line:
                            answer = 'HTTP/1.1 400 Bad Request'
                            break
                        line = line.strip()
                        line = line.replace(' ', '')
                        if not line :
                            empty_line = True
                        else :
                            line = line.split(':')
                            name = line[0]
                            type = line[1]

                            #vlastni preklad
                            if type == 'A':
                                if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", name):
                                    pass
                                else:
                                    # bude prekladat adresu na ip
                                    try:
                                        res = socket.gethostbyname(name)
                                        if not found:
                                            answer = 'HTTP/1.1 200 OK\r\n\r\n'
                                            found = True
                                        else:
                                            answer += '\r\n'
                                        answer += name
                                        answer += ':A='
                                        answer += res
                                    except:
                                        pass

                            elif type == 'PTR':
                                # preklad na adresu z ip
                                if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", name):
                                    try:
                                        res = socket.gethostbyaddr(name)
                                        if not found:
                                            answer = 'HTTP/1.1 200 OK \r\n\r\n'
                                            found = True
                                        else:
                                            answer += '\r\n'
                                        answer += name
                                        answer += ':PTR='
                                        answer += res[0]
                                    except:
                                        pass
                                else:
                                    pass
                            else:
                                pass

                    if not found:
                        answer = '404 Not Found'

                else:
                    answer = '400 Bad Request'
            else:
                answer = '400 Bad Request'
            #konec POST pozadavku
        else:
            print('Got invalid request.')
            answer = 'HTTP/1.1 405 Method Not Allowed'

        # posle odpoved
        answer += '\r\n'
        connection.send(str.encode(answer))

        # Ukonci pripojeni
        connection.close()
        print('Connection successfully ended.')
except KeyboardInterrupt:
    # pri stisku klavesy se ukonci a uzavre socket
    s.close()
    sys.exit()
