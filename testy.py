import sqlite3

db = sqlite3.connect('terminarz.db')
cursor = db.cursor()


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


typer = logowanie()
User.kolejka = kolejka()
gracz = User(typer=typer)
mecze = gracz.mecze()
data = gracz.terminy()
wynik = gracz.wyniki()
typ = gracz.typy_load()



data = tworzenie()
mecze = tworzenie()
print(data)
print(mecze)






