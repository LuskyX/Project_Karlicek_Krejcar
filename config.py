# database_connector
DB_FILE = "db/database.db"

# vaccination centers scrapper
URL_VACCENTERS = 'https://ockoreport.uzis.cz'
REGIONS = ["Hlavní město Praha", "Jihočeský", "Jihomoravský", "Karlovarský", "Liberecký",
        "Moravskoslezský", "Olomoucký", "Pardubický", "Plzeňský", "Středočeský", "Ústecký",
        "Vysočina", "Zlínský", "Královéhradecký"]
CENTER_TYPE = {"18+": 0, "16-17": 0, "12-15": 0, "without_registration": 0, "self-payers": 0}
VACCINES = {'COMIRNATY':0, 'SPIKEVAX': 0, 'JANSSEN': 0, 'Vaxzevria': 0}


# latitude longitude
adresa2gps = {'Londýnská 160/39, Praha 2': [50.07685127162937, 14.432848113734048],
              'Wilsonova 300/8, 11000 Praha 2 - Vinohrady': [50.08330619236537, 14.435705199748115],
              'Plzeňská 8, 150 00 Praha 5 - Smíchov, 150 00': [50.07330618231973, 14.402896328584372],
              'WESTFIELD CHODOV, Roztylská 2321/19': [50.03226214835474, 14.49158628439986],
              'Michnova 1622/4, 149 00 Praha 11 - Chodov': [50.03150640018952, 14.521377667197102],
              'Výstaviště 405/1, 603 00 Brno-střed': [49.18666132617922, 16.57663111688435],
              'U Dálnice 777, Modřice, 664 42': [49.13826856328991, 16.63305488486378],
              'Masarykovo nám. 34, 697 01 Kyjov': [49.010747461365725, 17.12307950948735],
              'Purkyňova 279': [49.34796008952216, 16.4347554457612],
              'Rooseveltova 31, 602 00 Brno-střed': [49.198433871442525, 16.611651999716518],
              'Jantarová 3344/4, Ostrava - Moravská Ostrava, 702 00': [49.83090827074483, 18.285877242065865],
              'Polská 1201/1, 77900 Olomouc': [49.58773055202256, 17.255481298370007],
              'Skalka 1693, Česká Třebová': [49.90772954256867, 16.447024724865845],
              'Pivovar Plzeňský Prazdroj, U Prazdroje 7, 301 00 Plzeň': [49.7467530382881, 13.387266011335827],
              'OČM Kongresové centrum (GASK), Kremnická 239/7, Kutná Hora 284 01': [49.94758634535838, 15.261859874727008],
              'Bílinská 3490/6, 400 01 Ústí nad Labem-centrum': [50.6588646076688, 14.040446282566183],
              'Hruškové Dvory 123, 586 01 Jihlava - Hruškové Dvory': [49.4097022929482, 15.607990759253532],
              'PSG Aréna, Březnická 5513, 760 01 Zlín': [49.2179394741856, 17.659829294148217],
              'Obchodní 1507, 686 01 Uherské Hradiště': [49.06977144158275, 17.46353272854849],
              'Dukelská tř. 1713/7, Hradec Králové, 500 02': [50.21351993055662, 15.818755694183947]}