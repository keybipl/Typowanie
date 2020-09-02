# -*- coding: utf-8 -*-
import sqlite3
import mysql.connector

bd = mysql.connector.connect(
    host='sql7.freemysqlhosting.net',
    user='sql7363086',
    passwd='GAPFESBwKp',
    database='sql7363086'
)

mycursor = bd.cursor()
# mycursor.execute("CREATE TABLE Mecze (kolejka int, para varchar(50), date varchar(50))")
# bd.commit()

db = sqlite3.connect('terminarz.db')
cursor = db.cursor()

def typy_load():
    # TWORZENIE LISTY TYPOW DANEJ KOLEJKI
    cursor.execute('''SELECT typ FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, typer.lower()))
    typy = cursor.fetchall()
    typ = []  # typy w danej kolejce
    for i in typy:
        typ.append(i[0])
    return typ


def zestawpar():
    # TWORZENIE LISTY MECZÓW KOLEJKI
    kolejka = 1
    cursor.execute('''SELECT para FROM typowanie WHERE kolejka_nr="{}"'''.format(kolejka))
    pary = cursor.fetchall()
    mecze = []  # mecze danej kolejki
    for i in pary:
        mecze.append(i[0])
    for i in range(8):
        print(mecze[i])
        test = 'abc'
        mecz = mecze[i]
        mycursor.execute("INSERT INTO Mecze (kolejka, para) VALUES (%s,%s)", (kolejka, mecz))
        bd.commit()
    print(mecze)
    bd.close()
    return mecze


def zestawpar_show():
    # WYŚWIETLANIE ZESTAWU PAR KOLEJKI
    typ = typy_load()
    print(f'Zestaw par dla kolejki nr {kolejka}')
    ile = []
    for i in range(len(mecze)):
        ile.append(len(mecze[i]) + len(data[i]) + len(wynik[i]))
    for i in range(len(mecze)):
        print('{}. {} {} {} ({}) typ: {}'.format(i + 1, mecze[i], ' ' * (max(ile) - 15 - len(mecze[i])), data[i], wynik[i], typ[i]))






class User:

    kolejka = 0

    def __init__(self, typer):
        self.typer = typer

    def mecze(self):
        # TWORZENIE LISTY MECZÓW KOLEJKI
        cursor.execute(
            '''SELECT para FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(User.kolejka, typer.lower()))
        pary = cursor.fetchall()
        mecze = []  # mecze danej kolejki
        for i in pary:
            mecze.append(i[0])
        return mecze

    def terminy(self):
        cursor.execute(
            '''SELECT data FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(User.kolejka, typer.lower()))
        daty = cursor.fetchall()
        data = []  # daty w danej kolejce
        for i in daty:
            data.append(i[0])
        return data

    def wyniki(self):
        cursor.execute(
            '''SELECT wynik FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(User.kolejka, typer.lower()))
        wyniki = cursor.fetchall()
        wynik = []  # wyniki meczów w kolejce
        for i in wyniki:
            wynik.append(i[0])
        return wynik

    def typy_load(self):
        # TWORZENIE LISTY TYPOW DANEJ KOLEJKI
        cursor.execute(
            '''SELECT typ FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(User.kolejka, typer.lower()))
        typy = cursor.fetchall()
        typ = []  # typy w danej kolejce
        for i in typy:
            typ.append(i[0])
        return typ


def logowanie():

    typer = ''
    req = str('kuba' or 'mateusz' or 'krzysztof')
    while typer.lower() != req:
        typer = str(input('Imię: '))
        if typer.lower() == 'kuba':
            print()
            break
        elif typer.lower() == 'mateusz':
            print()
            break
        elif typer.lower() == 'krzysztof':
            print()
            break
        else:
            print('Przykro mi, ale TYPOWANIE jest tylko dla Mateusza, Kuby i ich taty. Będę rozmawiał tylko z nimi!')
            input('\nWciśnij ENTER')
    return typer


def kolejka():
    while True:
        try:
            while True:
                kolejka = int(input('Wpisz numer kolejki: '))
                if kolejka >= 31 or kolejka <= 0:
                    print('Jest tylko 30 kolejek! Podaj prawidlówą wartość.')
                elif kolejka <= 30:
                    break
            break
        except ValueError:
            print('Podaj proszę prawidłowy numer. To co zostało wpisane nie jest poprawną wartością')
    return kolejka

zestawpar()