from os import system, name
import sqlite3
from bs4 import BeautifulSoup
from requests import get
import ctypes
import datetime


db = sqlite3.connect('terminarz.db')
cursor = db.cursor()

# miesiące przyporządkowane do liczby
konwersja = {

        'sierpnia': 8,
        'września': 9,
        'października': 10,
        'listopada': 11,
        'grudnia': 12,
        'stycznia': 1,
        'lutego': 2,
        'marca': 3,
        'kwietnia': 4,
        'maja': 5,
        'czerwca': 6,
        'lipca': 7,

    }

# miesiące przyporządkowane do roku
rok = {

    'sierpnia': 2020,
    'września': 2020,
    'października': 2020,
    'listopada': 2020,
    'grudnia': 2020,
    'stycznia': 2021,
    'lutego': 2021,
    'marca': 2021,
    'kwietnia': 2021,
    'maja': 2021,
    'czerwca': 2021,
    'lipca': 2021,

}


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')


def fonts():
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "Lucida Console"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))


def logowanie():
    global typer
    global punkty
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
            clear()

    cursor.execute('''SELECT SUM(punkty) FROM typowanie WHERE typer="{}"'''.format(typer.lower()))
    points = cursor.fetchall()
    punkty = points[0][0]
    db.commit()
    print(f'Cześć {typer.title()}!')

    return typer


def menu():
    wyniki90()
    zliczanie()
    clear()
    print('')
    choice = None
    while choice != 0:
        print('Wybierz {} co chcesz zrobić?'.format(typer.title()))
        print(f'\nKolejka nr {kolejka}')
        print('\n1 - Zobacz zestaw par')
        print('2 - Typuj / zobacz swoje typy')
        print('3 - Zobacz typy wszystkich graczy')
        print('4 - Punktacja')
        print('5 - Zmień kolejkę')
        print('6 - Zmień typera')
        while True:
            try:
                choice = int(input('\nTwój wybór: '))
                break
            except ValueError:
                print('To co zostało wpisane nie jest poprawną wartością')
                input('Wciśnij ENTER')
                clear()
                menu()
        if choice > 6 or choice <= 0:
            print('Nie ma takiego punktu!')
            input('Wciśnij ENTER')
            clear()
        else:
            clear()
            while choice != 0:
                if choice == 1:
                    zestawpar()
                    zestawpar_show()
                    input('Wciśnij ENTER')
                    clear()
                    break
                if choice == 2:
                    typowanieedit()
                    typy_load()
                    typy_show()
                    clear()
                    break
                if choice == 3:
                    typyall()
                    input('Wciśnij ENTER')
                    clear()
                    break
                if choice == 4:
                    # zliczanie()
                    punktacja()
                    punktacjakolejka()
                    input('Wciśnij ENTER')
                    clear()
                    break
                if choice == 5:
                    wczytanie()
                    clear()
                    break
                if choice == 6:
                    logowanie()
                    wczytanie()
                    menu()
                    break


def punktacja():
    typerp = 'kuba'
    cursor.execute('''SELECT SUM(punkty) FROM typowanie WHERE typer="{}"'''.format(typerp.lower()))
    kuba = cursor.fetchall()[0][0]

    typerp = 'mateusz'
    cursor.execute('''SELECT SUM(punkty) FROM typowanie WHERE typer="{}"'''.format(typerp.lower()))
    mati = cursor.fetchall()[0][0]

    typerp = 'krzysztof'
    cursor.execute('''SELECT SUM(punkty) FROM typowanie WHERE typer="{}"'''.format(typerp.lower()))
    tata = cursor.fetchall()[0][0]

    punktacja = {
        'Kuba': kuba,
        'Mati': mati,
        'Tata': tata
    }

    sort_punktacja = sorted(punktacja.items(), key=lambda x: x[1], reverse=True)

    cursor.execute('''SELECT punkty FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, typer.lower()))
    punktk = cursor.fetchall()
    punktyk = list(sum(punktk, ()))
    pointyk = sum(punktyk)
    print('{} - Twoje punkty w tej kolejce: {}'.format(kolejka, pointyk))
    print('')

    print('Tak wygląda klasyfikacja generalna typerów:\n')
    for x, i in enumerate(sort_punktacja):
        print('{}. {} - {}'.format(x + 1, i[0], i[1]))


def punktacjakolejka():
    scorer = ['kuba', 'mateusz', 'krzysztof']
    print()
    input('Wciśnij ENTER i zobacz jak gracze typowali w poszczególnych kolejkach:')

    for i in range(30):
        print('')
        punkts = []
        for a in scorer:
            cursor.execute('''SELECT punkty FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(i+1, a.lower()))
            punkt = cursor.fetchall()
            punkty = list(sum(punkt, ()))
            pointy = sum(punkty)
            pointy = int(pointy)
            punkts.append(pointy)

        punktacja = {

            'Kuba': punkts[0],
            'Mati': punkts[1],
            'Tata': punkts[2],

        }

        sort_punktacja = sorted(punktacja.items(), key=lambda x: x[1], reverse=True)

        print('')
        print('Punktacja w kolejce nr {}:\n'.format(i+1))
        for x, i in enumerate(sort_punktacja):
            print('{}. {} - {}'.format(x + 1, i[0].title(), i[1]))

    input('')


def terminy():
    cursor.execute('''SELECT data FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, typer.lower()))
    daty = cursor.fetchall()
    data = []  # daty w danej kolejce
    for i in daty:
        data.append(i[0])
    return data


def typowanie():
    # TYPOWANIE WSZYSTKICH MECZÓW
    for i in range(len(mecze)):
        typ = input('Podaj typ meczu {}: '.format(mecze[i]))
        cursor.execute(
            '''UPDATE typowanie SET typ="{}" WHERE para="{}" AND typer="{}"'''.format(typ, mecze[i], typer.lower()))
        db.commit()


def typowanieedit():
    typy_show()
    while True:
        try:
            numer = input('Wpisz numer meczu, dla którego chesz podać/zmienić typ (0 - wyjście do menu): ')
            i = int(numer)
            if i > 8 or i < 0:
                print('Nie ma takiego meczu!')
                input('Wciśnij ENTER')
                clear()
                typowanieedit()
            else:
                break
        except ValueError:
            print('To co zostało wpisane nie jest poprawną wartością.')
            input('Wciśnij ENTER')
            clear()
            typowanieedit()

    if i == 0:
        menu()
    else:
        cursor.execute('''SELECT data FROM typowanie WHERE kolejka_nr="{}"'''.format(kolejka))
        termin = cursor.fetchall()
        daty = list(sum(termin, ()))
        kon = daty[i-1].split(' ')
        if len(kon) != 3:
            typek = input('Podaj typ meczu {}: '.format(mecze[i - 1]))
            cursor.execute(
                '''UPDATE typowanie SET typ="{}" WHERE para="{}" AND typer="{}"'''.format(typek, mecze[i - 1], typer.lower()))
            db.commit()
            clear()
            typowanieedit()
        else:
            month = konwersja[kon[1]]
            year = int(rok[kon[1]])
            day = int(kon[0])
            hour = kon[2].split(':')
            hourh = int(hour[0])
            minutes = int(hour[1])
            date1 = datetime.datetime(year, month, day, hourh, minutes)
            date2 = datetime.datetime.now()

            if date1 > date2 or date1 == 'test':
                typek = input('Podaj typ meczu {}: '.format(mecze[i - 1]))
                cursor.execute(
                    '''UPDATE typowanie SET typ="{}" WHERE para="{}" AND typer="{}"'''.format(typek, mecze[i - 1], typer.lower()))
                db.commit()
                clear()
                typowanieedit()
            else:
                print('Niestety mecz juz trwa lub się zakończył, nie możesz typować :(')
                input('Wciśnij ENTER')


def typyall():
    typyall = ['kuba', 'mateusz', 'krzysztof']

    for a in typyall:

        cursor.execute('''SELECT typ FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, a))
        typy = cursor.fetchall()
        typ = []  # daty w danej kolejce
        for i in typy:
            typ.append(i[0])

        print('Typy typera {} dla kolejki nr {}'.format(a.title(), kolejka))
        ile = []
        for i in range(len(mecze)):
            ile.append(len(mecze[i]) + len(typ[i]))
        for i in range(len(mecze)):
            print('{}. {} {} {}'.format(i + 1, mecze[i], ' ' * (max(ile) - len(mecze[i])), typ[i]))
        print('')


def typy_load():
    # TWORZENIE LISTY TYPOW DANEJ KOLEJKI
    cursor.execute('''SELECT typ FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, typer.lower()))
    typy = cursor.fetchall()
    typ = []  # typy w danej kolejce
    for i in typy:
        typ.append(i[0])
    return typ


def typy_show():
    # WYSWIETLANIE TYPÓW DANEJ KOLEJKI
    typ = typy_load()
    print('{} - Twoje typy dla kolejki nr {}'.format(typer.title(), kolejka))
    ile = []
    for i in range(len(mecze)):
        ile.append(len(mecze[i]) + len(data[i]) + len(typ[i]))
    for i in range(len(mecze)):
        print('{}. {} {} {}'.format(i + 1, mecze[i], ' ' * (max(ile) - 15 - len(mecze[i])), typ[i]))


def wyniki():
    cursor.execute(
        '''SELECT wynik FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, typer.lower()))
    wyniki = cursor.fetchall()
    wynik = []  # wyniki meczów w kolejce
    for i in wyniki:
        wynik.append(i[0])
    return wynik


def wyniki90():
    # POZYSKANIE WYNIKÓW i DAT ZE STRONY
    URL = 'http://www.90minut.pl/liga/1/liga11233.html'
    # URL = 'http://www.90minut.pl/liga/1/liga10549.html'
    page = get(URL)
    bs = BeautifulSoup(page.content, 'html.parser')
    wyniki = []  # multiple wyniki
    for wynik in bs.find_all('td', width='50'):
        w = wynik.get_text().strip()
        wyniki.append(w)

    a = 0
    b = 8
    results = []  # rezultaty dla poszczególnych kolejek
    for i in range(30):
        results.append(wyniki[a:b])
        a += 8
        b += 8


    term = []  # multiple terms
    for daty in bs.find_all('td', width="190"):
        f = daty.get_text().strip()
        term.append(f)

    a = 0
    b = 8
    termin = []
    for i in range(30):
        termin.append(term[a:b])
        a += 8
        b += 8

    for i in range(30):
        result = results[i]
        data = termin[i]
        cursor.execute('''SELECT para FROM typowanie WHERE kolejka_nr="{}"'''.format(i+1))
        pary = cursor.fetchall()
        mecze = []  # mecze danej kolejki
        for i in pary:
            mecze.append(i[0])
        for a in range(8):
            cursor.execute(
                '''UPDATE typowanie SET wynik="{}" WHERE para="{}"'''.format(result[a], mecze[a]))
            dane = str(data[a])
            dane = dane.replace(',', '')
            try:
                if dane[-1] == '0':
                    cursor.execute('''UPDATE typowanie SET data="{}" WHERE para="{}"'''.format(dane, mecze[a]))
                    db.commit()
            except IndexError as error:
                continue


def wczytanie():
    global kolejka
    global mecze
    global data
    global wynik
    global typ

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

    mecze = zestawpar()
    data = terminy()
    wynik = wyniki()
    typ = typy_load()
    return kolejka, mecze, data, wynik, typ


def zestawpar():
    # TWORZENIE LISTY MECZÓW KOLEJKI
    cursor.execute('''SELECT para FROM typowanie WHERE kolejka_nr="{}" AND typer="{}"'''.format(kolejka, typer.lower()))
    pary = cursor.fetchall()
    mecze = []  # mecze danej kolejki
    for i in pary:
        mecze.append(i[0])
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


def zliczanie():
    # ZLICZANIE PUNKTÓW
    typery = ["kuba", "mateusz", "krzysztof"]
    for a in typery:
        cursor.execute('''SELECT typ FROM typowanie WHERE typer="{}"'''.format(a))
        test = cursor.fetchall()
        cursor.execute('''SELECT wynik  FROM typowanie WHERE typer="{}"'''.format(a))
        test2 = cursor.fetchall()
        for i in range(240):
            typz = str(test[i][0])
            wynikz = str(test2[i][0])
            points = 0
            if len(typz) >= 3 and len(wynikz) >= 3:
                if typz[0] == wynikz[0] and typz[2] == wynikz[2]:
                    points += 2
                if typz[0] > typz[2] and wynikz[0] > wynikz[2] or \
                        typz[0] == typz[2] and wynikz[0] == wynikz[2] or \
                        typz[0] < typz[2] and wynikz[0] < wynikz[2]:
                    points += 1
                    cursor.execute(
                        '''UPDATE typowanie SET punkty="{}" WHERE typ="{}" AND wynik="{}" AND typer="{}"'''.format(
                            points, test[i][0], test2[i][0], a))
                    db.commit()

                else:
                    points = 0
                    cursor.execute(
                        '''UPDATE typowanie SET punkty="{}" WHERE typ="{}" AND wynik="{}" AND typer="{}"'''.format(
                            points, test[i][0], test2[i][0], a))
                    db.commit()
            else:
                points = 0
                cursor.execute(
                    '''UPDATE typowanie SET punkty="{}" WHERE typ="{}" AND wynik="{}" AND typer="{}"'''.format(points,
                                                                                                               test[i][
                                                                                                                   0],
                                                                                                               test2[i][
                                                                                                                   0],
                                                                                                               a))
                db.commit()


fonts()
wyniki90()
zliczanie()

logowanie()
wczytanie()
menu()

db.close()