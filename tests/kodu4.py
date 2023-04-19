from checks import *

def tests():
    return [
            titleLayer('Kodutöö 4'),

            titleLayer('Vaade v_turniiripartiid'),
            getCheckViewExistsQuery('v_turniiripartiid', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'turniir_nimi', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'toimumiskoht', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'partii_id', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'partii_algus', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'partii_lopp', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'kes_voitis', points=1),
            getCheckDataQuery('v_turniiripartiid', 'COUNT(*)', expectedValue=299, points=1),
            getCheckDataQuery('v_turniiripartiid', 'LOWER(kes_voitis)', where='partii_id = 270', expectedValue='valge', points=1),
            getCheckDataQuery('v_turniiripartiid', 'LOWER(kes_voitis)', where='partii_id = 241', expectedValue='must', points=1),
            getCheckDataQuery('v_turniiripartiid', 'LOWER(kes_voitis)', where='partii_id = 193', expectedValue='viik', points=1),

            titleLayer('Vaade v_klubipartiikogused'),
            getCheckViewExistsQuery('v_klubipartiikogused', points=1),
            getCheckColumnQuery('v_klubipartiikogused', 'klubi_nimi', points=1),
            getCheckColumnQuery('v_klubipartiikogused', 'partiisid', points=1),
            getCheckDataQuery('v_klubipartiikogused', 'COUNT(*)', expectedValue=12, points=1),
            getCheckDataQuery('v_klubipartiikogused', 'SUM(partiisid)', expectedValue=571, points=1),

            titleLayer('Vaade v_keskminepartii'),
            getCheckViewExistsQuery('v_keskminepartii', points=1),
            getCheckColumnQuery('v_keskminepartii', 'turniiri_nimi', points=1),
            getCheckColumnQuery('v_keskminepartii', 'keskmine_partii', points=1),
            getCheckDataQuery('v_keskminepartii', 'COUNT(*)', expectedValue=5, points=1),
            getCheckDataQuery('v_keskminepartii', 'ROUND(keskmine_partii, 3)', where="turniiri_nimi = 'Plekkkarikas 2010'", expectedValue='23.765', points=1),
            getCheckDataQuery('v_keskminepartii', 'ROUND(keskmine_partii, 3)', where="turniiri_nimi = 'Kolme klubi kohtumine'", expectedValue='23.040', points=1),

            titleLayer('Materialseeritud vaade mv_vaate_kontroll'),
            #select * from pg_matviews where matviewname = 'mv_partiide_arv_valgetega'
            getCheckDataQuery('mv_partiide_arv_valgetega', 'COUNT(*)', expectedValue=85, points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', '*', where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'", points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', 'MIN(partiisid_valgetega)', expectedValue=0, points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', 'MAX(partiisid_valgetega)', expectedValue=14, points=1),
    ]