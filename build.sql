--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: badges; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE badges (
    badge_id integer NOT NULL,
    description character varying(50)
);


ALTER TABLE public.badges OWNER TO postgres;

--
-- Name: badges_badge_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE badges_badge_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.badges_badge_id_seq OWNER TO postgres;

--
-- Name: badges_badge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE badges_badge_id_seq OWNED BY badges.badge_id;


--
-- Name: book_rating; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE book_rating (
    "BookRating" integer NOT NULL,
    book_id integer,
    rating_id integer
);


ALTER TABLE public.book_rating OWNER TO postgres;

--
-- Name: book_rating_BookRating_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "book_rating_BookRating_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."book_rating_BookRating_seq" OWNER TO postgres;

--
-- Name: book_rating_BookRating_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "book_rating_BookRating_seq" OWNED BY book_rating."BookRating";


--
-- Name: books; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE books (
    book_id integer NOT NULL,
    title character varying(150),
    description character varying(500),
    isbn character varying(150),
    image_url character varying(150),
    book_type character varying(10)
);


ALTER TABLE public.books OWNER TO postgres;

--
-- Name: books_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE books_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.books_book_id_seq OWNER TO postgres;

--
-- Name: books_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE books_book_id_seq OWNED BY books.book_id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE ratings (
    rating_id integer NOT NULL,
    comment character varying(350),
    user_id integer,
    book_id integer,
    session_id integer
);


ALTER TABLE public.ratings OWNER TO postgres;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ratings_rating_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ratings_rating_id_seq OWNER TO postgres;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ratings_rating_id_seq OWNED BY ratings.rating_id;


--
-- Name: reading_sessions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE reading_sessions (
    session_id integer NOT NULL,
    date timestamp without time zone,
    time_length integer,
    badges_awarded integer,
    rating_score integer,
    user_id integer,
    book_id integer,
    sidekick_id integer
);


ALTER TABLE public.reading_sessions OWNER TO postgres;

--
-- Name: reading_sessions_session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE reading_sessions_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reading_sessions_session_id_seq OWNER TO postgres;

--
-- Name: reading_sessions_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE reading_sessions_session_id_seq OWNED BY reading_sessions.session_id;


--
-- Name: sidekicks; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sidekicks (
    sidekick_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    password character varying(25),
    user_id integer
);


ALTER TABLE public.sidekicks OWNER TO postgres;

--
-- Name: sidekicks_sidekick_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sidekicks_sidekick_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sidekicks_sidekick_id_seq OWNER TO postgres;

--
-- Name: sidekicks_sidekick_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sidekicks_sidekick_id_seq OWNED BY sidekicks.sidekick_id;


--
-- Name: site_rating; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE site_rating (
    "SiteRating" integer NOT NULL,
    site_id integer,
    rating_id integer
);


ALTER TABLE public.site_rating OWNER TO postgres;

--
-- Name: site_rating_SiteRating_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "site_rating_SiteRating_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."site_rating_SiteRating_seq" OWNER TO postgres;

--
-- Name: site_rating_SiteRating_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "site_rating_SiteRating_seq" OWNED BY site_rating."SiteRating";


--
-- Name: sites; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sites (
    site_id integer NOT NULL,
    name character varying(50),
    location character varying(50)
);


ALTER TABLE public.sites OWNER TO postgres;

--
-- Name: sites_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sites_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sites_site_id_seq OWNER TO postgres;

--
-- Name: sites_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sites_site_id_seq OWNED BY sites.site_id;


--
-- Name: user_badge; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE user_badge (
    "UserBadge" integer NOT NULL,
    user_id integer
);


ALTER TABLE public.user_badge OWNER TO postgres;

--
-- Name: user_badge_UserBadge_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "user_badge_UserBadge_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."user_badge_UserBadge_seq" OWNER TO postgres;

--
-- Name: user_badge_UserBadge_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE "user_badge_UserBadge_seq" OWNED BY user_badge."UserBadge";


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    birthday date,
    grade integer,
    password character varying(25),
    site_id integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: badge_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY badges ALTER COLUMN badge_id SET DEFAULT nextval('badges_badge_id_seq'::regclass);


--
-- Name: BookRating; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_rating ALTER COLUMN "BookRating" SET DEFAULT nextval('"book_rating_BookRating_seq"'::regclass);


--
-- Name: book_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY books ALTER COLUMN book_id SET DEFAULT nextval('books_book_id_seq'::regclass);


--
-- Name: rating_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings ALTER COLUMN rating_id SET DEFAULT nextval('ratings_rating_id_seq'::regclass);


--
-- Name: session_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY reading_sessions ALTER COLUMN session_id SET DEFAULT nextval('reading_sessions_session_id_seq'::regclass);


--
-- Name: sidekick_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sidekicks ALTER COLUMN sidekick_id SET DEFAULT nextval('sidekicks_sidekick_id_seq'::regclass);


--
-- Name: SiteRating; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY site_rating ALTER COLUMN "SiteRating" SET DEFAULT nextval('"site_rating_SiteRating_seq"'::regclass);


--
-- Name: site_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sites ALTER COLUMN site_id SET DEFAULT nextval('sites_site_id_seq'::regclass);


--
-- Name: UserBadge; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_badge ALTER COLUMN "UserBadge" SET DEFAULT nextval('"user_badge_UserBadge_seq"'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: badges; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY badges (badge_id, description) FROM stdin;
1	'you earned a badge for reading 20min!'
2	'you earned a badge for reading 40min!'
3	'you earned a badge for reading 60min!'
\.


--
-- Name: badges_badge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('badges_badge_id_seq', 1, false);


--
-- Data for Name: book_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY book_rating ("BookRating", book_id, rating_id) FROM stdin;
\.


--
-- Name: book_rating_BookRating_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"book_rating_BookRating_seq"', 1, false);


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY books (book_id, title, description, isbn, image_url, book_type) FROM stdin;
1	Stuart Little	mouse and car	64410927	www.bookpix1.com	c
2	Charlotte's web	girl and pig	64400557	www.bookpix2.com	c
3	Harry Potter and the Sorcerer's Stone	boy and owl	1781100489	www.bookpix.com3	c
4	Richard Scarry's Best Little Board Book Ever	talking animals	449819019	www.bookpix.com4	p
5	Little Miss Litterbug	don't litter	1438925190	www.bookpix.com5	p
6	Little Miss Splendid	happy happy	698177266	www.bookpix.com6	p
\.


--
-- Name: books_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('books_book_id_seq', 1, false);


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY ratings (rating_id, comment, user_id, book_id, session_id) FROM stdin;
1	"good story!"	1	1	1
2	"love wilbur"	2	2	2
\.


--
-- Name: ratings_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('ratings_rating_id_seq', 1, false);


--
-- Data for Name: reading_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY reading_sessions (session_id, date, time_length, badges_awarded, rating_score, user_id, book_id, sidekick_id) FROM stdin;
1	2014-01-01 00:00:00	30	2	5	1	1	1
2	2014-01-02 00:00:00	15	1	5	2	3	2
3	2014-01-03 00:00:00	40	3	5	3	2	3
5	2016-02-17 07:22:53.594531	20	1	5	16	1	1
7	2016-02-17 00:00:00	20	1	5	16	1	1
9	2016-02-17 00:00:00	20	1	5	8	1	6
11	2016-02-17 00:00:00	20	1	5	18	5	1
\.


--
-- Name: reading_sessions_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('reading_sessions_session_id_seq', 11, true);


--
-- Data for Name: sidekicks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sidekicks (sidekick_id, first_name, last_name, password, user_id) FROM stdin;
1	victoria	cendejas	password	1
2	melissa	f	password	2
3	elizabeth	o	password	3
4	matt	m	password	4
6	Preeti	Purry	password	\N
\.


--
-- Name: sidekicks_sidekick_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sidekicks_sidekick_id_seq', 6, true);


--
-- Data for Name: site_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY site_rating ("SiteRating", site_id, rating_id) FROM stdin;
\.


--
-- Name: site_rating_SiteRating_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"site_rating_SiteRating_seq"', 1, false);


--
-- Data for Name: sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sites (site_id, name, location) FROM stdin;
1	Berkeley Arts Magnet	Berkeley
2	Cragmont Elementary	Berkeley
3	Emerson Elementary, Berkeley	Berkeley
4	Jefferson Elementary	Berkeley
5	John Muir Elementary	Berkeley
6	LeConte Elementary School	Berkeley
7	Malcolm X Elementary School	Berkeley
8	Oxford Elementary	Berkeley
9	Rosa Parks 	Berkeley
10	Thousand Oaks	Berkeley
11	Washington Elementary	Berkeley
12	Bahia School Age Program	Berkeley
13	Berkeley Maynard Academy	Berkeley
14	Berkeley Youth Alternatives	Berkeley
15	Emerson Elementary	Oakland
16	Lafayette Elementary	Oakland
17	Think College Now	Oakland
18	James Kenney Recreation Center	Berkeley
19	Martin Luther King, Jr. Elementary School	Oakland
20	Sankofa	Oakland
21	Young Adult Project	Berkeley
\.


--
-- Name: sites_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sites_site_id_seq', 1, false);


--
-- Data for Name: user_badge; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY user_badge ("UserBadge", user_id) FROM stdin;
\.


--
-- Name: user_badge_UserBadge_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"user_badge_UserBadge_seq"', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (user_id, first_name, last_name, birthday, grade, password, site_id) FROM stdin;
1	daniel	tiger	2003-01-01	7	password	\N
2	meggie	mittens	2004-01-01	6	password	\N
3	lilly	kitty	2005-01-01	5	password	\N
4	auden	burton	2006-01-01	4	password	\N
5	ezra	burton	2007-01-01	3	password	\N
6	ammy	keung	2008-01-01	2	password	\N
8	emily	fluffy	2014-09-09	6	password	1
10	Russian	Blue	2005-05-05	2	password	2
12	Curly	Bishop	2000-05-21	8	password	21
14	ammy	Keung	2008-01-01	2	password	1
16	julius	tsui	2009-02-02	1	password	2
18	pumba	rahmati	2010-10-10	1	password	17
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_user_id_seq', 18, true);


--
-- Name: badges_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY badges
    ADD CONSTRAINT badges_pkey PRIMARY KEY (badge_id);


--
-- Name: book_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY book_rating
    ADD CONSTRAINT book_rating_pkey PRIMARY KEY ("BookRating");


--
-- Name: books_image_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY books
    ADD CONSTRAINT books_image_url_key UNIQUE (image_url);


--
-- Name: books_isbn_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY books
    ADD CONSTRAINT books_isbn_key UNIQUE (isbn);


--
-- Name: books_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY books
    ADD CONSTRAINT books_pkey PRIMARY KEY (book_id);


--
-- Name: ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (rating_id);


--
-- Name: reading_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_pkey PRIMARY KEY (session_id);


--
-- Name: sidekicks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sidekicks
    ADD CONSTRAINT sidekicks_pkey PRIMARY KEY (sidekick_id);


--
-- Name: site_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY site_rating
    ADD CONSTRAINT site_rating_pkey PRIMARY KEY ("SiteRating");


--
-- Name: sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (site_id);


--
-- Name: user_badge_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY user_badge
    ADD CONSTRAINT user_badge_pkey PRIMARY KEY ("UserBadge");


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: book_rating_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_rating
    ADD CONSTRAINT book_rating_book_id_fkey FOREIGN KEY (book_id) REFERENCES books(book_id);


--
-- Name: book_rating_rating_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_rating
    ADD CONSTRAINT book_rating_rating_id_fkey FOREIGN KEY (rating_id) REFERENCES ratings(rating_id);


--
-- Name: ratings_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_book_id_fkey FOREIGN KEY (book_id) REFERENCES books(book_id);


--
-- Name: ratings_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_session_id_fkey FOREIGN KEY (session_id) REFERENCES reading_sessions(session_id);


--
-- Name: ratings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: reading_sessions_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_book_id_fkey FOREIGN KEY (book_id) REFERENCES books(book_id);


--
-- Name: reading_sessions_sidekick_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_sidekick_id_fkey FOREIGN KEY (sidekick_id) REFERENCES sidekicks(sidekick_id);


--
-- Name: reading_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: sidekicks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sidekicks
    ADD CONSTRAINT sidekicks_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: site_rating_rating_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY site_rating
    ADD CONSTRAINT site_rating_rating_id_fkey FOREIGN KEY (rating_id) REFERENCES ratings(rating_id);


--
-- Name: site_rating_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY site_rating
    ADD CONSTRAINT site_rating_site_id_fkey FOREIGN KEY (site_id) REFERENCES sites(site_id);


--
-- Name: user_badge_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_badge
    ADD CONSTRAINT user_badge_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: users_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_site_id_fkey FOREIGN KEY (site_id) REFERENCES sites(site_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

