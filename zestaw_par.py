from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

URL = 'http://www.90minut.pl/liga/1/liga11233.html'

db = sqlite3.connect('terminarz.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE pary (kolejka_nr INTEGER, para TEXT, data TEXT)''')
    quit()


page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')

URL = 'http://www.90minut.pl/liga/1/liga11233.html'

page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')

no = []  # numery kolejki w liście
termin = []  # daty w liście

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
    termin.append(data)

    cursor.execute('INSERT INTO pary VALUES (?, ?, ?)', (kolejka_nr, 'test', 'test2'))
    db.commit()

db.close()

lista = []  # multiple teams
for clubs in bs.find_all('td', width="180"):
    t = clubs.get_text().strip()
    lista.append(t)

a = 0
b = 16
zestaw_par = []
for i in range(len(no)):
    zestaw_par.append(lista[a:b])
    a += 16
    b += 16

term = []  # multiple terms
for daty in bs.find_all('td', width="190"):
    f = daty.get_text().strip()
    term.append(f)

a = 0
b = 8
terminy = []  # terminy dla poszczególnych kolejek w listach
for i in range(len(no)):
    terminy.append(term[a:b])
    a += 8
    b += 8

nr = int(input('nr: '))
dana = zestaw_par[nr-1]
mecz = terminy[nr-1]
print('')

print('***** Zestaw par kolejki nr {} z {} sezonu 2020/2021 *****'.format(nr, termin[nr-1]))

ile = []
a = 0
z = 0
for _ in range(8):
    ile.append(len(dana[a]) + len(dana[a+1]) + len(terminy[z]))
    a += 2
    z += 1
a = 0
z = 0
for i in range(8):
    tem = len(dana[a] + dana[a+1])
    print('{}. {} - {} {} {}'.format(i+1, dana[a], dana[a+1], ' ' * (max(ile) - tem - 6), mecz[z]))
    a = a + 2
    z += 1

input('')

nr = 0

for i in range(30):
    dana = zestaw_par[nr]
    mecz = terminy[nr]
    print('\n***** Zestaw par kolejki nr {} z {} sezonu 2020/2021 *****'.format(nr+1, termin[nr]))
    nr += 1
    ile = []
    a = 0
    z = 0
    for _ in range(8):
        ile.append(len(dana[a]) + len(dana[a + 1]) + len(terminy[z]))
        a += 2
        z += 1
    a = 0
    z = 0
    for i in range(8):
        tem = len(dana[a] + dana[a + 1])
        print('{}. {} - {} {} {}'.format(i+1, dana[a], dana[a+1], ' ' * (max(ile) - tem - 6), mecz[z]))
        a = a + 2
        z += 1