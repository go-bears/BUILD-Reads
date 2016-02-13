--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
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
-- Name: badges; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE badges (
    badge_id integer NOT NULL,
    description character varying(50),
    image_url character varying(150)
);


ALTER TABLE public.badges OWNER TO "user";

--
-- Name: badges_badge_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE badges_badge_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.badges_badge_id_seq OWNER TO "user";

--
-- Name: badges_badge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE badges_badge_id_seq OWNED BY badges.badge_id;


--
-- Name: book_rating; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE book_rating (
    "BookRating" integer NOT NULL,
    book_id integer NOT NULL,
    rating_id integer NOT NULL
);


ALTER TABLE public.book_rating OWNER TO "user";

--
-- Name: book_rating_BookRating_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE "book_rating_BookRating_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."book_rating_BookRating_seq" OWNER TO "user";

--
-- Name: book_rating_BookRating_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE "book_rating_BookRating_seq" OWNED BY book_rating."BookRating";


--
-- Name: books; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE books (
    book_id integer NOT NULL,
    title character varying(150) NOT NULL,
    description character varying(500),
    isbn character varying(150),
    image_url character varying(150),
    book_type character varying(10)
);


ALTER TABLE public.books OWNER TO "user";

--
-- Name: books_book_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE books_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.books_book_id_seq OWNER TO "user";

--
-- Name: books_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE books_book_id_seq OWNED BY books.book_id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE ratings (
    rating_id integer NOT NULL,
    comment character varying(350),
    user_id integer NOT NULL,
    book_id integer NOT NULL
);


ALTER TABLE public.ratings OWNER TO "user";

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE ratings_rating_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ratings_rating_id_seq OWNER TO "user";

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE ratings_rating_id_seq OWNED BY ratings.rating_id;


--
-- Name: reading_sessions; Type: TABLE; Schema: public; Owner: user; Tablespace: 
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


ALTER TABLE public.reading_sessions OWNER TO "user";

--
-- Name: reading_sessions_session_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE reading_sessions_session_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reading_sessions_session_id_seq OWNER TO "user";

--
-- Name: reading_sessions_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE reading_sessions_session_id_seq OWNED BY reading_sessions.session_id;


--
-- Name: sidekicks; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE sidekicks (
    sidekick_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    password character varying(25),
    user_id integer
);


ALTER TABLE public.sidekicks OWNER TO "user";

--
-- Name: sidekicks_sidekick_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE sidekicks_sidekick_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sidekicks_sidekick_id_seq OWNER TO "user";

--
-- Name: sidekicks_sidekick_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE sidekicks_sidekick_id_seq OWNED BY sidekicks.sidekick_id;


--
-- Name: site_rating; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE site_rating (
    "SiteRating" integer NOT NULL,
    site_id integer NOT NULL,
    rating_id integer NOT NULL
);


ALTER TABLE public.site_rating OWNER TO "user";

--
-- Name: site_rating_SiteRating_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE "site_rating_SiteRating_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."site_rating_SiteRating_seq" OWNER TO "user";

--
-- Name: site_rating_SiteRating_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE "site_rating_SiteRating_seq" OWNED BY site_rating."SiteRating";


--
-- Name: sites; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE sites (
    site_id integer NOT NULL,
    name character varying(50),
    location character varying(50)
);


ALTER TABLE public.sites OWNER TO "user";

--
-- Name: sites_site_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE sites_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sites_site_id_seq OWNER TO "user";

--
-- Name: sites_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE sites_site_id_seq OWNED BY sites.site_id;


--
-- Name: user_badge; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE user_badge (
    "UserBadge" integer NOT NULL
);


ALTER TABLE public.user_badge OWNER TO "user";

--
-- Name: user_badge_UserBadge_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE "user_badge_UserBadge_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."user_badge_UserBadge_seq" OWNER TO "user";

--
-- Name: user_badge_UserBadge_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE "user_badge_UserBadge_seq" OWNED BY user_badge."UserBadge";


--
-- Name: users; Type: TABLE; Schema: public; Owner: user; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    birthday date,
    grade integer,
    password character varying(25)
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: badge_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY badges ALTER COLUMN badge_id SET DEFAULT nextval('badges_badge_id_seq'::regclass);


--
-- Name: BookRating; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY book_rating ALTER COLUMN "BookRating" SET DEFAULT nextval('"book_rating_BookRating_seq"'::regclass);


--
-- Name: book_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY books ALTER COLUMN book_id SET DEFAULT nextval('books_book_id_seq'::regclass);


--
-- Name: rating_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY ratings ALTER COLUMN rating_id SET DEFAULT nextval('ratings_rating_id_seq'::regclass);


--
-- Name: session_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY reading_sessions ALTER COLUMN session_id SET DEFAULT nextval('reading_sessions_session_id_seq'::regclass);


--
-- Name: sidekick_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY sidekicks ALTER COLUMN sidekick_id SET DEFAULT nextval('sidekicks_sidekick_id_seq'::regclass);


--
-- Name: SiteRating; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY site_rating ALTER COLUMN "SiteRating" SET DEFAULT nextval('"site_rating_SiteRating_seq"'::regclass);


--
-- Name: site_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY sites ALTER COLUMN site_id SET DEFAULT nextval('sites_site_id_seq'::regclass);


--
-- Name: UserBadge; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY user_badge ALTER COLUMN "UserBadge" SET DEFAULT nextval('"user_badge_UserBadge_seq"'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: badges; Type: TABLE DATA; Schema: public; Owner: user
--

COPY badges (badge_id, description, image_url) FROM stdin;
1	You read for 20 min! Congrats!	\N
\.


--
-- Name: badges_badge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('badges_badge_id_seq', 1, true);


--
-- Data for Name: book_rating; Type: TABLE DATA; Schema: public; Owner: user
--

COPY book_rating ("BookRating", book_id, rating_id) FROM stdin;
\.


--
-- Name: book_rating_BookRating_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('"book_rating_BookRating_seq"', 1, false);


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: user
--

COPY books (book_id, title, description, isbn, image_url, book_type) FROM stdin;
1	stuart little	mouse gets car	09090909	wwww.ack.com	c
\.


--
-- Name: books_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('books_book_id_seq', 1, false);


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: user
--

COPY ratings (rating_id, comment, user_id, book_id) FROM stdin;
1	sad chapter	1	1
\.


--
-- Name: ratings_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('ratings_rating_id_seq', 4, true);


--
-- Data for Name: reading_sessions; Type: TABLE DATA; Schema: public; Owner: user
--

COPY reading_sessions (session_id, date, time_length, badges_awarded, rating_score, user_id, book_id, sidekick_id) FROM stdin;
1	\N	20	\N	4	\N	\N	\N
2	\N	20	\N	4	\N	\N	\N
3	\N	20	\N	4	\N	\N	\N
4	\N	20	\N	4	\N	\N	\N
\.


--
-- Name: reading_sessions_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('reading_sessions_session_id_seq', 4, true);


--
-- Data for Name: sidekicks; Type: TABLE DATA; Schema: public; Owner: user
--

COPY sidekicks (sidekick_id, first_name, last_name, password, user_id) FROM stdin;
1	melissa	F	\N	\N
\.


--
-- Name: sidekicks_sidekick_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('sidekicks_sidekick_id_seq', 1, true);


--
-- Data for Name: site_rating; Type: TABLE DATA; Schema: public; Owner: user
--

COPY site_rating ("SiteRating", site_id, rating_id) FROM stdin;
\.


--
-- Name: site_rating_SiteRating_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('"site_rating_SiteRating_seq"', 1, false);


--
-- Data for Name: sites; Type: TABLE DATA; Schema: public; Owner: user
--

COPY sites (site_id, name, location) FROM stdin;
1	berkeley arts magnet	berkeley
\.


--
-- Name: sites_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('sites_site_id_seq', 1, false);


--
-- Data for Name: user_badge; Type: TABLE DATA; Schema: public; Owner: user
--

COPY user_badge ("UserBadge") FROM stdin;
\.


--
-- Name: user_badge_UserBadge_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('"user_badge_UserBadge_seq"', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY users (user_id, first_name, last_name, birthday, grade, password) FROM stdin;
1	meggie	mittens	2004-01-01	\N	\N
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('users_user_id_seq', 1, true);


--
-- Name: badges_image_url_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY badges
    ADD CONSTRAINT badges_image_url_key UNIQUE (image_url);


--
-- Name: badges_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY badges
    ADD CONSTRAINT badges_pkey PRIMARY KEY (badge_id);


--
-- Name: book_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY book_rating
    ADD CONSTRAINT book_rating_pkey PRIMARY KEY ("BookRating");


--
-- Name: books_image_url_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY books
    ADD CONSTRAINT books_image_url_key UNIQUE (image_url);


--
-- Name: books_isbn_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY books
    ADD CONSTRAINT books_isbn_key UNIQUE (isbn);


--
-- Name: books_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY books
    ADD CONSTRAINT books_pkey PRIMARY KEY (book_id);


--
-- Name: ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (rating_id);


--
-- Name: reading_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_pkey PRIMARY KEY (session_id);


--
-- Name: sidekicks_password_key; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY sidekicks
    ADD CONSTRAINT sidekicks_password_key UNIQUE (password);


--
-- Name: sidekicks_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY sidekicks
    ADD CONSTRAINT sidekicks_pkey PRIMARY KEY (sidekick_id);


--
-- Name: site_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY site_rating
    ADD CONSTRAINT site_rating_pkey PRIMARY KEY ("SiteRating");


--
-- Name: sites_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (site_id);


--
-- Name: user_badge_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY user_badge
    ADD CONSTRAINT user_badge_pkey PRIMARY KEY ("UserBadge");


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: user; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: book_rating_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY book_rating
    ADD CONSTRAINT book_rating_book_id_fkey FOREIGN KEY (book_id) REFERENCES books(book_id);


--
-- Name: book_rating_rating_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY book_rating
    ADD CONSTRAINT book_rating_rating_id_fkey FOREIGN KEY (rating_id) REFERENCES ratings(rating_id);


--
-- Name: ratings_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_book_id_fkey FOREIGN KEY (book_id) REFERENCES books(book_id);


--
-- Name: ratings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY ratings
    ADD CONSTRAINT ratings_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: reading_sessions_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_book_id_fkey FOREIGN KEY (book_id) REFERENCES books(book_id);


--
-- Name: reading_sessions_sidekick_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_sidekick_id_fkey FOREIGN KEY (sidekick_id) REFERENCES sidekicks(sidekick_id);


--
-- Name: reading_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY reading_sessions
    ADD CONSTRAINT reading_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: sidekicks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY sidekicks
    ADD CONSTRAINT sidekicks_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: site_rating_rating_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY site_rating
    ADD CONSTRAINT site_rating_rating_id_fkey FOREIGN KEY (rating_id) REFERENCES ratings(rating_id);


--
-- Name: site_rating_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY site_rating
    ADD CONSTRAINT site_rating_site_id_fkey FOREIGN KEY (site_id) REFERENCES sites(site_id);


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

