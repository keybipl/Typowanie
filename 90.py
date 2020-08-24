from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

URL = 'http://www.90minut.pl/liga/1/liga11233.html'

db = sqlite3.connect('terminarz.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE terminarz (kolejka_nr TEXT, data TEXT)''')
    quit()

page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')

no = []
for offer in bs.find_all('u'):
    kolejka = offer.get_text().split(' ')
    kolejka[2] = ':'
    kolejka = str(kolejka)
    kolejka = kolejka.replace('[','')
    kolejka = kolejka.replace('\'','')
    kolejka = kolejka.replace(']','')
    kolejka = kolejka.replace(',','')
    kolejka = kolejka.split(' :')
    kolejka[0] = str(kolejka[0]).replace('Kolejka ','')
    kolejka_nr = kolejka[0]
    data = kolejka[1]
    data = data.strip()
    no.append(kolejka_nr)

    cursor.execute('INSERT INTO terminarz VALUES (?, ?)', (kolejka_nr, data))
    db.commit()

db.close()

print(no)


lista = []
for clubs in bs.find_all('td', width="180"):
    t = clubs.get_text().strip()
    lista.append(t)

print(lista)

print(len(lista))

a = 0
b = 16
c = 0
zestaw_par  = []
for i in range(len(no)):
    zestaw_par.append(lista[a:b])
    print(lista[a:b])
    a = a + 16
    b = b + 16

print(zestaw_par)

nr = int(input('nr: '))

print(zestaw_par[nr-1])

dana = zestaw_par[nr-1]

print('Zestaw par kolejki nr {}:'.format(nr))
a = 0
for i in range(8):
    print('{} - {}'.format(dana[a], dana[a+1]))
    a = a + 2





