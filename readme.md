# IPK projekt 1

Letní 2019/2020

Body: 14/20

## Zadání

Cílem projektu bylo vytvořit server na překlad doménových jmen v jednom z vybraných jazyků,
a to za použití pouze základních knihoven. Konkrétně musel server umět obshluhovat dva požadavky, GET a POST.

## Implementace

Zvolila jsem implementaci v jazyku Python s využitím knihoven `socket`, `sys` a `re`.

### Server

Program vytvoří socket, naváže na port čísla předaného argumentem a začne naslouchat. Samotný server je poté implementován jako nekonečná smyčka, která se ukončí a zavře socket pouze při přerušení z klávesnice. Jakmile dojde v připojení klienta ve smyčce, přijme od něj data, zpracuje, pošle odpověď, zavře spojení a znovu čeká.

### GET

Server zkontroluje správnost formátu přijatých dat, vyextrahuje z nich klíčové informace (jméno/adresu a typ operace) a na jejich základě pomocí funkce `gethostbyname` nebo `gethostbyaddr` získá překlad. V případě, že dostane výsledek, ho odešle klientovi. Kontroluje také (pomocí regulárního výrazu na IPv4 adresu), zda-li není kombinace doménové jméno a typ A nebo naopak ip adresa a typ PTR.

### POST

Server zkontroluje správnost formátu dat. Pro každý řádek za hlavičkou provede stejný postup jako pro metodu GET. Zároveň si pamatuje, zda vůbec nějaký výsledek již našel, aby mohl případně na konci zaslat správný chybový kód. 

### Návratové kódy

- 200 OK: Pokud překlad proběhl bez problému. U GET znamená, že skončil dotaz úspěšně. U POST jde o situaci, kdy aspoň jeden z dotazů byl úspěšně přeložen.
- 405 Method Not Allowed: Zasláno v případě, že požadavek není POST ani GET.
- 404 Not Found: Zaslán v případě, že u GET nebyla daná adresa/jméno nalezeno, u POST pokud se nenalezlo ani k jednomu z požadavků.
- 400 Bad Request: Vráceno v případě špatného formátu požadavku.
