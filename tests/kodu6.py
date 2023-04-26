from checks import *

user1 = 123456
user2 = 123457
partiiId = 123123

def tests():
    return [
        titleLayer('Kodutöö 6'),

        getCheckIndex('ix_riiginimi', 0.25),
        getCheckIndex('ix_suurus', 0.25),

        # getExecuteQuery('CALL trigger_partiiaeg(0.8, 70)'),
        # getExecuteQuery('CALL trigger_klubi_olemasolu(0.8, 70)'),

        getCheckTrigger('tg_partiiaeg', ['UPDATE', 'INSERT'], 'BEFORE', 0.5),

        getExecuteQuery("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
        getExecuteQuery("ALTER TABLE public.partiid ENABLE TRIGGER tg_partiiaeg"),
        getExecuteQuery("ALTER TABLE public.isikud DISABLE TRIGGER ALL"),
        getExecuteQuery("ALTER TABLE public.isikud ENABLE TRIGGER tg_klubi_olemasolu"),

        getExecuteQuery(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({user1},'Man', 'Ka')", hasFeedback=False,),
        getExecuteQuery(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({user2},'Kan', 'Ma')", hasFeedback=False,),
        getExecuteQuery(f"INSERT INTO public.partiid VALUES (44,'2023-04-22 17:45:24.000','2023-03-22 17:45:24.000',{user1},{user2},2,0, {partiiId})",),
        getCheckDataQuery('isikud', '*', where=f"public.isikud.id = {user1}", ),
        getCheckDataQuery('isikud', '*', where=f"public.isikud.id = {user2}", ),
        getCheckDataQuery(
            'partiid',
            'lopphetk',
            where=f"valge = {user1} AND must = {user2}",
            expectedValue='NULL',
            points=0.25,
            customSuccess="partii kuupäevadega '2023-04-22 17:45:24.000','2023-03-22 17:45:24.000' lõppaeg jäeti sisestamata",
            customFailure="partii kuupäevadega '2023-04-22 17:45:24.000','2023-03-22 17:45:24.000' sisestati"
        ),

        getCheckTrigger('tg_klubi_olemasolu', ['UPDATE', 'INSERT'], 'AFTER', points=0.5),
        getCheckDataQuery(
            'isikud',
            '*',
            join=f"public.klubid ON public.klubid.id=isikud.klubis",
            where=f"public.isikud.id = {user1} AND public.klubid.nimi LIKE '%ubitu%'",
            points=0.25,
            customSuccess='Klupita isikule lisati õige klubi id',
            customFailure='Klupita isikule ei lisatud õiget klubi id',
        ),
    ]