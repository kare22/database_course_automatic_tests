from checks import *

def tests():
    return [
        titleLayer('Funktsioon f_vanus'),
        getCheckFunction('f_vanus', "'09.09.2000'", expectedValue=22, points=1),
        getCheckFunction('f_vanus', "'01.01.2000'", expectedValue=23, points=1),

        titleLayer('Funktsioon f_klubiranking'),
        getCheckFunction('f_klubiranking', 54, expectedValue=1279.6, dataType='float', points=1),
        getCheckFunction('f_klubiranking', 59, expectedValue=1407.0, dataType='float', points=1),

        titleLayer('Funktsioon f_top10'),
        getCheckFunction('f_top10', 44, checkCount=10, points=1),
        getCheckFunction('f_top10', 44, where="mangija LIKE 'Murakas%'", points=1),

    ]