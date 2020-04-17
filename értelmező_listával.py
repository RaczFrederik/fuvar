#taxi_id;     indulas;          idotartam;  tavolsag;  viteldij;  borravalo;  fizetes_modja
#  [0]          [1]                [2]         [3]        [4]         [5]           [6]                         
#5240;  2016-12-15 23:45:00;       900;        2,5;      10,75;      2,45;      bankkártya

import sqlite3
conn = sqlite3.connect("fuvar.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS fuvar
        (taxi_id       INTEGER,
        indulas        TEXT,
        idotartam      INTEGER,
        tavolsag       REAL,
        viteldij       REAL,
        borravalo      REAL,
        fizetes_modja  TEXT)
        ''')
conn.commit()
def file_to_sql():
    with open("fuvar.csv", 'r', encoding='UTF-8-sig') as f:
        fejlec = f.readline()
        for sor in f:
            r = sor.replace(',','.').strip().split(';')
            c.execute("INSERT INTO fuvar Values(?,?,?,?,?,?,?)", (r[0],r[1],r[2],r[3],r[4],r[5],r[6]) )
    conn.commit()
c.execute("SELECT * FROM fuvar")
data = c.fetchall()
print( len(data) )

# sql 4.fel.
c.execute("SELECT SUM(viteldij+borravalo) FROM fuvar WHERE taxi_id = 6185")
bevetel = c.fetchall()[0][0]
print(bevetel)


#sql 5.fel.
c.execute("SELECT fizetes_modja, COUNT(*) FROM fuvar GROUP BY fizetes_modja")
fizetes_modja = c.fetchall()
print(fizetes_modja)

#beolvasás
with open("fuvar.csv", 'r', encoding='UTF-8-sig') as f:
    fejlec = f.readline()
    matrix = [sor.replace(',','.').strip().split(';') for sor in f]

#3.feladat
print(f' 3.feladat: {len(matrix)} fuvar' )

#4.feladat
bevetelek = 0
fuvar = 0
for sor in matrix:
    if sor[0] == "6185":
        fuvar     += 1
        viteldij   = float(sor[4])
        borravalo  = float(sor[5])
        bevetelek += viteldij + borravalo
print(f' 4.feladat: {fuvar} fuvar alatt {bevetelek} $' )

#5.feladat

fiz_mod = []
for sor in matrix:
    fiz_mod.append(sor[6])

fiz_mod_halmaz = set(fiz_mod)
for i in fiz_mod_halmaz:
    db = fiz_mod.count(i)
    print(i, db)
    
#6.fel
miles = 0
for sor in matrix:
    miles += float(sor[3])
print(f'6.feladat: {miles*1.6:.2f}')  #a ':.2' a tizedespont után 2 tizedesjeggyel adja meg a számot!

#7.fel
leghosszabb = 0
adatok = []
for sor in matrix:
    if int(sor[2]) > leghosszabb:
        leghosszabb = int(sor[2])
        adatok = sor
print(adatok)

#8.fel
with open("hibak.txt", 'w', encoding='UTF-8') as f:
    f.write(fejlec)
    for r in matrix:
        tav    = float(r[3]) == 0
        ido    = float(r[2]) == 0
        vitel  = float(r[4]) == 0
        if tav and not ido and not vitel:
            sor = f"{r[0]};{r[1]};{r[2]};{r[3]};{r[4]};{r[5]};{r[6]}".replace(",",";")
            print(f"{r[0]};{r[1]};{sor}", file = f)
        