--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Homebrew)
-- Dumped by pg_dump version 14.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: isikud; Type: TABLE; Schema: public; Owner: karelpaan
--

CREATE TABLE public.isikud (
    id integer NOT NULL,
    eesnimi character varying(50) NOT NULL,
    perenimi character varying(50) NOT NULL,
    isikukood character varying(11),
    klubis integer,
    synniaeg date,
    sugu character(1) DEFAULT 'm'::bpchar NOT NULL,
    ranking integer
);


ALTER TABLE public.isikud OWNER TO karelpaan;

--
-- Name: isikud_id_seq; Type: SEQUENCE; Schema: public; Owner: karelpaan
--

CREATE SEQUENCE public.isikud_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.isikud_id_seq OWNER TO karelpaan;

--
-- Name: isikud_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: karelpaan
--

ALTER SEQUENCE public.isikud_id_seq OWNED BY public.isikud.id;


--
-- Name: klubid; Type: TABLE; Schema: public; Owner: karelpaan
--

CREATE TABLE public.klubid (
    id integer NOT NULL,
    nimi character varying(100) NOT NULL,
    asukoht character varying(70) DEFAULT 'Tartu'::character varying NOT NULL
);


ALTER TABLE public.klubid OWNER TO karelpaan;

--
-- Name: klubid_id_seq; Type: SEQUENCE; Schema: public; Owner: karelpaan
--

CREATE SEQUENCE public.klubid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.klubid_id_seq OWNER TO karelpaan;

--
-- Name: klubid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: karelpaan
--

ALTER SEQUENCE public.klubid_id_seq OWNED BY public.klubid.id;


--
-- Name: partiid; Type: TABLE; Schema: public; Owner: karelpaan
--

CREATE TABLE public.partiid (
    turniir integer NOT NULL,
    algushetk timestamp without time zone NOT NULL,
    lopphetk timestamp without time zone,
    valge integer NOT NULL,
    must integer NOT NULL,
    valge_tulemus smallint,
    must_tulemus smallint,
    id integer NOT NULL,
    CONSTRAINT ajakontroll CHECK ((lopphetk >= algushetk)),
    CONSTRAINT vastavus CHECK (((valge_tulemus + must_tulemus) = 2))
);


ALTER TABLE public.partiid OWNER TO karelpaan;

--
-- Name: partiid_id_seq; Type: SEQUENCE; Schema: public; Owner: karelpaan
--

CREATE SEQUENCE public.partiid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.partiid_id_seq OWNER TO karelpaan;

--
-- Name: partiid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: karelpaan
--

ALTER SEQUENCE public.partiid_id_seq OWNED BY public.partiid.id;


--
-- Name: turniirid; Type: TABLE; Schema: public; Owner: karelpaan
--

CREATE TABLE public.turniirid (
    id integer NOT NULL,
    nimi character varying(100) NOT NULL,
    toimumiskoht character varying(100),
    alguskuupaev date NOT NULL,
    loppkuupaev date,
    CONSTRAINT ajakontroll CHECK ((alguskuupaev <= loppkuupaev))
);


ALTER TABLE public.turniirid OWNER TO karelpaan;

--
-- Name: turniirid_id_seq; Type: SEQUENCE; Schema: public; Owner: karelpaan
--

CREATE SEQUENCE public.turniirid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.turniirid_id_seq OWNER TO karelpaan;

--
-- Name: turniirid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: karelpaan
--

ALTER SEQUENCE public.turniirid_id_seq OWNED BY public.turniirid.id;


--
-- Name: isikud id; Type: DEFAULT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.isikud ALTER COLUMN id SET DEFAULT nextval('public.isikud_id_seq'::regclass);


--
-- Name: klubid id; Type: DEFAULT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.klubid ALTER COLUMN id SET DEFAULT nextval('public.klubid_id_seq'::regclass);


--
-- Name: partiid id; Type: DEFAULT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.partiid ALTER COLUMN id SET DEFAULT nextval('public.partiid_id_seq'::regclass);


--
-- Name: turniirid id; Type: DEFAULT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.turniirid ALTER COLUMN id SET DEFAULT nextval('public.turniirid_id_seq'::regclass);


--
-- Data for Name: isikud; Type: TABLE DATA; Schema: public; Owner: karelpaan
--

INSERT INTO public.isikud VALUES (9, 'Tarmo', 'Kooser', '37209112028', NULL, '1972-09-11', 'm', 1076);
INSERT INTO public.isikud VALUES (71, 'Arvo', 'Mets', '33911230101', 51, '1939-11-23', 'm', 1066);
INSERT INTO public.isikud VALUES (73, 'Pjotr', 'Pustota', '36602240707', 59, '1966-02-24', 'm', 1646);
INSERT INTO public.isikud VALUES (74, 'Kalle', 'Kivine', '36006230808', 57, '1960-06-23', 'm', 1411);
INSERT INTO public.isikud VALUES (147, 'Kalev', 'Jőud', '35304040404', 50, '1953-04-04', 'm', 1255);
INSERT INTO public.isikud VALUES (156, 'Tőnu', 'Tőrs', '34805050505', 52, '1948-05-05', 'm', 1497);
INSERT INTO public.isikud VALUES (78, 'Andrei', 'Sosnov', '37704220102', 59, '1977-04-22', 'm', 1813);
INSERT INTO public.isikud VALUES (12, 'Piia', 'Looser', '47303142014', 50, '1973-03-14', 'n', 1091);
INSERT INTO public.isikud VALUES (10, 'Tiina', 'Kooser', '47401010224', NULL, '1974-01-01', 'n', 1027);
INSERT INTO public.isikud VALUES (8, 'Taimi', 'Sabel', '47510142025', NULL, '1975-10-14', 'n', 1851);
INSERT INTO public.isikud VALUES (199, 'Sander', 'Saabas', '38707303030', 61, '1987-07-30', 'm', 1047);
INSERT INTO public.isikud VALUES (201, 'Lembit', 'Allveelaev', '36608080808', 61, '1966-08-08', 'm', 1040);
INSERT INTO public.isikud VALUES (13, 'Laura', 'Kask', '47303142020', NULL, '1973-03-14', 'n', 1268);
INSERT INTO public.isikud VALUES (6, 'Kaia', 'Maja', '47001221010', NULL, '1970-01-22', 'n', 1704);
INSERT INTO public.isikud VALUES (192, 'Keiu', 'Vői', '48412242424', 61, '1984-12-24', 'n', 1047);
INSERT INTO public.isikud VALUES (193, 'Heli', 'Jälg', '48112313131', 61, '1981-12-31', 'n', 1429);
INSERT INTO public.isikud VALUES (194, 'Kaja', 'Lood', '47005040405', 61, '1970-05-04', 'n', 1006);
INSERT INTO public.isikud VALUES (195, 'Laine', 'Hari', '46807171720', 61, '1968-07-17', 'n', 1124);
INSERT INTO public.isikud VALUES (196, 'Kalju', 'Saaremets', '36308171015', 61, '1963-08-17', 'm', 1205);
INSERT INTO public.isikud VALUES (197, 'Priit', 'Pőder', '36709291416', 61, '1967-09-29', 'm', 1666);
INSERT INTO public.isikud VALUES (2, 'Margus', 'Muru', '37602022016', 61, '1976-02-02', 'm', 1167);
INSERT INTO public.isikud VALUES (90, 'Urmas', 'Ubin', '35803081803', 58, '1958-03-08', 'm', 1028);
INSERT INTO public.isikud VALUES (162, 'Urmas', 'Ümbrik', '37304152020', 52, '1973-04-15', 'm', 1039);
INSERT INTO public.isikud VALUES (198, 'Urmas', 'Uljas', '36805221413', 61, '1968-05-22', 'm', 1005);
INSERT INTO public.isikud VALUES (93, 'Nadja', 'Puhasmaa', '45906301219', 57, '1959-06-30', 'n', 1058);
INSERT INTO public.isikud VALUES (94, 'Maria', 'Lihtne', '44907172613', 54, '1949-07-17', 'n', 1075);
INSERT INTO public.isikud VALUES (148, 'Heli', 'Kopter', '47108271519', 50, '1971-08-27', 'n', 1654);
INSERT INTO public.isikud VALUES (150, 'Katrin', 'Kask', '47011182050', 50, '1970-11-18', 'n', 1298);
INSERT INTO public.isikud VALUES (151, 'Kati', 'Karu', '46110221681', 50, '1961-10-22', 'n', 1030);
INSERT INTO public.isikud VALUES (152, 'Pille', 'Porgand', '46809101030', 50, '1968-09-10', 'n', 1144);
INSERT INTO public.isikud VALUES (157, 'Kristi', 'Kirves', '46901173020', 52, '1969-01-17', 'n', 1050);
INSERT INTO public.isikud VALUES (160, 'Ulvi', 'Uus', '46802012414', 52, '1968-02-01', 'n', 1175);
INSERT INTO public.isikud VALUES (163, 'Tatjana', 'Umnaja', '45510092514', 53, '1955-10-09', 'n', 1045);
INSERT INTO public.isikud VALUES (154, 'Ingo', 'Ilus', '36712044050', 55, '1967-12-04', 'm', 1041);
INSERT INTO public.isikud VALUES (165, 'Aljona', 'Aljas', '46603312628', 53, '1966-03-31', 'n', 1088);
INSERT INTO public.isikud VALUES (171, 'Sanna', 'Sari', '47309291414', 56, '1973-09-29', 'n', 1035);
INSERT INTO public.isikud VALUES (173, 'Hiie', 'Hiid', '47704143256', 56, '1977-04-14', 'n', 1453);
INSERT INTO public.isikud VALUES (175, 'Anna', 'Raha', '46605012233', 56, '1966-05-01', 'n', 1014);
INSERT INTO public.isikud VALUES (186, 'Tiiu', 'Talutütar', '45406124152', 60, '1954-06-12', 'n', 1048);
INSERT INTO public.isikud VALUES (187, 'Ere', 'Valgus', '48108182819', 60, '1981-08-18', 'n', 1002);
INSERT INTO public.isikud VALUES (80, 'Henno', 'Hiis', '37907063645', 55, '1976-07-06', 'm', 1237);
INSERT INTO public.isikud VALUES (86, 'Toomas', 'Remmelgas', '37812082134', 54, '1978-12-08', 'm', 1010);
INSERT INTO public.isikud VALUES (88, 'Mihkel', 'Maakamar', '38702106253', 59, '1987-02-10', 'm', 1020);
INSERT INTO public.isikud VALUES (89, 'Artur', 'Muld', '36911235164', 58, '1969-11-23', 'm', 1063);
INSERT INTO public.isikud VALUES (92, 'Toomas', 'Umnik', '36803261144', 57, '1968-03-26', 'm', 1029);
INSERT INTO public.isikud VALUES (145, 'Tarmo', 'Tarm', '36710301122', 50, '1967-10-30', 'm', 1128);
INSERT INTO public.isikud VALUES (146, 'Peeter', 'Peet', '36502125462', 50, '1965-02-12', 'm', 1053);
INSERT INTO public.isikud VALUES (79, 'Helina', 'Hiis', '46909099999', 55, '1969-09-09', 'n', 1000);
INSERT INTO public.isikud VALUES (82, 'Maria', 'Murakas', '46701226020', 54, '1967-01-22', 'n', 2013);
INSERT INTO public.isikud VALUES (83, 'Maria', 'Medvedovna', '47409193456', 58, '1974-09-19', 'n', 1492);
INSERT INTO public.isikud VALUES (85, 'Liis', 'Metsonen', '48006065123', 54, '1980-06-06', 'n', 1295);
INSERT INTO public.isikud VALUES (87, 'Anna', 'Ristik', '47606143265', 55, '1976-06-14', 'n', 1125);
INSERT INTO public.isikud VALUES (91, 'Jelena', 'Pirn', '46210125040', 58, '1962-10-12', 'n', 1068);
INSERT INTO public.isikud VALUES (72, 'Maari', 'Mustikas', '48012250202', 54, '1980-12-25', 'n', 1005);
INSERT INTO public.isikud VALUES (75, 'Malle', 'Maasikas', '46906220808', 57, '1969-06-22', 'n', 1645);
INSERT INTO public.isikud VALUES (167, 'Valve', 'Vask', '45602091010', 53, '1956-02-09', 'n', 1116);
INSERT INTO public.isikud VALUES (149, 'Kalju', 'Kotkas', '35306032623', 50, '1953-06-03', 'm', 1090);
INSERT INTO public.isikud VALUES (153, 'Ilo', 'Ilus', '37502282135', 55, '1975-02-28', 'm', 1343);
INSERT INTO public.isikud VALUES (155, 'Mart', 'Mari', '37602232513', 55, '1976-02-23', 'm', 1249);
INSERT INTO public.isikud VALUES (159, 'Tőnis', 'Tőrv', '36609112425', 52, '1966-09-11', 'm', 1289);
INSERT INTO public.isikud VALUES (161, 'Uljas', 'Ratsanik', '38108203514', 52, '1981-08-20', 'm', 1132);
INSERT INTO public.isikud VALUES (164, 'Boriss', 'Borissov', '36909211561', 53, '1969-09-21', 'm', 1039);
INSERT INTO public.isikud VALUES (166, 'Mihkel', 'Välk', '37009302563', 53, '1970-09-30', 'm', 1012);
INSERT INTO public.isikud VALUES (168, 'Peeter', 'Aljas', '36911112528', 53, '1969-11-11', 'm', 1086);
INSERT INTO public.isikud VALUES (169, 'Meelis', 'Meel', '36709252525', 56, '1967-09-25', 'm', 1622);
INSERT INTO public.isikud VALUES (170, 'Mati', 'All', '36511284135', 56, '1965-11-28', 'm', 1001);
INSERT INTO public.isikud VALUES (172, 'Peeter', 'Sari', '37011161616', 56, '1970-11-16', 'm', 2060);
INSERT INTO public.isikud VALUES (174, 'Ahto', 'Palk', '38311152463', 56, '1983-11-15', 'm', 1138);
INSERT INTO public.isikud VALUES (176, 'Tormi', 'Hoiatus', '38608015361', 56, '1986-08-01', 'm', 1004);
INSERT INTO public.isikud VALUES (177, 'Ahti', 'Mőisamees', '37701093658', 56, '1977-01-09', 'm', 1223);
INSERT INTO public.isikud VALUES (188, 'Toomas', 'Toom', '37501055555', 60, '1975-01-05', 'm', 1061);
INSERT INTO public.isikud VALUES (189, 'Kristjan', 'Kuld', '38609165632', 60, '1986-09-16', 'm', 1068);
INSERT INTO public.isikud VALUES (190, 'Kaarel', 'Kaaren', '36911306452', 60, '1969-11-30', 'm', 1057);
INSERT INTO public.isikud VALUES (191, 'Kait', 'Kalamees', '37905312634', 60, '1979-05-31', 'm', 1006);
INSERT INTO public.isikud VALUES (158, 'Anneli', 'Mets', '46511132627', 52, '1965-11-13', 'n', 1628);
INSERT INTO public.isikud VALUES (76, 'Linda', 'Sammal', '46710101010', 58, '1967-10-10', 'n', 1943);
INSERT INTO public.isikud VALUES (84, 'Ilona', 'Polje', '48201291516', 51, '1982-01-29', 'n', 1086);
INSERT INTO public.isikud VALUES (77, 'Arvo', 'Angervaks', '35911111111', 59, '1959-11-11', 'm', 1149);
INSERT INTO public.isikud VALUES (200, 'Siim', 'Susi', '37101012048', 51, '1971-01-01', 'm', 1217);
INSERT INTO public.isikud VALUES (15, 'Oleg', 'Oll', '65453067841', 4, '1999-02-02', 'm', 1000);
INSERT INTO public.isikud VALUES (16, 'Olga', 'Oll', '35453067841', 4, '1999-02-02', 'n', 1001);
INSERT INTO public.isikud VALUES (17, 'Vahur', 'Kahur', '55453067441', 4, '2002-02-02', 'm', 1500);
INSERT INTO public.isikud VALUES (18, 'Valli', 'Kraav', '50302026224', 4, '2003-02-02', 'm', 2300);
INSERT INTO public.isikud VALUES (19, 'Valter', 'Vale', '50404046321', 4, '2004-04-04', 'm', 2600);
INSERT INTO public.isikud VALUES (81, 'Irys', 'Kompvek', '46901195849', 51, '1969-01-19', 'n', 1053);


--
-- Data for Name: klubid; Type: TABLE DATA; Schema: public; Owner: karelpaan
--

INSERT INTO public.klubid VALUES (59, 'Musta kivi kummardajad', 'Tartu');
INSERT INTO public.klubid VALUES (57, 'Vőitmatu Valge', 'Tartu');
INSERT INTO public.klubid VALUES (55, 'Ruudu Liine', 'Tartu');
INSERT INTO public.klubid VALUES (51, 'Laudnikud', 'Tartu');
INSERT INTO public.klubid VALUES (54, 'Ajurebend', 'Tartu');
INSERT INTO public.klubid VALUES (50, 'Raudne Ratsu', 'Tallinn');
INSERT INTO public.klubid VALUES (52, 'Pärnu Parimad', 'Pärnu');
INSERT INTO public.klubid VALUES (53, 'Vabaettur', 'Narva');
INSERT INTO public.klubid VALUES (56, 'Maletäht', 'Tallinn');
INSERT INTO public.klubid VALUES (60, 'Chess', 'Viljandi');
INSERT INTO public.klubid VALUES (61, 'Areng', 'Tallinn');
INSERT INTO public.klubid VALUES (1, 'Tallinna ratsud', 'Tallinn');
INSERT INTO public.klubid VALUES (3, 'Odamehed', 'Tartu');
INSERT INTO public.klubid VALUES (4, 'Osav oda', 'Otepää');
INSERT INTO public.klubid VALUES (58, 'Valge Mask', 'Valga');


--
-- Data for Name: partiid; Type: TABLE DATA; Schema: public; Owner: karelpaan
--

INSERT INTO public.partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:33:22', 150, 75, 2, 0, 1);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:29:01', 152, 91, 1, 1, 2);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:01:00', '2005-03-04 11:27:01', 87, 93, 2, 0, 3);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:11:24', 193, 148, 1, 1, 4);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:01:00', '2005-03-04 16:22:52', 71, 73, 0, 2, 5);
INSERT INTO public.partiid VALUES (41, '2005-01-12 13:09:00', '2005-01-12 13:32:17', 93, 75, 0, 2, 6);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:02:00', '2007-09-01 10:22:44', 195, 152, 1, 1, 7);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:02:00', '2007-09-01 09:26:18', 176, 82, 2, 0, 8);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:17:08', 172, 168, 2, 0, 9);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:41:40', 175, 165, 2, 0, 10);
INSERT INTO public.partiid VALUES (47, '2010-10-14 10:01:00', '2010-10-14 10:27:26', 91, 81, 0, 2, 11);
INSERT INTO public.partiid VALUES (47, '2010-10-14 12:01:00', '2010-10-14 12:21:52', 80, 73, 1, 1, 12);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:02:00', '2005-03-04 10:29:06', 85, 80, 2, 0, 13);
INSERT INTO public.partiid VALUES (41, '2005-01-12 16:02:00', '2005-01-12 16:24:16', 93, 74, 0, 2, 14);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:17:56', 153, 82, 0, 2, 15);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:34:30', 161, 77, 1, 1, 16);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:03:00', '2005-03-04 16:39:04', 79, 90, 1, 1, 17);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:13:02', 171, 166, 0, 2, 18);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:28:44', 192, 187, 1, 1, 19);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:41:18', 191, 165, 2, 0, 20);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:32:01', 199, 177, 1, 1, 21);
INSERT INTO public.partiid VALUES (47, '2010-10-14 11:02:00', '2010-10-14 11:22:07', 90, 81, 1, 1, 22);
INSERT INTO public.partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:28:50', 171, 161, 1, 1, 23);
INSERT INTO public.partiid VALUES (41, '2005-01-12 16:02:00', '2005-01-12 16:24:07', 92, 75, 1, 1, 24);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:30:50', 76, 82, 1, 1, 25);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:28:19', 148, 145, 1, 1, 26);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:34:47', 84, 83, 0, 2, 27);
INSERT INTO public.partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:22:43', 81, 85, 2, 0, 28);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:02:00', '2006-06-04 09:36:04', 190, 162, 1, 1, 29);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:22:59', 147, 86, 2, 0, 30);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:21:20', 191, 167, 2, 0, 31);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:02:00', '2005-03-04 09:23:07', 88, 76, 2, 0, 32);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:02:00', '2006-06-04 10:14:53', 152, 83, 1, 1, 33);
INSERT INTO public.partiid VALUES (47, '2010-10-14 11:03:00', '2010-10-14 11:37:51', 94, 88, 1, 1, 34);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:02:00', '2005-03-04 08:29:14', 74, 89, 0, 2, 35);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:03:00', '2006-06-04 17:40:26', 79, 78, 0, 2, 36);
INSERT INTO public.partiid VALUES (47, '2010-10-14 10:05:00', '2010-10-14 10:36:14', 90, 88, 1, 1, 37);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:33:03', 189, 188, 2, 0, 38);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:35:18', 88, 87, 2, 0, 39);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:01:00', '2005-03-04 14:22:38', 92, 79, 1, 1, 40);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:21:46', 73, 83, 1, 1, 41);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:25:51', 87, 82, 0, 2, 42);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:01:00', '2005-03-04 14:22:10', 88, 79, 2, 0, 43);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:02:00', '2005-03-04 13:32:08', 82, 89, 1, 1, 44);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:35:05', 172, 165, 2, 0, 45);
INSERT INTO public.partiid VALUES (47, '2010-10-14 14:01:00', '2010-10-14 14:23:45', 94, 81, 1, 1, 46);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:19:02', 90, 87, 0, 2, 47);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:28:23', 201, 73, 0, 2, 48);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:28:15', 170, 87, 2, 0, 49);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:03:00', '2005-03-04 09:33:11', 82, 92, 1, 1, 50);
INSERT INTO public.partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:18:58', 198, 82, 0, 2, 51);
INSERT INTO public.partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:33:26', 192, 161, 0, 2, 52);
INSERT INTO public.partiid VALUES (41, '2005-01-12 16:02:00', '2005-01-12 16:14:40', 77, 73, 0, 2, 53);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:03:00', '2005-03-04 12:19:28', 89, 75, 1, 1, 54);
INSERT INTO public.partiid VALUES (47, '2010-10-14 08:04:00', '2010-10-14 08:28:49', 89, 82, 2, 0, 55);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:26:21', 197, 159, 2, 0, 56);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:03:00', '2005-03-04 10:31:36', 81, 77, 0, 2, 57);
INSERT INTO public.partiid VALUES (41, '2005-01-12 11:08:00', '2005-01-12 11:35:48', 78, 92, 2, 0, 58);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:04:00', '2005-03-04 13:14:50', 87, 81, 0, 2, 59);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:22:46', 151, 87, 0, 2, 60);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:04:00', '2005-03-04 12:17:17', 91, 80, 2, 0, 61);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:19:22', 171, 83, 0, 2, 62);
INSERT INTO public.partiid VALUES (47, '2010-10-14 09:10:00', '2010-10-14 09:45:48', 94, 84, 1, 1, 63);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:01:00', '2006-06-04 16:39:54', 201, 147, 0, 2, 64);
INSERT INTO public.partiid VALUES (41, '2005-01-12 10:04:00', '2005-01-12 10:28:23', 80, 79, 1, 1, 65);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:25:42', 156, 86, 2, 0, 66);
INSERT INTO public.partiid VALUES (44, '2007-09-01 13:01:00', '2007-09-01 13:31:37', 81, 74, 0, 2, 67);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:04:00', '2005-03-04 12:15:11', 93, 91, 0, 2, 68);
INSERT INTO public.partiid VALUES (47, '2010-10-14 17:01:00', '2010-10-14 17:16:56', 83, 82, 2, 0, 69);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:02:00', '2007-09-01 11:28:41', 160, 157, 2, 0, 70);
INSERT INTO public.partiid VALUES (41, '2005-01-12 14:06:00', '2005-01-12 14:24:26', 73, 74, 2, 0, 71);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:18:34', 175, 152, 1, 1, 72);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:15:54', 187, 84, 1, 1, 73);
INSERT INTO public.partiid VALUES (47, '2010-10-14 14:01:00', '2010-10-14 14:22:13', 87, 84, 1, 1, 74);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:03:00', '2005-03-04 11:24:35', 92, 76, 1, 1, 75);
INSERT INTO public.partiid VALUES (41, '2005-01-12 11:03:00', '2005-01-12 11:31:54', 75, 80, 2, 0, 76);
INSERT INTO public.partiid VALUES (41, '2005-01-12 10:04:00', '2005-01-12 10:33:03', 92, 79, 2, 0, 77);
INSERT INTO public.partiid VALUES (43, '2006-06-04 15:01:00', '2006-06-04 15:19:57', 168, 85, 2, 0, 78);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:02:00', '2007-09-01 16:37:18', 188, 146, 0, 2, 79);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:19:08', 91, 71, 2, 0, 80);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:03:00', '2006-06-04 12:30:47', 173, 77, 1, 1, 81);
INSERT INTO public.partiid VALUES (42, '2005-03-04 15:02:00', '2005-03-04 15:26:39', 73, 76, 1, 1, 82);
INSERT INTO public.partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:20:49', 191, 85, 1, 1, 83);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:19:52', 157, 85, 0, 2, 84);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:23:53', 90, 78, 0, 2, 85);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:31:28', 156, 72, 2, 0, 86);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:02:00', '2006-06-04 11:25:11', 199, 195, 2, 0, 87);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:24:47', 190, 145, 1, 1, 88);
INSERT INTO public.partiid VALUES (44, '2007-09-01 08:04:00', '2007-09-01 08:22:49', 147, 83, 0, 2, 89);
INSERT INTO public.partiid VALUES (44, '2007-09-01 13:02:00', '2007-09-01 13:36:46', 198, 188, 2, 0, 90);
INSERT INTO public.partiid VALUES (43, '2006-06-04 15:01:00', '2006-06-04 15:16:17', 167, 166, 2, 0, 91);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:20:30', 201, 198, 2, 0, 92);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:31:21', 149, 93, 2, 0, 93);
INSERT INTO public.partiid VALUES (41, '2005-01-12 17:03:00', '2005-01-12 17:26:14', 93, 80, 1, 1, 94);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:15:26', 89, 73, 1, 1, 95);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:02:00', '2005-03-04 10:26:31', 75, 84, 2, 0, 96);
INSERT INTO public.partiid VALUES (41, '2005-01-12 10:05:00', '2005-01-12 10:29:15', 93, 87, 1, 1, 97);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:31:07', 188, 78, 1, 1, 98);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:30:59', 167, 156, 0, 2, 99);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:28:37', 175, 162, 2, 0, 100);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:21:20', 192, 155, 0, 2, 101);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:19:44', 73, 81, 1, 1, 102);
INSERT INTO public.partiid VALUES (47, '2010-10-14 16:04:00', '2010-10-14 16:23:00', 90, 72, 0, 2, 103);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:25:08', 172, 160, 1, 1, 104);
INSERT INTO public.partiid VALUES (41, '2005-01-12 12:02:00', '2005-01-12 12:25:05', 92, 87, 2, 0, 105);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:02:00', '2005-03-04 11:26:46', 90, 71, 0, 2, 106);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:31:29', 146, 75, 2, 0, 107);
INSERT INTO public.partiid VALUES (44, '2007-09-01 08:01:00', '2007-09-01 08:18:13', 191, 167, 0, 2, 108);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:21:52', 82, 72, 2, 0, 109);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:33:30', 172, 79, 1, 1, 110);
INSERT INTO public.partiid VALUES (41, '2005-01-12 08:02:00', '2005-01-12 08:19:28', 73, 92, 1, 1, 111);
INSERT INTO public.partiid VALUES (44, '2007-09-01 13:01:00', '2007-09-01 13:30:35', 200, 146, 0, 2, 112);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:03:00', '2006-06-04 08:35:03', 168, 91, 2, 0, 113);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:02:00', '2006-06-04 10:17:30', 175, 148, 1, 1, 114);
INSERT INTO public.partiid VALUES (41, '2005-01-12 17:03:00', '2005-01-12 17:22:58', 88, 93, 1, 1, 115);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:03:00', '2007-09-01 12:31:06', 167, 163, 0, 2, 116);
INSERT INTO public.partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:25:22', 83, 80, 1, 1, 117);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:01:00', '2005-03-04 16:30:37', 89, 84, 1, 1, 118);
INSERT INTO public.partiid VALUES (41, '2005-01-12 13:07:00', '2005-01-12 13:32:46', 78, 74, 0, 2, 119);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:23:23', 165, 92, 0, 2, 120);
INSERT INTO public.partiid VALUES (47, '2010-10-14 13:01:00', '2010-10-14 13:27:29', 91, 84, 0, 2, 121);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:20:52', 193, 176, 1, 1, 122);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:03:00', '2005-03-04 16:31:01', 93, 81, 0, 2, 123);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:22:34', 86, 74, 2, 0, 124);
INSERT INTO public.partiid VALUES (41, '2005-01-12 09:03:00', '2005-01-12 09:30:53', 75, 79, 2, 0, 125);
INSERT INTO public.partiid VALUES (47, '2010-10-14 15:04:00', '2010-10-14 15:26:44', 89, 77, 2, 0, 126);
INSERT INTO public.partiid VALUES (47, '2010-10-14 12:10:00', '2010-10-14 12:30:06', 87, 77, 1, 1, 127);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:01:00', '2005-03-04 14:29:17', 72, 76, 2, 0, 128);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:21:14', 166, 72, 1, 1, 129);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:30:44', 87, 72, 0, 2, 130);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:03:00', '2005-03-04 14:25:29', 75, 82, 2, 0, 131);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:02:00', '2005-03-04 11:30:30', 81, 71, 0, 2, 132);
INSERT INTO public.partiid VALUES (47, '2010-10-14 13:01:00', '2010-10-14 13:21:17', 73, 72, 1, 1, 133);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:25:59', 76, 91, 1, 1, 134);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:25:44', 200, 155, 0, 2, 135);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:33:14', 91, 77, 2, 0, 136);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:25:27', 164, 158, 0, 2, 137);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:01:00', '2005-03-04 11:25:14', 85, 89, 1, 1, 138);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:29:10', 196, 160, 1, 1, 139);
INSERT INTO public.partiid VALUES (44, '2007-09-01 08:02:00', '2007-09-01 08:28:03', 195, 172, 1, 1, 140);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:35:36', 172, 78, 0, 2, 141);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:27:31', 167, 77, 2, 0, 142);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:02:00', '2007-09-01 16:25:41', 186, 82, 0, 2, 143);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:23:35', 191, 71, 1, 1, 144);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:20:20', 159, 148, 1, 1, 145);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:21:05', 153, 84, 2, 0, 146);
INSERT INTO public.partiid VALUES (44, '2007-09-01 13:01:00', '2007-09-01 13:23:54', 197, 90, 2, 0, 147);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:21:29', 172, 71, 0, 2, 148);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:02:00', '2005-03-04 11:22:12', 88, 81, 2, 0, 149);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:31:59', 157, 92, 0, 2, 150);
INSERT INTO public.partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:18:10', 194, 80, 2, 0, 151);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:24:39', 157, 72, 0, 2, 152);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:03:00', '2005-03-04 12:26:21', 83, 79, 1, 1, 153);
INSERT INTO public.partiid VALUES (43, '2006-06-04 15:01:00', '2006-06-04 15:32:38', 197, 176, 2, 0, 154);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:26:22', 190, 77, 1, 1, 155);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:24:23', 173, 171, 0, 2, 156);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:35:18', 80, 82, 0, 2, 157);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:19:09', 175, 84, 1, 1, 158);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:32:10', 165, 72, 2, 0, 159);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:33:28', 78, 75, 0, 2, 160);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:01:00', '2005-03-04 14:36:27', 86, 79, 1, 1, 161);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:22:25', 159, 153, 1, 1, 162);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:05:00', '2005-03-04 17:27:42', 92, 83, 1, 1, 163);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:14:51', 152, 81, 1, 1, 164);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:14:20', 91, 83, 2, 0, 165);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:02:00', '2007-09-01 12:20:01', 200, 173, 0, 2, 166);
INSERT INTO public.partiid VALUES (41, '2005-01-12 08:04:00', '2005-01-12 08:35:35', 77, 87, 2, 0, 167);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:16:48', 186, 81, 2, 0, 168);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:01:00', '2006-06-04 16:26:22', 200, 76, 1, 1, 169);
INSERT INTO public.partiid VALUES (47, '2010-10-14 09:04:00', '2010-10-14 09:23:35', 85, 83, 0, 2, 170);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:32:00', 171, 164, 0, 2, 171);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:37:03', 173, 94, 1, 1, 172);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:25:33', 150, 93, 0, 2, 173);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:01:00', '2006-06-04 16:29:59', 93, 72, 2, 0, 174);
INSERT INTO public.partiid VALUES (41, '2005-01-12 12:04:00', '2005-01-12 12:22:23', 73, 79, 0, 2, 175);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:25:45', 190, 93, 0, 2, 176);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:02:00', '2006-06-04 08:39:56', 198, 191, 1, 1, 177);
INSERT INTO public.partiid VALUES (47, '2010-10-14 08:03:00', '2010-10-14 08:22:14', 87, 85, 1, 1, 178);
INSERT INTO public.partiid VALUES (41, '2005-01-12 16:05:00', '2005-01-12 16:31:44', 78, 80, 1, 1, 179);
INSERT INTO public.partiid VALUES (47, '2010-10-14 16:02:00', '2010-10-14 16:26:46', 89, 79, 2, 0, 180);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:03:00', '2006-06-04 13:29:28', 89, 86, 1, 1, 181);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:17:15', 72, 74, 2, 0, 182);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:21:23', 74, 72, 1, 1, 183);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:29:58', 200, 162, 2, 0, 184);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:01:00', '2005-03-04 08:14:49', 87, 79, 0, 2, 185);
INSERT INTO public.partiid VALUES (41, '2005-01-12 13:04:00', '2005-01-12 13:29:53', 88, 80, 0, 2, 186);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:15:22', 166, 80, 1, 1, 187);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:28:28', 80, 76, 2, 0, 188);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:31:41', 161, 88, 1, 1, 189);
INSERT INTO public.partiid VALUES (41, '2005-01-12 12:09:00', '2005-01-12 12:41:36', 77, 74, 1, 1, 190);
INSERT INTO public.partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:19:05', 90, 91, 2, 0, 191);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:27:29', 91, 72, 1, 1, 192);
INSERT INTO public.partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:39:55', 169, 79, 1, 1, 193);
INSERT INTO public.partiid VALUES (47, '2010-10-14 13:05:00', '2010-10-14 13:33:30', 88, 82, 0, 2, 194);
INSERT INTO public.partiid VALUES (41, '2005-01-12 09:01:00', '2005-01-12 09:26:50', 78, 77, 2, 0, 195);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:03:00', '2005-03-04 14:17:21', 91, 84, 2, 0, 196);
INSERT INTO public.partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:26:53', 186, 87, 2, 0, 197);
INSERT INTO public.partiid VALUES (47, '2010-10-14 09:01:00', '2010-10-14 09:21:04', 90, 78, 1, 1, 198);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:02:00', '2005-03-04 13:11:41', 89, 88, 1, 1, 199);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:25:37', 155, 150, 0, 2, 200);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:02:00', '2007-09-01 12:31:31', 169, 165, 2, 0, 201);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:02:00', '2006-06-04 13:30:53', 172, 145, 1, 1, 202);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:31:05', 94, 74, 1, 1, 203);
INSERT INTO public.partiid VALUES (43, '2006-06-04 14:02:00', '2006-06-04 14:38:17', 94, 78, 0, 2, 204);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:27:37', 81, 78, 0, 2, 205);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:16:11', 71, 92, 0, 2, 206);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:02:00', '2005-03-04 17:33:51', 84, 88, 2, 0, 207);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:41:24', 190, 79, 1, 1, 208);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:17:57', 186, 148, 1, 1, 209);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:34:46', 186, 79, 2, 0, 210);
INSERT INTO public.partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:27:03', 77, 72, 1, 1, 211);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:25:01', 76, 93, 1, 1, 212);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:30:11', 174, 90, 2, 0, 213);
INSERT INTO public.partiid VALUES (43, '2006-06-04 13:02:00', '2006-06-04 13:18:42', 169, 168, 1, 1, 214);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:01:00', '2005-03-04 08:17:12', 71, 93, 0, 2, 215);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:03:00', '2007-09-01 09:32:16', 195, 74, 0, 2, 216);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:26:05', 194, 186, 0, 2, 217);
INSERT INTO public.partiid VALUES (47, '2010-10-14 17:01:00', '2010-10-14 17:25:52', 89, 85, 2, 0, 218);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:05:00', '2005-03-04 08:34:11', 85, 86, 1, 1, 219);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:30:16', 83, 74, 1, 1, 220);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:31:09', 93, 89, 0, 2, 221);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:28:56', 82, 74, 0, 2, 222);
INSERT INTO public.partiid VALUES (44, '2007-09-01 15:02:00', '2007-09-01 15:25:08', 160, 74, 1, 1, 223);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:29:53', 156, 155, 1, 1, 224);
INSERT INTO public.partiid VALUES (47, '2010-10-14 09:04:00', '2010-10-14 09:33:34', 88, 86, 0, 2, 225);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:20:47', 161, 152, 0, 2, 226);
INSERT INTO public.partiid VALUES (47, '2010-10-14 11:04:00', '2010-10-14 11:17:54', 83, 80, 2, 0, 227);
INSERT INTO public.partiid VALUES (42, '2005-03-04 11:01:00', '2005-03-04 11:34:58', 82, 78, 2, 0, 228);
INSERT INTO public.partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:28:13', 160, 72, 0, 2, 229);
INSERT INTO public.partiid VALUES (47, '2010-10-14 08:01:00', '2010-10-14 08:33:12', 90, 86, 1, 1, 230);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:21:44', 162, 80, 2, 0, 231);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:05:00', '2005-03-04 08:28:16', 85, 91, 1, 1, 232);
INSERT INTO public.partiid VALUES (47, '2010-10-14 09:06:00', '2010-10-14 09:16:42', 89, 73, 1, 1, 233);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:01:00', '2005-03-04 08:20:45', 73, 82, 1, 1, 234);
INSERT INTO public.partiid VALUES (42, '2005-03-04 15:02:00', '2005-03-04 15:25:22', 86, 74, 1, 1, 235);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:16:37', 85, 81, 0, 2, 236);
INSERT INTO public.partiid VALUES (43, '2006-06-04 16:03:00', '2006-06-04 16:23:12', 175, 80, 0, 2, 237);
INSERT INTO public.partiid VALUES (47, '2010-10-14 13:01:00', '2010-10-14 13:19:02', 90, 76, 1, 1, 238);
INSERT INTO public.partiid VALUES (41, '2005-01-12 09:03:00', '2005-01-12 09:21:57', 88, 92, 1, 1, 239);
INSERT INTO public.partiid VALUES (47, '2010-10-14 15:03:00', '2010-10-14 15:29:37', 79, 78, 0, 2, 240);
INSERT INTO public.partiid VALUES (47, '2010-10-14 10:02:00', '2010-10-14 10:39:29', 85, 77, 0, 2, 241);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:02:00', '2005-03-04 08:25:43', 92, 84, 1, 1, 242);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:21:28', 190, 83, 1, 1, 243);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:28:17', 74, 92, 0, 2, 244);
INSERT INTO public.partiid VALUES (47, '2010-10-14 16:01:00', '2010-10-14 16:28:27', 91, 82, 0, 2, 245);
INSERT INTO public.partiid VALUES (47, '2010-10-14 15:07:00', '2010-10-14 15:30:53', 86, 83, 2, 0, 246);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:04:00', '2005-03-04 14:18:37', 78, 85, 2, 0, 247);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:04:00', '2007-09-01 16:30:28', 167, 74, 2, 0, 248);
INSERT INTO public.partiid VALUES (41, '2005-01-12 17:02:00', '2005-01-12 17:14:43', 78, 79, 1, 1, 249);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:19:56', 169, 80, 1, 1, 250);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:03:00', '2005-03-04 17:19:04', 74, 79, 0, 2, 251);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:25:54', 169, 78, 1, 1, 252);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:28:16', 160, 75, 0, 2, 253);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:02:00', '2007-09-01 17:35:01', 192, 94, 0, 2, 254);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:32:52', 193, 73, 1, 1, 255);
INSERT INTO public.partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:33:44', 87, 74, 0, 2, 256);
INSERT INTO public.partiid VALUES (47, '2010-10-14 12:02:00', '2010-10-14 12:25:51', 89, 84, 2, 0, 257);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:03:00', '2006-06-04 10:37:49', 165, 161, 0, 2, 258);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:02:00', '2005-03-04 14:30:33', 89, 80, 1, 1, 259);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:25:11', 197, 149, 2, 0, 260);
INSERT INTO public.partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:24:37', 92, 78, 1, 1, 261);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:23:47', 165, 159, 0, 2, 262);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:23:08', 84, 71, 0, 2, 263);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:28:54', 188, 175, 2, 0, 264);
INSERT INTO public.partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:27:05', 162, 159, 1, 1, 265);
INSERT INTO public.partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:32:31', 191, 75, 2, 0, 266);
INSERT INTO public.partiid VALUES (47, '2010-10-14 17:01:00', '2010-10-14 17:40:04', 87, 73, 0, 2, 267);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:02:00', '2005-03-04 17:37:07', 71, 88, 0, 2, 268);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:12:26', 72, 85, 2, 0, 269);
INSERT INTO public.partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:28:51', 147, 78, 2, 0, 270);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:22:58', 71, 79, 0, 2, 271);
INSERT INTO public.partiid VALUES (42, '2005-03-04 14:01:00', '2005-03-04 14:34:55', 73, 92, 1, 1, 272);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:29:10', 85, 84, 2, 0, 273);
INSERT INTO public.partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:30:31', 89, 78, 1, 1, 274);
INSERT INTO public.partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:28:01', 197, 89, 1, 1, 275);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:02:00', '2007-09-01 14:23:37', 198, 171, 1, 1, 276);
INSERT INTO public.partiid VALUES (47, '2010-10-14 13:03:00', '2010-10-14 13:21:13', 78, 71, 0, 2, 277);
INSERT INTO public.partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:25:21', 149, 85, 1, 1, 278);
INSERT INTO public.partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:21:49', 73, 86, 1, 1, 279);
INSERT INTO public.partiid VALUES (42, '2005-03-04 08:02:00', '2005-03-04 08:31:34', 89, 81, 1, 1, 280);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:23:30', 192, 173, 1, 1, 281);
INSERT INTO public.partiid VALUES (41, '2005-01-12 14:05:00', '2005-01-12 14:31:47', 78, 75, 0, 2, 282);
INSERT INTO public.partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:33:38', 157, 78, 1, 1, 283);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:17:57', 93, 77, 0, 2, 284);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:27:38', 170, 153, 2, 0, 285);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:18:16', 191, 170, 0, 2, 286);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:22:31', 86, 71, 2, 0, 287);
INSERT INTO public.partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:25:09', 201, 169, 1, 1, 288);
INSERT INTO public.partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:21:26', 193, 157, 2, 0, 289);
INSERT INTO public.partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:27:17', 168, 155, 0, 2, 290);
INSERT INTO public.partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:21:21', 192, 156, 0, 2, 291);
INSERT INTO public.partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:21:39', 174, 168, 0, 2, 292);
INSERT INTO public.partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:38:35', 194, 147, 2, 0, 293);
INSERT INTO public.partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:23:51', 82, 77, 1, 1, 294);
INSERT INTO public.partiid VALUES (42, '2005-03-04 16:03:00', '2005-03-04 16:17:55', 93, 75, 0, 2, 295);
INSERT INTO public.partiid VALUES (47, '2010-10-14 11:02:00', '2010-10-14 11:26:28', 82, 71, 2, 0, 296);
INSERT INTO public.partiid VALUES (44, '2007-09-01 08:01:00', '2007-09-01 08:32:47', 162, 90, 0, 2, 297);
INSERT INTO public.partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:22:34', 198, 168, 1, 1, 298);
INSERT INTO public.partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:30:53', 76, 85, 1, 1, 299);


--
-- Data for Name: turniirid; Type: TABLE DATA; Schema: public; Owner: karelpaan
--

INSERT INTO public.turniirid VALUES (41, 'Kolme klubi kohtumine', 'Kambja', '2005-01-12', '2005-01-12');
INSERT INTO public.turniirid VALUES (42, 'Tartu lahtised meistrivőistlused 2005', 'Tartu', '2005-03-04', '2005-03-17');
INSERT INTO public.turniirid VALUES (47, 'Plekkkarikas 2010', 'Elva', '2010-10-14', '2010-10-14');
INSERT INTO public.turniirid VALUES (43, 'Viljandi lahtised meistrivőistlused 2006', 'Viiratsi', '2006-06-04', '2006-06-04');
INSERT INTO public.turniirid VALUES (44, 'Eesti meistrivőistlused 2007', 'Tallinn', '2007-09-01', '2007-09-01');


--
-- Name: isikud_id_seq; Type: SEQUENCE SET; Schema: public; Owner: karelpaan
--

SELECT pg_catalog.setval('public.isikud_id_seq', 19, true);


--
-- Name: klubid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: karelpaan
--

SELECT pg_catalog.setval('public.klubid_id_seq', 4, true);


--
-- Name: partiid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: karelpaan
--

SELECT pg_catalog.setval('public.partiid_id_seq', 299, true);


--
-- Name: turniirid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: karelpaan
--

SELECT pg_catalog.setval('public.turniirid_id_seq', 1, false);


--
-- Name: isikud isikud_pk; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.isikud
    ADD CONSTRAINT isikud_pk PRIMARY KEY (id);


--
-- Name: klubid klubid_nimi_key; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.klubid
    ADD CONSTRAINT klubid_nimi_key UNIQUE (nimi);


--
-- Name: klubid klubid_pk; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.klubid
    ADD CONSTRAINT klubid_pk PRIMARY KEY (id);


--
-- Name: isikud nimi_unique; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.isikud
    ADD CONSTRAINT nimi_unique UNIQUE (eesnimi, perenimi);


--
-- Name: partiid partiid_pk; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.partiid
    ADD CONSTRAINT partiid_pk PRIMARY KEY (id);


--
-- Name: turniirid turniirid_nimi_key; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.turniirid
    ADD CONSTRAINT turniirid_nimi_key UNIQUE (nimi);


--
-- Name: turniirid turniirid_pk; Type: CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.turniirid
    ADD CONSTRAINT turniirid_pk PRIMARY KEY (id);


--
-- Name: isikud fk_isikud2klubid; Type: FK CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.isikud
    ADD CONSTRAINT fk_isikud2klubid FOREIGN KEY (klubis) REFERENCES public.klubid(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: partiid fk_partiid2must; Type: FK CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.partiid
    ADD CONSTRAINT fk_partiid2must FOREIGN KEY (must) REFERENCES public.isikud(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: partiid fk_partiid2turniirid; Type: FK CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.partiid
    ADD CONSTRAINT fk_partiid2turniirid FOREIGN KEY (turniir) REFERENCES public.turniirid(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: partiid fk_partiid2valge; Type: FK CONSTRAINT; Schema: public; Owner: karelpaan
--

ALTER TABLE ONLY public.partiid
    ADD CONSTRAINT fk_partiid2valge FOREIGN KEY (valge) REFERENCES public.isikud(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

