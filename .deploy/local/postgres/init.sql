--
-- PostgreSQL database dump
--

-- Dumped from database version 10.9 (Ubuntu 10.9-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.9 (Ubuntu 10.9-0ubuntu0.18.04.1)

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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO task_office_user;

--
-- Name: boards; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.boards (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    meta json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(80) NOT NULL,
    description character varying(255),
    owner_uuid uuid NOT NULL,
    is_active boolean
);


ALTER TABLE public.boards OWNER TO task_office_user;

--
-- Name: boards_id_seq; Type: SEQUENCE; Schema: public; Owner: task_office_user
--

CREATE SEQUENCE public.boards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boards_id_seq OWNER TO task_office_user;

--
-- Name: boards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: task_office_user
--

ALTER SEQUENCE public.boards_id_seq OWNED BY public.boards.id;


--
-- Name: columns; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.columns (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    meta json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(120) NOT NULL,
    "position" integer,
    board_uuid uuid NOT NULL
);


ALTER TABLE public.columns OWNER TO task_office_user;

--
-- Name: columns_id_seq; Type: SEQUENCE; Schema: public; Owner: task_office_user
--

CREATE SEQUENCE public.columns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.columns_id_seq OWNER TO task_office_user;

--
-- Name: columns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: task_office_user
--

ALTER SEQUENCE public.columns_id_seq OWNED BY public.columns.id;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    meta json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    role integer,
    user_uuid uuid NOT NULL,
    board_uuid uuid NOT NULL
);


ALTER TABLE public.permissions OWNER TO task_office_user;

--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: task_office_user
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_id_seq OWNER TO task_office_user;

--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: task_office_user
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    meta json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    expire_at timestamp without time zone,
    label character varying(80),
    name character varying(120) NOT NULL,
    description character varying(120) NOT NULL,
    state integer,
    "position" integer,
    column_uuid uuid NOT NULL,
    creator_uuid uuid NOT NULL
);


ALTER TABLE public.tasks OWNER TO task_office_user;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: task_office_user
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO task_office_user;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: task_office_user
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    meta json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(255) NOT NULL,
    bio character varying(300),
    phone character varying(300),
    password bytea,
    is_active boolean,
    is_superuser boolean
);


ALTER TABLE public.users OWNER TO task_office_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: task_office_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO task_office_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: task_office_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_tasks; Type: TABLE; Schema: public; Owner: task_office_user
--

CREATE TABLE public.users_tasks (
    task_uuid uuid NOT NULL,
    user_uuid uuid NOT NULL
);


ALTER TABLE public.users_tasks OWNER TO task_office_user;

--
-- Name: boards id; Type: DEFAULT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.boards ALTER COLUMN id SET DEFAULT nextval('public.boards_id_seq'::regclass);


--
-- Name: columns id; Type: DEFAULT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.columns ALTER COLUMN id SET DEFAULT nextval('public.columns_id_seq'::regclass);


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.alembic_version (version_num) FROM stdin;
d99344769ddd
\.


--
-- Data for Name: boards; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.boards (id, uuid, meta, created_at, updated_at, name, description, owner_uuid, is_active) FROM stdin;
1	74cb6568-2c5c-437b-a8e5-a226443f220c	{}	2020-04-04 19:37:13.167729	2020-04-04 19:37:13.167734	Board #1 name	Board #1 description	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	t
2	f46f0533-f94b-40ab-aa4d-286bb433d79d	{}	2020-04-04 19:37:24.722797	2020-04-04 19:37:24.722803	Board #2 name	Board #2 description	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	t
3	3dd6f7b8-d72a-4da8-a94f-5f665577c2bb	{}	2020-04-04 19:37:33.883561	2020-04-04 19:37:33.883567	Board #3 name	Board #3 description	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	t
\.


--
-- Data for Name: columns; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.columns (id, uuid, meta, created_at, updated_at, name, "position", board_uuid) FROM stdin;
4	4223251e-6a4d-4be5-a4db-632381dcc18e	{}	2020-04-04 19:42:45.543069	2020-04-04 19:42:45.543076	High priority	1	74cb6568-2c5c-437b-a8e5-a226443f220c
1	09a57486-cb0f-4981-bbfe-880161810aee	{}	2020-04-04 19:40:47.659333	2020-04-04 19:42:45.553613	Done	4	74cb6568-2c5c-437b-a8e5-a226443f220c
3	e55ff02a-ca1b-4f17-998c-b606e5c295b4	{}	2020-04-04 19:42:35.497317	2020-04-04 19:42:45.553613	Low priority	2	74cb6568-2c5c-437b-a8e5-a226443f220c
2	a793e93e-ed03-47f5-995c-cf13dada93c0	{}	2020-04-04 19:41:18.115626	2020-04-04 19:42:45.553613	Rejected tasks	3	74cb6568-2c5c-437b-a8e5-a226443f220c
6	74a9c56e-c44b-4d1d-bb9c-378c3e580d2c	{}	2020-04-04 19:47:28.867338	2020-04-04 19:47:28.867344	Column name2	1	f46f0533-f94b-40ab-aa4d-286bb433d79d
5	e806769c-746a-40d2-8666-f970acac1455	{}	2020-04-04 19:47:23.347919	2020-04-04 19:47:28.874041	Column name1	2	f46f0533-f94b-40ab-aa4d-286bb433d79d
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.permissions (id, uuid, meta, created_at, updated_at, role, user_uuid, board_uuid) FROM stdin;
1	5220680b-33d4-4973-b35a-576a98ef5a88	{}	2020-04-04 19:37:13.177124	2020-04-04 19:37:13.17713	1	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	74cb6568-2c5c-437b-a8e5-a226443f220c
2	46ee1a2b-4500-4c74-a7a7-2a4ec4884778	{}	2020-04-04 19:37:24.72541	2020-04-04 19:37:24.725415	1	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	f46f0533-f94b-40ab-aa4d-286bb433d79d
3	bdc8b9fc-ecca-4101-8baf-8682883b8eb4	{}	2020-04-04 19:37:33.886127	2020-04-04 19:37:33.886132	1	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	3dd6f7b8-d72a-4da8-a94f-5f665577c2bb
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.tasks (id, uuid, meta, created_at, updated_at, expire_at, label, name, description, state, "position", column_uuid, creator_uuid) FROM stdin;
2	61fdc381-9c8b-46b7-9e98-dd04ecbf1103	{}	2020-04-04 19:46:03.883278	2020-04-04 19:46:03.883284	2020-05-25 05:30:11	Label1	Task #2 name	Task #2 description	1	1	4223251e-6a4d-4be5-a4db-632381dcc18e	2ce70298-e3d9-47aa-a58e-ce55d9c351fd
1	89771883-849f-4aef-930c-285f0131ae56	{}	2020-04-04 19:44:47.12337	2020-04-04 19:46:03.887337	2020-05-25 05:30:11	Label1	Task #1 name	Task #1 description	1	2	4223251e-6a4d-4be5-a4db-632381dcc18e	2ce70298-e3d9-47aa-a58e-ce55d9c351fd
3	a4a9594b-7b12-4b9c-b892-d48d666f711c	{}	2020-04-04 19:49:44.812372	2020-04-04 19:49:44.812383	2021-05-25 05:30:11	Label1	Task ##2 name	Task ##2 description	1	1	74a9c56e-c44b-4d1d-bb9c-378c3e580d2c	2ce70298-e3d9-47aa-a58e-ce55d9c351fd
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.users (id, uuid, meta, created_at, updated_at, username, email, bio, phone, password, is_active, is_superuser) FROM stdin;
1	2ce70298-e3d9-47aa-a58e-ce55d9c351fd	{}	2020-04-04 19:35:33.864782	2020-04-04 19:35:33.86479	Amigo	amigo@gmaill.com	\N	\N	\\x243262243132246741684f36616f4a744d7350364d745737426d43637557616477596d3837617578447a31354e7a4c36653856356953595961683853	t	f
2	df362410-c706-4ad8-9009-98eee9ff4a82	{}	2020-04-04 19:36:14.527745	2020-04-04 19:36:14.527751	Sergio	sergio@gmaill.com	\N	\N	\\x2432622431322443423036463073594363497750682e7354323641766542664852414f6e58594a4d623837326a594b305364374151315576456b4c6d	t	f
\.


--
-- Data for Name: users_tasks; Type: TABLE DATA; Schema: public; Owner: task_office_user
--

COPY public.users_tasks (task_uuid, user_uuid) FROM stdin;
61fdc381-9c8b-46b7-9e98-dd04ecbf1103	df362410-c706-4ad8-9009-98eee9ff4a82
a4a9594b-7b12-4b9c-b892-d48d666f711c	2ce70298-e3d9-47aa-a58e-ce55d9c351fd
a4a9594b-7b12-4b9c-b892-d48d666f711c	df362410-c706-4ad8-9009-98eee9ff4a82
\.


--
-- Name: boards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: task_office_user
--

SELECT pg_catalog.setval('public.boards_id_seq', 3, true);


--
-- Name: columns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: task_office_user
--

SELECT pg_catalog.setval('public.columns_id_seq', 6, true);


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: task_office_user
--

SELECT pg_catalog.setval('public.permissions_id_seq', 3, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: task_office_user
--

SELECT pg_catalog.setval('public.tasks_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: task_office_user
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: boards boards_pkey; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.boards
    ADD CONSTRAINT boards_pkey PRIMARY KEY (id, uuid);


--
-- Name: boards boards_uuid_key; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.boards
    ADD CONSTRAINT boards_uuid_key UNIQUE (uuid);


--
-- Name: columns columns_pkey; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT columns_pkey PRIMARY KEY (id, uuid);


--
-- Name: columns columns_uuid_key; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT columns_uuid_key UNIQUE (uuid);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id, uuid);


--
-- Name: permissions permissions_uuid_key; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_uuid_key UNIQUE (uuid);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id, uuid);


--
-- Name: tasks tasks_uuid_key; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_uuid_key UNIQUE (uuid);


--
-- Name: columns unique_board__board_column_name; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT unique_board__board_column_name UNIQUE (board_uuid, name);


--
-- Name: permissions unique_board_owner_permission; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT unique_board_owner_permission UNIQUE (board_uuid, user_uuid);


--
-- Name: boards unique_name_owner_board; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.boards
    ADD CONSTRAINT unique_name_owner_board UNIQUE (name, owner_uuid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id, uuid);


--
-- Name: users_tasks users_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT users_tasks_pkey PRIMARY KEY (task_uuid, user_uuid);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: users users_uuid_key; Type: CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_uuid_key UNIQUE (uuid);


--
-- Name: ix_boards_description; Type: INDEX; Schema: public; Owner: task_office_user
--

CREATE INDEX ix_boards_description ON public.boards USING btree (description);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: task_office_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: boards boards_owner_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.boards
    ADD CONSTRAINT boards_owner_uuid_fkey FOREIGN KEY (owner_uuid) REFERENCES public.users(uuid);


--
-- Name: columns columns_board_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT columns_board_uuid_fkey FOREIGN KEY (board_uuid) REFERENCES public.boards(uuid);


--
-- Name: permissions permissions_board_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_board_uuid_fkey FOREIGN KEY (board_uuid) REFERENCES public.boards(uuid);


--
-- Name: permissions permissions_user_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_user_uuid_fkey FOREIGN KEY (user_uuid) REFERENCES public.users(uuid);


--
-- Name: tasks tasks_column_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_column_uuid_fkey FOREIGN KEY (column_uuid) REFERENCES public.columns(uuid);


--
-- Name: tasks tasks_creator_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_creator_uuid_fkey FOREIGN KEY (creator_uuid) REFERENCES public.users(uuid);


--
-- Name: users_tasks users_tasks_task_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT users_tasks_task_uuid_fkey FOREIGN KEY (task_uuid) REFERENCES public.tasks(uuid);


--
-- Name: users_tasks users_tasks_user_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: task_office_user
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT users_tasks_user_uuid_fkey FOREIGN KEY (user_uuid) REFERENCES public.users(uuid);


--
-- PostgreSQL database dump complete
--

