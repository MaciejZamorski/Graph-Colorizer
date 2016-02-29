import random


class Graf:
    def __init__(self):
        self.wierzcholki = []
        self.krawedzie = []

    def __str__(self):
        return 'Wierzcholkow: {}, Krawedzi: {}.'.format(
            self.ilosc_wierzcholkow(), self.ilosc_krawedzi())

    def ilosc_krawedzi(self):
        return len(self.krawedzie)

    def ilosc_wierzcholkow(self):
        return len(self.wierzcholki)


def ewaluacja(chromosom):
    """Funkcją przystosowania jest ilość użytych kolorów. Im mniejsza tym
    lepiej.
    """
    pokolorowanie = dekoduj(chromosom)
    return len(set([k for _, k in pokolorowanie]))


def koloruj(graf):
    populacja = zapoczatkuj_populacje(graf)
    print('Zapoczątkowano populację...')
    t = 0
    wyniki = [(najlepszy(populacja))]
    while not stop(t, populacja):
        print('Ropoczynam iterację {}.'.format(t+1))
        populacja = selekcja(populacja)
        populacja = krzyzuj(populacja)
        populacja = mutuj(populacja)
        wyniki.append(najlepszy(populacja))
        t += 1

    return najlepszy(populacja)


def zapoczatkuj_populacje(graf):
    # v = graf.wierzcholki
    # random.seed()
    # populacja = []
    # while len(populacja) < liczebnosc:
    #     kolory = [i for i in range(len(v))]
    #     pokolorowanie = []
    #     for i in range(len(v)):
    #         w = i + 1
    #         wyb_kolor = random.choice(kolory)
    #         kolory.remove(wyb_kolor)
    #         pokolorowanie.append((w, wyb_kolor))
    #     if poprawne(graf, pokolorowanie):
    #         chromosom = zakoduj(pokolorowanie)
    #         populacja.append(chromosom)
    # return populacja
    v = graf.wierzcholki
    random.seed()
    populacja = []
    while len(populacja) < liczebnosc:
        kolory = [i for i in range(len(v))]
        pokolorowanie = []
        for i in range(len(v)):
            w = i + 1
            wyb_kolor = random.choice(kolory)
            pokolorowanie.append((w, wyb_kolor))
        if poprawne(graf, pokolorowanie):
            chromosom = zakoduj(pokolorowanie)
            populacja.append(chromosom)
    return populacja


def zakoduj(pokolorowanie, dlugosc_chr=None):
    if dlugosc_chr is None:
        dlugosc_chr = dlugosc_chromosomu

    chromosom = 0
    for w, k in pokolorowanie:
        chromosom |= k << (w * dlugosc_chr)
        binary = bin(chromosom)
        pass
    return chromosom


def dekoduj(chromosom, dlugosc_chr=None, ilosc_w=None):
    if dlugosc_chr is None:
        dlugosc_chr = dlugosc_chromosomu
    if ilosc_w is None:
        ilosc_w = ilosc_wierzcholkow

    pokolorowanie = []
    maska = 0
    for i in range(dlugosc_chr):
        maska |= 1 << i

    for i in range(ilosc_w):
        w = i + 1
        obecna_maska_bin = bin(maska << (w * dlugosc_chr))
        obecna_maska = maska << (w * dlugosc_chr)
        kolor = (chromosom & obecna_maska) >> (w * dlugosc_chr)
        pokolorowanie.append((w, kolor))

    return pokolorowanie


def poprawne(graf, pokolorowanie):
    """Sprawdzamy poprawność pokolorowania grafu. Wystarczy, że dla każdej
    pary, kolor przypiszany obu wierzchołkom nie będzie tym samym kolorem.
    :param graf: graf zawierający krawędzie, które będziemy sprawdzać
    :param pokolorowanie: lista krotek (nr wierzchołka, nr koloru)
    :return True, jeśli wszystkie krawędzie mają różne kolory, False w.p.p.
    """
    e = graf.krawedzie
    lk = pokolorowanie
    return all(kolor(w1, lk) != kolor(w2, lk) for w1, w2 in e)


def kolor(wierzcholek, pokolorowanie):
    for w, k in pokolorowanie:
        if w == wierzcholek:
            return k


def stop(t, populacja):
    return t == T or istnieje_rozwiazanie(populacja)


def istnieje_rozwiazanie(populacja):
    return any([poprawne(g, dekoduj(osobnik)) for osobnik in populacja])


def przystosowania(populacja):
    return [(chromosom, ewaluacja(chromosom)) for chromosom in populacja]


def selekcja(populacja):
    """ Wybieramy populacja/2 po selekcji"""
    przystosowania_populacji = przystosowania(populacja)

    suma_przystosowan = 0
    do_selekcji = []
    for chromosom, przystosowanie in przystosowania_populacji:
        suma_przystosowan += przystosowanie
        do_selekcji.append((chromosom, suma_przystosowan))

    po_selekcji = []
    for i in range(liczebnosc):
        wyselekcjonowany_chromosom = ruletka(do_selekcji, suma_przystosowan)
        po_selekcji.append(wyselekcjonowany_chromosom)

    return po_selekcji


def ruletka(do_selekcji, suma):
    los = random.randint(0, int(suma))
    for chromosom, suma_przystosowan in do_selekcji:
        if suma_przystosowan >= los:
            return chromosom


def krzyzuj(populacja):
    pary_chromosomow = []
    for i in range(liczebnosc // 2):
        chromosom1 = random.choice(populacja)
        chromosom2 = random.choice(populacja)
        pary_chromosomow.append((chromosom1, chromosom2))

    po_krzyzowaniu = []
    for c1, c2 in pary_chromosomow:
        po_krzyzowaniu.extend(krzyzuj_chromosomy(c1, c2))

    return po_krzyzowaniu


def krzyzuj_chromosomy(c1, c2):
    if random.uniform(0.0, 1.0) < prawd_krzyzowania:
        miejsce_krzyzowania = random.randint(0, dlugosc_chromosomu)
        maska = 0
        for i in range(miejsce_krzyzowania):
            maska |= 1 << i
        nowy_c1 = (c1 & maska) | (c2 & ~maska)
        nowy_c2 = (c1 & ~maska) | (c2 & maska)
        return nowy_c1, nowy_c2
    else:
        return c1, c2


def mutuj(populacja):
    po_mutacji = []
    for chromosom in populacja:
        po_mutacji.append(mutuj_chromosom(chromosom))

    return po_mutacji


def mutuj_chromosom(chromosom):
    for nr_bitu in range(dlugosc_chromosomu):
        if random.uniform(0.0, 1.0) < prawd_mutacji:
            chromosom = zmien_bit(chromosom, nr_bitu)
    return chromosom


def zmien_bit(chromosom, index):
    if chromosom & (1 << index):
        return chromosom & ~(1 << index)
    else:
        return chromosom | (1 << index)


def najlepszy(populacja):
    pokolorowania = [dekoduj(chromosom) for chromosom in populacja]
    akceptowalne = [zakoduj(pokolorowanie) for pokolorowanie in pokolorowania
                    if poprawne(g, pokolorowanie)]
    try:
        naj_chr, naj_przyst = akceptowalne[0], ewaluacja(akceptowalne[0])
    except IndexError:
        print('Nie znaleziono odpowiedniego pokolorowania.')
        naj_chr, naj_przyst = None, None
    return naj_chr, naj_przyst


def wczytaj_graf(sciezka):
    g = Graf()
    with open(sciezka, mode='r') as f:
        for line in f.readlines():
            if line.split()[0] == 'e':
                _, w1, w2, _ = line.split()
                if w1 != w2:
                    g.krawedzie.append((int(w1), int(w2)))
            elif line.split()[0] == 'n':
                _, w, _ = line.split()
                g.wierzcholki.append(int(w))

    return g


def bitow_na_wierzcholek(n):
    """Oblicza ilość bitów potrzebną do zakodowania informacji o wierzchołku
    w zależności od liczby wierzchołków w grafie.
    :param n: Liczba wierzchołków.
    :return minimalna liczba bitów potrzebna do zakodowania n
    """
    i = 1
    while 2 ** i <= n:
        i += 1
    return i

if __name__ == '__main__':
    g = wczytaj_graf('files/GEOM20a.col')
    ilosc_wierzcholkow = len(g.wierzcholki)
    ilosc_krawedzi = len(g.krawedzie)
    dlugosc_chromosomu = bitow_na_wierzcholek(ilosc_wierzcholkow)

    T = 1000
    liczebnosc = 10
    prawd_mutacji = 0.1
    prawd_krzyzowania = 0.75

    chromosom, ilosc_kolorow = koloruj(g)
    print(chromosom)
    print(ilosc_kolorow)
