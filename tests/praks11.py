from checks import *

def tests():
    return [
        titleLayer('Praktikum 11'),
        titleLayer('Pea meeles, et kõik ei pidanudki valmis saama!'),

        getCheckFunction('f_mangija_punktid_turniiril', '92,42', expectedValue=5.5, dataType='float', numberOfParameters=2, points=0.25),

        getCheckFunction('f_infopump', '', checkCount=105, numberOfParameters=0, points=0.25),

        getCheckFunction('f_klubisuurus', '54', expectedValue=5, numberOfParameters=1, points=0.25),

        getCheckFunction('f_nimi', "'test', 'kesk'", expectedValue='kesk, test', numberOfParameters=2, points=0.25),

        getCheckFunction('f_mangija_koormus', '73', expectedValue=18, numberOfParameters=1, points=0.25),

        getCheckFunction('f_mangija_voite_turniiril', '197,43', expectedValue=3, numberOfParameters=2, points=0.25),
        getCheckFunction('f_mangija_voite_turniiril', '75,44', expectedValue=0, numberOfParameters=2, points=0.25),

        getCheckFunction('f_mangija_viike_turniiril', '197,43', expectedValue=1, numberOfParameters=2, points=0.25),
        getCheckFunction('f_mangija_viike_turniiril', '75,44', expectedValue=0, numberOfParameters=2, points=0.25),

        getCheckFunction('f_mangija_kaotusi_turniiril', '197,43', expectedValue=0, numberOfParameters=2, points=0.25),
        getCheckFunction('f_mangija_kaotusi_turniiril', '75,44', expectedValue=2, numberOfParameters=2, points=0.25),

        getCheckFunction('f_klubiparimad', "'Areng'", checkCount=3, numberOfParameters=1, points=0.25),
        getCheckFunction('f_klubiparimad', "'Areng'", attributeName='punktisumma', where="isik = 'Pőder, Priit'", expectedValue=4.5, numberOfParameters=1, points=0.25),

        getCheckFunction('f_voit_viik_kaotus', '44', checkCount=63, numberOfParameters=1, points=0.25),
        getCheckFunction('f_voit_viik_kaotus', '44', attributeName='voite', where="id = 193", expectedValue=1, numberOfParameters=1, points=0.25),
        getCheckFunction('f_voit_viik_kaotus', '44', attributeName='viike', where="id = 193", expectedValue=1, numberOfParameters=1, points=0.25),
        getCheckFunction('f_voit_viik_kaotus', '44', attributeName='kaotusi', where="id = 193", expectedValue=0, numberOfParameters=1, points=0.25),
    ]