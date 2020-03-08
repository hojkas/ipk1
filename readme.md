# IPK projekt 1

## Zadání

Cílem projektu bylo vytvořit server na překlad doménových jmen v jednom z vybraných jazyků,
a to za použití pouze základních knihoven. Konkrétně musel server umět obshluhovat dva požadavky, GET a POST.

## Implementace

Zvolila jsem implementaci v jazyku Python.

### Server

Za pomocí knihovny `socket` se vytvoří socket, naváže na port čísla předaného argumentem a začne naslouchat. Samotný server je poté implementován jako nekonečná smyčka, která se ukončí a zavře socket pouze při přerušení z klávesnice. Jakmile dojde v připojení klienta ve smyčce, přijme od něj data, zpracuje, pošle odpověď, zavře spojení a znovu čeká.

### GET

### POST

### Návratové kódy

- 200 OK: Pokud překlad proběhl bez problému. U GET znamená, že skončil dotaz úspěšně. U POST jde o situaci, kdy aspoň jeden z dotazů byl úspěšně přeložen.
- 405 Method Not Allowed: Zasláno v případě, že požadavek není POST ani GET.
- 404 Not Found: Zaslán v případě, že u GET nebyla daná adresa/jméno nalezeno, u POST pokud se nenalezlo ani k jednomu z požadavků.
- 400 Bad Request: Vráceno v případě špatného formátu požadavku.
