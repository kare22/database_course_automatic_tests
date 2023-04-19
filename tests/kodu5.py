from checks import *

def tests():
    return [
        titleLayer('Funktsioon f_vanus'),
        getCheckFunction('f_vanus', "'09.09.2000'", expectedValue=22, points=0.25),
        getCheckFunction('f_vanus', "'01.01.2000'", expectedValue=23, points=0.25),

        titleLayer('Funktsioon f_klubiranking'),
        getCheckFunction('f_klubiranking', 54, expectedValue=1279.6, dataType='float', points=0.25),
        getCheckFunction('f_klubiranking', 59, expectedValue=1407.0, dataType='float', points=0.25),

        titleLayer('Funktsioon f_top10'),
        getCheckFunction('f_top10', 44, checkCount=10, points=0.25),
        getCheckFunction('f_top10', 44, where="mangija LIKE 'Murakas%'", points=0.25),

        titleLayer('Protseduur sp_uus_turniir'),
        getCheckProcedure(
            'sp_uus_turniir', "'Tartu Meister', '02.02.2022',1,'Tartu'",
            numberOfCols=4,
            preQuery="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
            resultQuery="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '02.02.2022'",
            points=0.25,
        ),
        getCheckProcedure(
            'sp_uus_turniir', "'Tartu Meister', '02.02.2022',2,'Tartu'",
            numberOfCols=4,
            preQuery="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
            resultQuery="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '03.02.2022'",
            points=0.25,
        ),
    ]