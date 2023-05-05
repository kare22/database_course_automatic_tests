from checks import *

jargId = 123456

def tests():
    return [
        titleLayer('Praktikum 11'),
        titleLayer('Pea meeles, et kõik ei pidanudki valmis saama!'),

        titleLayer('tg_ajakontroll'),
        getExecuteQuery("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
        getExecuteQuery("ALTER TABLE public.partiid ENABLE TRIGGER tg_ajakontroll"),

        getCheckTrigger('tg_ajakontroll', ['UPDATE', 'INSERT'], 'BEFORE', points=1),

        getExecuteQuery(f"INSERT INTO partiid (turniir, algushetk, valge, must, valge_tulemus, must_tulemus, id) VALUES (41, '2005-01-12 08:05:00.000', 73, 92, 1, 1, {jargId})", hasFeedback=False, ),
        getCheckDataQuery(
            'partiid',
            where=f"id = {jargId}",
            expectedValue='NULL',
            points=1,
            customSuccess="trigger tg_ajakontroll samal ajal toimub partii lisamine ei õnnestunud",
            customFailure="trigger tg_ajakontroll samal ajal toimub partii lisamine õnnestus"
        ),

        getExecuteQuery(f"INSERT INTO partiid (turniir, algushetk, valge, must, valge_tulemus, must_tulemus, id) VALUES (41, '2005-01-12 08:05:00.000', 201, 189, 1, 1, {jargId})", hasFeedback=False, ),
        getCheckDataQuery(
            'partiid',
            where=f"id = {jargId}",
            points=1,
            customSuccess="trigger tg_ajakontroll samal ajal toimub partii lisamine õnnestus",
            customFailure="trigger tg_ajakontroll samal ajal toimub partii lisamine ei õnnestunud"
        ),

        titleLayer('tg_riigid'),
        getExecuteQuery("ALTER TABLE public.riigid DISABLE TRIGGER ALL"),
        getExecuteQuery("ALTER TABLE public.riigid ENABLE TRIGGER tg_riigid"),

        getCheckTrigger('tg_riigid', ['INSERT'], 'BEFORE', points=1),

        getExecuteQuery(f"INSERT INTO riigid (id, nimi, pealinn) VALUES (123456, 'Bulgaria1', 'Sofia')", hasFeedback=False, ),
        getCheckDataQuery(
            'riigid',
            'COUNT(*)',
            where=f"nimi = 'Bulgaria'",
            points=1,
            expectedValue='1',
            customSuccess="trigger tg_riigid riigi 'Bulgaaria' lisamine lisamine õnnestus",
            customFailure="trigger tg_riigid riigi 'Bulgaaria' lisamine lisamine ei õnnestunud"
        ),

        getExecuteQuery(f"INSERT INTO riigid (id, nimi, pealinn) VALUES ({123457}, 'Test', 'Sofia')", hasFeedback=False, ),
        getCheckDataQuery(
            'riigid',
            'COUNT(*)',
            where=f"nimi = 'Test'",
            points=1,
            expectedValue='0',
            customSuccess="trigger tg_riigid riigi 'Test' lisamine lisamine ei õnnestunud",
            customFailure="trigger tg_riigid riigi 'Test' lisamine lisamine õnnestus"
        ),

        titleLayer('tg_kustuta_klubi'),
        getExecuteQuery("ALTER TABLE public.klubid DISABLE TRIGGER ALL"),
        getExecuteQuery("ALTER TABLE public.klubid ENABLE TRIGGER tg_kustuta_klubi"),

        getCheckTrigger('tg_kustuta_klubi', ['DELETE'], 'AFTER', points=1),
        getExecuteQuery(f"INSERT INTO Asulad VALUES (123456, 'Rakvere')", hasFeedback=False, ),
        getExecuteQuery(f"INSERT INTO Klubid (nimi, asula) VALUES ('Klubi Kustutamiseks', (select id from asulad where nimi = 'Rakvere'))", hasFeedback=False, ),
        getExecuteQuery(f"DELETE FROM klubid WHERE nimi='Klubi Kustutamiseks'", hasFeedback=False, ),

        getExecuteQuery(f"SELECT * FROM asulad", hasFeedback=False, ),

        getCheckDataQuery(
            'asulad',
            where=f"nimi = 'Rakvere'",
            expectedValue='NULL',
            points=1,
            customSuccess="trigger tg_kustuta_klubi asula kustumine koos ainsa klubiga ei õnnestunud",
            customFailure="trigger tg_kustuta_klubi asula kustumine koos ainsa klubiga õnnestus"
        ),

        getExecuteQuery(f"INSERT INTO Asulad VALUES (123457, 'Tapa')", hasFeedback=False, ),
        getExecuteQuery(f"INSERT INTO Klubid (nimi, asula) VALUES ('Uus_1', (select id from asulad where nimi = 'Tapa'))", hasFeedback=False, ),
        getExecuteQuery(f"INSERT INTO Klubid (nimi, asula) VALUES ('Uus_2', (select id from asulad where nimi = 'Tapa'))", hasFeedback=False, ),
        getExecuteQuery(f"DELETE FROM klubid WHERE nimi='Uus_1'", hasFeedback=False, ),

        getCheckDataQuery(
            'asulad',
            where=f"nimi = 'Tapa'",
            points=1,
            customSuccess="trigger tg_kustuta_klubi asula kustumine kus on veel klubisi õnnestus",
            customFailure="trigger tg_kustuta_klubi asula kustumine kus on veel klubisi ei õnnestunud"
        ),

        titleLayer('tg_partiiaeg1'),
        getExecuteQuery("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
        getExecuteQuery("ALTER TABLE public.partiid ENABLE TRIGGER tg_partiiaeg1"),

        getCheckTrigger('tg_partiiaeg1', ['UPDATE', 'INSERT'], 'BEFORE', points=1),

        getExecuteQuery(f"INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-10 08:04', 2,6, 123123)", hasFeedback=False, ),
        getCheckDataQuery(
            'partiid',
            where=f"id = 123123",
            points=1,
            expectedValue='NULL',
            customSuccess="tg_partiiaeg1 uus partii algab enne turniiri algust ei ole olemas",
            customFailure="tg_partiiaeg1 uus partii algab enne turniiri algust on olemas"
        ),
    ]

'''
		jarg_id := nextval('serial_registration');
		INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-10 08:04', 2,6, jarg_id);
		if 		not exists (select p.algushetk, p.lopphetk, t.alguskuupaev, t.loppkuupaev  from partiid p join turniirid t on t.id = p.turniir where p.id = jarg_id)
		then 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii algab enne turniiri algust', 'ei ole olemas', 'OK', 0, 0, praktikum_11_jr);
		else 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii algab enne turniiri algust', 'on olemas, ei tohiks', 'VIGA', 0, 0, praktikum_11_jr);
				delete from partiid where id = jarg_id;
		end if;
		
		jarg_id := nextval('serial_registration');
		INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-22 08:04', 2,6, jarg_id);
		if 		not exists (select p.algushetk, p.lopphetk, t.alguskuupaev, t.loppkuupaev  from partiid p join turniirid t on t.id = p.turniir where p.id = jarg_id)
		then 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii algab peale turniiri loppu', 'ei ole olemas', 'OK', 0, 0, praktikum_11_jr);
		else 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii algab peale turniiri loppu', 'on olemas, ei tohiks', 'VIGA', 0, 0, praktikum_11_jr);
				delete from partiid where id = jarg_id;
		end if;
		
		jarg_id := nextval('serial_registration');
		INSERT INTO Partiid(turniir, algushetk, lopphetk, valge, must, id) VALUES (41, '2005-01-12 08:04', '2005-01-22 09:10', 2,6, jarg_id);
		if 		not exists (select p.algushetk, p.lopphetk, t.alguskuupaev, t.loppkuupaev  from partiid p join turniirid t on t.id = p.turniir where p.id = jarg_id)
		then 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii loppeb peale turniiri loppu', 'ei ole olemas', 'OK', 0, 0, praktikum_11_jr);
		else 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii loppeb peale turniiri loppu', 'on olemas, ei tohiks', 'VIGA', 0, 0, praktikum_11_jr);
				delete from partiid where id = jarg_id;
		end if;
		
		jarg_id := nextval('serial_registration');
		INSERT INTO Partiid(turniir, algushetk, lopphetk, valge, must, id) VALUES (41, '2005-01-12 08:04', '2005-01-01 09:10', 2,6, jarg_id);
		if 		not exists (select p.algushetk, p.lopphetk, t.alguskuupaev, t.loppkuupaev  from partiid p join turniirid t on t.id = p.turniir where p.id = jarg_id)
		then 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii loppeb enne turniiri algust', 'ei ole olemas', 'OK', 0, 0, praktikum_11_jr);
		else 	insert into Staatus values('Praktikum 11', 'Triger "tg_partiiaeg1" uus partii loppeb enne turniiri algust', 'on olemas, ei tohiks', 'VIGA', 0, 0, praktikum_11_jr);
				delete from partiid where id = jarg_id;
		end if;

'''