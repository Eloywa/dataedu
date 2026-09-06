--
-- PostgreSQL database dump
--

\restrict ReUPFuVPhi9n7g6WuL00QMwE4vPXQSQCKd7APtBR3ax456zQUCdzPbHjci8A6Zg

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_role_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_achievements DROP CONSTRAINT IF EXISTS user_achievements_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_achievements DROP CONSTRAINT IF EXISTS user_achievements_achievement_id_fkey;
ALTER TABLE IF EXISTS ONLY public.tests DROP CONSTRAINT IF EXISTS tests_lesson_id_fkey;
ALTER TABLE IF EXISTS ONLY public.test_attempts DROP CONSTRAINT IF EXISTS test_attempts_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.test_attempts DROP CONSTRAINT IF EXISTS test_attempts_test_id_fkey;
ALTER TABLE IF EXISTS ONLY public.submissions DROP CONSTRAINT IF EXISTS submissions_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.submissions DROP CONSTRAINT IF EXISTS submissions_graded_by_fkey;
ALTER TABLE IF EXISTS ONLY public.submissions DROP CONSTRAINT IF EXISTS submissions_assignment_id_fkey;
ALTER TABLE IF EXISTS ONLY public.reflections DROP CONSTRAINT IF EXISTS reflections_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.reflections DROP CONSTRAINT IF EXISTS reflections_lesson_id_fkey;
ALTER TABLE IF EXISTS ONLY public.questions DROP CONSTRAINT IF EXISTS questions_test_id_fkey;
ALTER TABLE IF EXISTS ONLY public.modules DROP CONSTRAINT IF EXISTS modules_course_id_fkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_sender_id_fkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_recipient_id_fkey;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_course_id_fkey;
ALTER TABLE IF EXISTS ONLY public.lessons DROP CONSTRAINT IF EXISTS lessons_module_id_fkey;
ALTER TABLE IF EXISTS ONLY public.lesson_progress DROP CONSTRAINT IF EXISTS lesson_progress_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.lesson_progress DROP CONSTRAINT IF EXISTS lesson_progress_lesson_id_fkey;
ALTER TABLE IF EXISTS ONLY public.enrollments DROP CONSTRAINT IF EXISTS enrollments_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.enrollments DROP CONSTRAINT IF EXISTS enrollments_course_id_fkey;
ALTER TABLE IF EXISTS ONLY public.courses DROP CONSTRAINT IF EXISTS courses_author_id_fkey;
ALTER TABLE IF EXISTS ONLY public.course_topics DROP CONSTRAINT IF EXISTS course_topics_topic_id_fkey;
ALTER TABLE IF EXISTS ONLY public.course_topics DROP CONSTRAINT IF EXISTS course_topics_course_id_fkey;
ALTER TABLE IF EXISTS ONLY public.course_ratings DROP CONSTRAINT IF EXISTS course_ratings_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.course_ratings DROP CONSTRAINT IF EXISTS course_ratings_course_id_fkey;
ALTER TABLE IF EXISTS ONLY public.assignments DROP CONSTRAINT IF EXISTS assignments_lesson_id_fkey;
ALTER TABLE IF EXISTS ONLY public.assignments DROP CONSTRAINT IF EXISTS assignments_course_id_fkey;
ALTER TABLE IF EXISTS ONLY public.answer_submissions DROP CONSTRAINT IF EXISTS answer_submissions_question_id_fkey;
ALTER TABLE IF EXISTS ONLY public.answer_submissions DROP CONSTRAINT IF EXISTS answer_submissions_attempt_id_fkey;
ALTER TABLE IF EXISTS ONLY public.answer_submissions DROP CONSTRAINT IF EXISTS answer_submissions_answer_option_id_fkey;
ALTER TABLE IF EXISTS ONLY public.answer_options DROP CONSTRAINT IF EXISTS answer_options_question_id_fkey;
ALTER TABLE IF EXISTS ONLY public.activities DROP CONSTRAINT IF EXISTS activities_user_id_fkey;
DROP INDEX IF EXISTS public.idx_users_role;
DROP INDEX IF EXISTS public.idx_tests_lesson;
DROP INDEX IF EXISTS public.idx_test_attempts_user;
DROP INDEX IF EXISTS public.idx_test_attempts_test;
DROP INDEX IF EXISTS public.idx_submissions_user;
DROP INDEX IF EXISTS public.idx_submissions_assignment;
DROP INDEX IF EXISTS public.idx_questions_test;
DROP INDEX IF EXISTS public.idx_modules_course;
DROP INDEX IF EXISTS public.idx_messages_recipient;
DROP INDEX IF EXISTS public.idx_messages_pair;
DROP INDEX IF EXISTS public.idx_lessons_module;
DROP INDEX IF EXISTS public.idx_lesson_progress_user;
DROP INDEX IF EXISTS public.idx_enrollments_course;
DROP INDEX IF EXISTS public.idx_assignments_course;
DROP INDEX IF EXISTS public.idx_answer_submissions_attempt;
DROP INDEX IF EXISTS public.idx_answer_options_question;
DROP INDEX IF EXISTS public.idx_activities_user_time;
DROP INDEX IF EXISTS public.idx_activities_type;
ALTER TABLE IF EXISTS ONLY sandbox.students DROP CONSTRAINT IF EXISTS students_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.user_achievements DROP CONSTRAINT IF EXISTS user_achievements_user_id_achievement_id_key;
ALTER TABLE IF EXISTS ONLY public.user_achievements DROP CONSTRAINT IF EXISTS user_achievements_pkey;
ALTER TABLE IF EXISTS ONLY public.topics DROP CONSTRAINT IF EXISTS topics_pkey;
ALTER TABLE IF EXISTS ONLY public.topics DROP CONSTRAINT IF EXISTS topics_code_key;
ALTER TABLE IF EXISTS ONLY public.tests DROP CONSTRAINT IF EXISTS tests_pkey;
ALTER TABLE IF EXISTS ONLY public.test_attempts DROP CONSTRAINT IF EXISTS test_attempts_pkey;
ALTER TABLE IF EXISTS ONLY public.submissions DROP CONSTRAINT IF EXISTS submissions_pkey;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_pkey;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_code_key;
ALTER TABLE IF EXISTS ONLY public.reflections DROP CONSTRAINT IF EXISTS reflections_user_id_lesson_id_key;
ALTER TABLE IF EXISTS ONLY public.reflections DROP CONSTRAINT IF EXISTS reflections_pkey;
ALTER TABLE IF EXISTS ONLY public.questions DROP CONSTRAINT IF EXISTS questions_pkey;
ALTER TABLE IF EXISTS ONLY public.modules DROP CONSTRAINT IF EXISTS modules_pkey;
ALTER TABLE IF EXISTS ONLY public.modules DROP CONSTRAINT IF EXISTS modules_course_id_order_index_key;
ALTER TABLE IF EXISTS ONLY public.messages DROP CONSTRAINT IF EXISTS messages_pkey;
ALTER TABLE IF EXISTS ONLY public.lessons DROP CONSTRAINT IF EXISTS lessons_pkey;
ALTER TABLE IF EXISTS ONLY public.lessons DROP CONSTRAINT IF EXISTS lessons_module_id_order_index_key;
ALTER TABLE IF EXISTS ONLY public.lesson_progress DROP CONSTRAINT IF EXISTS lesson_progress_user_id_lesson_id_key;
ALTER TABLE IF EXISTS ONLY public.lesson_progress DROP CONSTRAINT IF EXISTS lesson_progress_pkey;
ALTER TABLE IF EXISTS ONLY public.enrollments DROP CONSTRAINT IF EXISTS enrollments_user_id_course_id_key;
ALTER TABLE IF EXISTS ONLY public.enrollments DROP CONSTRAINT IF EXISTS enrollments_pkey;
ALTER TABLE IF EXISTS ONLY public.courses DROP CONSTRAINT IF EXISTS courses_slug_key;
ALTER TABLE IF EXISTS ONLY public.courses DROP CONSTRAINT IF EXISTS courses_pkey;
ALTER TABLE IF EXISTS ONLY public.course_topics DROP CONSTRAINT IF EXISTS course_topics_pkey;
ALTER TABLE IF EXISTS ONLY public.course_ratings DROP CONSTRAINT IF EXISTS course_ratings_pkey;
ALTER TABLE IF EXISTS ONLY public.course_ratings DROP CONSTRAINT IF EXISTS course_ratings_course_id_user_id_key;
ALTER TABLE IF EXISTS ONLY public.assignments DROP CONSTRAINT IF EXISTS assignments_pkey;
ALTER TABLE IF EXISTS ONLY public.answer_submissions DROP CONSTRAINT IF EXISTS answer_submissions_pkey;
ALTER TABLE IF EXISTS ONLY public.answer_options DROP CONSTRAINT IF EXISTS answer_options_pkey;
ALTER TABLE IF EXISTS ONLY public.activities DROP CONSTRAINT IF EXISTS activities_pkey;
ALTER TABLE IF EXISTS ONLY public.achievements DROP CONSTRAINT IF EXISTS achievements_pkey;
ALTER TABLE IF EXISTS ONLY public.achievements DROP CONSTRAINT IF EXISTS achievements_code_key;
ALTER TABLE IF EXISTS sandbox.students ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS sandbox.students_id_seq;
DROP TABLE IF EXISTS sandbox.students;
DROP VIEW IF EXISTS public.v_student_course_progress;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.user_achievements;
DROP TABLE IF EXISTS public.topics;
DROP TABLE IF EXISTS public.tests;
DROP TABLE IF EXISTS public.test_attempts;
DROP TABLE IF EXISTS public.submissions;
DROP TABLE IF EXISTS public.roles;
DROP TABLE IF EXISTS public.reflections;
DROP TABLE IF EXISTS public.questions;
DROP TABLE IF EXISTS public.modules;
DROP TABLE IF EXISTS public.messages;
DROP TABLE IF EXISTS public.lessons;
DROP TABLE IF EXISTS public.lesson_progress;
DROP TABLE IF EXISTS public.enrollments;
DROP TABLE IF EXISTS public.courses;
DROP TABLE IF EXISTS public.course_topics;
DROP TABLE IF EXISTS public.course_ratings;
DROP TABLE IF EXISTS public.assignments;
DROP TABLE IF EXISTS public.answer_submissions;
DROP TABLE IF EXISTS public.answer_options;
DROP TABLE IF EXISTS public.activities;
DROP TABLE IF EXISTS public.achievements;
DROP TYPE IF EXISTS public.task_type;
DROP TYPE IF EXISTS public.task_level;
DROP TYPE IF EXISTS public.submission_status;
DROP TYPE IF EXISTS public.question_type;
DROP TYPE IF EXISTS public.progress_status;
DROP TYPE IF EXISTS public.enrollment_status;
DROP TYPE IF EXISTS public.activity_type;
DROP EXTENSION IF EXISTS pgcrypto;
DROP EXTENSION IF EXISTS citext;
DROP SCHEMA IF EXISTS sandbox;
--
-- Name: sandbox; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA sandbox;


--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: activity_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.activity_type AS ENUM (
    'login',
    'lesson_view',
    'lesson_complete',
    'test_start',
    'test_finish',
    'sql_run',
    'submission',
    'achievement'
);


--
-- Name: enrollment_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.enrollment_status AS ENUM (
    'active',
    'completed',
    'dropped'
);


--
-- Name: progress_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.progress_status AS ENUM (
    'not_started',
    'in_progress',
    'completed'
);


--
-- Name: question_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.question_type AS ENUM (
    'single',
    'multiple',
    'text',
    'sql'
);


--
-- Name: submission_status; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.submission_status AS ENUM (
    'submitted',
    'graded',
    'returned'
);


--
-- Name: task_level; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.task_level AS ENUM (
    'basic',
    'medium',
    'advanced'
);


--
-- Name: task_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.task_type AS ENUM (
    'sql',
    'file',
    'text'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: achievements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.achievements (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code character varying(50) NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    icon character varying(100),
    xp_reward integer DEFAULT 0 NOT NULL,
    CONSTRAINT achievements_xp_reward_check CHECK ((xp_reward >= 0))
);


--
-- Name: activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activities (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    type public.activity_type NOT NULL,
    entity_type character varying(50),
    entity_id uuid,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: answer_options; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answer_options (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    question_id uuid NOT NULL,
    text text NOT NULL,
    is_correct boolean DEFAULT false NOT NULL,
    order_index integer DEFAULT 0 NOT NULL
);


--
-- Name: answer_submissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answer_submissions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    attempt_id uuid NOT NULL,
    question_id uuid NOT NULL,
    answer_option_id uuid,
    text_answer text,
    is_correct boolean
);


--
-- Name: assignments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assignments (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    course_id uuid NOT NULL,
    lesson_id uuid,
    title character varying(200) NOT NULL,
    description text,
    level public.task_level DEFAULT 'basic'::public.task_level NOT NULL,
    type public.task_type DEFAULT 'sql'::public.task_type NOT NULL,
    expected_sql text,
    max_score integer DEFAULT 100 NOT NULL,
    is_final boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT assignments_max_score_check CHECK ((max_score > 0))
);


--
-- Name: course_ratings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.course_ratings (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    course_id uuid NOT NULL,
    user_id uuid NOT NULL,
    rating integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    comment text,
    CONSTRAINT course_ratings_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


--
-- Name: course_topics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.course_topics (
    course_id uuid NOT NULL,
    topic_id uuid NOT NULL
);


--
-- Name: courses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.courses (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(200) NOT NULL,
    description text,
    semester character varying(20),
    author_id uuid,
    is_published boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    level public.task_level DEFAULT 'basic'::public.task_level NOT NULL,
    cover_url text
);


--
-- Name: enrollments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollments (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    course_id uuid NOT NULL,
    status public.enrollment_status DEFAULT 'active'::public.enrollment_status NOT NULL,
    enrolled_at timestamp with time zone DEFAULT now() NOT NULL,
    completed_at timestamp with time zone
);


--
-- Name: lesson_progress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lesson_progress (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    lesson_id uuid NOT NULL,
    status public.progress_status DEFAULT 'not_started'::public.progress_status NOT NULL,
    time_spent_sec integer DEFAULT 0 NOT NULL,
    visits integer DEFAULT 0 NOT NULL,
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    CONSTRAINT lesson_progress_time_spent_sec_check CHECK ((time_spent_sec >= 0)),
    CONSTRAINT lesson_progress_visits_check CHECK ((visits >= 0))
);


--
-- Name: lessons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lessons (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    module_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    theory_content text,
    order_index integer DEFAULT 0 NOT NULL,
    est_minutes integer,
    xp_reward integer DEFAULT 10 NOT NULL,
    CONSTRAINT lessons_est_minutes_check CHECK ((est_minutes > 0)),
    CONSTRAINT lessons_xp_reward_check CHECK ((xp_reward >= 0))
);


--
-- Name: messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    sender_id uuid NOT NULL,
    recipient_id uuid NOT NULL,
    course_id uuid,
    body text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    read_at timestamp with time zone
);


--
-- Name: modules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.modules (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    course_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    order_index integer DEFAULT 0 NOT NULL,
    week_number integer,
    CONSTRAINT modules_week_number_check CHECK (((week_number >= 1) AND (week_number <= 16)))
);


--
-- Name: questions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.questions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    test_id uuid NOT NULL,
    text text NOT NULL,
    type public.question_type DEFAULT 'single'::public.question_type NOT NULL,
    points integer DEFAULT 1 NOT NULL,
    order_index integer DEFAULT 0 NOT NULL,
    CONSTRAINT questions_points_check CHECK ((points > 0))
);


--
-- Name: reflections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reflections (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    lesson_id uuid NOT NULL,
    clarity_rating smallint,
    difficulty_rating smallint,
    comment text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT reflections_clarity_rating_check CHECK (((clarity_rating >= 1) AND (clarity_rating <= 5))),
    CONSTRAINT reflections_difficulty_rating_check CHECK (((difficulty_rating >= 1) AND (difficulty_rating <= 5)))
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code character varying(30) NOT NULL,
    name character varying(100) NOT NULL,
    description text
);


--
-- Name: submissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.submissions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    assignment_id uuid NOT NULL,
    user_id uuid NOT NULL,
    sql_query text,
    file_url text,
    text_answer text,
    score numeric(5,2),
    feedback text,
    status public.submission_status DEFAULT 'submitted'::public.submission_status NOT NULL,
    graded_by uuid,
    submitted_at timestamp with time zone DEFAULT now() NOT NULL,
    graded_at timestamp with time zone,
    CONSTRAINT submissions_score_check CHECK ((score >= (0)::numeric))
);


--
-- Name: test_attempts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.test_attempts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    test_id uuid NOT NULL,
    score numeric(5,2),
    is_passed boolean,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    finished_at timestamp with time zone,
    CONSTRAINT test_attempts_score_check CHECK (((score >= (0)::numeric) AND (score <= (100)::numeric)))
);


--
-- Name: tests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tests (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    lesson_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    pass_score integer DEFAULT 60 NOT NULL,
    time_limit_sec integer,
    CONSTRAINT tests_pass_score_check CHECK (((pass_score >= 0) AND (pass_score <= 100))),
    CONSTRAINT tests_time_limit_sec_check CHECK ((time_limit_sec > 0))
);


--
-- Name: topics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.topics (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code character varying(50) NOT NULL,
    name character varying(100) NOT NULL
);


--
-- Name: user_achievements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_achievements (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    achievement_id uuid NOT NULL,
    awarded_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email public.citext NOT NULL,
    password_hash text NOT NULL,
    full_name character varying(200) NOT NULL,
    role_id uuid NOT NULL,
    avatar_url text,
    xp integer DEFAULT 0 NOT NULL,
    level integer DEFAULT 1 NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    last_seen_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT users_level_check CHECK ((level >= 1)),
    CONSTRAINT users_xp_check CHECK ((xp >= 0))
);


--
-- Name: v_student_course_progress; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_student_course_progress AS
 SELECT e.user_id,
    e.course_id,
    count(DISTINCT l.id) AS total_lessons,
    count(DISTINCT lp.lesson_id) FILTER (WHERE (lp.status = 'completed'::public.progress_status)) AS completed_lessons,
    round(((100.0 * (count(DISTINCT lp.lesson_id) FILTER (WHERE (lp.status = 'completed'::public.progress_status)))::numeric) / (NULLIF(count(DISTINCT l.id), 0))::numeric), 1) AS completion_pct,
    round(avg(ta.score), 1) AS avg_test_score
   FROM (((((public.enrollments e
     JOIN public.modules m ON ((m.course_id = e.course_id)))
     JOIN public.lessons l ON ((l.module_id = m.id)))
     LEFT JOIN public.lesson_progress lp ON (((lp.lesson_id = l.id) AND (lp.user_id = e.user_id))))
     LEFT JOIN public.tests t ON ((t.lesson_id = l.id)))
     LEFT JOIN public.test_attempts ta ON (((ta.test_id = t.id) AND (ta.user_id = e.user_id))))
  GROUP BY e.user_id, e.course_id;


--
-- Name: students; Type: TABLE; Schema: sandbox; Owner: -
--

CREATE TABLE sandbox.students (
    id integer NOT NULL,
    full_name text,
    group_name text,
    xp integer
);


--
-- Name: students_id_seq; Type: SEQUENCE; Schema: sandbox; Owner: -
--

CREATE SEQUENCE sandbox.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: sandbox; Owner: -
--

ALTER SEQUENCE sandbox.students_id_seq OWNED BY sandbox.students.id;


--
-- Name: students id; Type: DEFAULT; Schema: sandbox; Owner: -
--

ALTER TABLE ONLY sandbox.students ALTER COLUMN id SET DEFAULT nextval('sandbox.students_id_seq'::regclass);


--
-- Data for Name: achievements; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.achievements (id, code, title, description, icon, xp_reward) FROM stdin;
0ac00000-0000-0000-0000-000000000001	first_lesson	Первый шаг	Завершён первый урок.	flag	20
0ac00000-0000-0000-0000-000000000002	first_query	Первый запрос	Выполнен первый SQL-запрос.	code	20
0ac00000-0000-0000-0000-000000000003	test_master	Знаток тестов	Пройден тест на 80+ баллов.	medal	30
0ac00000-0000-0000-0000-000000000004	no_miss_week	Неделя без пропусков	Активность 7 дней подряд.	fire	40
0ac00000-0000-0000-0000-000000000005	project_defender	Защитник проекта	Защищён итоговый проект.	trophy	100
\.


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.activities (id, user_id, type, entity_type, entity_id, metadata, created_at) FROM stdin;
39e7578b-8de9-4383-8841-11d37a067211	0a000000-0000-0000-0000-000000000002	login	\N	\N	\N	2025-10-20 18:25:00+03
e96c88d8-8a66-493f-9075-08b8d377f71a	0a000000-0000-0000-0000-000000000002	lesson_complete	lesson	0e000000-0000-0000-0000-000000000004	{"xp": 25}	2025-09-22 18:41:00+03
d47be493-a710-4d42-8453-c62f7509862f	0a000000-0000-0000-0000-000000000002	test_finish	test	0fa00000-0000-0000-0000-000000000001	{"score": 90}	2025-09-05 18:40:00+03
87620cba-d87a-4401-82dc-98c702b73f08	0a000000-0000-0000-0000-000000000002	sql_run	\N	\N	{"ok": true}	2025-10-14 19:00:00+03
5480fe63-020c-4eb7-8b78-b85e78a21d1f	0a000000-0000-0000-0000-000000000003	login	\N	\N	\N	2025-10-18 14:05:00+03
40d8dcbd-00d0-47c5-9f47-8a4c2035a5d9	0a000000-0000-0000-0000-000000000003	lesson_complete	lesson	0e000000-0000-0000-0000-000000000002	{"xp": 20}	2025-09-10 12:26:00+03
3c0673b1-1f66-4be5-bff4-663c6e3d628d	0a000000-0000-0000-0000-000000000004	login	\N	\N	\N	2025-10-06 11:55:00+03
9dffe9c0-4cce-4021-b962-2c5a77b7a45c	0a000000-0000-0000-0000-000000000004	lesson_view	lesson	0e000000-0000-0000-0000-000000000002	\N	2025-09-20 11:00:00+03
f1f5e6c4-d9d4-4269-b410-6a706de04bd4	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2025-10-19 20:00:00+03
3ad2bc5e-061e-4292-a8a4-316a0276f21e	0a000000-0000-0000-0000-000000000005	lesson_view	lesson	0e000000-0000-0000-0000-000000000001	\N	2025-10-19 20:02:00+03
2ffed5cd-cf7c-4729-a5cc-a6eee0ffa328	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 07:42:31.66+03
09fce6ab-7b74-4172-b5c9-9d2c8fd88003	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-10 07:43:51.738+03
d045ce3a-c7cc-4bf6-ac78-35c9a58d6bc2	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-10 08:49:20.387+03
df437641-ce93-4a54-b1a4-66d2a1e8bdea	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 08:49:37.301+03
dad13344-5f72-4df1-b818-a331bbc23f51	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 09:00:04.593+03
8f6b23a1-fa44-49ef-ba48-bc2ae27d596a	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 09:00:28.667+03
84319943-5097-4bfa-9779-c6493206ca63	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-10 09:13:39.742+03
ea7bc7b2-a7e2-4d31-8ece-0d7513651580	0a000000-0000-0000-0000-000000000005	submission	assignment	0aa00000-0000-0000-0000-000000000002	\N	2026-06-10 09:14:21.506+03
748034cb-2ce8-49e8-ad2e-8a1e854ca648	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-10 09:38:17.953+03
d425eed8-552d-4a8d-8e11-a127a2e92d51	0a000000-0000-0000-0000-000000000005	submission	assignment	0aa00000-0000-0000-0000-000000000002	\N	2026-06-10 09:39:20.566+03
fa2f7695-b7d8-4680-8afc-1728f4271186	0a000000-0000-0000-0000-000000000005	sql_run	\N	\N	\N	2026-06-10 09:40:05.826+03
e1046f8f-df26-41d6-a45f-adb19c7cbfb8	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 09:41:02.509+03
871d7857-4f94-4171-93af-9f7a5b0bb878	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 15:22:53.294+03
25f7ea0c-7624-4459-808c-56dd18ef3898	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 16:34:55.517+03
b81ad025-be0c-46cb-9b3d-307fcf9a2039	0a000000-0000-0000-0000-000000000001	sql_run	\N	\N	\N	2026-06-10 16:41:16.335+03
b4fd20a7-70d2-4ac7-b6f9-d9fd6b07e082	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-10 16:43:29.716+03
e0270a68-2057-4ba5-b926-b6c226d58960	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-10 20:03:32.129+03
c9f884d5-bcb1-4bc5-9207-a1ac822fdbf1	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-10 20:05:05.469+03
f54b45f8-ec1c-4010-885c-be30d4bc2ad0	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-11 08:48:26.89+03
a3a41fe0-ba07-4ac7-8827-f329252875e0	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-11 08:48:50.714+03
e34c19e8-87e6-45ee-8c2b-99ddc05926db	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-11 12:25:09.189+03
38ee4b13-bf2f-428a-ac53-2b40197dab55	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-11 12:25:38.703+03
63bf7db7-7f9a-4a45-8917-d7a1dc9b51dc	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 07:39:58.1+03
56e1104b-eaa1-49b0-8f44-046a5fab9088	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-12 07:40:56.611+03
e0455378-cb7f-4e51-8cfd-827d1f767eb4	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 07:41:11.402+03
d3be20f9-9d00-4b14-929b-1cad2004244d	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-12 07:41:27.56+03
603b41fc-985f-4f1f-8459-ae05f902ab6e	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 07:41:34.058+03
713b6e2c-acf0-4bb8-9a35-3c883d740032	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 07:56:20.884+03
f21f9e38-3910-450c-96fe-287dd7f9e6c4	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 14:33:11.744+03
ec92d0a9-f2d8-4584-96d8-8a18d8abc9b0	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-12 14:39:12.582+03
84f83a6b-f4e2-4c9e-bc7d-79e58b89e87f	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 14:41:24.148+03
9d8e1c5f-7df6-4b9c-8c92-6048926b1157	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-12 14:44:03.305+03
1167ea87-ad4c-461e-83f3-fa20ae9232de	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 14:44:40.936+03
436241a0-041b-4348-bd0d-22e06f339e30	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 14:45:03.46+03
96018cfc-b0db-4ea1-ba55-b581929070e8	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-12 14:45:11.051+03
0a9a8043-13e5-4e3c-b4da-f746fce7fd30	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 14:47:03.253+03
a188425a-cf4e-4628-959c-8217aed99fb2	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-12 14:48:00.234+03
9421f992-88fa-4d11-8b9e-8e134e43e299	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 14:53:11.572+03
dd7357e6-889d-4e5f-a5aa-81a7fef95a7d	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-12 16:14:51.088+03
5893d8c3-0a1d-4dad-999d-db6e652f7ed8	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 16:15:56.515+03
22846a06-b63d-40df-9161-e91e665ce389	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 18:43:40.788+03
c0dabfa0-158b-4fb1-af1a-41db5456a6e7	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-12 18:44:13.363+03
79bd6d06-3cf9-48b6-8810-8c712dbe2583	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-12 18:45:11.346+03
c1864953-895e-4ce8-9152-c1d8eedfabbd	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-12 18:45:47.505+03
a2c1975e-d2ea-465e-b252-52625475346d	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 20:04:24.036+03
1585208f-3de0-4bd9-80e5-692cc1b35514	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 20:22:41.005+03
3ac23b37-a9ca-4ed6-aeef-30d236294c8c	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-12 20:24:18.724+03
ac0aaf71-dc04-467f-92ba-07e9bf57130a	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-12 20:59:01.72+03
c36200e9-7830-4533-a27a-3f367351879b	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-12 20:59:59.195+03
4fcc7f5f-b1a2-4d2a-856b-073d456a437d	0a000000-0000-0000-0000-000000000002	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-05-31 21:12:44.922+03
98f8e353-829e-4d9e-8db2-6379c801a91a	0a000000-0000-0000-0000-000000000003	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-01 21:12:44.937+03
760320ee-debf-44b0-bf15-4479afcbb8f8	0a000000-0000-0000-0000-000000000004	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-02 21:12:44.943+03
265eb939-f230-41ad-a6ed-dd2a9e2e8d60	0a000000-0000-0000-0000-000000000005	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-03 21:12:44.947+03
ee4a1fd5-54cf-4a32-b0ba-d02a42b298e2	0a000000-0000-0000-0000-000000000010	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-04 21:12:44.953+03
13626596-f788-43f7-b525-b8c2fd71c0ea	0a000000-0000-0000-0000-000000000011	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-05 21:12:44.958+03
a1dacd81-fcbd-4a88-9dda-1728b289ac3b	0a000000-0000-0000-0000-000000000012	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-06 21:12:44.964+03
f82bbe8e-23a5-4a72-a6cf-52a9d1998590	0a000000-0000-0000-0000-000000000013	test_finish	test	f66edf0c-bef4-41ae-bff5-90475d5f01e7	\N	2026-06-07 21:12:44.969+03
4e0f7ba6-8948-4304-8186-e6f0ac4367ac	0a000000-0000-0000-0000-000000000002	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-05-31 21:12:44.981+03
4a109ce7-cc1b-4afd-a45e-132fc6643d40	0a000000-0000-0000-0000-000000000003	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-01 21:12:44.986+03
99299494-c1e7-451e-b454-430f73fd83a7	0a000000-0000-0000-0000-000000000004	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-02 21:12:44.99+03
888a1234-8c67-4fa8-ae18-1286d42f06e6	0a000000-0000-0000-0000-000000000005	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-03 21:12:44.994+03
fb69dbd7-7371-413b-87de-bc87c9a44ab6	0a000000-0000-0000-0000-000000000010	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-04 21:12:44.997+03
5d2219af-28cf-4814-b554-509a34ae8c64	0a000000-0000-0000-0000-000000000011	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-05 21:12:45.001+03
5fdeba55-57b9-4a50-ac6d-4c6d7bb9931a	0a000000-0000-0000-0000-000000000012	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-06 21:12:45.004+03
3fb8a7cf-c9a2-4c30-8275-5416e81d058c	0a000000-0000-0000-0000-000000000013	test_finish	test	113ab5a8-c3fd-4ffa-a09d-8e05ff62ec20	\N	2026-06-07 21:12:45.01+03
4fb6ba92-4eef-4e06-88ea-6eb6ccfde9e3	0a000000-0000-0000-0000-000000000002	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-05-31 21:12:45.02+03
87091ab2-7e9d-41d6-8111-99cff5b53f2f	0a000000-0000-0000-0000-000000000003	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-01 21:12:45.023+03
7eb27eef-b7e5-401c-9a11-161ba0f27417	0a000000-0000-0000-0000-000000000004	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-02 21:12:45.026+03
279199d1-9729-4152-90ef-6be4da550f41	0a000000-0000-0000-0000-000000000005	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-03 21:12:45.028+03
23ad2510-8f0b-4eea-863e-17c9eaa0560a	0a000000-0000-0000-0000-000000000010	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-04 21:12:45.031+03
857d4d5e-d8d1-4176-a956-787f51faf293	0a000000-0000-0000-0000-000000000011	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-05 21:12:45.033+03
8746b80d-2fb4-4baf-b412-31ecbf259d95	0a000000-0000-0000-0000-000000000012	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-06 21:12:45.036+03
abc93f81-438d-44ed-8c2e-3924a84e12b0	0a000000-0000-0000-0000-000000000013	test_finish	test	6befed6a-f6c5-45f9-9b89-b43770f59ee0	\N	2026-06-07 21:12:45.039+03
8e5e0999-593c-4493-a469-204c8029b093	0a000000-0000-0000-0000-000000000002	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-01 06:10:56.237+03
fc0d8c7e-baea-4949-bb43-575e41af0f2b	0a000000-0000-0000-0000-000000000003	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-02 06:10:56.272+03
1cc561e6-939b-4778-889a-e092713b26fb	0a000000-0000-0000-0000-000000000004	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-03 06:10:56.277+03
527d34df-e632-4e07-bd59-3aaef2316c26	0a000000-0000-0000-0000-000000000005	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-04 06:10:56.286+03
c5f3719a-853a-4ef2-9cf1-f98bd98b2a4a	0a000000-0000-0000-0000-000000000010	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-05 06:10:56.293+03
15160073-7ea2-4702-9c86-6bc1bc1b6050	0a000000-0000-0000-0000-000000000011	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-06 06:10:56.296+03
046f90ed-abd0-40b1-a742-2b7b7397cfed	0a000000-0000-0000-0000-000000000012	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-07 06:10:56.3+03
3fbbf6bd-d444-47a4-ae43-c60c489f9099	0a000000-0000-0000-0000-000000000013	test_finish	test	40a3c074-e728-4cda-8db6-549c536c1f97	\N	2026-06-08 06:10:56.303+03
728882e1-879c-4710-ad1d-4411579f561c	0a000000-0000-0000-0000-000000000002	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-01 06:10:56.314+03
7eb47ef5-870a-4762-98ed-d7b4384377d6	0a000000-0000-0000-0000-000000000003	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-02 06:10:56.318+03
5f8ba5c0-2a71-437c-8456-6df06bfa437c	0a000000-0000-0000-0000-000000000004	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-03 06:10:56.32+03
286b6946-d51a-4e4c-a48a-8406963caf0f	0a000000-0000-0000-0000-000000000005	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-04 06:10:56.324+03
b4a178bb-dd01-4770-b109-7abf8f20267e	0a000000-0000-0000-0000-000000000010	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-05 06:10:56.326+03
689c4f68-ec3d-4362-b41c-0191f9725424	0a000000-0000-0000-0000-000000000011	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-06 06:10:56.329+03
c5b01bda-b049-4c34-bb82-7f569bc110ba	0a000000-0000-0000-0000-000000000012	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-07 06:10:56.334+03
299fc6ec-9a29-477f-9777-3265eed999b6	0a000000-0000-0000-0000-000000000013	test_finish	test	441a00bd-b630-48b8-b393-1b3f9803a0ca	\N	2026-06-08 06:10:56.336+03
91b14a51-6575-47ad-8b3f-a2f6a96eaf0c	0a000000-0000-0000-0000-000000000002	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-01 06:10:56.343+03
4c86e10a-44d4-48a2-9327-7dfc9e16f9f7	0a000000-0000-0000-0000-000000000003	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-02 06:10:56.347+03
87457614-3c2e-4254-9a2b-0ec62eadb3f9	0a000000-0000-0000-0000-000000000004	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-03 06:10:56.35+03
13eab0ca-1cbf-47d3-b807-c6c06d3924b4	0a000000-0000-0000-0000-000000000005	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-04 06:10:56.353+03
89ded3ec-ddce-441d-a567-35d9a259f6f3	0a000000-0000-0000-0000-000000000010	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-05 06:10:56.355+03
63a78441-5e63-4daf-83b8-c0aaa9d4bd48	0a000000-0000-0000-0000-000000000011	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-06 06:10:56.358+03
1778a216-4b17-42c9-abd2-880097335f2b	0a000000-0000-0000-0000-000000000012	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-07 06:10:56.36+03
513147a0-c24f-4653-b256-f10baf76eb5e	0a000000-0000-0000-0000-000000000013	test_finish	test	bf26cac0-772c-45eb-b054-d1bca19c1191	\N	2026-06-08 06:10:56.363+03
078357d3-8033-42f2-b07b-341750f18a04	0a000000-0000-0000-0000-000000000002	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-01 07:21:59.174+03
bd5b122f-2595-4179-870e-6fd84dde6d32	0a000000-0000-0000-0000-000000000002	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-01 07:21:59.174+03
f9fbf6da-79b5-408f-b2ac-58f747788cd8	0a000000-0000-0000-0000-000000000003	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-02 07:21:59.191+03
9820136f-f9fe-487a-97f0-3bb2d5c97274	0a000000-0000-0000-0000-000000000003	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-02 07:21:59.191+03
3089f43a-2798-4a39-a76f-3c8f30fedd16	0a000000-0000-0000-0000-000000000004	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-03 07:21:59.195+03
b5266fdb-54c4-4787-9eb3-08fd406e760b	0a000000-0000-0000-0000-000000000004	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-03 07:21:59.195+03
7f41ed6d-a3c6-45df-b35f-af42ac136400	0a000000-0000-0000-0000-000000000005	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-04 07:21:59.2+03
9bc6e879-11f4-4298-bb19-b58b4b754a89	0a000000-0000-0000-0000-000000000005	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-04 07:21:59.2+03
bc0e33d1-91d3-4923-a8cb-1c227ad219c8	0a000000-0000-0000-0000-000000000010	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-05 07:21:59.204+03
1d269e48-6937-4d59-9f2c-7652513df81d	0a000000-0000-0000-0000-000000000010	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-05 07:21:59.204+03
4e5d0120-289e-49f8-ba8f-8ef0396a5762	0a000000-0000-0000-0000-000000000011	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-06 07:21:59.208+03
6e61747c-55b1-488e-b5a0-6e3da536608c	0a000000-0000-0000-0000-000000000011	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-06 07:21:59.208+03
5cc65ce4-c93e-4bac-8f19-678299ee685e	0a000000-0000-0000-0000-000000000012	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-07 07:21:59.211+03
3fb689ec-25b9-4d10-b77c-c92a2dddc98e	0a000000-0000-0000-0000-000000000012	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-07 07:21:59.211+03
31556754-8fae-454e-b29d-5369de5d4531	0a000000-0000-0000-0000-000000000013	test_finish	test	330d453f-8fcb-4579-b941-5e35d1ac5a35	\N	2026-06-08 07:21:59.215+03
4f684de9-f728-4c70-8c58-ab0e8f0ba4a1	0a000000-0000-0000-0000-000000000013	lesson_complete	lesson	656a356d-8ad7-4bb5-b5b5-3597d30936f8	\N	2026-06-08 07:21:59.215+03
d07713f1-47a5-43bd-8baa-4079e3ee3c55	0a000000-0000-0000-0000-000000000002	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-01 07:21:59.223+03
94e3b0c6-c76d-4b83-9b54-b6bddfccfae6	0a000000-0000-0000-0000-000000000002	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-01 07:21:59.223+03
5861b5cd-eadc-4969-b7cf-c58dc8def5c6	0a000000-0000-0000-0000-000000000003	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-02 07:21:59.226+03
bb2006d6-d52b-4927-a0e1-288e8a1deea3	0a000000-0000-0000-0000-000000000003	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-02 07:21:59.226+03
2d56f4c3-9f98-4fb8-a3f2-033ba7bac990	0a000000-0000-0000-0000-000000000004	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-03 07:21:59.23+03
b8e01d34-12b1-41b1-b310-8815cc4d76bb	0a000000-0000-0000-0000-000000000004	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-03 07:21:59.23+03
a6ac09c4-f787-4b60-b576-8dd40ba717e6	0a000000-0000-0000-0000-000000000005	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-04 07:21:59.234+03
ffdb054e-d8a0-488b-8f35-d45778839782	0a000000-0000-0000-0000-000000000005	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-04 07:21:59.234+03
79ff7cb8-93b9-4687-9c52-0bac5c4595d4	0a000000-0000-0000-0000-000000000010	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-05 07:21:59.239+03
c807d491-0064-4a42-a212-69943432ec57	0a000000-0000-0000-0000-000000000010	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-05 07:21:59.239+03
3ce377cc-a146-4024-adc3-9278793da049	0a000000-0000-0000-0000-000000000011	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-06 07:21:59.243+03
e5413d1a-f52a-423e-8a23-50ca2fab7663	0a000000-0000-0000-0000-000000000011	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-06 07:21:59.243+03
e4462edd-885b-453c-9cca-e8d3238388ed	0a000000-0000-0000-0000-000000000012	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-07 07:21:59.246+03
58ae2d4a-a489-4175-b011-0ae93167b084	0a000000-0000-0000-0000-000000000012	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-07 07:21:59.246+03
a0e5c7b4-a13a-40ca-95a3-9aa856f4e314	0a000000-0000-0000-0000-000000000013	test_finish	test	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	\N	2026-06-08 07:21:59.249+03
8e2b58f6-1588-44cd-b713-dcd536d8695a	0a000000-0000-0000-0000-000000000013	lesson_complete	lesson	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	\N	2026-06-08 07:21:59.249+03
9b3a1c48-3182-45f3-88a9-3bdf5520633a	0a000000-0000-0000-0000-000000000002	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-01 07:21:59.256+03
0a043805-09a6-4e44-98a7-d00f06f628a1	0a000000-0000-0000-0000-000000000002	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-01 07:21:59.256+03
e1bd7f78-9258-4996-a60f-420a8e1f0aa5	0a000000-0000-0000-0000-000000000003	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-02 07:21:59.259+03
b0dc6e26-86ee-478a-a014-45c9f3332496	0a000000-0000-0000-0000-000000000003	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-02 07:21:59.259+03
35cc0096-2e7f-40ed-a7f9-fe5987215abf	0a000000-0000-0000-0000-000000000004	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-03 07:21:59.264+03
270784de-23cf-4dd5-bb02-9906551e3408	0a000000-0000-0000-0000-000000000004	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-03 07:21:59.264+03
0bf895ee-f4ec-4b77-8b99-901f4fb1b4ac	0a000000-0000-0000-0000-000000000005	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-04 07:21:59.269+03
37bda7ed-7f73-4344-bde6-0ed726bebf55	0a000000-0000-0000-0000-000000000005	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-04 07:21:59.269+03
b74d61cf-c7a4-4c2f-83c9-b5c72c91b69d	0a000000-0000-0000-0000-000000000010	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-05 07:21:59.272+03
9090413f-8edf-4be0-84d0-efe4b5acf9b3	0a000000-0000-0000-0000-000000000010	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-05 07:21:59.272+03
281b8564-199d-47f7-9350-a14b4b865810	0a000000-0000-0000-0000-000000000011	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-06 07:21:59.275+03
da8bf285-94eb-46d5-ad20-92895eb1b4ed	0a000000-0000-0000-0000-000000000011	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-06 07:21:59.275+03
b66202fa-dcb2-4309-b17b-e1e7ce09f9f1	0a000000-0000-0000-0000-000000000012	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-07 07:21:59.277+03
75addf47-96f4-4e14-ad3f-1185551fd84f	0a000000-0000-0000-0000-000000000012	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-07 07:21:59.277+03
6566db7f-5456-4766-b65d-3a1eea6a69a5	0a000000-0000-0000-0000-000000000013	test_finish	test	9ae38d39-0a6e-47a8-929f-60e48f7311c9	\N	2026-06-08 07:21:59.279+03
261399d1-b4f6-4f9d-8a89-81d3d32cbfcf	0a000000-0000-0000-0000-000000000013	lesson_complete	lesson	216f012b-02e7-49c4-81e1-08e8a9af6dcd	\N	2026-06-08 07:21:59.279+03
5aef0b48-0c24-4e10-bc90-d25d9a29c546	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-13 10:57:12.203+03
0ef0752b-d590-4cc1-be5c-dfd7865a3fc5	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-13 10:58:56.236+03
4c09ef00-4b23-405f-b4a4-f69740f471ad	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-13 11:02:00.664+03
cbbc7908-a971-415e-94d4-c477931ca621	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-13 11:37:23.375+03
a96a2804-fce7-4dc3-9cb9-ecf921e3cafd	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-13 11:37:39.429+03
a4919eb7-6344-4456-95e9-ef812407f4cd	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-14 13:25:23.415+03
ffa06ab1-6a44-4766-b27b-e8e8b1cfafaf	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-14 13:30:30.963+03
95204517-5fb0-43f8-ab4b-70b961653968	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-14 13:31:42.821+03
71ea9ac6-4551-4e0d-9b98-920b053d2b72	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-14 13:32:36.326+03
43083322-4990-40cc-bb12-15a2c0daf316	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-14 13:33:06.733+03
af6898b3-4fde-4534-95b7-66cc1cc511e5	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-14 19:08:32.016+03
5e824ab2-d018-4d93-9b0b-bd929d5f8f16	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-14 19:09:31.99+03
abccb1d1-0e46-433f-a5b5-a166e92f8810	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-14 19:11:21.079+03
4c26a3d7-415e-429d-8ac4-32e94a0509b2	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-14 19:12:55.19+03
ad4e6420-bc67-4d3e-b843-9d402f38ff53	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	login	\N	\N	\N	2026-06-14 23:10:02.309+03
d7166e4b-447b-479f-af98-4aead1cc18c4	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-18 21:51:43.586+03
63ef9734-5566-47b2-af89-884afcc5ca2f	dac3fbb0-f253-4492-a731-27496f3ed123	login	\N	\N	\N	2026-06-18 21:56:26.837+03
3aaccb51-e87c-4ba5-84f6-3ec5480008c0	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-18 21:57:42.793+03
ffb2ea59-24aa-461d-a48c-b81cd538d0ff	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-18 22:00:13.935+03
85b8234a-9087-4c18-8333-7c953d4a720d	0a000000-0000-0000-0000-000000000005	submission	assignment	0aa00000-0000-0000-0000-000000000002	\N	2026-06-18 22:01:35.988+03
02cf9b79-fbf0-45ae-ba10-a781a6fac868	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-18 22:31:02.373+03
635ea362-ac98-4e2c-9bad-fcaa350f6a47	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-18 22:31:33.66+03
109026cd-f0ae-4146-8178-a3bb25c4d5d0	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-19 05:01:28.552+03
f147ece1-3e02-445c-be7b-d404f3c3c8c3	0a000000-0000-0000-0000-000000000001	login	\N	\N	\N	2026-06-19 05:44:59.479+03
33e19db0-758c-446d-b067-945b98f67bd7	0a000000-0000-0000-0000-000000000005	login	\N	\N	\N	2026-06-19 05:45:45.434+03
\.


--
-- Data for Name: answer_options; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.answer_options (id, question_id, text, is_correct, order_index) FROM stdin;
0ab00000-0000-0000-0000-000000000001	0ba00000-0000-0000-0000-000000000001	Организованное хранилище данных	t	1
0ab00000-0000-0000-0000-000000000002	0ba00000-0000-0000-0000-000000000001	Программа для рисования	f	2
0ab00000-0000-0000-0000-000000000003	0ba00000-0000-0000-0000-000000000001	Вид текстового документа	f	3
0ab00000-0000-0000-0000-000000000004	0ba00000-0000-0000-0000-000000000002	Строка (запись)	t	1
0ab00000-0000-0000-0000-000000000005	0ba00000-0000-0000-0000-000000000002	Столбец	f	2
0ab00000-0000-0000-0000-000000000006	0ba00000-0000-0000-0000-000000000002	Ячейка	f	3
0ab00000-0000-0000-0000-000000000007	0ba00000-0000-0000-0000-000000000003	Электронный журнал оценок	t	1
0ab00000-0000-0000-0000-000000000009	0ba00000-0000-0000-0000-000000000003	Бумажный плакат на стене	f	3
0ab00000-0000-0000-0000-000000000010	0ba00000-0000-0000-0000-000000000003	Устный пересказ урока	f	4
0ab00000-0000-0000-0000-000000000011	0ba00000-0000-0000-0000-000000000004	Однозначно идентифицирует строку	t	1
0ab00000-0000-0000-0000-000000000012	0ba00000-0000-0000-0000-000000000004	Хранит картинки	f	2
0ab00000-0000-0000-0000-000000000013	0ba00000-0000-0000-0000-000000000004	Удаляет таблицу	f	3
0ab00000-0000-0000-0000-000000000014	0ba00000-0000-0000-0000-000000000005	Связать строки разных таблиц	t	1
0ab00000-0000-0000-0000-000000000015	0ba00000-0000-0000-0000-000000000005	Ускорить печать	f	2
0ab00000-0000-0000-0000-000000000016	0ba00000-0000-0000-0000-000000000005	Изменить цвет таблицы	f	3
8c80d730-15aa-4a16-b55b-702ac90add3e	53ef5e70-13b4-4d11-b3f2-5e93445832eb	Один объект со значениями всех столбцов	t	1
6009a520-c7b6-48ec-bdb7-755dfc1bd3a9	53ef5e70-13b4-4d11-b3f2-5e93445832eb	Название одного столбца	f	2
134fe8fe-2c11-4cea-9497-b0097dc76bff	53ef5e70-13b4-4d11-b3f2-5e93445832eb	Тип данных	f	3
7431f852-8599-41de-9d91-5181e37df5d8	53ef5e70-13b4-4d11-b3f2-5e93445832eb	Связь между таблицами	f	4
dcb9ff67-490c-46dc-bf42-e6b342d61824	c2cfb6a1-8bda-4653-9c2a-9c4a28802e66	Чтобы задать, какие значения допустимы (текст, число, дата)	t	1
e3eea6fe-4bbf-46ff-ac45-c520f0704eb5	c2cfb6a1-8bda-4653-9c2a-9c4a28802e66	Чтобы окрасить столбец	f	2
4c60599f-1c07-46fb-8860-c16589330b03	c2cfb6a1-8bda-4653-9c2a-9c4a28802e66	Чтобы скрыть столбец	f	3
05e63f3b-02b5-4fbf-bbe5-082455eb72d4	c2cfb6a1-8bda-4653-9c2a-9c4a28802e66	Тип данных не нужен	f	4
68df7a8e-b7e8-4164-8c4f-aa40df6ee4c4	56f2fed4-1b45-4db8-814d-2e8c200cb3f3	Действуют строгие правила, и таблицы можно связывать между собой	t	1
22076b3f-75fe-40e2-9f11-db90e2bfcf02	56f2fed4-1b45-4db8-814d-2e8c200cb3f3	Она всегда меньше по размеру	f	2
5886c109-c5ec-4d94-9a83-c1c704c18fc1	56f2fed4-1b45-4db8-814d-2e8c200cb3f3	В ней нельзя хранить числа	f	3
a8912fbe-316c-4ab7-84b1-2a5de0d52e77	56f2fed4-1b45-4db8-814d-2e8c200cb3f3	Она не требует компьютера	f	4
a052cbe1-3291-41ab-9de1-cf24bf31fe8c	b44e3951-8ee3-4f7d-96ec-0fe60858a652	Объект предметной области, о котором собираем данные	t	1
a0866d3f-60d7-4ed5-9b71-5997fbd9d5d0	b44e3951-8ee3-4f7d-96ec-0fe60858a652	Цвет таблицы	f	2
79871d54-d5ab-4682-a49c-9e8f2ae61e80	b44e3951-8ee3-4f7d-96ec-0fe60858a652	Команда SQL	f	3
405355c1-7257-4dcd-9108-e821f568a279	b44e3951-8ee3-4f7d-96ec-0fe60858a652	Вид ключа	f	4
9cc65db1-4171-4f6c-82da-63137766ff02	db1b41f5-35dd-47bd-86e8-121d317af45f	Свойство сущности (фамилия, дата рождения)	t	1
c88b8421-b1ec-41d9-b357-414662c0f6f2	db1b41f5-35dd-47bd-86e8-121d317af45f	Другая таблица	f	2
e3085fe5-bd84-4f5c-9778-91a68f457dd1	db1b41f5-35dd-47bd-86e8-121d317af45f	Сервер базы данных	f	3
db5af8e9-773c-4a35-9017-0a56d4c68690	db1b41f5-35dd-47bd-86e8-121d317af45f	Запрос на выборку	f	4
0c5ee165-617b-46fe-a820-c2cd4b7f9070	42a753ac-23e7-484a-b3b4-5c02c03fe1d6	Подчёркивать существительные	t	1
ed471132-46b2-4725-8b3a-d93dff696748	42a753ac-23e7-484a-b3b4-5c02c03fe1d6	Считать глаголы	f	2
2995ddcf-afc2-416b-aa1d-20a20d55e191	42a753ac-23e7-484a-b3b4-5c02c03fe1d6	Удалять все слова	f	3
499185b0-3c3a-4fd7-8159-3f93a906ca68	42a753ac-23e7-484a-b3b4-5c02c03fe1d6	Искать только числа	f	4
8f9b31cc-8713-451d-9e3b-5cbd6c9d3812	3d3a4faa-5610-44a3-b4d3-8216979fbd35	CREATE TABLE	t	1
8ac62c07-7ca6-4316-a02c-d5ef3848c06d	3d3a4faa-5610-44a3-b4d3-8216979fbd35	NEW TABLE	f	2
d0f40c20-fce5-4323-9fc3-f2a9b42c6ea9	3d3a4faa-5610-44a3-b4d3-8216979fbd35	MAKE TABLE	f	3
22b4c9ec-79bd-46ce-a700-26302897ed56	3d3a4faa-5610-44a3-b4d3-8216979fbd35	ADD TABLE	f	4
08e81471-e7e6-411f-81d7-3480a74a32b6	90c909b8-fcad-44a9-96d7-836edc53316b	Запрещает оставлять поле пустым	t	1
91fb54c7-4829-4559-8741-5a03968acd01	90c909b8-fcad-44a9-96d7-836edc53316b	Делает поле первичным ключом	f	2
7b67f037-fc0d-4332-96c9-d8b6c0980985	90c909b8-fcad-44a9-96d7-836edc53316b	Удаляет таблицу	f	3
8a6bad89-789c-4226-862d-4a619cc68a80	90c909b8-fcad-44a9-96d7-836edc53316b	Разрешает повторяющиеся значения	f	4
a9c40e1c-6f5e-49cc-a7e7-d2718d055c89	8dbef985-44c0-4edd-bdfa-0804b2326f4e	Он однозначно определяет каждую строку таблицы	t	1
fe45a566-d9b4-4a9e-ba86-181ed9af01f9	8dbef985-44c0-4edd-bdfa-0804b2326f4e	Он всегда хранит текст	f	2
692ee093-b014-4616-adba-a377085586cb	8dbef985-44c0-4edd-bdfa-0804b2326f4e	Он необязателен и ни на что не влияет	f	3
3213fd2c-389a-4b9a-a030-4f8011dc4ab0	8dbef985-44c0-4edd-bdfa-0804b2326f4e	Он хранит пароль пользователя	f	4
c2e95945-89f3-4b19-bb19-b738da0619e5	13c0a935-26f8-4852-a072-bdb28bc7fa10	SELECT	t	1
b8b6dab4-a575-4eb6-8682-30544d691037	13c0a935-26f8-4852-a072-bdb28bc7fa10	READ	f	2
569d3d26-ada6-4cfe-b2b7-736fe2cdc6f7	13c0a935-26f8-4852-a072-bdb28bc7fa10	GET	f	3
b026a3a7-4f46-4a12-8819-ee3ecaba6553	13c0a935-26f8-4852-a072-bdb28bc7fa10	SHOW DATA	f	4
6ead8d71-c6af-4094-ac13-19eee4d8c017	ff192d35-dd59-4b66-9174-9c6583303086	Все столбцы всех строк таблицы students	t	1
23de8d96-d7c3-406d-858b-71878183be29	ff192d35-dd59-4b66-9174-9c6583303086	Только первую строку	f	2
b39e2ac8-a4f1-49df-8b86-a1e5a27bee83	ff192d35-dd59-4b66-9174-9c6583303086	Только названия столбцов	f	3
31694ea2-420b-449f-8070-a732b5d73fee	ff192d35-dd59-4b66-9174-9c6583303086	Ничего не вернёт	f	4
5713261b-0c9c-4f3f-ab80-f976a4136a34	c39985e7-39de-4642-adb4-85e537180625	Отобрать только строки, удовлетворяющие условию	t	1
4c22e480-6812-4b94-b74a-fdc6923648a7	c39985e7-39de-4642-adb4-85e537180625	Удалить таблицу	f	2
e71d41ff-369c-410a-b806-5ec30adf7f7f	c39985e7-39de-4642-adb4-85e537180625	Создать новый столбец	f	3
21777e3a-8ce3-4676-b64e-f5598b0d047b	c39985e7-39de-4642-adb4-85e537180625	Соединить две базы данных	f	4
0ab00000-0000-0000-0000-000000000008	0ba00000-0000-0000-0000-000000000003	Стопка тетрадей на столе	f	2
bbf75fee-5207-43c0-8c1b-d89d79d52eb5	2f587621-79fd-454a-8024-8707d781a4c1	Чтобы отобрать только строки, удовлетворяющие условию	t	1
0be46289-12e4-4cfe-8713-46629b0d2894	2f587621-79fd-454a-8024-8707d781a4c1	Чтобы создать новую таблицу	f	2
2d6ab8f7-b3e4-4d00-81e2-0528bc43dfd4	2f587621-79fd-454a-8024-8707d781a4c1	Чтобы задать тип данных столбца	f	3
36948687-009f-4419-91f3-62ee7fba403d	2f587621-79fd-454a-8024-8707d781a4c1	Чтобы удалить базу данных	f	4
3ab81c8c-dab4-4173-8714-8606a505f10f	f09ee98f-8cc6-4b24-bd38-5935d0708a48	В одинарных кавычках: 'Б-101'	t	1
bba34441-6a09-4a06-a525-c9747bd0b524	f09ee98f-8cc6-4b24-bd38-5935d0708a48	В двойных кавычках: "Б-101"	f	2
7742a368-79e4-4e78-ac0b-74da467497ed	f09ee98f-8cc6-4b24-bd38-5935d0708a48	Без кавычек: Б-101	f	3
2f7555ff-70b5-44bd-9c33-51d23776035b	f09ee98f-8cc6-4b24-bd38-5935d0708a48	В квадратных скобках: [Б-101]	f	4
04263f40-2e73-4ba8-96e8-ee1609e5f8a7	5d13e0bb-d1f1-47be-aeb8-69579afda898	Студентов группы Б-101 с баллом не меньше 60	t	1
ca220719-4fd8-4061-af45-128d15a926f0	5d13e0bb-d1f1-47be-aeb8-69579afda898	Всех, у кого балл ≥ 60, и отдельно всех из Б-101	f	2
65e06762-2da7-4350-8bfd-a533d2cb6007	5d13e0bb-d1f1-47be-aeb8-69579afda898	Только всех студентов группы Б-101	f	3
32913558-3be6-435e-9567-c8eab4cf4ce3	5d13e0bb-d1f1-47be-aeb8-69579afda898	Ошибку: нельзя объединять два условия	f	4
efcb3471-35ea-46da-ab5f-5f3b4a8938be	05ec09c4-7d1c-4ebb-9222-6ffa64f55bff	IN	t	1
9140eeff-572d-43df-b6c2-7c561fb2ae32	05ec09c4-7d1c-4ebb-9222-6ffa64f55bff	LIKE	f	2
56f9c07f-441b-4877-a36a-2376d08b8da6	05ec09c4-7d1c-4ebb-9222-6ffa64f55bff	BETWEEN	f	3
73316d7b-b26d-49d2-b452-ac4a2e24d9fd	05ec09c4-7d1c-4ebb-9222-6ffa64f55bff	IS NULL	f	4
dea2d3e8-0ead-46bd-94b6-a04037572731	93cb2db4-7ba0-4a60-8d92-2a2d18cd691b	WHERE last_seen IS NULL	t	1
7361ca7d-d483-4363-ba99-49ee8987e35f	93cb2db4-7ba0-4a60-8d92-2a2d18cd691b	WHERE last_seen = NULL	f	2
b39bbf3e-ebc8-4b19-b937-ee281c6f6530	93cb2db4-7ba0-4a60-8d92-2a2d18cd691b	WHERE last_seen == NULL	f	3
9520f8c3-12ec-4565-b84a-e8eac9473446	93cb2db4-7ba0-4a60-8d92-2a2d18cd691b	WHERE last_seen = 'пусто'	f	4
d98e8dab-9610-4342-b8a4-bc4dde110b67	906743ba-69ce-4c97-9f9a-b547a0812e61	Сортирует строки по баллу от большего к меньшему	t	1
164b167f-41b3-4eb8-8210-ab44c1e34fe0	906743ba-69ce-4c97-9f9a-b547a0812e61	Оставляет только строки с большим баллом	f	2
40d073ad-c1c0-4094-a5db-74b44c45406c	906743ba-69ce-4c97-9f9a-b547a0812e61	Удаляет столбец xp	f	3
c5e56c61-97c4-40e8-a400-ba97c41dab68	906743ba-69ce-4c97-9f9a-b547a0812e61	Суммирует все баллы	f	4
b1ac3cc4-7632-4bd6-a1d4-a29797c22a8d	55fb5f8c-e0c3-4359-b946-f3de1f352c20	Ограничить число строк в результате	t	1
97c8efb4-66d6-4d5b-b847-1a7b3d16e374	55fb5f8c-e0c3-4359-b946-f3de1f352c20	Задать условие отбора строк	f	2
17bd2b97-1f7d-4abc-8721-753a69123fb7	55fb5f8c-e0c3-4359-b946-f3de1f352c20	Переименовать столбец	f	3
8bf44c7b-7cdc-4f2d-97ff-8ca97baa57af	55fb5f8c-e0c3-4359-b946-f3de1f352c20	Создать индекс	f	4
07df65b8-997d-495d-8974-b711364366df	6ca5ee17-2595-47c7-8ef1-928f96f8b696	ORDER BY xp DESC LIMIT 3	t	1
26bc9368-0d36-4702-91ec-9ad4a1a299a9	6ca5ee17-2595-47c7-8ef1-928f96f8b696	WHERE xp = 3	f	2
0eba387b-4bd3-4ae5-824d-b1c3e74582c2	6ca5ee17-2595-47c7-8ef1-928f96f8b696	LIMIT 3 без сортировки	f	3
6223c3ba-723b-4330-a9fd-6897b8718b1f	6ca5ee17-2595-47c7-8ef1-928f96f8b696	ORDER BY xp ASC LIMIT 3	f	4
4a723743-1b3d-4fc8-b9d9-06ad3c3c5008	3f3b4a1a-af3f-43ba-952a-bb156a125068	Возвращает список групп без повторов	t	1
b8a9b0bc-4df2-4d13-9f61-046abdb973c8	3f3b4a1a-af3f-43ba-952a-bb156a125068	Сортирует группы по алфавиту	f	2
f1856a06-677f-4926-8059-7a145a815daf	3f3b4a1a-af3f-43ba-952a-bb156a125068	Считает количество групп	f	3
9852931e-e6dc-403a-bcf7-d7a53414737c	3f3b4a1a-af3f-43ba-952a-bb156a125068	Удаляет столбец group_name	f	4
6e9b6690-913b-4c1f-91e5-787ad6f121c7	de50745d-f109-4874-93c8-08b1fa8cfdd9	Сначала WHERE, затем ORDER BY, затем LIMIT	t	1
50435915-e2dc-40d9-8182-e307dfe76d29	de50745d-f109-4874-93c8-08b1fa8cfdd9	Сначала LIMIT, затем WHERE	f	2
8c7b5bc8-9010-4572-a851-8022c2a9b0d5	de50745d-f109-4874-93c8-08b1fa8cfdd9	Сначала ORDER BY, затем WHERE	f	3
5b0ac6c2-43b9-47f9-b054-92957b29e1ce	de50745d-f109-4874-93c8-08b1fa8cfdd9	Порядок не имеет значения	f	4
1ddf999f-ac5a-4552-951d-b0fc12bba979	d2cdde62-eb4f-4303-8e54-70a34e4508f0	INSERT	t	1
00e3796e-02e0-4ee2-ab9d-aa547b0e6b06	d2cdde62-eb4f-4303-8e54-70a34e4508f0	SELECT	f	2
0d2d5edd-69d5-4c13-bda2-294d68f272bf	d2cdde62-eb4f-4303-8e54-70a34e4508f0	UPDATE	f	3
809541bd-63d7-4b8b-9c7c-0908f7c32901	d2cdde62-eb4f-4303-8e54-70a34e4508f0	CREATE	f	4
3705445a-f07e-4f6a-8224-99b4d3e6cde8	1f4fff6f-347c-45bc-bb7b-2efdb318138c	Запрос остаётся понятным и не ломается при добавлении новых столбцов	t	1
ec3b5f4b-8192-4623-a352-4cb867a1e65e	1f4fff6f-347c-45bc-bb7b-2efdb318138c	Так данные занимают меньше места	f	2
f566f9d3-c889-4247-94ef-c055acd7379a	1f4fff6f-347c-45bc-bb7b-2efdb318138c	Иначе PostgreSQL не выполнит команду никогда	f	3
8c617406-0f4a-431e-a4ea-14429836d1e8	1f4fff6f-347c-45bc-bb7b-2efdb318138c	Чтобы автоматически отсортировать строки	f	4
b3e3708c-d223-4b44-b5b0-af52a214028b	8b0caabb-904d-4f46-ba08-965a5a149aa3	Перечислить несколько наборов VALUES через запятую	t	1
e837fa21-96cc-4f8d-881e-458cabb21892	8b0caabb-904d-4f46-ba08-965a5a149aa3	Это невозможно, только по одной	f	2
05d07d8b-dcef-4d61-a8fa-49253d565f85	8b0caabb-904d-4f46-ba08-965a5a149aa3	Использовать SELECT вместо INSERT	f	3
a5c837f1-5f93-4972-aee8-47d9f0ee066e	8b0caabb-904d-4f46-ba08-965a5a149aa3	Написать LIMIT	f	4
97c3fbfb-271d-471d-9f28-30df04a4fc10	0d4b2b99-b0d1-41be-a512-8c4652b5f9e9	Можно не указывать — база подставит значение сама	t	1
12d86545-a3dc-4306-8873-484e8bb9cdca	0d4b2b99-b0d1-41be-a512-8c4652b5f9e9	Нужно указывать обязательно вручную	f	2
7f6e8446-dff6-4fc9-83a7-1a8d56cf23ba	0d4b2b99-b0d1-41be-a512-8c4652b5f9e9	Нельзя использовать никогда	f	3
e823493b-d085-419b-af7f-35be8f7a8433	0d4b2b99-b0d1-41be-a512-8c4652b5f9e9	Нужно указать как NULL текстом	f	4
32528044-d26b-4193-bdd7-6d2d5d1eb4f2	a4261771-7e74-4c1c-99c4-79ab04cd7591	Возвращает данные добавленной строки, включая её id	t	1
4ae8584c-cec1-494a-9ea5-4107094b969f	a4261771-7e74-4c1c-99c4-79ab04cd7591	Откатывает добавление	f	2
14dae1d1-5182-483c-bc80-fc6fe97f1e0b	a4261771-7e74-4c1c-99c4-79ab04cd7591	Удаляет добавленную строку	f	3
f2c51bb7-0524-49ae-a911-048d1a108624	a4261771-7e74-4c1c-99c4-79ab04cd7591	Создаёт индекс по id	f	4
2ece23cf-6e14-490b-9108-d5cd7235d5fd	a070ca37-90c9-43d5-ad24-22ad083448c4	UPDATE	t	1
15be7070-aa39-42b4-9e29-08459ffffd2d	a070ca37-90c9-43d5-ad24-22ad083448c4	INSERT	f	2
b390a6aa-e3df-4916-bc8f-1c1355cbf6e4	a070ca37-90c9-43d5-ad24-22ad083448c4	SELECT	f	3
14de1ab7-73ea-49f0-97f9-e29e6b0da97d	a070ca37-90c9-43d5-ad24-22ad083448c4	DROP	f	4
c45e3390-b64f-4d5e-90a5-240ce45ddacc	e239c29f-fd06-4ca6-b894-98d81b15f9e7	Изменение применится ко всем строкам таблицы	t	1
df5b657f-37d5-443a-8283-d92b9636f37e	e239c29f-fd06-4ca6-b894-98d81b15f9e7	Команда не выполнится без ошибки и ничего не изменит	f	2
184d8324-bff2-4f52-b626-805d40bc3fd4	e239c29f-fd06-4ca6-b894-98d81b15f9e7	Изменится только первая строка	f	3
32853149-6bc0-4712-b7b5-0d04c353ce4e	e239c29f-fd06-4ca6-b894-98d81b15f9e7	База автоматически подставит нужное условие	f	4
7d39cd3c-831a-4b2f-95f9-1c75729b45ae	5b2c2fad-ed08-4d6b-8081-94c1e42ba363	Увеличит баллы студента с id = 5 на 10	t	1
a0686e16-7027-4a89-8b0e-3f9f7cc24df7	5b2c2fad-ed08-4d6b-8081-94c1e42ba363	Установит всем студентам ровно 10 баллов	f	2
930c0726-3d0e-41ce-bc9c-ef99fe32bb79	5b2c2fad-ed08-4d6b-8081-94c1e42ba363	Удалит студента с id = 5	f	3
3b58ec5f-ae5f-4052-8567-f42e76feea57	5b2c2fad-ed08-4d6b-8081-94c1e42ba363	Создаст нового студента	f	4
53ea1339-10e0-415d-9f05-9a376a6319b8	d47d5bde-a499-4c73-93b6-c9dfec6c5b58	Выполнить SELECT с тем же WHERE и проверить, какие строки попадут	t	1
2503db6c-bd74-4710-8716-9ce69b5302e2	d47d5bde-a499-4c73-93b6-c9dfec6c5b58	Удалить всю таблицу для надёжности	f	2
f6294bc9-4ddf-4638-8489-63b9326f682e	d47d5bde-a499-4c73-93b6-c9dfec6c5b58	Отключить интернет	f	3
4a9c0013-3ce7-401a-80df-54066c42f327	d47d5bde-a499-4c73-93b6-c9dfec6c5b58	Ничего, DELETE всегда безопасен	f	4
5ae4e158-71f6-43a4-9a96-a5bf54c7e085	a8373ce9-7321-4c08-abbe-edc464b45e41	Чтобы можно было отменить изменения, если что-то пошло не так	t	1
7bb68f35-c342-4c8e-b2b5-a49519e3f170	a8373ce9-7321-4c08-abbe-edc464b45e41	Чтобы ускорить SELECT	f	2
14c0d993-3335-44fe-ae0d-1d8f2f4178fe	a8373ce9-7321-4c08-abbe-edc464b45e41	Чтобы создать индекс	f	3
382490a1-415f-41e2-8527-da0c7551c7fd	a8373ce9-7321-4c08-abbe-edc464b45e41	Чтобы перевести таблицу в 1НФ	f	4
f98b78bd-8e07-429b-9734-ccf4c046ac3d	411968e1-2e18-40f4-90fb-e1f3bee1d16b	Вычисляет среднее значение баллов	t	1
1f6d8c26-a697-40f4-853b-a9fa59ed872f	411968e1-2e18-40f4-90fb-e1f3bee1d16b	Находит максимальный балл	f	2
4e3384e2-65c0-4388-81a2-e8dabbe52b1f	411968e1-2e18-40f4-90fb-e1f3bee1d16b	Считает количество строк	f	3
1aadb7e1-a12a-4855-8f3d-d98a0df0b130	411968e1-2e18-40f4-90fb-e1f3bee1d16b	Суммирует баллы	f	4
b6ae8760-6543-4885-8b76-80c7e2112690	8fe277ac-2405-4bbe-b58b-a2d427c5d0df	COUNT(*) считает все строки, COUNT(столбец) — только строки с непустым значением	t	1
4ec6f9e8-87fd-40e9-8c24-7ee6eee45609	8fe277ac-2405-4bbe-b58b-a2d427c5d0df	Это полностью одно и то же	f	2
ad828f1b-ecda-4fc7-942a-2fc88a363b5c	8fe277ac-2405-4bbe-b58b-a2d427c5d0df	COUNT(*) считает только пустые строки	f	3
c79f6ea3-1695-4b26-a77a-dc818488f0fc	8fe277ac-2405-4bbe-b58b-a2d427c5d0df	COUNT(столбец) суммирует значения	f	4
13ad5ca5-0b6e-40ef-80bb-5f4fa9784a77	41920440-682d-4da1-8adc-b2a54f245706	Число различных групп	t	1
2442b846-2046-4270-a7c5-48f1821b8ace	41920440-682d-4da1-8adc-b2a54f245706	Общее число студентов	f	2
1009d822-8837-4155-b8ad-c13981aa2298	41920440-682d-4da1-8adc-b2a54f245706	Список всех групп	f	3
da3a77a5-425b-47a9-a00d-60a03e4d3c8a	41920440-682d-4da1-8adc-b2a54f245706	Среднее по группам	f	4
a6e20da9-7595-4fe3-99e6-9fcb1d5e7172	30394892-b435-4ff9-9b5f-328e10817a63	Чтобы дать результату понятное имя столбца	t	1
e3ca02e8-aeef-4e63-8fb0-19c72b97f27a	30394892-b435-4ff9-9b5f-328e10817a63	Чтобы ускорить вычисление	f	2
01c7ade1-fad7-44e5-8f60-5caeba62fd00	30394892-b435-4ff9-9b5f-328e10817a63	Чтобы отсортировать результат	f	3
200071ac-ef48-42cb-9d75-bc3d1b7191a6	30394892-b435-4ff9-9b5f-328e10817a63	Чтобы отфильтровать строки	f	4
edfed71a-fcf1-44c4-a1a8-96c5d210a489	e6d347cc-2ddb-4b6c-8c8f-b005660ea176	Одну строку с итоговым значением	t	1
381d4dc2-966c-419d-a108-bd6182c35c13	e6d347cc-2ddb-4b6c-8c8f-b005660ea176	Столько же, сколько строк в таблице	f	2
abc9ea1d-8c9d-42c9-873d-a2115089fc65	e6d347cc-2ddb-4b6c-8c8f-b005660ea176	Ни одной	f	3
ee90bebe-0fbd-4e68-8133-0d40a34d2e92	e6d347cc-2ddb-4b6c-8c8f-b005660ea176	По одной на каждую группу	f	4
c6ac3101-ce97-4051-b41b-9792bed14f8e	38407d26-9f17-4dbf-88ed-83daca46f8c7	Делит строки на группы по значению group_name для подсчёта итогов в каждой	t	1
1a13f6d8-936f-45de-a151-ec73d2e665a0	38407d26-9f17-4dbf-88ed-83daca46f8c7	Сортирует строки по group_name	f	2
a68cdfb7-a148-4ffe-801b-aeaf47a09dba	38407d26-9f17-4dbf-88ed-83daca46f8c7	Удаляет столбец group_name	f	3
228a3d3e-b145-41be-9cba-93581aeeaa52	38407d26-9f17-4dbf-88ed-83daca46f8c7	Оставляет только одну группу	f	4
cb0dcc27-89bc-45f0-ae2e-dfc305b4676d	cbfbacdb-2e37-417b-83f8-f471a17d2945	Сам group_name и агрегатные функции (COUNT, AVG и т.п.)	t	1
cf4151bf-12e7-48ec-b8b2-f19ff241a775	cbfbacdb-2e37-417b-83f8-f471a17d2945	Любые столбцы таблицы без ограничений	f	2
f8141e37-ed31-4fa6-8b36-a1a32dea24f0	cbfbacdb-2e37-417b-83f8-f471a17d2945	Только full_name	f	3
ed1ff4fe-e420-486d-977a-16f7b8890144	cbfbacdb-2e37-417b-83f8-f471a17d2945	Только id	f	4
2f65adae-f215-4b54-a9f0-bef23dc03c0e	6e58dec4-f01b-4dbd-b312-a4cff7758276	HAVING фильтрует группы после группировки, WHERE — строки до неё	t	1
4d50c946-e9df-49e2-bc6d-244313a4cf70	6e58dec4-f01b-4dbd-b312-a4cff7758276	Это одно и то же	f	2
e3139519-9486-4f47-8ccb-a685a9466827	6e58dec4-f01b-4dbd-b312-a4cff7758276	HAVING фильтрует строки, WHERE — группы	f	3
79fe5171-2931-4a40-9171-8d25689c5e1f	6e58dec4-f01b-4dbd-b312-a4cff7758276	HAVING используется только без GROUP BY	f	4
e7990d84-6ce8-4a56-94c2-320a33d38fa7	d54a7e5a-8791-45c3-9043-648f5493703a	Группы, у которых средний балл меньше 50	t	1
d54a8c6e-0925-4aaf-ad79-a05b3267eaad	d54a7e5a-8791-45c3-9043-648f5493703a	Студентов с баллом меньше 50	f	2
b49bcf9d-2dac-4580-8f4d-1765ad4fa322	d54a7e5a-8791-45c3-9043-648f5493703a	Все группы без исключения	f	3
43ee7c78-2415-4526-80e4-f537a639bf2e	d54a7e5a-8791-45c3-9043-648f5493703a	Одну строку с общим средним	f	4
9e323325-9174-40e7-9301-8d09920b94b3	27e9581c-bfd4-4bbf-9ca2-edf66eb9b944	WHERE → GROUP BY → HAVING	t	1
1b213381-5578-474d-8771-711156eafc48	27e9581c-bfd4-4bbf-9ca2-edf66eb9b944	HAVING → GROUP BY → WHERE	f	2
9200c06a-0612-486c-a28e-046a03e9872d	27e9581c-bfd4-4bbf-9ca2-edf66eb9b944	GROUP BY → WHERE → HAVING	f	3
90f2a3dd-635b-423d-81a0-c35a543e2921	27e9581c-bfd4-4bbf-9ca2-edf66eb9b944	Порядок не важен	f	4
f335de58-dc41-4f77-9382-43249d55a935	8143f4cb-b1f6-44f2-80f2-7affc223d8ec	Чтобы показать вместе данные из нескольких связанных таблиц	t	1
f0bdd2ca-8173-4fe8-80e0-be501753c2cb	8143f4cb-b1f6-44f2-80f2-7affc223d8ec	Чтобы удалить таблицу	f	2
59d8d977-7ae0-4dc6-9694-3ecc34c10ac1	8143f4cb-b1f6-44f2-80f2-7affc223d8ec	Чтобы отсортировать строки	f	3
76e46ca9-6f49-4da9-bbed-7955ad86ff6c	8143f4cb-b1f6-44f2-80f2-7affc223d8ec	Чтобы создать индекс	f	4
13bd490c-3125-4594-b8d0-7256b87a19e5	54b440d7-9115-407c-9d88-91291e5f6371	Только строки, для которых нашлась пара по условию ON	t	1
722f2818-4958-45f4-9486-9a33e0e71b6e	54b440d7-9115-407c-9d88-91291e5f6371	Все строки обеих таблиц без исключения	f	2
70289188-4060-4433-8878-842eaf7a5029	54b440d7-9115-407c-9d88-91291e5f6371	Все строки левой таблицы	f	3
8108302f-59a4-41bd-8542-4f1326e0c314	54b440d7-9115-407c-9d88-91291e5f6371	Только строки без совпадений	f	4
bda68a4d-d94f-4aaf-b314-c62b06bb1825	3a9d1967-27f3-48d6-a485-43b63d3915b8	Связь ключей, например g.student_id = s.id	t	1
6c5550cd-4ce9-4ca7-a990-bdfe377b4b75	3a9d1967-27f3-48d6-a485-43b63d3915b8	Название новой таблицы	f	2
a3d4f13f-e477-4e2c-821b-53f0ca6c6032	3a9d1967-27f3-48d6-a485-43b63d3915b8	Список столбцов для вывода	f	3
902702a8-9d48-4fd1-af6f-1bf4622324dc	3a9d1967-27f3-48d6-a485-43b63d3915b8	Количество строк	f	4
b66bbaeb-ea04-42bb-a0b3-c72cb65ecce9	828140f3-b07e-4941-bf59-03eff42b11e3	Чтобы коротко и однозначно обращаться к столбцам разных таблиц	t	1
2052c5c0-5ee7-4c56-bb9f-d7199f3b8b3d	828140f3-b07e-4941-bf59-03eff42b11e3	Чтобы удалить лишние строки	f	2
b0c1c2df-2768-4397-980c-d9d7a72a9c3c	828140f3-b07e-4941-bf59-03eff42b11e3	Чтобы ускорить INSERT	f	3
2854c62f-eba3-4f8d-9106-67333415b02b	828140f3-b07e-4941-bf59-03eff42b11e3	Это обязательное имя файла	f	4
27ffd554-4fae-40fc-98aa-be6a9fae4752	d1e62523-810b-4577-b4ae-89fdca1d9d01	Нет, ведь для неё нет совпадающей строки	t	1
5f07b01e-d1a7-487f-83ff-68451105f220	d1e62523-810b-4577-b4ae-89fdca1d9d01	Да, с пустыми (NULL) оценками	f	2
53c3dff2-6f5b-434d-9f6d-d50181de7bfe	d1e62523-810b-4577-b4ae-89fdca1d9d01	Да, продублируется несколько раз	f	3
af652f96-2e3f-468d-9006-114b60168ef3	d1e62523-810b-4577-b4ae-89fdca1d9d01	Запрос завершится ошибкой	f	4
12f28e30-6be1-42fb-bbad-b67e1984c7a5	40e6c47f-5fbe-4ad3-8446-6d2a289cdc34	Берёт все строки левой таблицы, подставляя данные правой или NULL	t	1
df4656d1-2f8f-4805-b321-9ca0825410a3	40e6c47f-5fbe-4ad3-8446-6d2a289cdc34	Оставляет только совпавшие строки	f	2
a5fda49f-2f14-4b67-9047-f362f44979d1	40e6c47f-5fbe-4ad3-8446-6d2a289cdc34	Берёт все строки правой таблицы	f	3
f596083b-9d9b-457f-b384-40701cb26e86	40e6c47f-5fbe-4ad3-8446-6d2a289cdc34	Удаляет строки без пары	f	4
30a9baac-2814-4deb-811c-0b5ebc9ac45c	635c7305-f0f9-4852-a7ea-199f0e09adfb	Значением NULL	t	1
c19d658c-ed0a-4fd5-969a-86bd7c3e3b5f	635c7305-f0f9-4852-a7ea-199f0e09adfb	Нулём 0	f	2
a47fb3b2-2502-44c2-9744-c01a8aa250ed	635c7305-f0f9-4852-a7ea-199f0e09adfb	Пустым текстом, который нельзя отличить от значения	f	3
cf05c311-6159-412d-9f5c-8fecd86488b3	635c7305-f0f9-4852-a7ea-199f0e09adfb	Строка просто исчезнет	f	4
3a57afb5-3db3-48f3-8078-94cd434bb199	593fa247-4127-4274-817b-b92db3f368fb	LEFT JOIN со grades и условие WHERE g.id IS NULL	t	1
e87cf502-ae8b-41ff-bd76-b8b01022c6fa	593fa247-4127-4274-817b-b92db3f368fb	INNER JOIN со grades	f	2
273125fc-a953-4d17-869d-6b351a27b9ac	593fa247-4127-4274-817b-b92db3f368fb	Просто SELECT * FROM students	f	3
a31a3087-d8bd-4a90-8eb0-2866e605c145	593fa247-4127-4274-817b-b92db3f368fb	GROUP BY без условий	f	4
320b0412-f0ce-4016-ae8a-2a74e2c99654	f96be62a-fa21-4ce0-b527-0e16798654c9	FULL JOIN	t	1
5df227d7-766a-4117-8d88-e2d32bec591c	f96be62a-fa21-4ce0-b527-0e16798654c9	INNER JOIN	f	2
80bc2bf8-5eb4-4dad-bbfd-ff99370c56de	f96be62a-fa21-4ce0-b527-0e16798654c9	LEFT JOIN	f	3
0a5b5510-7c4d-4743-bd26-d5f02415f0dc	f96be62a-fa21-4ce0-b527-0e16798654c9	Такого соединения нет	f	4
01ee0c77-13d2-4ea5-84b0-57ebedd4f625	fba5ca96-cf9f-4358-85f7-f81b60ac7f8e	Когда нужны только связанные данные, а «пустые» случаи не интересны	t	1
4eac19a7-0c56-494b-bef7-7a1708f51058	fba5ca96-cf9f-4358-85f7-f81b60ac7f8e	Когда нужно показать студентов без оценок	f	2
e9ab4b3e-b417-46b1-895d-3ae3dddfef89	fba5ca96-cf9f-4358-85f7-f81b60ac7f8e	Когда таблица всего одна	f	3
06dcff8e-8eb4-4be8-a69f-9d9a8cdce226	fba5ca96-cf9f-4358-85f7-f81b60ac7f8e	INNER JOIN не используют никогда	f	4
dd1c90d5-83e3-44bd-8983-ad41ad80051d	4ec9a30e-b191-4a48-847a-fa8aad000416	Набор правил, как разложить данные по таблицам без избыточности	t	1
b6865b1b-0ced-40cc-85cc-da779d6b5032	4ec9a30e-b191-4a48-847a-fa8aad000416	Команда удаления таблицы	f	2
fd47d26a-9834-4b6f-ba09-00c214c7172a	4ec9a30e-b191-4a48-847a-fa8aad000416	Способ сортировки строк	f	3
9909723f-4000-4d8d-a925-25c43f3b9cd5	4ec9a30e-b191-4a48-847a-fa8aad000416	Тип данных для чисел	f	4
f2ba6d71-72bc-456f-8624-9c1f9afe6093	0201f609-7035-4379-8421-2fb22e54c165	Список из нескольких значений в одной ячейке	t	1
b5197755-906d-4854-b029-f31c9784b6ee	0201f609-7035-4379-8421-2fb22e54c165	Наличие первичного ключа	f	2
dd2eb234-9e56-49f9-b9c3-f002277fd220	0201f609-7035-4379-8421-2fb22e54c165	Использование внешнего ключа	f	3
d2737db7-8af1-405b-a7c4-3d5d827842c1	0201f609-7035-4379-8421-2fb22e54c165	Сортировка строк	f	4
4cd0dcef-28e5-4418-91b5-65f149b9730b	c3881aa8-41b0-4988-90c3-e5e4490e8884	Повторяющиеся данные приходится править во многих местах, рискуя пропустить	t	1
16ae1430-cf67-40cb-b0b9-400561034ac5	c3881aa8-41b0-4988-90c3-e5e4490e8884	Невозможность отсортировать таблицу	f	2
e8a678c1-f6ef-446f-8888-d5731c999507	c3881aa8-41b0-4988-90c3-e5e4490e8884	Ошибка подключения к базе	f	3
cf5b3f3f-254b-4217-b6c3-ef7c71c7ac9a	c3881aa8-41b0-4988-90c3-e5e4490e8884	Слишком быстрый запрос	f	4
1ec9b174-3b81-4e22-aace-72dbff5e0334	2ac33c62-2141-44a4-8e2d-51d4651df661	Она порождает аномалии и противоречия в данных	t	1
e924ea33-aeb4-4900-aa82-b1c394dc8a91	2ac33c62-2141-44a4-8e2d-51d4651df661	Она всегда ускоряет запросы	f	2
5ee7097e-b54d-4b5f-a71d-9094b135e83c	2ac33c62-2141-44a4-8e2d-51d4651df661	Она уменьшает размер базы	f	3
4126c66a-6b53-407b-9cb0-ab98bb9a5462	2ac33c62-2141-44a4-8e2d-51d4651df661	Она ни на что не влияет	f	4
f23e8a91-0805-4974-ac43-a1bdc1f193e0	4374d4d0-5378-4fc3-9747-19903d4edb11	Одно неделимое значение, а не список	t	1
b7f2f821-0735-4e2a-8352-bc03d03ddeff	4374d4d0-5378-4fc3-9747-19903d4edb11	Очень большое число	f	2
cbf9d5b3-ae71-4629-817c-49bc13a3ff2b	4374d4d0-5378-4fc3-9747-19903d4edb11	Значение, которое нельзя изменить	f	3
e8c42989-de5c-461e-9e93-b5ce30623951	4374d4d0-5378-4fc3-9747-19903d4edb11	Зашифрованный текст	f	4
5dbf43e3-ba33-474c-bf88-6c5d6872e544	ecbb9e8c-3775-49bd-8450-456725f26934	Когда первичный ключ составной (из нескольких столбцов)	t	1
92b8a253-916e-46c5-aa4c-a0fe9df1c926	ecbb9e8c-3775-49bd-8450-456725f26934	Только когда в таблице нет ключа	f	2
02ea9bc6-ff8a-48a6-8c67-c99b63734f17	ecbb9e8c-3775-49bd-8450-456725f26934	Когда в таблице одна строка	f	3
fe96f413-ad38-40b1-8967-0b5fe9a2c6bf	ecbb9e8c-3775-49bd-8450-456725f26934	2НФ не связана с ключом	f	4
e5162635-119b-4664-a397-4a6413f24d96	fae4743d-b137-4122-b867-6b7d20b1a762	Транзитивные зависимости — когда неключевой столбец зависит от другого неключевого	t	1
d205e00b-bf69-4bb5-b487-b2a89e5e38af	fae4743d-b137-4122-b867-6b7d20b1a762	Первичные ключи	f	2
7d886d61-90e9-4b97-9631-d091228b2120	fae4743d-b137-4122-b867-6b7d20b1a762	Все связи между таблицами	f	3
ff133079-1094-4ddd-8992-0b46e24f60b2	fae4743d-b137-4122-b867-6b7d20b1a762	Сортировку данных	f	4
5d876f69-a6b7-4f4c-8dd4-eb4d572a7b47	9fd151d7-9afd-486a-8833-df32634a60d9	Вынести группу с куратором в отдельную таблицу, а в студентах оставить ссылку	t	1
315147f6-2278-45c5-9d10-932f1716a3a1	9fd151d7-9afd-486a-8833-df32634a60d9	Удалить столбец «группа»	f	2
e3c53b5c-35b8-4290-a49a-6dcf7a8d598c	9fd151d7-9afd-486a-8833-df32634a60d9	Записать куратора списком в одну ячейку	f	3
b8bdf9bb-81dd-44e5-be80-c732a02201f0	9fd151d7-9afd-486a-8833-df32634a60d9	Ничего не делать — это нормально	f	4
ce27799f-7768-4c54-8b55-2ba06814953c	b8656a4b-aadb-4109-b473-35a6d895ba8b	Каждый факт хранится один раз, поэтому изменение делается в одном месте	t	1
fecfec0a-9454-4c25-bf86-cb315b40e107	b8656a4b-aadb-4109-b473-35a6d895ba8b	Данные всегда занимают больше места	f	2
65d3837c-a235-4c82-af00-4e60393f6f88	b8656a4b-aadb-4109-b473-35a6d895ba8b	Запросы становятся невозможны	f	3
83c5d3a2-1958-491e-a36c-6b44dac455ce	b8656a4b-aadb-4109-b473-35a6d895ba8b	Не нужны первичные ключи	f	4
f8add678-ec86-4c48-84f2-e1572194842c	de0187e9-f36d-4a11-8f05-dc679a7afab1	Осознанный отказ от части нормализации ради скорости в нагруженных системах	t	1
f907fdf5-ad3c-4146-8f4f-cde8ea4c6c33	de0187e9-f36d-4a11-8f05-dc679a7afab1	Ошибка проектирования, которую нельзя допускать никогда	f	2
68769571-4850-4b9e-9414-a845af150ec8	de0187e9-f36d-4a11-8f05-dc679a7afab1	Синоним первой нормальной формы	f	3
77329cfa-ed1c-4c78-b128-5a15b2a8c041	de0187e9-f36d-4a11-8f05-dc679a7afab1	Команда SQL	f	4
481710b2-4751-47bb-8c95-1e99b27e0962	c825b791-73ad-440d-b906-e0a969c250c9	Значение уникально и не пустое, однозначно определяет строку	t	1
63b83c82-efd0-4356-b63f-6065047ab104	c825b791-73ad-440d-b906-e0a969c250c9	Значение может повторяться	f	2
9129fb7a-bb4e-4f0d-bed9-3ae1e3f51a3b	c825b791-73ad-440d-b906-e0a969c250c9	Поле можно оставлять пустым	f	3
40c62120-5fcf-4cc5-95bb-61478393986e	c825b791-73ad-440d-b906-e0a969c250c9	Столбец хранит только текст	f	4
6b367208-22c9-4c81-9e2b-f92a855e8c22	abedd9bf-4174-42a1-a242-014995d2f7aa	Требует, чтобы поле было обязательно заполнено	t	1
4e0b027d-9f30-469d-8805-ef753633c8d6	abedd9bf-4174-42a1-a242-014995d2f7aa	Запрещает дубликаты	f	2
df6e486a-f670-4513-aeac-1d1281936e2d	abedd9bf-4174-42a1-a242-014995d2f7aa	Удаляет пустые строки	f	3
9ba28c74-2ccd-45e3-9a40-eecf837c59f8	abedd9bf-4174-42a1-a242-014995d2f7aa	Ускоряет поиск	f	4
74f113c5-5ff4-4892-819a-066ae5e0e061	7ffc08ac-6d90-447b-98d3-3e7a36bb3ba6	Чтобы ссылка вела только на реально существующую строку другой таблицы	t	1
a248bfae-11dd-4c5d-9f39-045bd3c07e48	7ffc08ac-6d90-447b-98d3-3e7a36bb3ba6	Чтобы зашифровать данные	f	2
d13f3b51-bf89-47b1-9ca8-99c8ec63fbad	7ffc08ac-6d90-447b-98d3-3e7a36bb3ba6	Чтобы отсортировать таблицу	f	3
dc0fa116-190c-4391-9d1b-d13bcd21cc6f	7ffc08ac-6d90-447b-98d3-3e7a36bb3ba6	Чтобы хранить картинки	f	4
252d7422-527a-4284-b0bc-9889567b91d4	52a765d7-07f7-4a86-950a-19eac1bca3a7	При удалении родительской строки удаляются и связанные с ней строки	t	1
d784f6cf-d392-479c-8740-9a59f4986eb5	52a765d7-07f7-4a86-950a-19eac1bca3a7	Запрещает любое удаление	f	2
448ee382-addd-425f-9f9a-c64f8ad9c6e5	52a765d7-07f7-4a86-950a-19eac1bca3a7	Создаёт резервную копию	f	3
ce3f2e90-12cd-42b1-a8f7-c4aee032ea0c	52a765d7-07f7-4a86-950a-19eac1bca3a7	Обнуляет все баллы	f	4
98344f24-e407-4bbb-857e-26df31586a4b	87b7c455-7b1a-42ff-8d59-c4613cc9d5cc	Тогда их нельзя случайно обойти, с какой бы стороны ни пришли данные	t	1
902ca912-acef-4cf0-a68b-fc97337041bf	87b7c455-7b1a-42ff-8d59-c4613cc9d5cc	Потому что в программе это невозможно	f	2
fd62144d-6eb7-4bdf-a7c6-b5df01c0d0e2	87b7c455-7b1a-42ff-8d59-c4613cc9d5cc	Чтобы база занимала меньше места	f	3
5e496ed5-3a1f-45ae-ae61-c3afb25c6a7b	87b7c455-7b1a-42ff-8d59-c4613cc9d5cc	Это не имеет значения	f	4
cb37a9db-e81a-4ab1-8857-de003faa5d11	fc56d41d-e7d6-45c2-8fb4-98c69163a111	Вспомогательная структура для быстрого поиска строк, как алфавитный указатель	t	1
ba7c0bac-5df0-4e15-a2d8-62a0781301dc	fc56d41d-e7d6-45c2-8fb4-98c69163a111	Копия всей таблицы	f	2
4f8ba1f1-6da0-4563-a2c5-45a878dbc6da	fc56d41d-e7d6-45c2-8fb4-98c69163a111	Тип данных для дат	f	3
cc4118a7-e101-4776-ae65-354340c39517	fc56d41d-e7d6-45c2-8fb4-98c69163a111	Команда удаления	f	4
236fb2e8-e30b-48a9-845c-4660fad92cf9	37074ade-642b-4419-98db-f2e6101082db	По которым часто идёт поиск (WHERE) или соединение (JOIN)	t	1
3f7a9f23-0df8-4851-86a8-517369c949ad	37074ade-642b-4419-98db-f2e6101082db	Для всех столбцов без исключения	f	2
e5984c42-d70c-4e89-9e4e-bb5fa3364dc7	37074ade-642b-4419-98db-f2e6101082db	Только для пустых столбцов	f	3
8e1c92c3-bd85-48ff-bace-f7d1817d210d	37074ade-642b-4419-98db-f2e6101082db	Индексы бесполезны	f	4
658f3ed1-821c-4c90-8f1e-ce76bf440667	6c924639-70a8-4bdb-807d-682912f4bd3e	Он занимает место и немного замедляет добавление/изменение строк	t	1
2c94ee24-c5a4-48aa-9322-f87e16ed9b92	6c924639-70a8-4bdb-807d-682912f4bd3e	Он удаляет данные	f	2
86d1653d-0bea-46e4-849a-1109f655bc16	6c924639-70a8-4bdb-807d-682912f4bd3e	Он замедляет любой SELECT	f	3
0548a157-d165-474b-a35e-780aa4153ece	6c924639-70a8-4bdb-807d-682912f4bd3e	Никаких недостатков нет	f	4
e775175e-9c07-4bb4-8fe1-ce207cae2a1a	4a86e893-9cb9-41b4-9f7b-96f35cc2e9d4	Сохранённый запрос, к которому обращаются как к таблице	t	1
ce4dacf9-8f84-470d-ab82-488bc91149a5	4a86e893-9cb9-41b4-9f7b-96f35cc2e9d4	Резервная копия базы	f	2
dd4da8dd-3974-44f6-9ae4-7ff46032b7ab	4a86e893-9cb9-41b4-9f7b-96f35cc2e9d4	Отдельная физическая таблица с данными	f	3
3b1f0189-cce0-4479-a8b7-12ea57f93e77	4a86e893-9cb9-41b4-9f7b-96f35cc2e9d4	Тип ограничения целостности	f	4
9ade9ecb-fc07-47f2-bf8a-5bc684ad6895	b676a51d-0432-4000-933d-b4283d286b51	Нет, оно каждый раз выполняет заложенный запрос на актуальных данных	t	1
91ce2f9a-793f-4977-b1be-7e6e6219f140	b676a51d-0432-4000-933d-b4283d286b51	Да, оно дублирует все строки таблицы	f	2
fae169ba-cf31-42d0-8e4a-3863616b55ff	b676a51d-0432-4000-933d-b4283d286b51	Да, но только числа	f	3
f168c64f-d4f4-4e1f-b51d-bd28c7cfb7f8	b676a51d-0432-4000-933d-b4283d286b51	Только пока открыт браузер	f	4
62e9fa76-2cc9-4251-9ed4-1a0c77f4cafa	6c206b42-d436-4937-92e8-428266117a87	30 строк — по одной на студента, значения групп повторяются	t	0
450f1e50-14ae-45d9-82da-75dbbc687c4e	6c206b42-d436-4937-92e8-428266117a87	3 строки — по одной на каждую группу	f	1
647c453c-7aad-48ec-af0e-dbb9517c1257	6c206b42-d436-4937-92e8-428266117a87	1 строку со списком всех групп	f	2
24a0530a-e8fc-4706-94e0-1350fc77ef6d	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	Запрос завершится ошибкой	t	0
c3c934f0-3e8e-4c1d-bfae-55524141aa81	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	Столбец вернётся заполненным NULL	f	1
89522908-aaf5-450b-9338-e0ad283b273a	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	Столбец молча пропустится	f	2
c1ac01d7-b683-4d9c-a62e-088fd28b9577	2021684f-ec30-4b62-b24c-b62c0c45d351	SELECT DISTINCT group_name	t	0
3f2ab43f-c0a0-4819-89e0-4a7cbe152e3d	2021684f-ec30-4b62-b24c-b62c0c45d351	SELECT UNIQUE group_name	f	1
c050cde6-141d-4350-9cac-50d309269675	2021684f-ec30-4b62-b24c-b62c0c45d351	SELECT group_name GROUP	f	2
2fc584a7-22ef-4e7a-87a3-0d9046279982	274978a3-7443-4516-98b8-a81a1df46b38	5	t	0
37c4c1af-f3b8-40fa-a0ba-6f59a0f34dfc	274978a3-7443-4516-98b8-a81a1df46b38	25	f	1
b52e4d39-cd0f-4d0c-b272-098210997a4e	274978a3-7443-4516-98b8-a81a1df46b38	0 — со значением NULL нельзя сравнивать	f	2
36b0598e-5b51-43fc-9cbc-4ce4baa74c28	3828b5ec-f126-4eae-bdf8-d159c446f1a9	Сравнение с NULL даёт «неизвестно»; нужно IS NULL	t	0
58ba4889-5e8d-4b61-887a-60ec0bc36a1e	3828b5ec-f126-4eae-bdf8-d159c446f1a9	NULL запрещён в WHERE	f	1
d0a02551-c6f1-4f50-9409-655433ff71da	3828b5ec-f126-4eae-bdf8-d159c446f1a9	Нужно писать avg_grade == NULL	f	2
1a1bbad5-afde-41df-a1db-9ca8b9577330	79129577-4bb9-407a-b75f-59182dfff0ef	Студентов из П-101, а также любых с баллом выше 4	t	0
b6e557d7-140c-47ac-86a3-791b1635d601	79129577-4bb9-407a-b75f-59182dfff0ef	Только студентов П-101 с баллом выше 4	f	1
5c43fea1-0cdc-4d3b-bb72-2fa506e44d65	79129577-4bb9-407a-b75f-59182dfff0ef	Ошибку: нельзя смешивать текст и число	f	2
24a142d7-23a0-4261-996a-ce8166bb67d9	57085e9e-1172-41dd-b553-1b9ede0f45c5	Считает только строки, где avg_grade не NULL	t	0
77f23b6d-99a5-4700-91a1-f8946992dc28	57085e9e-1172-41dd-b553-1b9ede0f45c5	Считает сумму баллов	f	1
dffd400f-3c46-4e3e-8549-31bcfce4b0c2	57085e9e-1172-41dd-b553-1b9ede0f45c5	Всегда даёт то же число, что COUNT(*)	f	2
f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	Одно число — средний балл по всем студентам	t	0
217021c8-68b7-4630-89e5-ec70a9563203	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	Средний балл по каждой группе	f	1
e87ee2b3-f5e6-48f3-8035-9fa5e42f8fea	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	Список баллов по убыванию	f	2
f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	281cbfde-fc59-417c-a26c-a26750c9ffc7	ORDER BY avg_grade DESC	t	0
ab003557-7fd7-46bb-98d3-492bdba0e08a	281cbfde-fc59-417c-a26c-a26750c9ffc7	ORDER BY avg_grade ASC	f	1
7d5746a7-9f2e-46e8-8a6d-29b2da1ccd4c	281cbfde-fc59-417c-a26c-a26750c9ffc7	SORT BY avg_grade DESC	f	2
f8747a4f-5600-43f1-86ff-4fac7588215b	21570212-319a-42d0-a88d-8ef3e848c9a3	Ровно один (возможно, составной)	t	0
453d197f-20ce-460e-9b67-6e55dd715291	21570212-319a-42d0-a88d-8ef3e848c9a3	Сколько угодно	f	1
9c399360-cbde-4c3b-a8d3-ca5fbfca6d12	21570212-319a-42d0-a88d-8ef3e848c9a3	Минимум два	f	2
cef7082e-96ff-4942-aebd-e45aca54b15f	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	Через связующую таблицу с двумя внешними ключами	t	0
e90a53ef-d821-4f09-b928-4ae5c282e751	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	Одним внешним ключом на стороне «много»	f	1
ab179f84-5ed8-40e7-b590-680fb6e5e202	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	Полем со списком значений	f	2
1cedecb8-a975-4679-961d-49b4247a4392	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	Ссылочную целостность: нельзя сослаться на несуществующую строку	t	0
b80e3241-ee49-435a-a8f7-c9b5ddc04137	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	Уникальность всех значений столбца	f	1
f25d67d6-f198-4b89-8237-6b626ab08a46	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	Автоматическую сортировку строк	f	2
d601edcb-a678-479f-96ac-b921b4f27b86	bf58f4fa-11a2-4890-8282-de57b6886991	Внешний ключ group_id в таблице студентов	t	0
fa171c36-c41c-4e5d-b145-1c3f77fcede1	bf58f4fa-11a2-4890-8282-de57b6886991	Внешний ключ student_id в таблице групп	f	1
991fef65-8d9f-4811-a00b-15f84b24f3a8	bf58f4fa-11a2-4890-8282-de57b6886991	Отдельная связующая таблица	f	2
04ec336e-74d2-4898-a04f-4996be33f7ec	73961e85-87a7-4e52-9471-a91b87d56b97	Он стабилен и не меняется при изменении данных	t	0
017b9009-282d-4a3c-9310-1e7c68928dfb	73961e85-87a7-4e52-9471-a91b87d56b97	Он занимает больше места и потому надёжнее	f	1
9627142a-4b8a-4e79-ab8a-2bcdf79585b3	73961e85-87a7-4e52-9471-a91b87d56b97	Естественный атрибут нельзя сделать первичным ключом	f	2
863f015a-988a-4c5f-9efc-37304cf1c424	b19b875e-34ef-4803-b1e6-e8830b2216ca	Избыточность данных и аномалии вставки/обновления/удаления	t	0
92d1a13e-06ac-4db6-b317-1a91e4391f70	b19b875e-34ef-4803-b1e6-e8830b2216ca	Медленные запросы на чтение	f	1
aa9e78aa-480e-4cfe-a2e2-8327176d7e54	b19b875e-34ef-4803-b1e6-e8830b2216ca	Необходимость во внешних ключах	f	2
13202b7d-0bbb-4459-9d63-f918a1a55261	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	Первой нормальной формы (1НФ)	t	0
5cb709a7-7ec5-45cd-bf47-8c5ea56f8e20	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	Второй нормальной формы (2НФ)	f	1
6f973f54-84fe-42fd-a743-f023ec4f22ad	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	Третьей нормальной формы (3НФ)	f	2
69242308-35f8-4e56-8e8b-269d5cdd55a3	3faa7ed1-20e7-4584-b567-de45a858e0a6	2НФ	t	0
cb295dbc-99aa-4c5e-beca-ee5f3dc39e85	3faa7ed1-20e7-4584-b567-de45a858e0a6	1НФ	f	1
8993c5a9-f599-4cfc-aa2a-26bf3d3477c8	3faa7ed1-20e7-4584-b567-de45a858e0a6	НФБК	f	2
00c1c0c1-cd9c-4abf-9888-c3d5c955b075	22ddc903-87d8-4ef0-b50d-13815b3a9fea	3НФ	t	0
016e05a0-912b-4850-90ed-0857fa4a1e62	22ddc903-87d8-4ef0-b50d-13815b3a9fea	1НФ	f	1
76c32466-2024-491c-b5aa-416931dd6f0b	22ddc903-87d8-4ef0-b50d-13815b3a9fea	2НФ	f	2
f18d5e8c-630c-4555-b401-de0873bbe2f2	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	Ускорить чтение ценой управляемой избыточности	t	0
50e1b346-b37f-42d4-ac28-f0b8a18c2b17	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	Полностью убрать любое дублирование	f	1
60bb1575-047c-4506-a978-ea723c8c07ce	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	Гарантированно привести таблицы к 3НФ	f	2
05cb713f-b9b1-497d-be3e-3ad20fc857c9	8830c3fa-2dfe-42a7-894c-a57cc1e88598	Операции транзакции применяются целиком или не применяются вовсе	t	0
62b38773-b565-4edc-8ec8-f399af801a9e	8830c3fa-2dfe-42a7-894c-a57cc1e88598	Изменения переживут сбой питания	f	1
6655377b-9918-4b5d-8471-30e5e1b8c7f2	8830c3fa-2dfe-42a7-894c-a57cc1e88598	Параллельные транзакции не мешают друг другу	f	2
f817c18d-be66-4e00-a713-28cf0e4e31bb	1467d970-0d52-4d24-bc46-5a304049b5bf	Read Committed	t	0
ab507cf2-cd48-4576-b074-f878d9e3a00b	1467d970-0d52-4d24-bc46-5a304049b5bf	Serializable	f	1
76af77a9-a087-424f-87e5-2887c32a9e62	1467d970-0d52-4d24-bc46-5a304049b5bf	Read Uncommitted	f	2
49f2f6e4-4adb-4c9b-9afc-7d5ce5c5136e	4fb1ed42-6579-448c-80a9-80d60efa9b55	Чтение не блокирует запись, а запись — чтение	t	0
2470a2df-cc26-4fa5-9fcc-1d773cfaf9aa	4fb1ed42-6579-448c-80a9-80d60efa9b55	Любая запись блокирует всю таблицу	f	1
6aa44620-ff60-4817-9a78-32e883efc5c8	4fb1ed42-6579-448c-80a9-80d60efa9b55	Грязное чтение происходит всегда	f	2
d076c5ed-d8cd-4157-afc8-848fea793c0b	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	Обнаруживает её и откатывает одну из транзакций	t	0
78673371-6661-4907-9a48-d22aa9857733	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	Бесконечно ждёт освобождения ресурса	f	1
77679332-ee59-4a2f-a3b2-72d0fb888b88	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	Завершает работу сервера	f	2
d96f6331-d9e9-40ef-8a4f-e6cd5e484668	b45f71fc-f02a-436c-ad77-c9aff83da125	UPDATE с проверкой version изменил 0 строк	t	0
c8323ac8-56a6-4c22-9645-15b7913a2587	b45f71fc-f02a-436c-ad77-c9aff83da125	Сервер вернул ошибку соединения	f	1
74e35d4d-f5fb-4016-8b61-9dba1d4fe175	b45f71fc-f02a-436c-ad77-c9aff83da125	Строка оказалась удалена	f	2
231a2937-a51d-4be1-bdb6-00a6e480a324	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	Замедляет их — индекс приходится обновлять	t	0
bfba517f-500c-4faa-b635-39767a41f766	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	Ускоряет их	f	1
dbcce211-79c4-4a33-a9b5-c0a9d06173f4	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	Никак не влияет	f	2
5897051d-a091-4aa4-8f52-d7f038c25e85	b06828c8-31f6-4bac-9430-f369e5f104a4	EXPLAIN ANALYZE	t	0
6f7152bc-c1d3-4a6b-8b2f-7634595b8ca3	b06828c8-31f6-4bac-9430-f369e5f104a4	EXPLAIN	f	1
a6f34d13-189b-4d81-97e0-002e1e9a390b	b06828c8-31f6-4bac-9430-f369e5f104a4	ANALYZE	f	2
9eab6b0e-fcff-4f99-9fdb-5ab16949c492	e217a42d-636d-45bc-92ed-addcc56b4db7	LIKE '%абв%' (подстрока в середине)	t	0
c464d94d-fe3c-4300-b86c-ce2bd4ab0b66	e217a42d-636d-45bc-92ed-addcc56b4db7	WHERE x = 5	f	1
d2f6c1dc-44bf-47e4-a3ce-3c9ad41b804f	e217a42d-636d-45bc-92ed-addcc56b4db7	ORDER BY x	f	2
d51b6c5b-9dc0-4828-8d92-58d47a42613b	3b23312f-f34f-41c5-bf90-4cab5989c8af	По group_id и по group_id + avg_grade	t	0
c7a3ede9-4622-49ba-b5fe-f8f10c5704e2	3b23312f-f34f-41c5-bf90-4cab5989c8af	Только по avg_grade	f	1
20d08bde-d080-4552-b0bf-68c01ddd3c38	3b23312f-f34f-41c5-bf90-4cab5989c8af	По любому одному столбцу одинаково	f	2
63efc862-3301-4be7-90b4-3f46866f5962	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	Обновить статистику, по которой планировщик выбирает план	t	0
430bc5c4-c85e-47a1-a886-8933488a6d52	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	Создать индекс на столбце	f	1
559fb3af-81f3-441e-a071-dd5823c8bcec	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	Удалить мёртвые версии строк	f	2
ca7f83e3-da58-45ad-9477-34a657dd2517	094ffddf-f429-4b8c-90e8-cd88d4789eb0	\\dt	t	0
a5ef4eca-9ceb-497c-b77c-5394f43d09bc	094ffddf-f429-4b8c-90e8-cd88d4789eb0	\\l	f	1
33371af1-68cb-4a32-8c42-925a7335611a	094ffddf-f429-4b8c-90e8-cd88d4789eb0	\\timing	f	2
a7b86e42-ab8e-458d-ae1a-17f76ac693c9	03afd3fa-fa28-4953-bff2-cf59386cbc97	numeric	t	0
ff64c464-d464-469f-b1ec-fb90d1190ae3	03afd3fa-fa28-4953-bff2-cf59386cbc97	real	f	1
7a002d80-40f3-48ea-aeb2-a5435c995c6a	03afd3fa-fa28-4953-bff2-cf59386cbc97	text	f	2
be3dcc07-f35e-49b8-9086-852f49b5c71b	3144f678-6efa-4037-a089-53a6484cae43	0, если avg_grade равно NULL, иначе сам avg_grade	t	0
afb852bf-123a-4d42-82db-c5edfd04f7da	3144f678-6efa-4037-a089-53a6484cae43	Округлённый avg_grade	f	1
66848776-896a-4c25-9d40-b7a5ecab33d8	3144f678-6efa-4037-a089-53a6484cae43	Строки, где avg_grade не NULL	f	2
1371a00a-ce79-4e01-bb46-f1c509494dbf	1299e0dd-b153-46a1-8a32-8ec70877a4c6	VIEW не хранит данные, а вычисляет запрос при обращении	t	0
6d28f0ff-533d-44ad-bf97-403bf3ec36d6	1299e0dd-b153-46a1-8a32-8ec70877a4c6	VIEW хранит отдельную копию данных	f	1
f08f23ba-30ae-4e8e-b231-c3209b886104	1299e0dd-b153-46a1-8a32-8ec70877a4c6	К VIEW нельзя обращаться через SELECT	f	2
b93a8812-b244-4aaf-aeba-b527280df2ca	f014541c-9b76-4e6b-bd30-814fb530e34f	Дать имя подзапросу и улучшить читаемость запроса	t	0
ddf8a354-4c82-4958-a058-bf4e4e993939	f014541c-9b76-4e6b-bd30-814fb530e34f	Создать индекс на столбце	f	1
b0e5c195-8711-4c8e-97f2-3f12b74cb605	f014541c-9b76-4e6b-bd30-814fb530e34f	Ускорить вставку данных	f	2
f63a29cf-ca3e-496a-8b17-f0faeb5e4447	1d71b18a-562a-42ed-97d2-b0f515ed8b30	Не схлопывает строки — оставляет все, добавляя вычисленное значение	t	0
9729453f-dd4b-4a2e-addb-d3b54863ae27	1d71b18a-562a-42ed-97d2-b0f515ed8b30	Всегда возвращает ровно одну строку	f	1
a0a14f4c-aa7e-40e8-840d-304b928149b3	1d71b18a-562a-42ed-97d2-b0f515ed8b30	Работает только с числовыми столбцами	f	2
e1afecde-ea6a-4a6a-adeb-07774e82f0e1	0f06a907-24b1-4b9b-8ba8-15b79786445a	Делит строки на секции, считая функцию в каждой отдельно	t	0
4e3c1da7-ec6a-46d4-aa17-566f48ec82e7	0f06a907-24b1-4b9b-8ba8-15b79786445a	Просто сортирует результат	f	1
f70fa6e7-06ce-48d2-9029-3f2cf6c3e3e2	0f06a907-24b1-4b9b-8ba8-15b79786445a	Убирает повторяющиеся строки	f	2
19457b73-3ad5-4b3a-a849-e77631d76312	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	RANK пропускает следующие ранги (1,2,2,4), DENSE_RANK — нет (1,2,2,3)	t	0
f4771f75-66ca-4170-8c2f-b767c967db3b	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	Они всегда дают одинаковый результат	f	1
f80c52b1-70da-47de-ba5f-aa0c1cdaaba3	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	DENSE_RANK всегда выдаёт уникальные номера	f	2
e3679052-478b-46a2-8fed-ac4c402b5242	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	NULL — предыдущей строки нет	t	0
4707570f-3fd3-40f1-b289-0b1b3e50b0e2	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	0	f	1
0ca06928-c4a2-488f-afde-a02dbb255a6a	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	Значение последней строки	f	2
6f4254ba-ecda-4bbd-bdc7-e490e371fa74	24a18078-b33b-41fe-a689-cfa05324c386	Нарастающий итог от начала окна до текущей строки	t	0
3ebb44fc-f015-42d0-9d0d-a2d139679a06	24a18078-b33b-41fe-a689-cfa05324c386	Общую сумму по всей таблице в каждой строке	f	1
45d063e6-8e30-4ef9-a9f1-1884aac1b11f	24a18078-b33b-41fe-a689-cfa05324c386	Сумму только текущей строки	f	2
\.


--
-- Data for Name: answer_submissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.answer_submissions (id, attempt_id, question_id, answer_option_id, text_answer, is_correct) FROM stdin;
ed2e9598-7d10-4d27-b2e6-7765d79e023d	0fb00000-0000-0000-0000-000000000001	0ba00000-0000-0000-0000-000000000001	0ab00000-0000-0000-0000-000000000001	\N	t
dd125d8f-9839-41e1-908e-dd41e0fcaa20	0fb00000-0000-0000-0000-000000000001	0ba00000-0000-0000-0000-000000000002	0ab00000-0000-0000-0000-000000000004	\N	t
56cad97a-89be-4779-9896-4663ca0c1adc	0fb00000-0000-0000-0000-000000000001	0ba00000-0000-0000-0000-000000000003	0ab00000-0000-0000-0000-000000000007	\N	t
545a3b42-9f1c-4354-a9fe-669beacd1af5	0fb00000-0000-0000-0000-000000000001	0ba00000-0000-0000-0000-000000000003	0ab00000-0000-0000-0000-000000000008	\N	t
d9262848-cce5-4ca0-8508-f4f5edbbdd83	1ab4905d-5140-4d01-8660-2714849536c7	0ba00000-0000-0000-0000-000000000001	0ab00000-0000-0000-0000-000000000001	\N	t
d6c02d74-ea69-47d1-ab76-2ba68fcb2a93	1ab4905d-5140-4d01-8660-2714849536c7	0ba00000-0000-0000-0000-000000000002	0ab00000-0000-0000-0000-000000000004	\N	t
14ff9df3-b02f-472f-96d9-f8c91bf5c348	1ab4905d-5140-4d01-8660-2714849536c7	0ba00000-0000-0000-0000-000000000003	0ab00000-0000-0000-0000-000000000007	\N	t
b70be5c1-7599-4e32-80ee-f6bb0ddd3edb	66ab8adf-963b-4912-951c-e3731fedfe5d	0ba00000-0000-0000-0000-000000000001	0ab00000-0000-0000-0000-000000000001	\N	t
e5de909a-fa62-4bdf-81da-e9c6610cb48a	66ab8adf-963b-4912-951c-e3731fedfe5d	0ba00000-0000-0000-0000-000000000002	0ab00000-0000-0000-0000-000000000004	\N	t
ade0bd9b-3b22-496c-ab55-0c0761dd6cef	66ab8adf-963b-4912-951c-e3731fedfe5d	0ba00000-0000-0000-0000-000000000003	0ab00000-0000-0000-0000-000000000007	\N	t
feac8c72-770b-4c45-9d80-a3ffd79d7749	21a5e40e-cc90-40d0-babf-5ce913a335b3	6c206b42-d436-4937-92e8-428266117a87	62e9fa76-2cc9-4251-9ed4-1a0c77f4cafa	\N	t
36ac81fa-ffe9-4ac0-8b14-f1e15debba2a	21a5e40e-cc90-40d0-babf-5ce913a335b3	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
977807cc-18a7-4ab8-9260-e8972998eeab	21a5e40e-cc90-40d0-babf-5ce913a335b3	2021684f-ec30-4b62-b24c-b62c0c45d351	c1ac01d7-b683-4d9c-a62e-088fd28b9577	\N	t
b265c7a3-fe72-455d-8ea4-74e160e3318b	3118f442-68d3-4eb8-8f56-da8493743655	6c206b42-d436-4937-92e8-428266117a87	450f1e50-14ae-45d9-82da-75dbbc687c4e	\N	f
b714ae27-67af-4e6a-8b89-8e13220ff714	3118f442-68d3-4eb8-8f56-da8493743655	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
d5a9bb0d-7383-4aef-bada-bd55abddba2c	3118f442-68d3-4eb8-8f56-da8493743655	2021684f-ec30-4b62-b24c-b62c0c45d351	c050cde6-141d-4350-9cac-50d309269675	\N	f
cbc7bf4c-45b2-4107-a70c-8160f852bcf0	0eff89f0-e4c7-42c3-8803-598be0ba7dd4	6c206b42-d436-4937-92e8-428266117a87	647c453c-7aad-48ec-af0e-dbb9517c1257	\N	f
ad55ffa9-8942-4f3b-b0e3-2fb462fb9c73	0eff89f0-e4c7-42c3-8803-598be0ba7dd4	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
75e4b6f0-98e4-4654-8db1-27a5f26fa7ee	0eff89f0-e4c7-42c3-8803-598be0ba7dd4	2021684f-ec30-4b62-b24c-b62c0c45d351	c1ac01d7-b683-4d9c-a62e-088fd28b9577	\N	t
0c46b5cf-93f6-4f8d-9d09-cb07b092f879	2e4e0e03-9f01-42e3-a944-7d9ead45cc74	6c206b42-d436-4937-92e8-428266117a87	450f1e50-14ae-45d9-82da-75dbbc687c4e	\N	f
f4b8b4f3-b0f8-4864-84f8-740f148da1a4	2e4e0e03-9f01-42e3-a944-7d9ead45cc74	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
5ded989e-65c1-49d9-bb8f-e91e2a61e34f	2e4e0e03-9f01-42e3-a944-7d9ead45cc74	2021684f-ec30-4b62-b24c-b62c0c45d351	c050cde6-141d-4350-9cac-50d309269675	\N	f
c6ecfea3-4034-4520-ac32-cb15fe3d16a2	ba45956c-17cc-42cd-8e51-bd3fbbd5d813	6c206b42-d436-4937-92e8-428266117a87	62e9fa76-2cc9-4251-9ed4-1a0c77f4cafa	\N	t
34d07a3a-071e-4ecd-812f-67d2b59bc6aa	ba45956c-17cc-42cd-8e51-bd3fbbd5d813	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
588711d8-6b29-491f-aab5-d4b4c6ec9f1f	ba45956c-17cc-42cd-8e51-bd3fbbd5d813	2021684f-ec30-4b62-b24c-b62c0c45d351	c1ac01d7-b683-4d9c-a62e-088fd28b9577	\N	t
24af4cf4-24c1-4f59-825b-3f48ea828f09	648d5891-3996-4173-8147-58c8f19ce281	6c206b42-d436-4937-92e8-428266117a87	450f1e50-14ae-45d9-82da-75dbbc687c4e	\N	f
5777013f-5f39-439e-8396-d5a660a1a98d	648d5891-3996-4173-8147-58c8f19ce281	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
2859924d-f96e-4a51-953d-d060626bf68f	648d5891-3996-4173-8147-58c8f19ce281	2021684f-ec30-4b62-b24c-b62c0c45d351	3f2ab43f-c0a0-4819-89e0-4a7cbe152e3d	\N	f
32b3831a-1a0a-4a77-9820-e13b011a928e	e6e446fd-967e-4401-a1ca-f080c59bff0a	6c206b42-d436-4937-92e8-428266117a87	647c453c-7aad-48ec-af0e-dbb9517c1257	\N	f
e2ed1492-3821-460e-94bf-cde886e486be	e6e446fd-967e-4401-a1ca-f080c59bff0a	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	24a0530a-e8fc-4706-94e0-1350fc77ef6d	\N	t
1a83dedf-b989-4dcf-8822-c46d57d2caf5	e6e446fd-967e-4401-a1ca-f080c59bff0a	2021684f-ec30-4b62-b24c-b62c0c45d351	c050cde6-141d-4350-9cac-50d309269675	\N	f
a4a1ac0f-967a-4d94-83f2-2c6b5a3239f1	be305657-8326-45de-9166-8476ac7e02bb	6c206b42-d436-4937-92e8-428266117a87	647c453c-7aad-48ec-af0e-dbb9517c1257	\N	f
7f0b6f97-d7ca-426a-b74d-c020cd1dd390	be305657-8326-45de-9166-8476ac7e02bb	7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	89522908-aaf5-450b-9338-e0ad283b273a	\N	f
f9d05e1c-28b6-400b-8760-d0f85f59bdce	be305657-8326-45de-9166-8476ac7e02bb	2021684f-ec30-4b62-b24c-b62c0c45d351	c1ac01d7-b683-4d9c-a62e-088fd28b9577	\N	t
cb5a3720-9df4-4b13-b8a8-7ea33fc9d227	bc8f4bb1-83ca-4ed3-b297-31b917cb2d94	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
7dc6e830-8ede-49d1-a3d0-368f5fffc1cb	bc8f4bb1-83ca-4ed3-b297-31b917cb2d94	3828b5ec-f126-4eae-bdf8-d159c446f1a9	36b0598e-5b51-43fc-9cbc-4ce4baa74c28	\N	t
c43b784f-52b2-40d2-b3cf-ab3812b8744c	bc8f4bb1-83ca-4ed3-b297-31b917cb2d94	79129577-4bb9-407a-b75f-59182dfff0ef	1a1bbad5-afde-41df-a1db-9ca8b9577330	\N	t
e659c220-2f0b-49a0-87f4-a657834000a2	05c4a323-efc8-4281-bee1-ad8460e03e39	274978a3-7443-4516-98b8-a81a1df46b38	b52e4d39-cd0f-4d0c-b272-098210997a4e	\N	f
8c4489c3-1c4d-48ec-8c53-3375173ca044	05c4a323-efc8-4281-bee1-ad8460e03e39	3828b5ec-f126-4eae-bdf8-d159c446f1a9	d0a02551-c6f1-4f50-9409-655433ff71da	\N	f
3fc91663-679a-4242-b0b3-cb333578077e	05c4a323-efc8-4281-bee1-ad8460e03e39	79129577-4bb9-407a-b75f-59182dfff0ef	b6e557d7-140c-47ac-86a3-791b1635d601	\N	f
962e500b-16a8-4793-836a-59709f731cba	2fb54e31-0a8d-4bdc-b196-e2dcdcf19ea5	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
125b8383-3be0-4584-a5a4-3de46dc4a7f9	2fb54e31-0a8d-4bdc-b196-e2dcdcf19ea5	3828b5ec-f126-4eae-bdf8-d159c446f1a9	58ba4889-5e8d-4b61-887a-60ec0bc36a1e	\N	f
70021e00-f3ba-4ee6-9d02-7789808d0dca	2fb54e31-0a8d-4bdc-b196-e2dcdcf19ea5	79129577-4bb9-407a-b75f-59182dfff0ef	1a1bbad5-afde-41df-a1db-9ca8b9577330	\N	t
4c3e7ac2-c867-44d2-ac7b-2da481d726fb	d4cf5862-076b-46a3-8d57-be286cb32cb6	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
5f414d82-b7ec-4b87-8fe5-26b3ef3f0601	d4cf5862-076b-46a3-8d57-be286cb32cb6	3828b5ec-f126-4eae-bdf8-d159c446f1a9	58ba4889-5e8d-4b61-887a-60ec0bc36a1e	\N	f
76be1ccb-b091-4ef8-a53b-267547159e2b	d4cf5862-076b-46a3-8d57-be286cb32cb6	79129577-4bb9-407a-b75f-59182dfff0ef	b6e557d7-140c-47ac-86a3-791b1635d601	\N	f
f33cc51c-5c02-406a-b56d-dd50ebfc44a7	15442db2-0fdf-461d-87f5-8ef24665e63c	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
a39e5de5-8fe8-4c69-af56-0bb433242c38	15442db2-0fdf-461d-87f5-8ef24665e63c	3828b5ec-f126-4eae-bdf8-d159c446f1a9	d0a02551-c6f1-4f50-9409-655433ff71da	\N	f
aba411c6-847a-4873-b926-17d2496dd4f2	15442db2-0fdf-461d-87f5-8ef24665e63c	79129577-4bb9-407a-b75f-59182dfff0ef	5c43fea1-0cdc-4d3b-bb72-2fa506e44d65	\N	f
7a2cdc6f-c0b1-460b-9a39-83b8b7674bdc	a3233a1e-366f-4f54-8492-363dc9843806	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
ef58efe8-1547-4595-b105-9ed83281c0db	a3233a1e-366f-4f54-8492-363dc9843806	3828b5ec-f126-4eae-bdf8-d159c446f1a9	d0a02551-c6f1-4f50-9409-655433ff71da	\N	f
e80df8ef-d6f3-400a-809e-739b5e35f611	a3233a1e-366f-4f54-8492-363dc9843806	79129577-4bb9-407a-b75f-59182dfff0ef	b6e557d7-140c-47ac-86a3-791b1635d601	\N	f
54405a12-3105-4a0c-943d-02ffd4323131	916bae6d-32b6-4bbf-98db-2d8e632bdf91	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
069a1709-88d5-4c6d-95af-982681a2c388	916bae6d-32b6-4bbf-98db-2d8e632bdf91	3828b5ec-f126-4eae-bdf8-d159c446f1a9	36b0598e-5b51-43fc-9cbc-4ce4baa74c28	\N	t
887a3ae8-63ff-40d3-a49c-f7ec54ee9e37	916bae6d-32b6-4bbf-98db-2d8e632bdf91	79129577-4bb9-407a-b75f-59182dfff0ef	1a1bbad5-afde-41df-a1db-9ca8b9577330	\N	t
607f5735-6baa-4d4e-940b-68434f23d8f2	38663c7f-dae3-4088-bfe9-c088cdff9c93	274978a3-7443-4516-98b8-a81a1df46b38	2fc584a7-22ef-4e7a-87a3-0d9046279982	\N	t
534e8927-65ab-4859-b147-bf87017258ab	38663c7f-dae3-4088-bfe9-c088cdff9c93	3828b5ec-f126-4eae-bdf8-d159c446f1a9	58ba4889-5e8d-4b61-887a-60ec0bc36a1e	\N	f
fdc10a1c-cdd9-402f-868e-0b7331101dab	38663c7f-dae3-4088-bfe9-c088cdff9c93	79129577-4bb9-407a-b75f-59182dfff0ef	5c43fea1-0cdc-4d3b-bb72-2fa506e44d65	\N	f
2f952ee3-e8b1-42da-990f-2cd50a2b489d	0ed8b0cc-3420-440d-ac85-b724791b9b61	57085e9e-1172-41dd-b553-1b9ede0f45c5	dffd400f-3c46-4e3e-8549-31bcfce4b0c2	\N	f
f44e3ee5-5689-49e0-acbf-22bf9b8fd642	0ed8b0cc-3420-440d-ac85-b724791b9b61	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
ee6b03a4-f738-4550-b017-3ba691bd58d2	0ed8b0cc-3420-440d-ac85-b724791b9b61	281cbfde-fc59-417c-a26c-a26750c9ffc7	f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	\N	t
9d9cd309-33ae-4c77-8ca2-ae09902e7e3b	85c00fbd-bb63-4656-b2ed-1d5541635d87	57085e9e-1172-41dd-b553-1b9ede0f45c5	24a142d7-23a0-4261-996a-ce8166bb67d9	\N	t
4ceb6bca-f629-47e2-a549-cddf4bc89569	85c00fbd-bb63-4656-b2ed-1d5541635d87	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
d14a3a15-3ea3-4c05-b6b8-5b25b92d9ee3	85c00fbd-bb63-4656-b2ed-1d5541635d87	281cbfde-fc59-417c-a26c-a26750c9ffc7	f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	\N	t
a2d46521-d97f-4abb-ae86-34766b234b1f	12267ead-50cf-4a3b-a80a-9aaa0fecffd4	57085e9e-1172-41dd-b553-1b9ede0f45c5	24a142d7-23a0-4261-996a-ce8166bb67d9	\N	t
af13c8cd-ac3b-42d5-8121-82eeb4ba4343	12267ead-50cf-4a3b-a80a-9aaa0fecffd4	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
e4899aa6-b356-43c2-b52f-7b6b98c4f630	12267ead-50cf-4a3b-a80a-9aaa0fecffd4	281cbfde-fc59-417c-a26c-a26750c9ffc7	7d5746a7-9f2e-46e8-8a6d-29b2da1ccd4c	\N	f
14fc757d-5125-41d3-898f-72c819968c54	b07973a3-a2bb-490c-a76e-b6fce3f2a316	57085e9e-1172-41dd-b553-1b9ede0f45c5	24a142d7-23a0-4261-996a-ce8166bb67d9	\N	t
4344a8d1-cab3-4baa-a13f-01b9e162197e	b07973a3-a2bb-490c-a76e-b6fce3f2a316	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
0cf0bff8-7b51-429d-b34a-148687aaf461	b07973a3-a2bb-490c-a76e-b6fce3f2a316	281cbfde-fc59-417c-a26c-a26750c9ffc7	7d5746a7-9f2e-46e8-8a6d-29b2da1ccd4c	\N	f
1b65b4b1-5501-45ac-8d83-4eac7f92b387	8da19b6a-2596-4e6f-a1b2-8f7bcf141491	57085e9e-1172-41dd-b553-1b9ede0f45c5	24a142d7-23a0-4261-996a-ce8166bb67d9	\N	t
a4e7fa7a-b28e-41e1-bd56-56a8e65e4c82	8da19b6a-2596-4e6f-a1b2-8f7bcf141491	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
e96dd10d-5808-4d5e-a765-18cd769c3b52	8da19b6a-2596-4e6f-a1b2-8f7bcf141491	281cbfde-fc59-417c-a26c-a26750c9ffc7	f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	\N	t
c0f46287-9f83-4e44-bc1f-06e8297fcb73	d4a91558-0239-4150-a2ea-ed33048ba508	57085e9e-1172-41dd-b553-1b9ede0f45c5	24a142d7-23a0-4261-996a-ce8166bb67d9	\N	t
bb6fbd14-5fb5-42d6-9dab-9ba63a32f998	d4a91558-0239-4150-a2ea-ed33048ba508	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
247eb4cb-30b7-40fc-b162-385a74ce50fa	d4a91558-0239-4150-a2ea-ed33048ba508	281cbfde-fc59-417c-a26c-a26750c9ffc7	f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	\N	t
1249ada3-0228-49f0-99d1-0dd10dc123cf	be5715fc-1a02-4474-b573-bbf2b22bd416	57085e9e-1172-41dd-b553-1b9ede0f45c5	dffd400f-3c46-4e3e-8549-31bcfce4b0c2	\N	f
b0e43f1f-532b-410e-b045-487ffc766418	be5715fc-1a02-4474-b573-bbf2b22bd416	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	f2ef2851-a0d7-4bd1-9e45-aa6d6ec470bd	\N	t
bb69eed8-5b2f-4ead-8dab-56fc4a713fd6	be5715fc-1a02-4474-b573-bbf2b22bd416	281cbfde-fc59-417c-a26c-a26750c9ffc7	f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	\N	t
595db25d-de33-4985-92f1-798b3cfe3300	6c54a6cd-c17c-46bc-ae61-9ec7a226f3e9	57085e9e-1172-41dd-b553-1b9ede0f45c5	24a142d7-23a0-4261-996a-ce8166bb67d9	\N	t
70de9ee2-c6c7-4056-a786-d3c849077447	6c54a6cd-c17c-46bc-ae61-9ec7a226f3e9	8d905a71-a150-4a3d-ae83-dd6619fbf1fb	217021c8-68b7-4630-89e5-ec70a9563203	\N	f
cc53eae5-1600-4e02-9c6a-f44b86e208b0	6c54a6cd-c17c-46bc-ae61-9ec7a226f3e9	281cbfde-fc59-417c-a26c-a26750c9ffc7	f2c881f4-b9ff-4d2d-8554-af6a3cfd48d0	\N	t
91ce5549-a5e7-49b8-8bc5-4fcca52fd5fd	d581ccb3-6f92-4fad-a8f1-35f87215e8e3	21570212-319a-42d0-a88d-8ef3e848c9a3	453d197f-20ce-460e-9b67-6e55dd715291	\N	f
f0026cb3-4391-4575-a61a-4b6d857185c8	d581ccb3-6f92-4fad-a8f1-35f87215e8e3	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	e90a53ef-d821-4f09-b928-4ae5c282e751	\N	f
29c7ef8a-9011-48ad-98a3-23a1a8661aa7	d581ccb3-6f92-4fad-a8f1-35f87215e8e3	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	1cedecb8-a975-4679-961d-49b4247a4392	\N	t
80e4c5ea-9eec-4c44-92f7-fa70f5732146	d581ccb3-6f92-4fad-a8f1-35f87215e8e3	bf58f4fa-11a2-4890-8282-de57b6886991	991fef65-8d9f-4811-a00b-15f84b24f3a8	\N	f
1ddd1de6-7067-47e4-be05-37bbb1e96a22	d581ccb3-6f92-4fad-a8f1-35f87215e8e3	73961e85-87a7-4e52-9471-a91b87d56b97	04ec336e-74d2-4898-a04f-4996be33f7ec	\N	t
beb33d8e-e1fa-4ed0-9777-7dc1af5163b9	bfea2af4-fd2e-40ce-83de-d649c6103e8f	21570212-319a-42d0-a88d-8ef3e848c9a3	f8747a4f-5600-43f1-86ff-4fac7588215b	\N	t
d0ad4eff-0596-46a1-b9ef-cc22818b4a37	bfea2af4-fd2e-40ce-83de-d649c6103e8f	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	cef7082e-96ff-4942-aebd-e45aca54b15f	\N	t
1bfc6ccd-d286-443d-96b3-98b0bfc51bb6	bfea2af4-fd2e-40ce-83de-d649c6103e8f	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	1cedecb8-a975-4679-961d-49b4247a4392	\N	t
70abbfbd-6c5d-40de-8b30-fb707a05b2be	bfea2af4-fd2e-40ce-83de-d649c6103e8f	bf58f4fa-11a2-4890-8282-de57b6886991	fa171c36-c41c-4e5d-b145-1c3f77fcede1	\N	f
4cbc3bf9-878a-43eb-b4e7-0cc8c9e27e8f	bfea2af4-fd2e-40ce-83de-d649c6103e8f	73961e85-87a7-4e52-9471-a91b87d56b97	04ec336e-74d2-4898-a04f-4996be33f7ec	\N	t
c3636d1a-086b-43a4-889d-c469922e78b3	4c5e6452-8f32-4a12-8146-fb734f8b021c	21570212-319a-42d0-a88d-8ef3e848c9a3	453d197f-20ce-460e-9b67-6e55dd715291	\N	f
45d39719-f824-4714-94b2-dd5e9da9b6c8	4c5e6452-8f32-4a12-8146-fb734f8b021c	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	cef7082e-96ff-4942-aebd-e45aca54b15f	\N	t
c89741db-227d-4590-bddd-236724c158d5	4c5e6452-8f32-4a12-8146-fb734f8b021c	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	1cedecb8-a975-4679-961d-49b4247a4392	\N	t
ac6d5a41-7bd0-4ec9-8caf-ad66cd5d412d	4c5e6452-8f32-4a12-8146-fb734f8b021c	bf58f4fa-11a2-4890-8282-de57b6886991	d601edcb-a678-479f-96ac-b921b4f27b86	\N	t
99a000fb-ae1d-47c3-8d2a-cc8ce9b09a1b	4c5e6452-8f32-4a12-8146-fb734f8b021c	73961e85-87a7-4e52-9471-a91b87d56b97	9627142a-4b8a-4e79-ab8a-2bcdf79585b3	\N	f
73034972-28ec-4660-b044-be7950f4e968	496db3f9-e66d-438f-91cd-f9d157af1d91	21570212-319a-42d0-a88d-8ef3e848c9a3	f8747a4f-5600-43f1-86ff-4fac7588215b	\N	t
09f47d37-12db-46c5-9705-8092f2ae7418	496db3f9-e66d-438f-91cd-f9d157af1d91	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	e90a53ef-d821-4f09-b928-4ae5c282e751	\N	f
e9f9b5ae-4c7c-43f2-ae21-93dd04b63a7a	496db3f9-e66d-438f-91cd-f9d157af1d91	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	1cedecb8-a975-4679-961d-49b4247a4392	\N	t
0238d2f3-6ac2-4baa-94cb-0ce753e1dfac	496db3f9-e66d-438f-91cd-f9d157af1d91	bf58f4fa-11a2-4890-8282-de57b6886991	991fef65-8d9f-4811-a00b-15f84b24f3a8	\N	f
d3870b56-9337-4bbf-b81a-b19023bd20b2	496db3f9-e66d-438f-91cd-f9d157af1d91	73961e85-87a7-4e52-9471-a91b87d56b97	017b9009-282d-4a3c-9310-1e7c68928dfb	\N	f
3c3a55a9-5577-499b-b7f3-e8a2a23feeae	f68e9838-1d4a-43b9-90ad-feef347483a0	21570212-319a-42d0-a88d-8ef3e848c9a3	9c399360-cbde-4c3b-a8d3-ca5fbfca6d12	\N	f
507fde71-8d7f-4389-b147-116905efa9e0	f68e9838-1d4a-43b9-90ad-feef347483a0	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	cef7082e-96ff-4942-aebd-e45aca54b15f	\N	t
a6f3a2ed-aa64-4a2a-9f1e-d130cec06d28	f68e9838-1d4a-43b9-90ad-feef347483a0	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	f25d67d6-f198-4b89-8237-6b626ab08a46	\N	f
5be4da49-3b48-4d24-9834-9faf202335a4	f68e9838-1d4a-43b9-90ad-feef347483a0	bf58f4fa-11a2-4890-8282-de57b6886991	d601edcb-a678-479f-96ac-b921b4f27b86	\N	t
7206868e-7291-467c-9c8b-fc5110800abb	f68e9838-1d4a-43b9-90ad-feef347483a0	73961e85-87a7-4e52-9471-a91b87d56b97	04ec336e-74d2-4898-a04f-4996be33f7ec	\N	t
2562f9e9-6642-4b00-afb5-bc13f6d191d4	78828310-33f0-4114-b083-7f35b00e8aad	21570212-319a-42d0-a88d-8ef3e848c9a3	f8747a4f-5600-43f1-86ff-4fac7588215b	\N	t
f47a1fd1-5e8e-460a-bc38-c2d9e8eba06c	78828310-33f0-4114-b083-7f35b00e8aad	d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	ab179f84-5ed8-40e7-b590-680fb6e5e202	\N	f
8dd2c5db-536c-4766-8f76-ac4a3b953edf	78828310-33f0-4114-b083-7f35b00e8aad	5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	1cedecb8-a975-4679-961d-49b4247a4392	\N	t
2f38ff55-047a-4fd5-83fd-8768735acc40	78828310-33f0-4114-b083-7f35b00e8aad	bf58f4fa-11a2-4890-8282-de57b6886991	d601edcb-a678-479f-96ac-b921b4f27b86	\N	t
57a1c0f2-f9e9-44f2-a66c-6e541d130f1b	78828310-33f0-4114-b083-7f35b00e8aad	73961e85-87a7-4e52-9471-a91b87d56b97	9627142a-4b8a-4e79-ab8a-2bcdf79585b3	\N	f
8f8c2d6e-8537-484a-9064-de4665886352	019407f4-2317-464e-88e1-a329b4bd5429	b19b875e-34ef-4803-b1e6-e8830b2216ca	92d1a13e-06ac-4db6-b317-1a91e4391f70	\N	f
6d673f3e-f374-4fdd-a2f1-4f4736fe79e5	019407f4-2317-464e-88e1-a329b4bd5429	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	6f973f54-84fe-42fd-a743-f023ec4f22ad	\N	f
1f4ea092-2d2e-4e62-b78a-ee05d5845c34	019407f4-2317-464e-88e1-a329b4bd5429	3faa7ed1-20e7-4584-b567-de45a858e0a6	cb295dbc-99aa-4c5e-beca-ee5f3dc39e85	\N	f
d51c982e-74bb-4560-930b-8afed423bbf6	019407f4-2317-464e-88e1-a329b4bd5429	22ddc903-87d8-4ef0-b50d-13815b3a9fea	76c32466-2024-491c-b5aa-416931dd6f0b	\N	f
77388db5-d3f3-4f42-ae24-3a8021682c83	019407f4-2317-464e-88e1-a329b4bd5429	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	f18d5e8c-630c-4555-b401-de0873bbe2f2	\N	t
b3b7bbb7-95a0-4ac1-9f17-82a17933a747	24befe89-4b98-41ef-8ebb-0bc7bea3d4d7	b19b875e-34ef-4803-b1e6-e8830b2216ca	92d1a13e-06ac-4db6-b317-1a91e4391f70	\N	f
e4cae8b4-8abb-4d21-9e30-16163aaaad50	24befe89-4b98-41ef-8ebb-0bc7bea3d4d7	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	5cb709a7-7ec5-45cd-bf47-8c5ea56f8e20	\N	f
e3d388ed-9eac-4e1a-ae2f-e6494e5ff296	24befe89-4b98-41ef-8ebb-0bc7bea3d4d7	3faa7ed1-20e7-4584-b567-de45a858e0a6	cb295dbc-99aa-4c5e-beca-ee5f3dc39e85	\N	f
b29f9dc8-da36-4f6e-91e5-c4240dbc9861	24befe89-4b98-41ef-8ebb-0bc7bea3d4d7	22ddc903-87d8-4ef0-b50d-13815b3a9fea	016e05a0-912b-4850-90ed-0857fa4a1e62	\N	f
c05e7599-9d88-4449-b3c7-52ad9c168702	24befe89-4b98-41ef-8ebb-0bc7bea3d4d7	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	60bb1575-047c-4506-a978-ea723c8c07ce	\N	f
cbc1841b-e485-4248-a56d-f1e16b16e0ab	86bb7325-6555-4f31-af51-3d9b8ac3b424	b19b875e-34ef-4803-b1e6-e8830b2216ca	863f015a-988a-4c5f-9efc-37304cf1c424	\N	t
9e26304b-e293-470e-99d5-f96c13d292ab	86bb7325-6555-4f31-af51-3d9b8ac3b424	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	13202b7d-0bbb-4459-9d63-f918a1a55261	\N	t
0a0602e7-84c2-4588-8880-6e224b0288fc	86bb7325-6555-4f31-af51-3d9b8ac3b424	3faa7ed1-20e7-4584-b567-de45a858e0a6	69242308-35f8-4e56-8e8b-269d5cdd55a3	\N	t
4f5d8fff-c973-416d-a70b-e4ddc83739a6	86bb7325-6555-4f31-af51-3d9b8ac3b424	22ddc903-87d8-4ef0-b50d-13815b3a9fea	016e05a0-912b-4850-90ed-0857fa4a1e62	\N	f
5f08a23c-68a1-46ab-9513-e85df816ada2	86bb7325-6555-4f31-af51-3d9b8ac3b424	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	50e1b346-b37f-42d4-ac28-f0b8a18c2b17	\N	f
e5826240-0222-4058-8c85-59e60d508f6f	5c49c681-b5e1-44a0-9aed-49e8315ff24e	b19b875e-34ef-4803-b1e6-e8830b2216ca	863f015a-988a-4c5f-9efc-37304cf1c424	\N	t
1ea89b51-72fe-4a54-a930-7d3f5b6b8520	5c49c681-b5e1-44a0-9aed-49e8315ff24e	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	13202b7d-0bbb-4459-9d63-f918a1a55261	\N	t
2e2b9e01-1394-4c87-948c-9ca8712b19b5	5c49c681-b5e1-44a0-9aed-49e8315ff24e	3faa7ed1-20e7-4584-b567-de45a858e0a6	69242308-35f8-4e56-8e8b-269d5cdd55a3	\N	t
bfa72f17-6864-4d07-ac40-774ba157cfdf	5c49c681-b5e1-44a0-9aed-49e8315ff24e	22ddc903-87d8-4ef0-b50d-13815b3a9fea	00c1c0c1-cd9c-4abf-9888-c3d5c955b075	\N	t
9a36eec0-a663-4632-8a39-1952f4e91859	5c49c681-b5e1-44a0-9aed-49e8315ff24e	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	60bb1575-047c-4506-a978-ea723c8c07ce	\N	f
e3444095-7fca-4abb-90c0-3bae294d2773	12cecddd-5572-4c35-8cf8-4e6d6b9564c8	b19b875e-34ef-4803-b1e6-e8830b2216ca	92d1a13e-06ac-4db6-b317-1a91e4391f70	\N	f
b59de465-fe49-43e2-b687-2f7030dfb34e	12cecddd-5572-4c35-8cf8-4e6d6b9564c8	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	6f973f54-84fe-42fd-a743-f023ec4f22ad	\N	f
af404202-85d5-4902-a415-d5581a59cbe3	12cecddd-5572-4c35-8cf8-4e6d6b9564c8	3faa7ed1-20e7-4584-b567-de45a858e0a6	8993c5a9-f599-4cfc-aa2a-26bf3d3477c8	\N	f
4e4767b7-d152-41c4-b1d3-b81a57762da2	12cecddd-5572-4c35-8cf8-4e6d6b9564c8	22ddc903-87d8-4ef0-b50d-13815b3a9fea	00c1c0c1-cd9c-4abf-9888-c3d5c955b075	\N	t
399e00d7-8718-4870-82ae-8e473466511a	12cecddd-5572-4c35-8cf8-4e6d6b9564c8	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	f18d5e8c-630c-4555-b401-de0873bbe2f2	\N	t
5559d45f-3e14-49d3-8b82-56b3ab1c4b4c	6b817e58-fdc5-415b-a181-4c9af823bfcd	b19b875e-34ef-4803-b1e6-e8830b2216ca	863f015a-988a-4c5f-9efc-37304cf1c424	\N	t
2740bfa2-eabc-48d3-a3c7-b622e85fde46	6b817e58-fdc5-415b-a181-4c9af823bfcd	72ef060a-ef88-48ea-9aea-eb85c3b0db1e	13202b7d-0bbb-4459-9d63-f918a1a55261	\N	t
f01187c4-ba36-4633-b165-8eef406dd646	6b817e58-fdc5-415b-a181-4c9af823bfcd	3faa7ed1-20e7-4584-b567-de45a858e0a6	8993c5a9-f599-4cfc-aa2a-26bf3d3477c8	\N	f
60f36dc4-37f1-4c3e-a119-9e3426164eb7	6b817e58-fdc5-415b-a181-4c9af823bfcd	22ddc903-87d8-4ef0-b50d-13815b3a9fea	016e05a0-912b-4850-90ed-0857fa4a1e62	\N	f
c492ead9-5e29-4958-8d64-82a261418d3d	6b817e58-fdc5-415b-a181-4c9af823bfcd	bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	50e1b346-b37f-42d4-ac28-f0b8a18c2b17	\N	f
d4d4de6a-29de-4fb8-8898-bce90d1612e1	1946718b-eb30-44f3-94f1-8b1072634175	8830c3fa-2dfe-42a7-894c-a57cc1e88598	62b38773-b565-4edc-8ec8-f399af801a9e	\N	f
55bec995-64d3-41cb-a21e-cf83140fec73	1946718b-eb30-44f3-94f1-8b1072634175	1467d970-0d52-4d24-bc46-5a304049b5bf	ab507cf2-cd48-4576-b074-f878d9e3a00b	\N	f
9e39ca6f-e9a3-4819-90ff-05e766f33be0	1946718b-eb30-44f3-94f1-8b1072634175	4fb1ed42-6579-448c-80a9-80d60efa9b55	49f2f6e4-4adb-4c9b-9afc-7d5ce5c5136e	\N	t
57a1e702-0cb6-4e99-a438-c569b967a83e	1946718b-eb30-44f3-94f1-8b1072634175	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	78673371-6661-4907-9a48-d22aa9857733	\N	f
2589b4ff-449f-4326-9c2a-1c5b7ea15d4f	1946718b-eb30-44f3-94f1-8b1072634175	b45f71fc-f02a-436c-ad77-c9aff83da125	d96f6331-d9e9-40ef-8a4f-e6cd5e484668	\N	t
2fb9a6e7-e68e-4d3e-b3ef-822000eb981b	eb4f667d-8efc-4299-977a-3290c6880410	8830c3fa-2dfe-42a7-894c-a57cc1e88598	6655377b-9918-4b5d-8471-30e5e1b8c7f2	\N	f
4799bf72-5cf4-4dd0-8ecf-6c76e0e80e5a	eb4f667d-8efc-4299-977a-3290c6880410	1467d970-0d52-4d24-bc46-5a304049b5bf	76af77a9-a087-424f-87e5-2887c32a9e62	\N	f
f2c82bef-5c5e-4a55-8ad7-655c6972c414	eb4f667d-8efc-4299-977a-3290c6880410	4fb1ed42-6579-448c-80a9-80d60efa9b55	6aa44620-ff60-4817-9a78-32e883efc5c8	\N	f
1d6e788d-aea1-4203-94b0-fcb28faefa1e	eb4f667d-8efc-4299-977a-3290c6880410	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	77679332-ee59-4a2f-a3b2-72d0fb888b88	\N	f
2c0794c0-86ed-4cd0-9eef-cd6ce2127625	eb4f667d-8efc-4299-977a-3290c6880410	b45f71fc-f02a-436c-ad77-c9aff83da125	c8323ac8-56a6-4c22-9645-15b7913a2587	\N	f
35f3f7b5-eece-4832-b7ed-ee0f3ee9e204	dec6dd7e-1a61-47f0-bbee-6374ae2cbb41	8830c3fa-2dfe-42a7-894c-a57cc1e88598	6655377b-9918-4b5d-8471-30e5e1b8c7f2	\N	f
97d8c220-92f8-49f6-94bf-6aed582cc5eb	dec6dd7e-1a61-47f0-bbee-6374ae2cbb41	1467d970-0d52-4d24-bc46-5a304049b5bf	ab507cf2-cd48-4576-b074-f878d9e3a00b	\N	f
414f410d-be0c-4773-815b-d0208fcf1dcc	dec6dd7e-1a61-47f0-bbee-6374ae2cbb41	4fb1ed42-6579-448c-80a9-80d60efa9b55	49f2f6e4-4adb-4c9b-9afc-7d5ce5c5136e	\N	t
2be2ac52-00ab-4681-8cba-0fafbcc17ea0	dec6dd7e-1a61-47f0-bbee-6374ae2cbb41	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	d076c5ed-d8cd-4157-afc8-848fea793c0b	\N	t
ce51772b-3707-489c-8185-54c2264171a8	dec6dd7e-1a61-47f0-bbee-6374ae2cbb41	b45f71fc-f02a-436c-ad77-c9aff83da125	74e35d4d-f5fb-4016-8b61-9dba1d4fe175	\N	f
acf4d018-bc6a-425b-a973-c147053d5dc4	f32d1267-a4e2-465d-9ded-7502737d2608	8830c3fa-2dfe-42a7-894c-a57cc1e88598	6655377b-9918-4b5d-8471-30e5e1b8c7f2	\N	f
884f21d6-d376-412b-a178-6bf2fb162c25	f32d1267-a4e2-465d-9ded-7502737d2608	1467d970-0d52-4d24-bc46-5a304049b5bf	76af77a9-a087-424f-87e5-2887c32a9e62	\N	f
3bb67728-3178-4a78-b435-cd7c9d0d4662	f32d1267-a4e2-465d-9ded-7502737d2608	4fb1ed42-6579-448c-80a9-80d60efa9b55	2470a2df-cc26-4fa5-9fcc-1d773cfaf9aa	\N	f
834643be-3b39-43a5-af71-f77ea56c3664	f32d1267-a4e2-465d-9ded-7502737d2608	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	d076c5ed-d8cd-4157-afc8-848fea793c0b	\N	t
14820ade-ec8b-4962-9d9a-baa37b0af90e	f32d1267-a4e2-465d-9ded-7502737d2608	b45f71fc-f02a-436c-ad77-c9aff83da125	c8323ac8-56a6-4c22-9645-15b7913a2587	\N	f
5b55e79c-6ca6-47fb-8aa6-6c4bc3f3ca2d	4f23ae45-5ec6-42f7-a5e7-be946f549f38	8830c3fa-2dfe-42a7-894c-a57cc1e88598	05cb713f-b9b1-497d-be3e-3ad20fc857c9	\N	t
230e7afb-6c33-49dd-a32f-8872113bed1f	4f23ae45-5ec6-42f7-a5e7-be946f549f38	1467d970-0d52-4d24-bc46-5a304049b5bf	76af77a9-a087-424f-87e5-2887c32a9e62	\N	f
d72b5243-64e6-4c69-8e63-b935e86d8e3d	4f23ae45-5ec6-42f7-a5e7-be946f549f38	4fb1ed42-6579-448c-80a9-80d60efa9b55	49f2f6e4-4adb-4c9b-9afc-7d5ce5c5136e	\N	t
9538057e-72c2-4a6a-a59d-ddb279bb1196	4f23ae45-5ec6-42f7-a5e7-be946f549f38	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	d076c5ed-d8cd-4157-afc8-848fea793c0b	\N	t
7aee4bcb-5bd7-450e-b3e7-bd8fa3313d0f	4f23ae45-5ec6-42f7-a5e7-be946f549f38	b45f71fc-f02a-436c-ad77-c9aff83da125	d96f6331-d9e9-40ef-8a4f-e6cd5e484668	\N	t
a6538945-ddd1-465f-ae2b-f621b2364ae8	2893d822-6b5a-431a-ae04-23cab221f2ca	8830c3fa-2dfe-42a7-894c-a57cc1e88598	05cb713f-b9b1-497d-be3e-3ad20fc857c9	\N	t
23ec76a3-8a46-4137-9b9d-49c35ce9def0	2893d822-6b5a-431a-ae04-23cab221f2ca	1467d970-0d52-4d24-bc46-5a304049b5bf	ab507cf2-cd48-4576-b074-f878d9e3a00b	\N	f
238c9eb8-0d89-4ae8-bbab-2cbca20cffcc	2893d822-6b5a-431a-ae04-23cab221f2ca	4fb1ed42-6579-448c-80a9-80d60efa9b55	49f2f6e4-4adb-4c9b-9afc-7d5ce5c5136e	\N	t
7160205e-7017-429b-bf60-85d366a35376	2893d822-6b5a-431a-ae04-23cab221f2ca	9bdc19f8-b247-4cb9-b942-9e4a57b6351f	78673371-6661-4907-9a48-d22aa9857733	\N	f
048a5c20-92e3-4cf1-91f3-de5f8e936b3b	2893d822-6b5a-431a-ae04-23cab221f2ca	b45f71fc-f02a-436c-ad77-c9aff83da125	d96f6331-d9e9-40ef-8a4f-e6cd5e484668	\N	t
a1f6a998-8eb5-438b-9402-c4dd8541911c	a0fa7c27-fed4-4377-b1c3-309e4e002f6a	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	bfba517f-500c-4faa-b635-39767a41f766	\N	f
795b5221-5a58-4561-b605-11fee2937650	a0fa7c27-fed4-4377-b1c3-309e4e002f6a	b06828c8-31f6-4bac-9430-f369e5f104a4	5897051d-a091-4aa4-8f52-d7f038c25e85	\N	t
7dae54ef-5fa3-441a-a0b1-833f3be28efc	a0fa7c27-fed4-4377-b1c3-309e4e002f6a	e217a42d-636d-45bc-92ed-addcc56b4db7	c464d94d-fe3c-4300-b86c-ce2bd4ab0b66	\N	f
6ab9f205-bc66-4a19-a58c-1026355f7fe3	a0fa7c27-fed4-4377-b1c3-309e4e002f6a	3b23312f-f34f-41c5-bf90-4cab5989c8af	c7a3ede9-4622-49ba-b5fe-f8f10c5704e2	\N	f
fbb1c5d1-c69d-4670-9f2f-382d85227227	a0fa7c27-fed4-4377-b1c3-309e4e002f6a	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	430bc5c4-c85e-47a1-a886-8933488a6d52	\N	f
ef16553d-c687-4629-8d8d-964d01395342	2ef4a297-0c55-4b7c-807d-75495b8df71d	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	231a2937-a51d-4be1-bdb6-00a6e480a324	\N	t
70ed04a5-ccb2-4944-8297-e9a7f2f7b44f	2ef4a297-0c55-4b7c-807d-75495b8df71d	b06828c8-31f6-4bac-9430-f369e5f104a4	5897051d-a091-4aa4-8f52-d7f038c25e85	\N	t
48aa3948-bb5d-41a1-8579-d05d56657843	2ef4a297-0c55-4b7c-807d-75495b8df71d	e217a42d-636d-45bc-92ed-addcc56b4db7	d2f6c1dc-44bf-47e4-a3ce-3c9ad41b804f	\N	f
908ed59e-eeb0-49ca-a9b3-5014f25f6ad8	2ef4a297-0c55-4b7c-807d-75495b8df71d	3b23312f-f34f-41c5-bf90-4cab5989c8af	20d08bde-d080-4552-b0bf-68c01ddd3c38	\N	f
7784fbea-797a-4cf9-9786-7ce1afb97799	2ef4a297-0c55-4b7c-807d-75495b8df71d	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	63efc862-3301-4be7-90b4-3f46866f5962	\N	t
142282a6-5e34-4c62-8e65-bd31c706aef8	523842f2-b2eb-4e66-86b9-555c80a6b8eb	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	bfba517f-500c-4faa-b635-39767a41f766	\N	f
a1c36675-8d6a-4b78-91b1-8a795ec27f03	523842f2-b2eb-4e66-86b9-555c80a6b8eb	b06828c8-31f6-4bac-9430-f369e5f104a4	6f7152bc-c1d3-4a6b-8b2f-7634595b8ca3	\N	f
20f5794f-9301-487e-9027-e83177185c0b	523842f2-b2eb-4e66-86b9-555c80a6b8eb	e217a42d-636d-45bc-92ed-addcc56b4db7	c464d94d-fe3c-4300-b86c-ce2bd4ab0b66	\N	f
4c0d8273-fea2-4597-bcd9-3e3f77218f53	523842f2-b2eb-4e66-86b9-555c80a6b8eb	3b23312f-f34f-41c5-bf90-4cab5989c8af	d51b6c5b-9dc0-4828-8d92-58d47a42613b	\N	t
c413b756-4210-4be5-ac28-621384e084ed	523842f2-b2eb-4e66-86b9-555c80a6b8eb	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	63efc862-3301-4be7-90b4-3f46866f5962	\N	t
40361c10-eb03-4a06-9c11-97f2c24c15c1	aa360042-86bc-49dc-9d1b-1714704e6fd8	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	231a2937-a51d-4be1-bdb6-00a6e480a324	\N	t
9cd81fbe-15a1-42ac-8a63-7f983b360bc6	aa360042-86bc-49dc-9d1b-1714704e6fd8	b06828c8-31f6-4bac-9430-f369e5f104a4	6f7152bc-c1d3-4a6b-8b2f-7634595b8ca3	\N	f
8759683b-8d8b-4458-a8b6-48e556118a7e	aa360042-86bc-49dc-9d1b-1714704e6fd8	e217a42d-636d-45bc-92ed-addcc56b4db7	c464d94d-fe3c-4300-b86c-ce2bd4ab0b66	\N	f
75037fcb-8fda-4d6e-bb9c-f9d6602b29ef	aa360042-86bc-49dc-9d1b-1714704e6fd8	3b23312f-f34f-41c5-bf90-4cab5989c8af	d51b6c5b-9dc0-4828-8d92-58d47a42613b	\N	t
e7c0dfa7-eabc-42fc-9577-7098486f0e3e	aa360042-86bc-49dc-9d1b-1714704e6fd8	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	63efc862-3301-4be7-90b4-3f46866f5962	\N	t
6d28d381-af92-4f5d-afd5-eb717b210c87	e269fdde-91d6-4ab4-b6d0-52e3baa38ce6	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	bfba517f-500c-4faa-b635-39767a41f766	\N	f
754d21c5-4a83-410c-b9f9-f7ccf61e6f68	e269fdde-91d6-4ab4-b6d0-52e3baa38ce6	b06828c8-31f6-4bac-9430-f369e5f104a4	5897051d-a091-4aa4-8f52-d7f038c25e85	\N	t
c23203fe-507b-4175-98b6-a6cd9cecb916	e269fdde-91d6-4ab4-b6d0-52e3baa38ce6	e217a42d-636d-45bc-92ed-addcc56b4db7	9eab6b0e-fcff-4f99-9fdb-5ab16949c492	\N	t
9c8e309d-2655-4676-8cd1-bbed286e3ef3	e269fdde-91d6-4ab4-b6d0-52e3baa38ce6	3b23312f-f34f-41c5-bf90-4cab5989c8af	d51b6c5b-9dc0-4828-8d92-58d47a42613b	\N	t
41dc318a-1ba3-44b7-abb8-20dbe028c784	e269fdde-91d6-4ab4-b6d0-52e3baa38ce6	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	559fb3af-81f3-441e-a071-dd5823c8bcec	\N	f
694e838d-a8ae-4d47-835e-58b866c4896a	3d46bfc0-f9e5-455d-a813-f01de69a3d48	0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	231a2937-a51d-4be1-bdb6-00a6e480a324	\N	t
2d09bf00-8c12-4b52-beb7-4a9cdc5c4970	3d46bfc0-f9e5-455d-a813-f01de69a3d48	b06828c8-31f6-4bac-9430-f369e5f104a4	5897051d-a091-4aa4-8f52-d7f038c25e85	\N	t
3e12f297-f655-4951-83d1-937cae78ca6b	3d46bfc0-f9e5-455d-a813-f01de69a3d48	e217a42d-636d-45bc-92ed-addcc56b4db7	9eab6b0e-fcff-4f99-9fdb-5ab16949c492	\N	t
c41a3747-1080-4071-b994-be32a372d4f5	3d46bfc0-f9e5-455d-a813-f01de69a3d48	3b23312f-f34f-41c5-bf90-4cab5989c8af	c7a3ede9-4622-49ba-b5fe-f8f10c5704e2	\N	f
5521fb2e-9667-40f1-9aa7-c6ac0295b5b3	3d46bfc0-f9e5-455d-a813-f01de69a3d48	ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	430bc5c4-c85e-47a1-a886-8933488a6d52	\N	f
625eae58-0cb6-4722-ba53-e1129bfc6d97	e02962ed-74ad-4464-a8c9-ea5dccf62739	094ffddf-f429-4b8c-90e8-cd88d4789eb0	ca7f83e3-da58-45ad-9477-34a657dd2517	\N	t
17be1bb2-6120-485e-ae10-7df79b07e4c5	e02962ed-74ad-4464-a8c9-ea5dccf62739	03afd3fa-fa28-4953-bff2-cf59386cbc97	ff64c464-d464-469f-b1ec-fb90d1190ae3	\N	f
d7235a91-5bca-4c03-aa28-dda2331f277c	e02962ed-74ad-4464-a8c9-ea5dccf62739	3144f678-6efa-4037-a089-53a6484cae43	be3dcc07-f35e-49b8-9086-852f49b5c71b	\N	t
a8ca6aab-fefe-4a90-8246-6ea85707ffc6	e02962ed-74ad-4464-a8c9-ea5dccf62739	1299e0dd-b153-46a1-8a32-8ec70877a4c6	1371a00a-ce79-4e01-bb46-f1c509494dbf	\N	t
3ac5deb5-0b06-4729-8cb9-3a4b2fd3a17d	e02962ed-74ad-4464-a8c9-ea5dccf62739	f014541c-9b76-4e6b-bd30-814fb530e34f	b0e5c195-8711-4c8e-97f2-3f12b74cb605	\N	f
c5e1cea4-bd1f-4f65-b052-aa97861012a9	075b1e6b-17a9-4602-a434-990d737649b4	094ffddf-f429-4b8c-90e8-cd88d4789eb0	ca7f83e3-da58-45ad-9477-34a657dd2517	\N	t
3ff358ba-4b79-4805-a06a-697ea3ada64c	075b1e6b-17a9-4602-a434-990d737649b4	03afd3fa-fa28-4953-bff2-cf59386cbc97	a7b86e42-ab8e-458d-ae1a-17f76ac693c9	\N	t
a57939b9-2717-4fd9-81bb-1d0048449e58	075b1e6b-17a9-4602-a434-990d737649b4	3144f678-6efa-4037-a089-53a6484cae43	66848776-896a-4c25-9d40-b7a5ecab33d8	\N	f
9c2d44be-1ed8-4dcb-9b54-aa7ab5d48341	075b1e6b-17a9-4602-a434-990d737649b4	1299e0dd-b153-46a1-8a32-8ec70877a4c6	1371a00a-ce79-4e01-bb46-f1c509494dbf	\N	t
5b62fa4f-8e95-4ba4-bb1d-99109ca1e4fb	075b1e6b-17a9-4602-a434-990d737649b4	f014541c-9b76-4e6b-bd30-814fb530e34f	ddf8a354-4c82-4958-a058-bf4e4e993939	\N	f
a7ee5a7c-59cf-4720-b310-5849c409d4b0	cee70db0-b351-4ec0-8fb3-db83930daf8f	094ffddf-f429-4b8c-90e8-cd88d4789eb0	ca7f83e3-da58-45ad-9477-34a657dd2517	\N	t
72ca9ddd-c98c-4e5c-9822-9d7adec532e3	cee70db0-b351-4ec0-8fb3-db83930daf8f	03afd3fa-fa28-4953-bff2-cf59386cbc97	ff64c464-d464-469f-b1ec-fb90d1190ae3	\N	f
2eb6d722-22f8-4387-9613-6683d9fcac8a	cee70db0-b351-4ec0-8fb3-db83930daf8f	3144f678-6efa-4037-a089-53a6484cae43	be3dcc07-f35e-49b8-9086-852f49b5c71b	\N	t
1542e7a3-3a6c-4dc1-bbd9-3d9e18b6f081	cee70db0-b351-4ec0-8fb3-db83930daf8f	1299e0dd-b153-46a1-8a32-8ec70877a4c6	1371a00a-ce79-4e01-bb46-f1c509494dbf	\N	t
e056fe90-e137-4e0e-8494-4e534ddfc328	cee70db0-b351-4ec0-8fb3-db83930daf8f	f014541c-9b76-4e6b-bd30-814fb530e34f	b0e5c195-8711-4c8e-97f2-3f12b74cb605	\N	f
fb74d7cd-dda7-40b0-8628-2d159a435911	8913de42-9d4b-470a-8c1d-d5ea0060572e	094ffddf-f429-4b8c-90e8-cd88d4789eb0	33371af1-68cb-4a32-8c42-925a7335611a	\N	f
dfad866b-380d-4b17-a1d2-88c53b71690a	8913de42-9d4b-470a-8c1d-d5ea0060572e	03afd3fa-fa28-4953-bff2-cf59386cbc97	7a002d80-40f3-48ea-aeb2-a5435c995c6a	\N	f
437867a2-ceea-4ca8-949c-df3a297f2043	8913de42-9d4b-470a-8c1d-d5ea0060572e	3144f678-6efa-4037-a089-53a6484cae43	be3dcc07-f35e-49b8-9086-852f49b5c71b	\N	t
a13a0c18-8c94-4495-a154-adf986d69461	8913de42-9d4b-470a-8c1d-d5ea0060572e	1299e0dd-b153-46a1-8a32-8ec70877a4c6	1371a00a-ce79-4e01-bb46-f1c509494dbf	\N	t
d3ec84b5-7589-423e-b72f-fdfad0ce42de	8913de42-9d4b-470a-8c1d-d5ea0060572e	f014541c-9b76-4e6b-bd30-814fb530e34f	b93a8812-b244-4aaf-aeba-b527280df2ca	\N	t
fb34ba24-ace9-4871-b433-24a81a374846	fd55f7bb-028e-4391-8780-9121cc81b669	094ffddf-f429-4b8c-90e8-cd88d4789eb0	ca7f83e3-da58-45ad-9477-34a657dd2517	\N	t
66e52933-4c9f-4d43-a2e6-b598e22aaa84	fd55f7bb-028e-4391-8780-9121cc81b669	03afd3fa-fa28-4953-bff2-cf59386cbc97	7a002d80-40f3-48ea-aeb2-a5435c995c6a	\N	f
848e9477-d9de-4272-a90c-40124ec47b95	fd55f7bb-028e-4391-8780-9121cc81b669	3144f678-6efa-4037-a089-53a6484cae43	be3dcc07-f35e-49b8-9086-852f49b5c71b	\N	t
34fb19f1-d422-4cff-bfe3-d8e565135410	fd55f7bb-028e-4391-8780-9121cc81b669	1299e0dd-b153-46a1-8a32-8ec70877a4c6	1371a00a-ce79-4e01-bb46-f1c509494dbf	\N	t
7e2cf755-f2e5-4533-8bf8-e63c2587ab9f	fd55f7bb-028e-4391-8780-9121cc81b669	f014541c-9b76-4e6b-bd30-814fb530e34f	b93a8812-b244-4aaf-aeba-b527280df2ca	\N	t
d612fc00-c48e-4bf2-8b7c-8b5cc2108618	09bcbf4a-e1d5-4527-a177-949d79c5c997	094ffddf-f429-4b8c-90e8-cd88d4789eb0	ca7f83e3-da58-45ad-9477-34a657dd2517	\N	t
2fe3799f-ad30-4482-bc50-c8ebec3300b6	09bcbf4a-e1d5-4527-a177-949d79c5c997	03afd3fa-fa28-4953-bff2-cf59386cbc97	ff64c464-d464-469f-b1ec-fb90d1190ae3	\N	f
820e18e0-c858-4ad5-8c04-b48b84e2111d	09bcbf4a-e1d5-4527-a177-949d79c5c997	3144f678-6efa-4037-a089-53a6484cae43	be3dcc07-f35e-49b8-9086-852f49b5c71b	\N	t
368ef5d0-b0a3-4084-9801-022567f25c91	09bcbf4a-e1d5-4527-a177-949d79c5c997	1299e0dd-b153-46a1-8a32-8ec70877a4c6	1371a00a-ce79-4e01-bb46-f1c509494dbf	\N	t
a112dd4d-1f69-485d-9382-c7e1839c5b4d	09bcbf4a-e1d5-4527-a177-949d79c5c997	f014541c-9b76-4e6b-bd30-814fb530e34f	ddf8a354-4c82-4958-a058-bf4e4e993939	\N	f
02caf465-6a61-4a8e-a6db-b081c4677c2f	ef4d2102-7442-4b64-9050-44d3e358ed90	1d71b18a-562a-42ed-97d2-b0f515ed8b30	a0a14f4c-aa7e-40e8-840d-304b928149b3	\N	f
af275087-0b79-401a-9898-0ea10fa849f7	ef4d2102-7442-4b64-9050-44d3e358ed90	0f06a907-24b1-4b9b-8ba8-15b79786445a	e1afecde-ea6a-4a6a-adeb-07774e82f0e1	\N	t
50e5097f-997d-411f-a49b-54559f821234	ef4d2102-7442-4b64-9050-44d3e358ed90	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	f4771f75-66ca-4170-8c2f-b767c967db3b	\N	f
e58bcabc-88ee-4a86-afdb-4ecbfabcd7c8	ef4d2102-7442-4b64-9050-44d3e358ed90	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	0ca06928-c4a2-488f-afde-a02dbb255a6a	\N	f
a1ad8516-366c-4d0c-a07f-ca9293cd00a6	ef4d2102-7442-4b64-9050-44d3e358ed90	24a18078-b33b-41fe-a689-cfa05324c386	3ebb44fc-f015-42d0-9d0d-a2d139679a06	\N	f
cf97860b-1413-4d5b-9523-961145e9dbdf	e2fc4a2b-d28b-4270-a621-c4801463e426	1d71b18a-562a-42ed-97d2-b0f515ed8b30	f63a29cf-ca3e-496a-8b17-f0faeb5e4447	\N	t
0995f3da-8528-46d5-bf43-02eae966f674	e2fc4a2b-d28b-4270-a621-c4801463e426	0f06a907-24b1-4b9b-8ba8-15b79786445a	e1afecde-ea6a-4a6a-adeb-07774e82f0e1	\N	t
dc20573a-3ffd-4cdd-97ee-84accf01892e	e2fc4a2b-d28b-4270-a621-c4801463e426	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	f4771f75-66ca-4170-8c2f-b767c967db3b	\N	f
1fcad0af-ae57-4077-8d49-275b1be658f3	e2fc4a2b-d28b-4270-a621-c4801463e426	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	4707570f-3fd3-40f1-b289-0b1b3e50b0e2	\N	f
becfc3cf-4db6-4559-9835-6d47c7f98bf0	e2fc4a2b-d28b-4270-a621-c4801463e426	24a18078-b33b-41fe-a689-cfa05324c386	6f4254ba-ecda-4bbd-bdc7-e490e371fa74	\N	t
1f6aca3a-a962-4232-a62f-bd966ad3e4b4	1006bebb-169e-4d39-833d-58dc36007052	1d71b18a-562a-42ed-97d2-b0f515ed8b30	f63a29cf-ca3e-496a-8b17-f0faeb5e4447	\N	t
c13187aa-38a7-4d29-8b01-ffe9990700cb	1006bebb-169e-4d39-833d-58dc36007052	0f06a907-24b1-4b9b-8ba8-15b79786445a	4e3c1da7-ec6a-46d4-aa17-566f48ec82e7	\N	f
fa8f7bff-e930-4a0b-9cdc-0d4fe8ce564d	1006bebb-169e-4d39-833d-58dc36007052	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	19457b73-3ad5-4b3a-a849-e77631d76312	\N	t
ca26d2a9-f420-44c9-9e7b-1186c5ab4417	1006bebb-169e-4d39-833d-58dc36007052	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	e3679052-478b-46a2-8fed-ac4c402b5242	\N	t
c97fb79b-dac8-4f46-81e5-2c8a978b3b4c	1006bebb-169e-4d39-833d-58dc36007052	24a18078-b33b-41fe-a689-cfa05324c386	6f4254ba-ecda-4bbd-bdc7-e490e371fa74	\N	t
6d7edcf6-823d-4e0b-a721-1b604198658f	e97b2d34-4d16-49b8-8a59-16f038b6c0bc	1d71b18a-562a-42ed-97d2-b0f515ed8b30	9729453f-dd4b-4a2e-addb-d3b54863ae27	\N	f
f2611e0f-de85-4e40-8fec-169e610a587d	e97b2d34-4d16-49b8-8a59-16f038b6c0bc	0f06a907-24b1-4b9b-8ba8-15b79786445a	e1afecde-ea6a-4a6a-adeb-07774e82f0e1	\N	t
95d9b006-1cd7-431e-9397-78c5920c1367	e97b2d34-4d16-49b8-8a59-16f038b6c0bc	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	19457b73-3ad5-4b3a-a849-e77631d76312	\N	t
f6eb005f-9843-4720-b8b9-3e4168602c23	e97b2d34-4d16-49b8-8a59-16f038b6c0bc	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	4707570f-3fd3-40f1-b289-0b1b3e50b0e2	\N	f
afebbc0f-0ce6-4267-85cb-922032a6b674	e97b2d34-4d16-49b8-8a59-16f038b6c0bc	24a18078-b33b-41fe-a689-cfa05324c386	3ebb44fc-f015-42d0-9d0d-a2d139679a06	\N	f
1a21bf70-03f5-44e6-bca3-2d0e9e641685	22c3b553-c22a-426f-aa26-af56d807022b	1d71b18a-562a-42ed-97d2-b0f515ed8b30	f63a29cf-ca3e-496a-8b17-f0faeb5e4447	\N	t
c9cc5b5d-805b-4bb0-8b3c-60f99656e3a0	22c3b553-c22a-426f-aa26-af56d807022b	0f06a907-24b1-4b9b-8ba8-15b79786445a	e1afecde-ea6a-4a6a-adeb-07774e82f0e1	\N	t
26e1c19b-52ba-4572-b3a6-6a6f49c31f42	22c3b553-c22a-426f-aa26-af56d807022b	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	f4771f75-66ca-4170-8c2f-b767c967db3b	\N	f
48db1dc5-f1bc-403b-a6fe-9ba56996ac8d	22c3b553-c22a-426f-aa26-af56d807022b	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	4707570f-3fd3-40f1-b289-0b1b3e50b0e2	\N	f
b479345a-47bd-4ba6-9fa2-d7e5852bbcca	22c3b553-c22a-426f-aa26-af56d807022b	24a18078-b33b-41fe-a689-cfa05324c386	45d063e6-8e30-4ef9-a9f1-1884aac1b11f	\N	f
c99c7576-4a7d-4ff8-857b-04d49a771dbe	a962b64c-08b0-4746-b65b-6bfefcaa97a0	1d71b18a-562a-42ed-97d2-b0f515ed8b30	f63a29cf-ca3e-496a-8b17-f0faeb5e4447	\N	t
eb1d6d2c-9c1b-4723-9575-989a070a4dc2	a962b64c-08b0-4746-b65b-6bfefcaa97a0	0f06a907-24b1-4b9b-8ba8-15b79786445a	f70fa6e7-06ce-48d2-9029-3f2cf6c3e3e2	\N	f
c0af2a72-1a64-42e9-be49-479c2a4a9edb	a962b64c-08b0-4746-b65b-6bfefcaa97a0	65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	f4771f75-66ca-4170-8c2f-b767c967db3b	\N	f
395a480b-e4bc-4010-88e1-cb5b4639d065	a962b64c-08b0-4746-b65b-6bfefcaa97a0	7f6f4fde-693d-4977-b2fb-fed71c2d3dda	0ca06928-c4a2-488f-afde-a02dbb255a6a	\N	f
ba52b8ca-7521-489c-9a45-6c2b0f099cff	a962b64c-08b0-4746-b65b-6bfefcaa97a0	24a18078-b33b-41fe-a689-cfa05324c386	3ebb44fc-f015-42d0-9d0d-a2d139679a06	\N	f
\.


--
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.assignments (id, course_id, lesson_id, title, description, level, type, expected_sql, max_score, is_final, created_at) FROM stdin;
0aa00000-0000-0000-0000-000000000001	0c000000-0000-0000-0000-000000000001	0e000000-0000-0000-0000-000000000005	Создать таблицу студентов	Создайте таблицу students с полями id, full_name, group_name.	basic	sql	CREATE TABLE students (id serial PRIMARY KEY, full_name text, group_name text);	100	f	2026-06-07 21:32:31.893381+03
0aa00000-0000-0000-0000-000000000002	0c000000-0000-0000-0000-000000000001	0e000000-0000-0000-0000-000000000006	Выбрать всех студентов	Напишите запрос, выбирающий всех студентов из таблицы students.	medium	sql	SELECT * FROM students;	100	f	2026-06-07 21:32:31.893381+03
0aa00000-0000-0000-0000-000000000003	0c000000-0000-0000-0000-000000000001	\N	Итоговый проект: учебная БД	Спроектируйте и реализуйте небольшую образовательную базу данных.	advanced	file	\N	100	t	2026-06-07 21:32:31.893381+03
\.


--
-- Data for Name: course_ratings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.course_ratings (id, course_id, user_id, rating, created_at, comment) FROM stdin;
386d1fa7-2790-43cc-996b-37f38ffef918	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000002	4	2026-06-08 21:10:53.637142+03	\N
94a9a471-d0de-4e9d-8d5a-3a860c33a247	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000004	5	2026-05-22 20:10:53.637142+03	\N
346bc932-c784-49a8-b2db-d320ce18e861	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000010	5	2026-06-01 06:10:53.637142+03	\N
8832b49c-cf28-46d4-869b-ab953f05c182	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000012	5	2026-06-19 08:10:53.637142+03	\N
2d2435a7-9b02-42f2-a5a7-d05b2fab66ad	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000014	4	2026-06-10 10:10:53.637142+03	\N
405d0a87-9cd0-4766-adde-ae88f6965d4c	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000015	5	2026-06-06 14:10:53.637142+03	\N
186df9ab-f64c-47f1-8daf-da99cd29cca5	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000002	5	2026-05-12 00:10:53.637142+03	\N
fd145d63-118d-401a-b98e-e8ead79e4c91	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000003	5	2026-05-12 20:10:53.637142+03	\N
096f716a-712f-43c1-b28f-21077961bdb5	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000004	5	2026-06-14 13:10:53.637142+03	\N
160ec33e-137b-491b-8b5c-0d88dd6d5816	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000005	4	2026-05-25 19:10:53.637142+03	\N
9f7babbc-e8a8-4b6e-ab81-941190dfc61e	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000011	5	2026-06-09 14:10:53.637142+03	\N
7013d189-6f3a-411a-80db-bf06eed591f6	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000012	5	2026-05-16 11:10:53.637142+03	\N
d4a21210-abac-42f3-b339-388dd9af6306	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000013	4	2026-06-04 14:10:53.637142+03	\N
7abac179-79d9-4e9b-ad33-b8be185b9d2c	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000016	5	2026-06-07 19:10:53.637142+03	\N
0c44f3af-42ff-4a48-8bae-ccfee67e5591	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000017	5	2026-06-17 04:10:53.637142+03	\N
2ebafe05-9792-437a-aa1b-7e09f16e2b6a	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000002	5	2026-06-01 05:10:53.637142+03	\N
a3fc3aa0-6e35-4322-a07f-c754e2fc058d	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000003	5	2026-05-28 18:10:53.637142+03	\N
ee90f59e-1a9a-4f70-ba55-7d862be32c9f	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000004	5	2026-06-17 19:10:53.637142+03	\N
8fb94f4d-e04d-49dd-89b4-a28346964bc3	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000005	5	2026-05-28 09:10:53.637142+03	\N
9deb33de-e8a1-425f-8132-853f458c81b7	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000010	5	2026-06-12 18:10:53.637142+03	\N
4fb091db-2f8d-422a-879d-762bcaeeaf06	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000012	5	2026-06-05 13:10:53.637142+03	\N
c9a3cd86-63e3-44c4-b852-4272e861481d	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000015	4	2026-06-07 17:10:53.637142+03	\N
21251104-861a-48d8-81c4-59c957e1e723	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000016	5	2026-05-24 14:10:53.637142+03	\N
92a7d8f5-df46-4e1c-a0e6-3cbb35dfc21f	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000002	4	2026-05-12 09:10:53.637142+03	\N
c7352dd5-c9ed-43c6-8380-7e455a59d5dc	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000003	4	2026-06-03 17:10:53.637142+03	\N
c8477208-2e3f-4604-aa3f-c3e87f28ec79	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000004	4	2026-06-18 23:10:53.637142+03	\N
17eb15dd-5e60-4d45-8c5a-bafda1eeb8d0	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000005	4	2026-05-19 13:10:53.637142+03	\N
5dccae73-ce90-41af-9b76-20194a442d86	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000010	4	2026-05-13 20:10:53.637142+03	\N
4d1cac21-3a6f-4b07-8080-009aa49e9b97	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000013	3	2026-06-16 10:10:53.637142+03	\N
ac0a7eb8-36f4-48bc-abbf-cf4a2e431eaa	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000002	3	2026-05-29 04:10:53.637142+03	\N
b0d58ebc-6c5c-4a90-8377-5cef81609a94	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000003	4	2026-06-12 03:10:53.637142+03	\N
833ee4bb-6247-40c8-9ed4-45cde5f1cc72	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000011	4	2026-05-10 16:10:53.637142+03	\N
b0dbf6f1-dd68-4e52-a365-b35952ec6ab6	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000012	4	2026-05-13 06:10:53.637142+03	\N
42bed802-6775-4f37-af4a-fc572aa00724	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000013	4	2026-05-21 13:10:53.637142+03	\N
cc07ce6f-1ea2-4c02-a2fa-7d2bd7f02607	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000003	5	2026-05-22 13:10:53.637142+03	\N
271c7f32-a6d0-4289-858d-da9fb65bbed6	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000004	5	2026-05-14 03:10:53.637142+03	\N
019e8c4e-8cea-4195-914c-be62f1f64a7f	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000005	5	2026-05-19 11:10:53.637142+03	\N
c10dee82-06f6-481d-a17f-042c08b83c90	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000010	5	2026-06-09 13:10:53.637142+03	\N
50218196-62ab-4c39-8341-0804521fa5dd	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000011	4	2026-06-04 20:10:53.637142+03	\N
40659825-a882-4cc8-9833-c5071ba69819	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000012	5	2026-06-16 11:10:53.637142+03	\N
7e0f7bf2-42fd-458c-8844-1c665e15420d	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000014	5	2026-05-18 08:10:53.637142+03	\N
5519e2f5-2d50-438e-8e71-53ec9553c13c	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000003	5	2026-05-14 02:10:53.637142+03	\N
99b750b8-fc11-4249-a845-c14a88f3ac9e	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000005	5	2026-05-12 23:10:53.637142+03	\N
4685740b-aaf3-4b51-af28-027d533867f5	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000010	4	2026-06-13 12:10:53.637142+03	\N
97dbc50d-9e9e-472c-97be-267794326af3	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000011	5	2026-06-12 06:10:53.637142+03	\N
f2f3aac9-f53f-4fdf-88ce-bb8f32012ca5	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000013	4	2026-06-13 11:10:53.637142+03	\N
7d0999bc-fb7e-4d1f-a8c0-8b544e0704b1	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000014	4	2026-05-29 09:10:53.637142+03	\N
cdacf6d1-3eb0-47bb-a149-38833d44f336	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000002	4	2026-05-15 13:10:53.637142+03	\N
98eb3208-d744-435c-8be9-88c7b1289acf	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000004	4	2026-05-25 08:10:53.637142+03	\N
2e4709cd-a96f-4210-a047-74724d590685	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000005	4	2026-05-22 17:10:53.637142+03	\N
b95c3508-75d5-46bc-b6e6-7ca5c0b066bc	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000010	4	2026-05-14 11:10:53.637142+03	\N
52cffd66-7ed6-4dd4-8348-a51b4866dd97	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000012	4	2026-05-24 15:10:53.637142+03	\N
db5345ca-20ce-4c93-bb76-d661f61f3c01	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000013	4	2026-06-16 05:10:53.637142+03	\N
08ae67f3-acf6-4d68-9a65-9ee4aee86898	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000015	4	2026-06-05 07:10:53.637142+03	\N
862a1440-f83b-43fe-8422-55d1e6bc7c15	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000010	5	2026-05-30 06:10:53.637142+03	Очень понятно объясняют, много практики.
e1a20ff5-9ac3-4c12-bbbd-de094319ff02	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000015	5	2026-05-27 06:10:53.637142+03	Чёткие примеры, всё по делу.
587f01c0-6ab2-4ab1-9f41-5611e4195220	758a89c8-4b2a-44c5-9156-200aaa59fcbe	0a000000-0000-0000-0000-000000000014	4	2026-06-02 21:10:53.637142+03	Сложновато местами, зато интересно.
aa3b9632-cee5-4e69-a488-8fad42940e09	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000014	5	2026-06-05 10:10:53.637142+03	Отличный курс — SQL наконец сложился в голове.
360ce462-b21a-47a2-970a-591d2faf85d5	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000011	5	2026-06-18 12:10:53.637142+03	Сложновато местами, зато интересно.
84d2d3a0-c859-4f7e-bbf6-4f400444e058	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	0a000000-0000-0000-0000-000000000013	5	2026-05-09 23:10:53.637142+03	Отличный курс — SQL наконец сложился в голове.
b9db17a9-2043-4ae4-bac8-8182ab3d1c41	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000015	5	2026-05-11 08:10:53.637142+03	Тренажёр реально помогает закрепить материал.
17016fd0-b7a3-4ab6-a346-3c6726912078	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000013	5	2026-05-26 16:10:53.637142+03	Очень понятно объясняют, много практики.
7666795f-10d4-49c8-9052-e2c370c57c52	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	0a000000-0000-0000-0000-000000000002	5	2026-05-12 21:10:53.637142+03	Сложновато местами, зато интересно.
a4047c8b-db95-43b0-8c88-6f0696937f4e	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000011	5	2026-05-25 22:10:53.637142+03	Очень понятно объясняют, много практики.
3156c941-51a6-46df-a9b9-d8358fcab314	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000013	4	2026-05-30 01:10:53.637142+03	Очень понятно объясняют, много практики.
3d2288f8-852c-4b08-af83-ee4a53e83c89	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000003	4	2026-05-19 09:10:53.637142+03	Очень понятно объясняют, много практики.
ade7b9cd-60bc-43ba-9252-c54377b5d07d	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000002	5	2026-06-07 17:10:53.637142+03	Отличный курс — SQL наконец сложился в голове.
1ecede0d-db94-4f1f-9a99-45a264c5cb05	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000004	5	2026-06-14 07:10:53.637142+03	Чёткие примеры, всё по делу.
af206471-98ad-46b4-8371-3aeba57264d9	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000004	3	2026-06-15 09:10:53.637142+03	Преподаватель объясняет доступно.
03597bb2-c64a-4677-abc1-949d9f672fcd	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000014	3	2026-06-04 12:10:53.637142+03	Прошёл с удовольствием, спасибо!
659332e6-0c59-4221-8d87-96e079bc7dd5	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000012	4	2026-05-26 22:10:53.637142+03	Преподаватель объясняет доступно.
599de556-0966-40d8-9e8d-7a31dce5b224	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000003	4	2026-06-14 03:10:53.637142+03	Очень понятно объясняют, много практики.
07ce5313-ee4c-4b7f-a00c-dbb0d582c32b	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000011	4	2026-05-20 13:10:53.637142+03	Чёткие примеры, всё по делу.
cd661769-3753-47ce-8dc2-efdf48cc4973	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	0a000000-0000-0000-0000-000000000014	4	2026-06-06 19:10:53.637142+03	Чёткие примеры, всё по делу.
2a08542a-1f5a-406a-95f0-2bf3e43d9a8d	f21476f6-df52-474c-88ca-b20c8e79eb71	0a000000-0000-0000-0000-000000000012	5	2026-06-17 22:10:53.637142+03	Преподаватель объясняет доступно.
138b7308-e74e-43ca-95da-be3378639edc	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000010	4	2026-06-02 13:10:53.637142+03	Очень понятно объясняют, много практики.
f824b068-c6e7-4170-8418-5ec250d5a5b0	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	0a000000-0000-0000-0000-000000000005	3	2026-05-18 05:10:53.637142+03	Сложновато местами, зато интересно.
891f3051-8984-49aa-8b67-9df18549e539	9e37f28b-b379-49b9-9aa2-d90d8a801c04	0a000000-0000-0000-0000-000000000011	4	2026-05-18 06:10:53.637142+03	Полезно для начинающих, рекомендую.
53e9c6ea-2729-42df-9e52-b7498fb770aa	0c000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000005	5	2026-06-19 05:55:10.474+03	test
\.


--
-- Data for Name: course_topics; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.course_topics (course_id, topic_id) FROM stdin;
0c000000-0000-0000-0000-000000000001	8c2acdbe-c962-46fd-9c1a-89b8890a0b37
0c000000-0000-0000-0000-000000000001	f99935dd-5cf0-487b-9efa-3b885d136fec
0c000000-0000-0000-0000-000000000001	854bb4bc-a757-47c0-94b1-8de546f4bb6f
758a89c8-4b2a-44c5-9156-200aaa59fcbe	8c2acdbe-c962-46fd-9c1a-89b8890a0b37
838f794f-2700-49ed-86f3-6f2a4ddbf5e0	15f929ac-53d5-4891-b073-c7fff41fc581
838f794f-2700-49ed-86f3-6f2a4ddbf5e0	8c2acdbe-c962-46fd-9c1a-89b8890a0b37
9e37f28b-b379-49b9-9aa2-d90d8a801c04	f99935dd-5cf0-487b-9efa-3b885d136fec
9e37f28b-b379-49b9-9aa2-d90d8a801c04	b2271f85-242b-45c3-a2f2-3c6989578471
1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	854bb4bc-a757-47c0-94b1-8de546f4bb6f
1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	f99935dd-5cf0-487b-9efa-3b885d136fec
f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	2a12d38d-4cd6-4622-8e3b-a6c50c43db37
f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	15f929ac-53d5-4891-b073-c7fff41fc581
f21476f6-df52-474c-88ca-b20c8e79eb71	3a11bf6f-cd97-4024-97c2-38afdeafcd33
f21476f6-df52-474c-88ca-b20c8e79eb71	c496bbb5-fbda-4b1a-a8c8-8e34fab0a9ef
f21476f6-df52-474c-88ca-b20c8e79eb71	15f929ac-53d5-4891-b073-c7fff41fc581
9320eb85-1c9e-42ef-8863-a4de7d4e38d8	8c2acdbe-c962-46fd-9c1a-89b8890a0b37
9320eb85-1c9e-42ef-8863-a4de7d4e38d8	15f929ac-53d5-4891-b073-c7fff41fc581
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.courses (id, title, slug, description, semester, author_id, is_published, created_at, level, cover_url) FROM stdin;
0c000000-0000-0000-0000-000000000001	Базы данных для будущих педагогов	databases-for-teachers	Электронный курс на семестр: основы баз данных, ER-моделирование и SQL в PostgreSQL для студентов педагогических направлений.	Осень 2025	0a000000-0000-0000-0000-000000000001	t	2025-09-01 08:30:00+03	basic	\N
758a89c8-4b2a-44c5-9156-200aaa59fcbe	SQL с нуля	sql-s-nulya	Базовый курс по языку SQL: выборки, фильтрация, сортировка и агрегация данных.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	basic	\N
838f794f-2700-49ed-86f3-6f2a4ddbf5e0	PostgreSQL на практике	postgresql-praktika	Возможности PostgreSQL: типы данных, функции, JSON, расширения и оконные запросы.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	medium	\N
9e37f28b-b379-49b9-9aa2-d90d8a801c04	Проектирование БД и ER-модель	proektirovanie-er	Сущности, связи и диаграммы ER, переход к корректной реляционной схеме.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	basic	\N
1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	Нормализация баз данных	normalizaciya	Нормальные формы 1NF–BCNF: устранение аномалий и избыточности данных.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	medium	\N
f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	Транзакции и блокировки	tranzakcii-blokirovki	ACID, уровни изоляции, блокировки и безопасный конкурентный доступ.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	advanced	\N
f21476f6-df52-474c-88ca-b20c8e79eb71	Индексы и производительность	indeksy-proizvoditelnost	B-tree и другие индексы, чтение плана запроса и оптимизация.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	advanced	\N
9320eb85-1c9e-42ef-8863-a4de7d4e38d8	Оконные функции SQL	okonnye-funkcii	OVER, PARTITION BY, ранжирование и аналитические запросы.	2025/26	0a000000-0000-0000-0000-000000000001	t	2026-06-12 11:07:17.345868+03	medium	\N
\.


--
-- Data for Name: enrollments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollments (id, user_id, course_id, status, enrolled_at, completed_at) FROM stdin;
42b3021c-7818-4819-b6a6-27f65e9f9d5b	0a000000-0000-0000-0000-000000000002	0c000000-0000-0000-0000-000000000001	active	2025-09-03 09:00:00+03	\N
78a3c04c-ec55-445f-bc06-db9ddec6523d	0a000000-0000-0000-0000-000000000003	0c000000-0000-0000-0000-000000000001	active	2025-09-03 09:05:00+03	\N
722e489d-ed8a-4903-8091-088aa31c4f1f	0a000000-0000-0000-0000-000000000004	0c000000-0000-0000-0000-000000000001	active	2025-09-03 09:10:00+03	\N
55ecfa17-7b3e-488c-80c0-b1f7dfd3fc52	0a000000-0000-0000-0000-000000000005	0c000000-0000-0000-0000-000000000001	active	2025-09-11 09:00:00+03	\N
867f6418-14ee-4266-9b69-05d8110323fe	0a000000-0000-0000-0000-000000000010	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
1c6dd6bc-50cb-47ce-ac53-638798480b2a	0a000000-0000-0000-0000-000000000011	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
b71b9eca-f904-4230-95b1-9630a54e8e84	0a000000-0000-0000-0000-000000000012	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
2283c8b1-4829-4ff6-b307-ab4a1b069820	0a000000-0000-0000-0000-000000000013	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
5948118e-6716-4696-b9f9-b534f592ff50	0a000000-0000-0000-0000-000000000014	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
c21c003c-5b62-4df9-a2b4-229a3afeb500	0a000000-0000-0000-0000-000000000015	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
7c146690-6574-4fec-a080-ded1abf8adbb	0a000000-0000-0000-0000-000000000016	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
b5479f68-bc12-47fe-9758-7a4b7e5b9aab	0a000000-0000-0000-0000-000000000017	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
9baf24fb-9c1d-4223-b067-49a2c25ea58d	0a000000-0000-0000-0000-000000000018	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
248ca07f-b25c-46b5-9793-b8127ae51fdc	0a000000-0000-0000-0000-000000000019	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
27d0f9ca-6c5a-4a48-8147-4b90edd5bcd2	0a000000-0000-0000-0000-00000000001a	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
3667bb0b-fdd1-477c-9f0f-ca5b89093bd8	0a000000-0000-0000-0000-00000000001b	0c000000-0000-0000-0000-000000000001	active	2026-06-09 23:23:44.059174+03	\N
5165d15b-46b2-44b5-a497-b1fc3900dda3	96a9242b-7429-4a6d-bfc3-0bdad53a8a73	0c000000-0000-0000-0000-000000000001	active	2026-06-12 14:36:49.096+03	\N
4a0f7971-d0f7-40ab-b716-5027b7202737	0a000000-0000-0000-0000-000000000005	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-06-12 16:17:18.373+03	\N
c1ad8270-9f6f-44e7-852d-5907dc67c8e0	0a000000-0000-0000-0000-000000000002	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.85+03	\N
b9c6a9f7-3547-4e40-b77e-33cc5a067dc8	0a000000-0000-0000-0000-000000000003	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.867+03	\N
b69fa224-d7de-468a-a92b-b4648ca03c31	0a000000-0000-0000-0000-000000000004	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.87+03	\N
379b24ef-d077-4496-b155-a812ae77e624	0a000000-0000-0000-0000-000000000010	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.873+03	\N
9bccd5cc-29fa-4908-a932-be1bf756c1ee	0a000000-0000-0000-0000-000000000011	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.875+03	\N
7d94168a-a5b1-4bf5-9067-7e03ad9bd5d7	0a000000-0000-0000-0000-000000000012	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.877+03	\N
6df00b58-dbf6-4604-baf2-4b71ef24b06d	0a000000-0000-0000-0000-000000000013	758a89c8-4b2a-44c5-9156-200aaa59fcbe	active	2026-05-23 21:12:44.878+03	\N
0d2f0adb-5e18-4d32-9818-2fdf81f80987	0a000000-0000-0000-0000-000000000002	9e37f28b-b379-49b9-9aa2-d90d8a801c04	active	2026-05-26 11:23:41.709+03	\N
1ba61e28-a640-4979-b7de-94116dddaad5	0a000000-0000-0000-0000-000000000003	9e37f28b-b379-49b9-9aa2-d90d8a801c04	active	2026-05-26 11:23:41.724+03	\N
c27feb93-eb1e-4e9a-82ab-9e34ebf518e0	0a000000-0000-0000-0000-000000000004	9e37f28b-b379-49b9-9aa2-d90d8a801c04	active	2026-05-26 11:23:41.726+03	\N
d304daf1-c77c-45b6-b0ff-f095bb4b7ac1	0a000000-0000-0000-0000-000000000005	9e37f28b-b379-49b9-9aa2-d90d8a801c04	active	2026-05-26 11:23:41.728+03	\N
f2086422-5e10-4e3f-b8e7-586604c0761b	0a000000-0000-0000-0000-000000000010	9e37f28b-b379-49b9-9aa2-d90d8a801c04	active	2026-05-26 11:23:41.729+03	\N
429b3fda-bc9d-4956-b525-59911d6ebfac	0a000000-0000-0000-0000-000000000011	9e37f28b-b379-49b9-9aa2-d90d8a801c04	active	2026-05-26 11:23:41.731+03	\N
0ffda512-d8b6-4951-8470-6500f4de0105	0a000000-0000-0000-0000-000000000002	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	active	2026-05-26 11:33:11.191+03	\N
20d03f7c-a2de-43d6-89a1-9051b35d1b76	0a000000-0000-0000-0000-000000000003	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	active	2026-05-26 11:33:11.193+03	\N
3e3e061b-ae90-41b2-9234-4dd103802565	0a000000-0000-0000-0000-000000000004	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	active	2026-05-26 11:33:11.194+03	\N
eb6f9169-f804-4a3c-921f-2f2573b0a544	0a000000-0000-0000-0000-000000000005	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	active	2026-05-26 11:33:11.195+03	\N
76891eb1-eb26-41c9-8716-d44623308b71	0a000000-0000-0000-0000-000000000010	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	active	2026-05-26 11:33:11.196+03	\N
15863e60-440c-476f-8567-c4d6c3c647a1	0a000000-0000-0000-0000-000000000011	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	active	2026-05-26 11:33:11.198+03	\N
9a4cb17e-68a0-4656-bb43-2fc010a06041	0a000000-0000-0000-0000-000000000002	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	active	2026-05-26 11:42:14.239+03	\N
8cbd64bd-4fc8-438a-85f3-c00b0bf55d8c	0a000000-0000-0000-0000-000000000003	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	active	2026-05-26 11:42:14.241+03	\N
2281f0fc-b389-4ddd-9c57-0d1d6f192df7	0a000000-0000-0000-0000-000000000004	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	active	2026-05-26 11:42:14.242+03	\N
3594ae3c-f8a0-44aa-9cdc-6db37adcd551	0a000000-0000-0000-0000-000000000005	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	active	2026-05-26 11:42:14.243+03	\N
4a143544-752a-4572-9cb1-8b5a698f94e2	0a000000-0000-0000-0000-000000000010	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	active	2026-05-26 11:42:14.244+03	\N
925ca0f9-4293-4560-8299-32f1d3697464	0a000000-0000-0000-0000-000000000011	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	active	2026-05-26 11:42:14.245+03	\N
4dd93af9-891f-49d8-8faf-cc3def36362f	0a000000-0000-0000-0000-000000000002	f21476f6-df52-474c-88ca-b20c8e79eb71	active	2026-05-26 11:49:49.009+03	\N
0e754435-6ae3-4b61-a63e-a279c29d7766	0a000000-0000-0000-0000-000000000003	f21476f6-df52-474c-88ca-b20c8e79eb71	active	2026-05-26 11:49:49.01+03	\N
d2219f86-8441-44f4-a603-0e11d1d96476	0a000000-0000-0000-0000-000000000004	f21476f6-df52-474c-88ca-b20c8e79eb71	active	2026-05-26 11:49:49.011+03	\N
b801aaf6-943e-493c-b317-10513d12dd85	0a000000-0000-0000-0000-000000000005	f21476f6-df52-474c-88ca-b20c8e79eb71	active	2026-05-26 11:49:49.012+03	\N
882024a6-086a-43bb-b2c0-11c603019f0b	0a000000-0000-0000-0000-000000000010	f21476f6-df52-474c-88ca-b20c8e79eb71	active	2026-05-26 11:49:49.013+03	\N
e6cb5eaf-8d1a-4bc2-98e2-954bf1bba600	0a000000-0000-0000-0000-000000000011	f21476f6-df52-474c-88ca-b20c8e79eb71	active	2026-05-26 11:49:49.014+03	\N
f35d3890-70c3-4fb6-9818-891a68766ad8	0a000000-0000-0000-0000-000000000002	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	active	2026-05-26 12:46:33.446+03	\N
db5f1e67-7a21-4339-878c-45e65305acf4	0a000000-0000-0000-0000-000000000003	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	active	2026-05-26 12:46:33.448+03	\N
2218526a-8b9f-4af8-9616-36d27883bb90	0a000000-0000-0000-0000-000000000004	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	active	2026-05-26 12:46:33.449+03	\N
5875d740-695c-45fd-b331-6d40b0b3a69d	0a000000-0000-0000-0000-000000000005	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	active	2026-05-26 12:46:33.45+03	\N
b716ccdf-327c-4824-9786-c12e367578dd	0a000000-0000-0000-0000-000000000010	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	active	2026-05-26 12:46:33.451+03	\N
72fc62d7-d4a5-47c4-a687-ca8dabacddcc	0a000000-0000-0000-0000-000000000011	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	active	2026-05-26 12:46:33.452+03	\N
cd087066-7655-47a3-93f5-36a019245453	0a000000-0000-0000-0000-000000000002	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	active	2026-05-28 16:30:10.822+03	\N
d9fbe18d-d56d-4db6-a76b-5c9982621299	0a000000-0000-0000-0000-000000000003	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	active	2026-05-28 16:30:10.824+03	\N
4c737d5e-b6fb-40e1-b583-df1670f44c03	0a000000-0000-0000-0000-000000000004	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	active	2026-05-28 16:30:10.825+03	\N
52fd99f6-f38f-4fe3-b975-f6c9fb9afff1	0a000000-0000-0000-0000-000000000005	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	active	2026-05-28 16:30:10.825+03	\N
387f14f1-82f1-43ff-b741-40f70f4010d8	0a000000-0000-0000-0000-000000000010	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	active	2026-05-28 16:30:10.826+03	\N
61b971cf-29e3-4383-b46e-3d470a54a89a	0a000000-0000-0000-0000-000000000011	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	active	2026-05-28 16:30:10.827+03	\N
\.


--
-- Data for Name: lesson_progress; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lesson_progress (id, user_id, lesson_id, status, time_spent_sec, visits, started_at, completed_at) FROM stdin;
179af951-a0f2-46b0-835b-7b091f0947bb	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000001	completed	1850	3	2025-09-05 18:00:00+03	2025-09-05 18:31:00+03
9b9363cf-13a1-4d4b-bb15-4a0c4302b1d9	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000002	completed	1700	2	2025-09-08 18:00:00+03	2025-09-08 18:29:00+03
3cb80486-4847-4806-9d9b-5029e5e7962e	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000003	completed	2200	2	2025-09-15 18:00:00+03	2025-09-15 18:37:00+03
d47cf123-9c3f-4d0e-ae28-f67ad33a1f7c	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000004	completed	2400	3	2025-09-22 18:00:00+03	2025-09-22 18:41:00+03
d00bf827-9479-40f1-966b-60361ce60041	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000005	in_progress	900	1	2025-10-13 18:00:00+03	\N
47a66933-85b2-40de-bbb1-b9e6a36c4698	0a000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000001	completed	1600	2	2025-09-06 12:00:00+03	2025-09-06 12:28:00+03
dde8a2b9-bb2d-401f-9b5b-b1b471a687d4	0a000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000002	completed	1500	1	2025-09-10 12:00:00+03	2025-09-10 12:26:00+03
50bb90fa-3d03-4c54-a015-82c41f41a267	0a000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000003	in_progress	600	1	2025-09-18 12:00:00+03	\N
9ef01323-dbef-4466-89f8-79c0c78d5bf6	0a000000-0000-0000-0000-000000000004	0e000000-0000-0000-0000-000000000001	completed	1400	2	2025-09-07 11:00:00+03	2025-09-07 11:24:00+03
fbdc4be9-8601-4639-b0f3-0ae3f37cf198	0a000000-0000-0000-0000-000000000004	0e000000-0000-0000-0000-000000000002	in_progress	400	1	2025-09-20 11:00:00+03	\N
fbc4320b-6fed-43a0-a957-9cfca2785dd1	0a000000-0000-0000-0000-000000000005	0e000000-0000-0000-0000-000000000001	completed	300	1	2025-10-19 20:00:00+03	2026-06-09 11:46:51.947+03
8623f4d5-765f-46d1-b274-28a9058fd128	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
ac611ef3-6001-42a8-a029-84bfb051a6ff	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
83d35a9d-5e88-4387-bf01-180a98e19d58	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000003	completed	0	0	\N	2026-06-09 23:23:44.059174+03
98dc3ae1-84c7-4868-b6a4-7d8ea0abecfc	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000004	completed	0	0	\N	2026-06-09 23:23:44.059174+03
316bd57e-5b9c-4f9c-a472-4088dbd78a4a	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000005	completed	0	0	\N	2026-06-09 23:23:44.059174+03
4cea3944-6ae1-4a21-929a-60575c862ac3	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000006	completed	0	0	\N	2026-06-09 23:23:44.059174+03
42b48141-4bab-47a0-9e50-6d78bc32a06f	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
45294f7c-cd53-40be-b87f-c292a49cefc4	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
3aab7fb8-b413-40e0-9858-f0c5506a247e	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000003	completed	0	0	\N	2026-06-09 23:23:44.059174+03
1357deb9-2c21-4269-9e75-e652a3ebb953	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000004	completed	0	0	\N	2026-06-09 23:23:44.059174+03
4bd94fa4-db4a-4a5e-a984-935b1605896c	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000005	completed	0	0	\N	2026-06-09 23:23:44.059174+03
77f3f72f-243c-47f4-b316-b8a3f312b499	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
067e4c1c-36cf-4864-95d2-f752fe7c28e0	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
6559a567-e508-4292-a15a-4ca7994ef587	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000003	completed	0	0	\N	2026-06-09 23:23:44.059174+03
ad35366d-e00c-4bd7-a87a-262c6fecbbfe	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000004	completed	0	0	\N	2026-06-09 23:23:44.059174+03
16e0dc1b-ca86-4388-bffd-70c5c9af6e98	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000005	completed	0	0	\N	2026-06-09 23:23:44.059174+03
6c481470-5bce-4f30-a3b2-c31e9c8d7bbf	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000006	completed	0	0	\N	2026-06-09 23:23:44.059174+03
c7e16472-ec40-4f69-bc0b-78f80434e669	0a000000-0000-0000-0000-000000000013	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
7df767ce-0d14-41f0-a315-d1c7a3dcea77	0a000000-0000-0000-0000-000000000013	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
b9ed8074-ee0b-4367-b7f1-70fabe216a2c	0a000000-0000-0000-0000-000000000013	0e000000-0000-0000-0000-000000000003	completed	0	0	\N	2026-06-09 23:23:44.059174+03
a2217a11-4866-4961-9e21-b0e056c2940b	0a000000-0000-0000-0000-000000000013	0e000000-0000-0000-0000-000000000004	completed	0	0	\N	2026-06-09 23:23:44.059174+03
27a961be-4716-476c-a0f7-26fb01c745ac	0a000000-0000-0000-0000-000000000014	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
9cee05e0-a200-408c-86ca-eb3bbbfba7aa	0a000000-0000-0000-0000-000000000014	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
9645596c-bd92-4fa6-aa9a-f236ba280a9a	0a000000-0000-0000-0000-000000000014	0e000000-0000-0000-0000-000000000003	completed	0	0	\N	2026-06-09 23:23:44.059174+03
459ebf76-2108-491c-b6ed-ebe66c22797f	0a000000-0000-0000-0000-000000000015	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
09971111-dc3d-4099-986c-8f9165ec5602	0a000000-0000-0000-0000-000000000015	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
8fd2211c-d8d2-476c-893a-ff20ae4ca13a	0a000000-0000-0000-0000-000000000016	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
4b238d64-a06b-4b16-8439-19a7f6f205f8	0a000000-0000-0000-0000-000000000016	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
0e5719d0-c677-447a-ab06-8dec0cd95ab3	0a000000-0000-0000-0000-000000000016	0e000000-0000-0000-0000-000000000003	completed	0	0	\N	2026-06-09 23:23:44.059174+03
3390a355-ca2c-4d94-a295-b6bd132b673e	0a000000-0000-0000-0000-000000000017	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
b23928de-6b4d-4f33-90de-e949080cb4bc	0a000000-0000-0000-0000-000000000017	0e000000-0000-0000-0000-000000000002	completed	0	0	\N	2026-06-09 23:23:44.059174+03
b831761e-a426-4662-bf65-53ff451a65e1	0a000000-0000-0000-0000-000000000018	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
c3d8d4d6-407c-43e3-9a96-68da9313cd8a	0a000000-0000-0000-0000-00000000001a	0e000000-0000-0000-0000-000000000001	completed	0	0	\N	2026-06-09 23:23:44.059174+03
1eb3f921-0f9f-43b0-9030-e9c0b11b73eb	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
a93ac806-57c0-43d8-8106-13b460dc98e3	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000008	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
6f8a55d9-ba55-4815-b516-87bf0227288b	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000009	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
c3b186d7-ed53-4cdf-9924-fad9be430aea	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-00000000000a	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
6c899462-fa9f-481e-9839-234135941083	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-00000000000b	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
d3bd4c31-5203-4d91-81e5-70d43aa60265	0a000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-00000000000c	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
24d65962-7d16-4f81-a62a-9c85479653fc	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
711e18a0-1056-47da-bd65-a2edc787d700	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000008	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
e1e12228-a503-4ddd-8c56-8dafb580ca84	0a000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000009	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
b97dcdea-3ebc-4380-92e7-c2c9a67487d6	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
f6e93f2b-d64d-43b5-b5b4-7552da98723f	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000008	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
c9e28ff2-dd59-4b53-bdc3-f5bb0a92abf6	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000009	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
789b6122-acc2-443a-81d2-4fefe4429e89	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-00000000000a	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
3c69be52-4a7f-4eab-af47-28c7e1391b73	0a000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-00000000000b	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
958e24a7-7873-48c6-907a-a1e490994e6e	0a000000-0000-0000-0000-000000000013	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
5e78cae8-5671-4639-896d-9dae5f93af20	0a000000-0000-0000-0000-000000000013	0e000000-0000-0000-0000-000000000008	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
c11f100c-969a-49fd-a0d6-17063a1a5eeb	0a000000-0000-0000-0000-000000000014	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
6c928e96-00f3-405a-b91d-2be4d359ccfa	0a000000-0000-0000-0000-000000000016	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
4700aa23-a847-4d12-a3a5-495979651eb5	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
ef2e6f00-ca44-4759-a07f-5a82bcdc067e	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000008	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
21713101-5bdd-4469-9d09-3baff4d7e9c5	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000009	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
f6b1f21e-bfc2-473a-8a2e-5b121139d51f	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-00000000000a	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
cac840be-fba9-4abf-a32b-7dd0a8c1f3ab	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-00000000000b	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
09efb0cb-021c-4c9f-82f8-792abcdbaefa	0a000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000007	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
9c414e5d-d02a-4582-b85a-63128d203092	0a000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000008	completed	1600	2	2026-05-22 23:48:37.152473+03	2026-06-02 23:48:37.152473+03
6f75c4e7-579c-40e3-86d7-16526f63cf8d	0a000000-0000-0000-0000-000000000005	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-03 21:12:44.947+03	2026-06-04 07:21:59.2+03
a313629d-3466-4032-b4b1-ab03796d8a28	0a000000-0000-0000-0000-000000000010	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-04 21:12:44.953+03	2026-06-05 07:21:59.204+03
6738144c-6020-4017-ab73-0502c9b4773b	0a000000-0000-0000-0000-000000000011	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-05 21:12:44.958+03	2026-06-06 07:21:59.208+03
5c7b182e-59a7-4e43-b76e-fba3a035b6a8	0a000000-0000-0000-0000-000000000012	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-06 21:12:44.964+03	2026-06-07 07:21:59.211+03
ac82abe3-6237-47ce-871f-639873419cdc	0a000000-0000-0000-0000-000000000013	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-07 21:12:44.969+03	2026-06-08 07:21:59.215+03
73c59bfb-9220-4e15-9c40-0cf52b335936	0a000000-0000-0000-0000-000000000003	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-01 21:12:44.937+03	2026-06-02 07:21:59.191+03
67217db0-0a63-40b2-a96a-d05c1db1fe8e	0a000000-0000-0000-0000-000000000003	8dae3fac-b120-4fa6-b46b-c166f2c1965f	completed	0	1	2026-06-06 11:49:49.025+03	2026-06-08 16:30:10.785+03
e6d50358-f937-4c83-8484-66324ccb16d5	0a000000-0000-0000-0000-000000000004	8dae3fac-b120-4fa6-b46b-c166f2c1965f	completed	0	1	2026-06-07 11:49:49.028+03	2026-06-09 16:30:10.787+03
590199f7-7d64-48d9-9e49-2bc01d72fb65	0a000000-0000-0000-0000-000000000005	8dae3fac-b120-4fa6-b46b-c166f2c1965f	completed	0	1	2026-06-08 11:49:49.029+03	2026-06-10 16:30:10.789+03
f07d2d5a-c9e4-4243-b36d-cccc66a92fd7	0a000000-0000-0000-0000-000000000010	8dae3fac-b120-4fa6-b46b-c166f2c1965f	completed	0	1	2026-06-09 11:49:49.031+03	2026-06-11 16:30:10.791+03
2224e9b5-3e49-464f-b6d4-24a294935c72	0a000000-0000-0000-0000-000000000011	8dae3fac-b120-4fa6-b46b-c166f2c1965f	completed	0	1	2026-06-10 11:49:49.033+03	2026-06-12 16:30:10.793+03
fb206835-1820-45e2-b137-657fb3ef5cdd	0a000000-0000-0000-0000-000000000002	1a340833-305a-415a-aab5-08d5e36d17c8	completed	0	1	2026-06-05 12:46:33.461+03	2026-06-07 16:30:10.809+03
b19ae1b6-29f0-4ffc-bf49-e33737a34f53	0a000000-0000-0000-0000-000000000003	1a340833-305a-415a-aab5-08d5e36d17c8	completed	0	1	2026-06-06 12:46:33.465+03	2026-06-08 16:30:10.811+03
35db6cf8-43d1-4d8d-a750-40afec8cfbf8	0a000000-0000-0000-0000-000000000004	1a340833-305a-415a-aab5-08d5e36d17c8	completed	0	1	2026-06-07 12:46:33.469+03	2026-06-09 16:30:10.813+03
b17b49e8-cf73-471a-b895-cf4e3968e1ad	0a000000-0000-0000-0000-000000000005	1a340833-305a-415a-aab5-08d5e36d17c8	completed	0	1	2026-06-08 12:46:33.472+03	2026-06-10 16:30:10.815+03
5d8d7080-04c8-404f-ac60-09fc97197646	0a000000-0000-0000-0000-000000000010	1a340833-305a-415a-aab5-08d5e36d17c8	completed	0	1	2026-06-09 12:46:33.474+03	2026-06-11 16:30:10.817+03
2e205030-622b-4f43-b8df-3d6ebb7e2065	0a000000-0000-0000-0000-000000000011	1a340833-305a-415a-aab5-08d5e36d17c8	completed	0	1	2026-06-10 12:46:33.478+03	2026-06-12 16:30:10.819+03
6060e983-6f3d-4a8e-a173-080acaa877cf	0a000000-0000-0000-0000-000000000002	42487a06-725b-48e1-a85d-9933d35a3b4b	completed	0	1	2026-06-07 16:30:10.834+03	2026-06-07 16:30:10.834+03
118a8ccc-76c4-4b86-b281-2fba5c365918	0a000000-0000-0000-0000-000000000002	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-05-31 21:12:44.922+03	2026-06-01 07:21:59.174+03
62e94cb4-9efc-45af-8122-9b74b2961b17	0a000000-0000-0000-0000-000000000004	656a356d-8ad7-4bb5-b5b5-3597d30936f8	completed	0	1	2026-06-02 21:12:44.943+03	2026-06-03 07:21:59.195+03
3c9bdbd2-44e2-4e7f-8426-a677dce3c24f	0a000000-0000-0000-0000-000000000002	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-05-31 21:12:44.981+03	2026-06-01 07:21:59.223+03
49b36f10-4c5e-4015-bfc4-99faf0e3dd90	0a000000-0000-0000-0000-000000000003	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-01 21:12:44.986+03	2026-06-02 07:21:59.226+03
846aa4b9-987a-4e14-a3c9-a8e859c882e7	0a000000-0000-0000-0000-000000000004	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-02 21:12:44.99+03	2026-06-03 07:21:59.23+03
8407790e-a05e-4205-a28a-014cbe4b5abc	0a000000-0000-0000-0000-000000000005	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-03 21:12:44.994+03	2026-06-04 07:21:59.234+03
7ab10022-1fa1-4f3e-ae91-fde362f6159a	0a000000-0000-0000-0000-000000000010	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-04 21:12:44.997+03	2026-06-05 07:21:59.239+03
4b2df6f7-4902-4bc5-9ece-7fee68268548	0a000000-0000-0000-0000-000000000011	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-05 21:12:45.001+03	2026-06-06 07:21:59.243+03
41fe366f-a958-4d56-be04-efea9835b652	0a000000-0000-0000-0000-000000000012	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-06 21:12:45.004+03	2026-06-07 07:21:59.246+03
1b7a0ea8-664c-466a-a814-2cdd986288bd	0a000000-0000-0000-0000-000000000013	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	completed	0	1	2026-06-07 21:12:45.01+03	2026-06-08 07:21:59.249+03
1c7fac17-4a8b-4191-8b81-888e27de431e	0a000000-0000-0000-0000-000000000002	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-05-31 21:12:45.02+03	2026-06-01 07:21:59.256+03
5a97f571-92bf-48dc-b054-a4288bbb7cbc	0a000000-0000-0000-0000-000000000003	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-01 21:12:45.023+03	2026-06-02 07:21:59.259+03
0507fb59-b611-4713-8e58-78e71db670d7	0a000000-0000-0000-0000-000000000004	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-02 21:12:45.026+03	2026-06-03 07:21:59.264+03
8a8a94ed-c297-4d73-b343-bee051edcb37	0a000000-0000-0000-0000-000000000005	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-03 21:12:45.028+03	2026-06-04 07:21:59.269+03
2aa43b5c-f858-4909-8ec9-90b5a6c2c821	0a000000-0000-0000-0000-000000000010	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-04 21:12:45.031+03	2026-06-05 07:21:59.272+03
c58cb533-2eea-4d27-a995-0e0c9734a1b0	0a000000-0000-0000-0000-000000000011	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-05 21:12:45.033+03	2026-06-06 07:21:59.275+03
a95a474e-47b2-461d-8536-1775a5326ac4	0a000000-0000-0000-0000-000000000012	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-06 21:12:45.036+03	2026-06-07 07:21:59.277+03
887e4230-def4-4f4c-af56-abf37ef4cdfd	0a000000-0000-0000-0000-000000000013	216f012b-02e7-49c4-81e1-08e8a9af6dcd	completed	0	1	2026-06-07 21:12:45.039+03	2026-06-08 07:21:59.279+03
7dc36f8a-e25e-4cbc-9122-3da93141dfe1	0a000000-0000-0000-0000-000000000003	42487a06-725b-48e1-a85d-9933d35a3b4b	completed	0	1	2026-06-08 16:30:10.843+03	2026-06-08 16:30:10.843+03
fd1d2601-fdfe-4f29-a01c-058b2d9759db	0a000000-0000-0000-0000-000000000004	42487a06-725b-48e1-a85d-9933d35a3b4b	completed	0	1	2026-06-09 16:30:10.845+03	2026-06-09 16:30:10.845+03
48a70b87-cd87-4873-bd73-002017636da9	0a000000-0000-0000-0000-000000000005	42487a06-725b-48e1-a85d-9933d35a3b4b	completed	0	1	2026-06-10 16:30:10.847+03	2026-06-10 16:30:10.847+03
b4a7207c-ab34-499a-aa78-e79a82706489	0a000000-0000-0000-0000-000000000010	42487a06-725b-48e1-a85d-9933d35a3b4b	completed	0	1	2026-06-11 16:30:10.849+03	2026-06-11 16:30:10.849+03
55572a98-3ccf-44ce-88d7-a5d146356f26	0a000000-0000-0000-0000-000000000011	42487a06-725b-48e1-a85d-9933d35a3b4b	completed	0	1	2026-06-12 16:30:10.851+03	2026-06-12 16:30:10.851+03
37a6968f-1e0c-4c61-a461-4f012d3da23f	0a000000-0000-0000-0000-000000000005	5d1a6e20-fd15-4a96-8790-2bd1e75d75f3	completed	0	1	2026-06-19 11:43:24.8+03	2026-06-19 11:43:24.8+03
cd60391c-2996-4659-8cad-00c4e8a4e59e	0a000000-0000-0000-0000-000000000002	12f8a209-f08e-4629-91d2-cdaa4af53c53	completed	0	1	2026-06-05 11:23:41.772+03	2026-06-07 16:30:10.662+03
3c95b01f-a610-43e8-ba91-4a2967e6e89e	0a000000-0000-0000-0000-000000000003	12f8a209-f08e-4629-91d2-cdaa4af53c53	completed	0	1	2026-06-06 11:23:41.806+03	2026-06-08 16:30:10.688+03
85953934-85f7-483b-9256-7309905bbe30	0a000000-0000-0000-0000-000000000004	12f8a209-f08e-4629-91d2-cdaa4af53c53	completed	0	1	2026-06-07 11:23:41.811+03	2026-06-09 16:30:10.692+03
48062d8e-bea7-4fa4-9593-4ec4ddfc6be9	0a000000-0000-0000-0000-000000000005	12f8a209-f08e-4629-91d2-cdaa4af53c53	completed	0	1	2026-06-08 11:23:41.816+03	2026-06-10 16:30:10.696+03
b4bf9ed3-eba7-426a-bc0f-d517241ad9a9	0a000000-0000-0000-0000-000000000010	12f8a209-f08e-4629-91d2-cdaa4af53c53	completed	0	1	2026-06-09 11:23:41.82+03	2026-06-11 16:30:10.7+03
b79c7e05-907e-4652-a7ad-724440294ff4	0a000000-0000-0000-0000-000000000011	12f8a209-f08e-4629-91d2-cdaa4af53c53	completed	0	1	2026-06-10 11:23:41.823+03	2026-06-12 16:30:10.703+03
d2434bde-5ec5-40b6-b75e-848828850b1e	0a000000-0000-0000-0000-000000000002	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	completed	0	1	2026-06-05 11:33:11.208+03	2026-06-07 16:30:10.722+03
67d33046-58e3-4815-a527-30be0364e045	0a000000-0000-0000-0000-000000000003	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	completed	0	1	2026-06-06 11:33:11.212+03	2026-06-08 16:30:10.725+03
bedceb65-4959-4919-8aa4-6d36799e3e42	0a000000-0000-0000-0000-000000000004	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	completed	0	1	2026-06-07 11:33:11.215+03	2026-06-09 16:30:10.728+03
3df79491-378b-49ed-8d49-d3e370a0afcb	0a000000-0000-0000-0000-000000000010	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	completed	0	1	2026-06-09 11:33:11.219+03	2026-06-11 16:30:10.735+03
919928db-799d-4e96-b811-6f8b8dff09ae	0a000000-0000-0000-0000-000000000011	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	completed	0	1	2026-06-10 11:33:11.222+03	2026-06-12 16:30:10.738+03
880388f8-a0b8-473b-bd9f-4e5f21ec20f4	0a000000-0000-0000-0000-000000000002	a76e62b1-ed81-4666-ab21-3ee82561ec15	completed	0	1	2026-06-05 11:42:14.253+03	2026-06-07 16:30:10.756+03
27fe9921-8781-4f31-a254-6fefd5554983	0a000000-0000-0000-0000-000000000003	a76e62b1-ed81-4666-ab21-3ee82561ec15	completed	0	1	2026-06-06 11:42:14.255+03	2026-06-08 16:30:10.757+03
3a8218fa-8d7a-4374-8c29-a71ba769f6df	0a000000-0000-0000-0000-000000000004	a76e62b1-ed81-4666-ab21-3ee82561ec15	completed	0	1	2026-06-07 11:42:14.257+03	2026-06-09 16:30:10.759+03
302772b5-2cdd-48f7-82c1-dfeeb240e67e	0a000000-0000-0000-0000-000000000005	a76e62b1-ed81-4666-ab21-3ee82561ec15	completed	0	1	2026-06-08 11:42:14.26+03	2026-06-10 16:30:10.762+03
b6e09808-04a4-43bd-8ef5-6b82072e1f2d	0a000000-0000-0000-0000-000000000010	a76e62b1-ed81-4666-ab21-3ee82561ec15	completed	0	1	2026-06-09 11:42:14.262+03	2026-06-11 16:30:10.764+03
a8303211-722d-46bc-b729-8e551777ae26	0a000000-0000-0000-0000-000000000011	a76e62b1-ed81-4666-ab21-3ee82561ec15	completed	0	1	2026-06-10 11:42:14.264+03	2026-06-12 16:30:10.767+03
48cf4cd7-d05a-47ca-94ab-004e4c8b249e	0a000000-0000-0000-0000-000000000005	3e61acfb-9f0d-4355-9275-c9c5e13639b5	completed	0	1	2026-06-19 11:43:24.819+03	2026-06-19 11:43:24.819+03
8dc3c0f7-b456-48d8-80bd-7b2100c21416	0a000000-0000-0000-0000-000000000005	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	completed	0	1	2026-06-08 11:33:11.217+03	2026-06-19 11:43:24.824+03
8c367015-130c-4224-bcfe-adcdf0c721f5	0a000000-0000-0000-0000-000000000005	c6961546-24cc-4c8c-9ab5-11dc836974a4	completed	0	1	2026-06-19 11:43:24.824+03	2026-06-19 11:43:24.824+03
5bf06f23-50cf-4891-b516-40d87fdc29d3	0a000000-0000-0000-0000-000000000002	8dae3fac-b120-4fa6-b46b-c166f2c1965f	completed	0	1	2026-06-05 11:49:49.022+03	2026-06-07 16:30:10.782+03
87a02e9a-ceb5-4e49-b489-051ad66d7d18	0a000000-0000-0000-0000-000000000005	8c275646-25f1-4e32-b229-c74e3fd3b193	completed	0	1	2026-06-19 11:43:24.821+03	2026-06-19 11:43:24.821+03
eefbfbb7-b41e-42e7-88a6-a3e570d4d009	0a000000-0000-0000-0000-000000000005	4aff43ad-be28-4469-8215-ccbd3c0b1a45	completed	0	1	2026-06-19 11:43:24.822+03	2026-06-19 11:43:24.822+03
1da1f494-22e1-4a02-ba11-870390e0a568	0a000000-0000-0000-0000-000000000005	67fd2b21-adf0-4cba-af96-30c691d48c56	completed	0	1	2026-06-19 11:43:24.823+03	2026-06-19 11:43:24.823+03
\.


--
-- Data for Name: lessons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lessons (id, module_id, title, theory_content, order_index, est_minutes, xp_reward) FROM stdin;
0e000000-0000-0000-0000-000000000001	0d000000-0000-0000-0000-000000000001	Что такое база данных	Каждый день учитель работает с данными, даже не называя их так: список класса, журнал оценок, табель посещаемости, расписание. Данные — это отдельные факты: фамилия ученика, его оценка, дата урока. Сами по себе факты разрознены; когда мы их упорядочиваем и связываем, они превращаются в информацию, на которую можно опереться при принятии решений.\n\nБаза данных — это организованное хранилище таких данных, устроенное так, чтобы их было удобно добавлять, искать, изменять и анализировать. Привычные примеры из образования: электронный журнал, система «Сетевой город», платформа Moodle. За каждой из них стоит база данных, в которой хранятся ученики, классы, оценки и связи между ними.\n\n## Чем база отличается от документа Word или Excel\n\nТекстовый документ хранит данные так, как их набрали. База данных хранит их по строгим правилам: каждая запись имеет одинаковый набор полей, а система следит, чтобы, например, оценка была числом, а дата — настоящей датой. Благодаря этому по базе можно мгновенно находить нужное (всех отличников группы), считать средние значения и строить отчёты — то, что в обычном документе пришлось бы делать вручную.\n\n## СУБД и PostgreSQL\n\nПрограмма, которая управляет базой данных, называется системой управления базами данных (СУБД). В этом курсе мы используем PostgreSQL — мощную и бесплатную СУБД, которую применяют и в небольших проектах, и в крупных организациях. Понимание того, как она устроена, поможет вам осознанно работать с цифровыми образовательными сервисами, а при необходимости — создавать собственные.	1	30	20
0e000000-0000-0000-0000-000000000002	0d000000-0000-0000-0000-000000000001	Таблица: строки и столбцы	Основной способ хранения данных в реляционной базе — таблица. Она устроена очень привычно: есть столбцы (поля) и строки (записи). Столбцы задают, какие сведения мы храним, а каждая строка — это один объект с конкретными значениями этих сведений.\n\nПредставьте таблицу «Студенты». Столбцы: фамилия, имя, группа, дата рождения. Тогда одна строка — это один студент: Смирнова, Анна, Б-101, 12 мая 2004. Сколько студентов — столько строк; набор столбцов при этом всегда один и тот же.\n\n## Типы данных\n\nУ каждого столбца есть тип — какие значения в нём допустимы: текст (фамилия), целое число (количество баллов), дата (дата рождения), логическое значение «да/нет» (зачёт сдан). Тип — это правило: в числовой столбец нельзя случайно записать слово, и база этого не позволит. Так данные остаются чистыми и пригодными для расчётов.\n\n## Чем это лучше таблицы в Excel\n\nНа первый взгляд таблица базы данных похожа на лист Excel, но отличия важные. В базе действуют строгие правила (типы, обязательность полей), несколько таблиц можно связывать между собой, и она спокойно работает с сотнями тысяч записей и множеством одновременных пользователей. Именно поэтому за электронными журналами стоит база данных, а не общий файл Excel.	2	30	20
0e000000-0000-0000-0000-000000000003	0d000000-0000-0000-0000-000000000002	Сущности и атрибуты	Прежде чем создавать таблицы, нужно понять, что именно мы храним. Для этого выделяют сущности — объекты предметной области, о которых мы собираем сведения. В школе сущностями будут: ученик, учитель, класс, предмет, оценка, урок.\n\nУ каждой сущности есть атрибуты — её свойства. У сущности «Ученик» атрибуты: фамилия, имя, дата рождения, класс. У сущности «Оценка»: значение, дата, предмет. Атрибуты — это будущие столбцы таблицы, а сама сущность — будущая таблица.\n\n## Как выделять сущности\n\nПолезный приём: прочитать описание задачи и подчеркнуть существительные. «Учитель ставит ученику оценку по предмету на уроке» — здесь сразу видны сущности: учитель, ученик, оценка, предмет, урок. Так из обычного описания рождается структура будущей базы.\n\nОдин из главных навыков проектировщика — не смешивать сущности. Например, оценки не стоит «приписывать» прямо к ученику списком в одной ячейке: оценка — это самостоятельная сущность со своими атрибутами (значение, дата, предмет), и для неё нужна отдельная таблица. К тому, как связать её с учеником, мы перейдём в следующем уроке.	1	40	25
0e000000-0000-0000-0000-000000000004	0d000000-0000-0000-0000-000000000002	Связи и ключи	Реальные данные связаны между собой: ученик принадлежит классу, оценка относится к ученику и к предмету. Чтобы база могла хранить эти связи, используют ключи.\n\n## Первичный ключ\n\nПервичный ключ — это поле, которое однозначно определяет каждую строку таблицы, как номер в журнале. Двух одинаковых первичных ключей быть не может. Обычно это специальное поле «id». Благодаря ему можно точно указать «вот этот конкретный ученик», даже если в школе три Ивановых Анны.\n\n## Внешний ключ\n\nВнешний ключ — это поле, которое ссылается на первичный ключ другой таблицы и так связывает их. В таблице «Оценки» поле «id ученика» — внешний ключ: оно показывает, какому ученику принадлежит оценка. База следит, чтобы нельзя было поставить оценку несуществующему ученику — это и есть защита целостности данных.\n\n## Виды связей\n\nСвязи бывают трёх видов. Один-к-одному (1:1): у одного ученика одно личное дело. Один-ко-многим (1:М): в одном классе много учеников, но каждый ученик — в одном классе. Многие-ко-многим (М:N): ученик изучает много предметов, и каждый предмет изучают многие ученики; такие связи разбивают через промежуточную таблицу. Правильно определить вид связи — значит верно спроектировать всю базу.	2	40	25
0e000000-0000-0000-0000-000000000005	0d000000-0000-0000-0000-000000000003	CREATE TABLE в PostgreSQL	Теперь от моделирования перейдём к практике. Таблицы в PostgreSQL создаются командой языка SQL — CREATE TABLE. В ней мы перечисляем название таблицы и её столбцы с типами.\n\n## Пример\n\nСоздадим таблицу студентов:\n\n```\nCREATE TABLE students (\n  id serial PRIMARY KEY,\n  full_name text,\n  group_name text\n);\n```\n\nЗдесь id — первичный ключ (serial означает автоматически растущий номер), full_name и group_name — текстовые поля. Точка с запятой завершает команду.\n\n## Ограничения целостности\n\nКроме типа, столбцу можно задать правила — ограничения. PRIMARY KEY делает поле первичным ключом. NOT NULL запрещает оставлять поле пустым. UNIQUE требует, чтобы значения не повторялись (например, у электронной почты). Эти правила база проверяет сама при каждой записи, не давая занести некорректные данные. Так структура, которую вы спроектировали как ER-модель, превращается в реальную таблицу.	1	45	30
0e000000-0000-0000-0000-000000000006	0d000000-0000-0000-0000-000000000003	SELECT: первая выборка	Данные мало хранить — их нужно извлекать. Для чтения данных служит команда SELECT, пожалуй, самая частая команда SQL. В простейшем виде она выглядит так: SELECT нужные_столбцы FROM таблица.\n\n## Примеры\n\nПоказать все столбцы всех студентов (звёздочка означает «все столбцы»):\n\n```\nSELECT * FROM students;\n```\n\nПоказать только фамилии:\n\n```\nSELECT full_name FROM students;\n```\n\n## Отбор по условию\n\nЧтобы получить не всех, а только нужных, добавляют условие WHERE. Например, выбрать студентов с количеством баллов больше 100:\n\n```\nSELECT full_name FROM students WHERE xp > 100;\n```\n\nБаза вернёт только те строки, которые удовлетворяют условию. Из таких выборок и складываются отчёты для учителя: успеваемость по группе, список не сдавших, активность за неделю. С этого и начинается учебная аналитика, которую вы видите на дашборде преподавателя.	2	45	30
0e000000-0000-0000-0000-000000000007	0d000000-0000-0000-0000-000000000004	WHERE: отбор нужных строк	Запрос SELECT * FROM students; возвращает все строки таблицы. Но на практике учителю редко нужны сразу все данные — чаще нужен срез: только студенты группы Б-101, только те, у кого баллов меньше 60, только давно не заходившие. Для такого отбора служит условие WHERE.\n\n## Как работает WHERE\n\nWHERE ставится после имени таблицы и задаёт условие, которому должна удовлетворять строка, чтобы попасть в результат. База проверяет условие для каждой строки по очереди и оставляет только подходящие.\n\n```\nSELECT full_name, xp\nFROM students\nWHERE xp >= 100;\n```\n\nНаглядно отбор выглядит так:\n\n```\nВсе строки            WHERE xp >= 100         Результат\n┌───────────┐                                ┌───────────┐\n│ Анна   90 │ ──┐                             │ Борис 120 │\n│ Борис 120 │   │  оставить строки,           │ Вика  100 │\n│ Вика  100 │   ├──►  где xp >= 100   ──►     └───────────┘\n│ Глеб   40 │ ──┘\n└───────────┘\n```\n\n## Операторы сравнения\n\nВ условиях используют привычные операторы: = (равно), <> или != (не равно), а также <, >, <=, >=. Сравнение работает и для текста: WHERE group_name = 'Б-101'. Текстовые значения всегда заключаются в одинарные кавычки; двойные кавычки в SQL означают имя объекта, а не текст.\n\n## Несколько условий: AND, OR, NOT\n\nУсловия объединяют логическими связками. AND требует, чтобы выполнялись оба условия; OR — чтобы выполнялось хотя бы одно; NOT инвертирует условие.\n\n```\nSELECT full_name\nFROM students\nWHERE group_name = 'Б-101' AND xp < 60;\n```\n\nТак мы найдём отстающих именно в группе Б-101 — это готовый список кандидатов на дополнительную помощь.\n\n## Удобные операторы: IN, BETWEEN, LIKE, IS NULL\n\nЧастые задачи решаются короче. IN проверяет вхождение в список: WHERE group_name IN ('Б-101', 'Б-102'). BETWEEN задаёт диапазон включительно: WHERE xp BETWEEN 60 AND 90. LIKE ищет по образцу, где знак % заменяет любую последовательность символов: WHERE full_name LIKE 'Ивано%' найдёт всех Ивановых. Пустые значения проверяют особым образом — WHERE last_seen IS NULL, потому что обычное сравнение с NULL не работает.	1	45	30
0e000000-0000-0000-0000-000000000008	0d000000-0000-0000-0000-000000000004	Сортировка и ограничение: ORDER BY, LIMIT	Выбрать нужные строки — половина дела. Часто их ещё надо упорядочить (например, от лучшего балла к худшему) и ограничить количество (показать первую десятку). За это отвечают ORDER BY и LIMIT.\n\n## ORDER BY — сортировка\n\nORDER BY ставится в конце запроса и указывает, по какому столбцу упорядочить результат. По умолчанию сортировка по возрастанию (ASC); чтобы получить по убыванию, добавляют DESC.\n\n```\nSELECT full_name, xp\nFROM students\nORDER BY xp DESC;\n```\n\nЭтот запрос построит рейтинг студентов от наибольшего балла к наименьшему. Можно сортировать сразу по нескольким столбцам — сначала по первому, при равенстве по второму:\n\n```\nSELECT full_name, group_name, xp\nFROM students\nORDER BY group_name ASC, xp DESC;\n```\n\n## LIMIT и OFFSET\n\nLIMIT ограничивает число строк в ответе. Вместе с сортировкой это даёт «топ-N»:\n\n```\nSELECT full_name, xp\nFROM students\nORDER BY xp DESC\nLIMIT 3;\n```\n\nТак мы получим тройку лучших. OFFSET пропускает заданное число строк с начала — это используют для постраничного вывода (например, показать студентов с 11-го по 20-го: LIMIT 10 OFFSET 10).\n\n## DISTINCT — только уникальные значения\n\nИногда нужен список без повторов — например, какие вообще группы есть в таблице. DISTINCT убирает дубликаты:\n\n```\nSELECT DISTINCT group_name\nFROM students;\n```\n\nПорядок частей запроса фиксирован: сначала WHERE (что отобрать), затем ORDER BY (как упорядочить), в конце LIMIT (сколько показать). Если перепутать порядок, PostgreSQL вернёт ошибку.	2	40	30
0e000000-0000-0000-0000-000000000009	0d000000-0000-0000-0000-000000000005	INSERT: добавление строк	До сих пор мы только читали данные. Теперь научимся их добавлять. Новые строки в таблицу вносит команда INSERT.\n\n## Базовый синтаксис\n\nВ INSERT указывают таблицу, перечень столбцов и значения для них:\n\n```\nINSERT INTO students (full_name, group_name, xp)\nVALUES ('Кузнецова Мария', 'Б-101', 0);\n```\n\nСтолбцы и значения сопоставляются по порядку: первому столбцу — первое значение и так далее. Перечислять столбцы явно — хорошая привычка: запрос остаётся понятным и не сломается, если в таблицу позже добавят новый столбец.\n\n## Несколько строк за раз\n\nЧтобы добавить сразу несколько записей, перечисляют несколько наборов значений через запятую — это быстрее, чем несколько отдельных команд:\n\n```\nINSERT INTO students (full_name, group_name, xp)\nVALUES\n  ('Орлов Иван', 'Б-102', 10),\n  ('Лебедева Анна', 'Б-102', 25),\n  ('Соколов Пётр', 'Б-101', 5);\n```\n\n## Значения по умолчанию и автоматические поля\n\nЧасть столбцов база заполняет сама. Если у столбца id задан DEFAULT (например, автонумерация или gen_random_uuid()), его не нужно указывать в INSERT — система подставит значение автоматически. То же касается полей с DEFAULT вроде даты создания.\n\n## RETURNING — узнать, что получилось\n\nПолезная особенность PostgreSQL: команда INSERT может сразу вернуть данные добавленной строки, в том числе сгенерированный id:\n\n```\nINSERT INTO students (full_name, group_name, xp)\nVALUES ('Зайцева Ольга', 'Б-101', 0)\nRETURNING id, full_name;\n```\n\nЭто избавляет от отдельного запроса «а какой id присвоился новой записи» и часто используется в программах, работающих с базой.	1	45	30
0e000000-0000-0000-0000-00000000000a	0d000000-0000-0000-0000-000000000005	UPDATE и DELETE: правка и удаление	Данные меняются: студент набрал новые баллы, перешёл в другую группу, отчислился. Изменяет существующие строки команда UPDATE, а удаляет — DELETE. Обе требуют особой аккуратности.\n\n## UPDATE — изменение данных\n\nUPDATE задаёт, какие столбцы и на какие значения поменять, а условие WHERE определяет, в каких именно строках:\n\n```\nUPDATE students\nSET xp = xp + 10\nWHERE full_name = 'Орлов Иван';\n```\n\nЗдесь баллы Ивана увеличиваются на 10. Обратите внимание: в SET можно использовать текущее значение столбца (xp = xp + 10) — база возьмёт старое значение и пересчитает.\n\n## Главное правило: не забывайте WHERE\n\nЕсли в UPDATE или DELETE забыть условие WHERE, операция применится КО ВСЕМ строкам таблицы. Это самая частая и болезненная ошибка новичков.\n\n```\nОпасно:  UPDATE students SET group_name = 'Б-101';\n         ── изменит группу у ВСЕХ студентов\n\nВерно:   UPDATE students SET group_name = 'Б-101'\n         WHERE id = 5;\n         ── изменит ровно одну нужную строку\n```\n\n## DELETE — удаление строк\n\nDELETE убирает строки, подходящие под условие:\n\n```\nDELETE FROM students\nWHERE xp = 0 AND group_name = 'Б-102';\n```\n\nКак и в UPDATE, без WHERE будут удалены все записи. Перед удалением полезно сначала выполнить SELECT с тем же условием и убедиться, что под него попадают именно те строки, которые вы собираетесь удалить.\n\n## Транзакции — страховка\n\nЧтобы изменения можно было отменить, их выполняют в транзакции: команды между BEGIN и COMMIT применяются все вместе; если что-то пошло не так, ROLLBACK откатывает их, будто ничего не было. Это защищает данные от случайной ошибки в большой операции.	2	45	30
0e000000-0000-0000-0000-00000000000b	0d000000-0000-0000-0000-000000000006	Агрегатные функции: COUNT, SUM, AVG, MIN, MAX	Часто нужны не сами строки, а итог по ним: сколько всего студентов, какой средний балл, кто набрал максимум. Такие сводные значения вычисляют агрегатные функции — они «схлопывают» множество строк в одно число.\n\n## Пять основных функций\n\nCOUNT считает количество строк, SUM суммирует значения столбца, AVG вычисляет среднее, MIN и MAX находят наименьшее и наибольшее значение.\n\n```\nSELECT COUNT(*) AS всего_студентов,\n       AVG(xp)  AS средний_балл,\n       MAX(xp)  AS лучший_результат\nFROM students;\n```\n\nОдна строка таблицы превращается в одну строку-итог:\n\n```\nБыло (много строк)        Стало (одна строка-итог)\n┌───────────┐             ┌───────┬────────┬───────┐\n│ Анна   90 │             │ всего │ средн. │ макс. │\n│ Борис 120 │   AVG/MAX   ├───────┼────────┼───────┤\n│ Вика  100 │  ───────►   │   4   │  87.5  │  120  │\n│ Глеб   40 │             └───────┴────────┴───────┘\n└───────────┘\n```\n\n## COUNT и его варианты\n\nCOUNT(*) считает все строки. COUNT(столбец) считает только строки, где значение не пустое (NOT NULL) — это удобно, чтобы узнать, у скольких студентов вообще заполнено поле. COUNT(DISTINCT столбец) считает число различных значений: COUNT(DISTINCT group_name) покажет, сколько разных групп.\n\n## Псевдонимы AS\n\nРезультат функции лучше называть понятным именем через AS, иначе столбец получит техническое имя вроде «count». Псевдоним делает отчёт читаемым.\n\n## Агрегаты вместе с WHERE\n\nСначала WHERE отбирает строки, а функция считает итог уже по отобранным. Например, средний балл только активной группы:\n\n```\nSELECT AVG(xp) AS средний_по_группе\nFROM students\nWHERE group_name = 'Б-101';\n```\n\nТак из «сырых» строк рождаются показатели, на которые учитель опирается, оценивая класс.	1	45	35
0e000000-0000-0000-0000-00000000000c	0d000000-0000-0000-0000-000000000006	GROUP BY и HAVING	Итог по всей таблице — это хорошо, но обычно интереснее сравнить группы между собой: средний балл в каждой группе, число студентов на каждом курсе. Для этого служит GROUP BY.\n\n## Идея группировки\n\nGROUP BY делит строки на группы по значению указанного столбца, и агрегатная функция считается отдельно внутри каждой группы.\n\n```\nSELECT group_name,\n       COUNT(*)  AS студентов,\n       AVG(xp)   AS средний_балл\nFROM students\nGROUP BY group_name;\n```\n\nСхематично:\n\n```\nСтроки                  GROUP BY group_name      Итог по группам\n┌──────┬─────┐                                   ┌───────┬─────┬──────┐\n│ Б-101│  90 │ ─┐  группа Б-101 ─► COUNT,AVG     │ Б-101 │  2  │ 95.0 │\n│ Б-101│ 100 │ ─┘                                 │ Б-102 │  2  │ 25.0 │\n│ Б-102│  40 │ ─┐  группа Б-102 ─► COUNT,AVG     └───────┴─────┴──────┘\n│ Б-102│  10 │ ─┘\n└──────┴─────┘\n```\n\n## Важное правило\n\nВ SELECT с группировкой можно выводить только столбцы, по которым идёт группировка (group_name), и агрегатные функции (COUNT, AVG и т.п.). Нельзя вывести «обычный» столбец вроде full_name — ведь в одной группе много разных фамилий, и непонятно, какую показать. PostgreSQL на это укажет ошибкой.\n\n## HAVING — фильтр по группам\n\nWHERE фильтрует отдельные строки ДО группировки. А если нужно отобрать сами группы по их итогу (например, только группы со средним баллом ниже 50), используют HAVING — он работает уже ПОСЛЕ группировки:\n\n```\nSELECT group_name, AVG(xp) AS средний\nFROM students\nGROUP BY group_name\nHAVING AVG(xp) < 50;\n```\n\nЗапомните разницу: WHERE — про строки, HAVING — про группы. Часто они работают вместе: WHERE сначала отсеивает лишние строки, GROUP BY группирует оставшиеся, HAVING отбирает нужные группы.	2	45	35
0e000000-0000-0000-0000-00000000000d	0d000000-0000-0000-0000-000000000007	INNER JOIN: соединяем таблицы	Реальные данные хранятся не в одной, а в нескольких связанных таблицах: студенты — в одной, их оценки — в другой, а связаны они по ключу. Чтобы показать данные вместе («фамилия студента и его оценка»), таблицы соединяют командой JOIN.\n\n## Зачем разносить данные\n\nХранить всё в одной таблице неудобно: если у студента много оценок, его фамилия повторялась бы в каждой строке. Поэтому фамилия лежит в таблице students, а оценки — в таблице grades, где есть столбец student_id, ссылающийся на students.id (внешний ключ из урока про связи и ключи).\n\n## INNER JOIN — соединение по совпадению\n\nINNER JOIN сопоставляет строки двух таблиц по условию в ON и оставляет только те пары, где совпадение нашлось:\n\n```\nSELECT s.full_name, g.subject, g.mark\nFROM students s\nINNER JOIN grades g ON g.student_id = s.id;\n```\n\n```\nstudents                 grades                  INNER JOIN\n┌────┬───────┐          ┌──────────┬─────┐       (только совпавшие)\n│ id │ name  │          │ stud_id  │ оц. │       ┌───────┬─────┐\n├────┼───────┤          ├──────────┼─────┤       │ Анна  │  5  │\n│ 1  │ Анна  │◄───┐     │    1     │  5  │       │ Анна  │  4  │\n│ 2  │ Борис │    └─────┤    1     │  4  │  ──►   │ Борис │  3  │\n│ 3  │ Вика  │          │    2     │  3  │       └───────┴─────┘\n└────┴───────┘          └──────────┴─────┘\n        Вика без оценок — в INNER JOIN не попадёт\n```\n\n## Псевдонимы таблиц\n\nДлинные имена таблиц сокращают псевдонимами (students s, grades g) и через них обращаются к столбцам: s.full_name, g.mark. Когда в обеих таблицах есть столбец с одинаковым именем (например, id), псевдоним обязателен, чтобы база поняла, о какой таблице речь.\n\n## Условие соединения ON\n\nВ ON пишут, по каким столбцам связаны таблицы — почти всегда это «внешний ключ = первичный ключ»: ON g.student_id = s.id. Это сердце соединения: именно ON определяет, какие строки считаются «парой». Перепутать здесь столбцы — частая ошибка, ведущая к бессмысленному результату.	1	50	35
0e000000-0000-0000-0000-00000000000e	0d000000-0000-0000-0000-000000000007	LEFT JOIN и виды соединений	INNER JOIN показывает только совпавшие строки. Но часто важны и те, у кого пары нет: студенты, ещё не получившие ни одной оценки. Для этого есть внешние соединения, главное из которых — LEFT JOIN.\n\n## LEFT JOIN — сохранить все строки левой таблицы\n\nLEFT JOIN берёт ВСЕ строки левой таблицы (той, что указана первой), и подставляет к ним данные из правой. Если пары нет, поля правой таблицы заполняются значением NULL.\n\n```\nSELECT s.full_name, g.mark\nFROM students s\nLEFT JOIN grades g ON g.student_id = s.id;\n```\n\n```\n       INNER JOIN              LEFT JOIN\n   (только пересечение)   (все студенты, даже без оценок)\n                          ┌───────┬──────┐\n       ┌──────┐          │ Анна  │  5   │\n      ┌┤ A∩B  ├┐         │ Борис │  3   │\n      └┴──────┴┘         │ Вика  │ NULL │ ◄─ оценок нет\n                          └───────┴──────┘\n```\n\n## Зачем это учителю\n\nИменно LEFT JOIN позволяет находить «пропущенных»: студентов без сданных работ, уроки без тестов, группы без преподавателя. Чтобы получить только таких, добавляют условие на NULL:\n\n```\nSELECT s.full_name\nFROM students s\nLEFT JOIN grades g ON g.student_id = s.id\nWHERE g.id IS NULL;\n```\n\nЭтот запрос вернёт студентов, у которых вообще нет оценок, — потенциальную группу риска.\n\n## RIGHT JOIN и FULL JOIN\n\nRIGHT JOIN — зеркальное отражение LEFT: сохраняет все строки правой таблицы. FULL JOIN сохраняет строки обеих таблиц, подставляя NULL там, где пары нет. На практике чаще всего используют именно LEFT JOIN, потому что обычно ясно, какую таблицу считать «главной», и её ставят слева.\n\n## Кратко о выборе\n\nINNER — когда нужны только связанные данные. LEFT — когда нужны все записи одной таблицы плюс связанные данные второй, включая «пустые» случаи. Правильный выбор соединения напрямую влияет на то, какие выводы учитель сделает по данным.	2	50	35
0e000000-0000-0000-0000-00000000000f	0d000000-0000-0000-0000-000000000008	Аномалии данных и первая нормальная форма	Базу можно спроектировать по-разному, и неудачная структура приводит к ошибкам и лишней работе. Нормализация — это набор правил, как разложить данные по таблицам, чтобы они хранились без избыточности. Начинается всё с первой нормальной формы (1НФ).\n\n## Проблема: всё в одной таблице\n\nПредставим, что студенты и их предметы свалены в одну таблицу, причём предметы записаны списком в одной ячейке:\n\n```\n┌────────┬─────────────────────────┬───────────┐\n│ студент│ предметы                │ препод.   │\n├────────┼─────────────────────────┼───────────┤\n│ Анна   │ Алгебра, Физика, Химия  │ Петров... │\n│ Борис  │ Алгебра, Физика         │ Петров... │\n└────────┴─────────────────────────┴───────────┘\n```\n\n## Три вида аномалий\n\nТакая структура порождает аномалии. Аномалия вставки: нельзя добавить новый предмет, пока на него не записан хотя бы один студент. Аномалия обновления: если предмет переименовали, придётся править его во всех ячейках, и легко что-то пропустить. Аномалия удаления: удалив последнего студента предмета, мы теряем и сам предмет. Всё это — следствие избыточности (одни и те же сведения хранятся много раз).\n\n## Первая нормальная форма (1НФ)\n\nТаблица в 1НФ, если в каждой ячейке хранится одно атомарное значение (не список), и нет повторяющихся групп столбцов. «Алгебра, Физика, Химия» в одной ячейке нарушает 1НФ.\n\n```\nНарушение 1НФ                Приведено к 1НФ\n(список в ячейке)            (одна строка = один факт)\n                             ┌────────┬─────────┐\n Анна | Алгебра,Физика  ──►  │ Анна   │ Алгебра │\n                             │ Анна   │ Физика  │\n                             │ Борис  │ Алгебра │\n                             └────────┴─────────┘\n```\n\n## Почему атомарность важна\n\nКогда в ячейке одно значение, по данным легко искать, фильтровать и считать: «сколько студентов на Физике» — это простой запрос с WHERE. Если же предметы лежат списком в строке, такой подсчёт превращается в мучительный разбор текста. 1НФ — обязательный фундамент: без неё остальные правила нормализации не имеют смысла.	1	50	35
0e000000-0000-0000-0000-000000000010	0d000000-0000-0000-0000-000000000008	Вторая и третья нормальные формы	После приведения к 1НФ данные ещё могут дублироваться. Вторая (2НФ) и третья (3НФ) нормальные формы убирают оставшуюся избыточность, разделяя таблицу на несколько связанных.\n\n## Вторая нормальная форма (2НФ)\n\n2НФ важна, когда первичный ключ составной (из нескольких столбцов). Правило: каждый неключевой столбец должен зависеть от всего ключа, а не от его части. Пример нарушения — таблица (студент, предмет, оценка, преподаватель_предмета): преподаватель зависит только от предмета, а не от пары «студент+предмет», поэтому он будет повторяться.\n\n```\nНарушение 2НФ: «препод» зависит только от предмета\n┌────────┬─────────┬──────┬───────────┐\n│ студент│ предмет │ оц.  │ препод.   │\n├────────┼─────────┼──────┼───────────┤\n│ Анна   │ Физика  │  5   │ Петров    │  ← Петров\n│ Борис  │ Физика  │  4   │ Петров    │  ← повторяется\n└────────┴─────────┴──────┴───────────┘\n```\n\nРешение — вынести предмет с его преподавателем в отдельную таблицу subjects, а в оценках ссылаться на неё по ключу.\n\n## Третья нормальная форма (3НФ)\n\n3НФ убирает транзитивные зависимости — когда неключевой столбец зависит от другого неключевого. Пример: в таблице студентов хранятся group_id и group_curator (куратор группы). Куратор зависит не от студента, а от группы; значит, для каждого студента группы куратор повторяется.\n\n```\nНарушение 3НФ: куратор зависит от группы, а не от студента\n┌────────┬─────────┬──────────────┐\n│ студент│ группа  │ куратор      │\n├────────┼─────────┼──────────────┤\n│ Анна   │ Б-101   │ Иванова И.И. │ ← дублируется\n│ Борис  │ Б-101   │ Иванова И.И. │ ← у всей группы\n└────────┴─────────┴──────────────┘\n```\n\nРешение — отдельная таблица groups (группа, куратор), а в студентах оставить только ссылку group_id.\n\n## Зачем это нужно на практике\n\nНормализованная база хранит каждый факт ровно один раз: сменился куратор — правим одну строку в groups, и изменение видно везде. Это убирает аномалии и противоречия. На очень больших и нагруженных системах иногда сознательно идут на частичную денормализацию ради скорости, но делать это осознанно можно лишь тогда, когда хорошо понимаешь, от чего отказываешься.	2	50	35
0e000000-0000-0000-0000-000000000011	0d000000-0000-0000-0000-000000000009	Ограничения целостности	База ценна тогда, когда данным в ней можно доверять. Чтобы в таблицу не попали бессмысленные или противоречивые значения, при проектировании задают ограничения целостности (constraints) — правила, которые СУБД проверяет автоматически.\n\n## Основные ограничения\n\nPRIMARY KEY — первичный ключ: значение уникально и не пустое, однозначно определяет строку. NOT NULL — поле обязано быть заполнено. UNIQUE — значения в столбце не повторяются (например, email). CHECK — произвольное условие, которому должно удовлетворять значение. FOREIGN KEY — внешний ключ, связывающий таблицу с другой.\n\n```\nCREATE TABLE students (\n  id         serial PRIMARY KEY,\n  email      text   UNIQUE NOT NULL,\n  full_name  text   NOT NULL,\n  xp         integer NOT NULL DEFAULT 0 CHECK (xp >= 0),\n  group_id   integer REFERENCES groups(id)\n);\n```\n\nЗдесь база сама не позволит создать двух студентов с одинаковым email, оставить пустой фамилию или записать отрицательные баллы.\n\n## FOREIGN KEY и ссылочная целостность\n\nВнешний ключ гарантирует, что ссылка ведёт на реально существующую строку: нельзя записать студента в несуществующую группу. Это и называется ссылочной целостностью.\n\n## Что делать при удалении: ON DELETE\n\nВозникает вопрос: что станет с оценками студента, если самого студента удалят? Поведение задаётся при описании внешнего ключа. ON DELETE CASCADE — удалить вместе со студентом и его оценки. ON DELETE RESTRICT — запретить удаление студента, пока у него есть оценки. ON DELETE SET NULL — оставить оценки, но обнулить ссылку.\n\n```\nУдаляем студента id=2\n\nCASCADE  ─► оценки студента 2 тоже удаляются\nRESTRICT ─► удаление запрещено (есть связанные оценки)\nSET NULL ─► оценки остаются, student_id становится NULL\n```\n\n## Почему лучше доверить это базе\n\nМожно проверять корректность данных в программе, но надёжнее, когда правила встроены в саму базу: тогда их невозможно случайно обойти, с какой бы стороны ни пришли данные. Ограничения — это «техника безопасности» базы, заданная один раз на этапе проектирования.	1	50	35
0e000000-0000-0000-0000-000000000012	0d000000-0000-0000-0000-000000000009	Индексы и представления (VIEW)	В завершение — два инструмента, делающих работу с базой быстрее и удобнее: индексы (ускоряют поиск) и представления (упрощают сложные запросы).\n\n## Что такое индекс\n\nИндекс — это вспомогательная структура, которая помогает базе быстро находить строки, не просматривая всю таблицу. Удобная аналогия — алфавитный указатель в конце учебника: вместо того чтобы листать всю книгу в поисках термина, вы открываете указатель и сразу узнаёте нужную страницу.\n\n```\nБез индекса: проверить ВСЕ строки подряд\n  [1][2][3][4][5]...[100000]  — медленно на больших таблицах\n\nС индексом по email: сразу прыгнуть к нужной\n  email ──► указатель ──► строка №57341  — быстро\n```\n\n## Как создать индекс\n\n```\nCREATE INDEX idx_students_group ON students(group_name);\n```\n\nПосле этого запросы с WHERE group_name = '...' будут выполняться заметно быстрее на большой таблице. Индексы особенно полезны для столбцов, по которым часто идёт поиск (WHERE) или соединение (JOIN).\n\n## У индексов есть цена\n\nИндекс занимает место на диске и немного замедляет добавление, изменение и удаление строк (базе приходится обновлять и сам индекс). Поэтому индексируют не всё подряд, а те столбцы, по которым действительно часто ищут. Первичные ключи и UNIQUE-поля индексируются автоматически.\n\n## Представления (VIEW)\n\nПредставление — это сохранённый запрос, к которому обращаются как к таблице. Если сложную выборку (например, сводку успеваемости с JOIN и группировкой) приходится делать часто, её оформляют как VIEW:\n\n```\nCREATE VIEW v_progress AS\nSELECT s.full_name, COUNT(g.id) AS оценок, AVG(g.mark) AS средний\nFROM students s\nLEFT JOIN grades g ON g.student_id = s.id\nGROUP BY s.full_name;\n```\n\nТеперь вместо длинного запроса достаточно написать SELECT * FROM v_progress. Представление не хранит данные отдельно — оно каждый раз выполняет заложенный запрос на актуальных данных. Именно так в нашей платформе устроена сводка прогресса студентов, которую видит преподаватель на дашборде.	2	50	35
8dae3fac-b120-4fa6-b46b-c166f2c1965f	b6ca775f-7a9c-455c-8099-49f8fc187f96	Мониторинг: pg_stat_statements	Чтобы оптимизировать, нужно сначала найти, что именно тормозит. Для этого в PostgreSQL есть встроенные средства мониторинга.\n\n## Расширение pg_stat_statements\n\n`pg_stat_statements` накапливает статистику по всем выполненным запросам: сколько раз каждый выполнялся, суммарное и среднее время. Так находят самые «дорогие» запросы — кандидаты на оптимизацию.\n\n```\nSELECT query, calls, mean_exec_time\nFROM pg_stat_statements\nORDER BY mean_exec_time DESC\nLIMIT 10;\n```\n\n## Системные представления\n\nPostgreSQL также показывает статистику таблиц и индексов (`pg_stat_user_tables`, `pg_stat_user_indexes`): сколько раз сканировалась таблица, используется ли индекс. Неиспользуемые индексы только замедляют запись — их стоит удалять.\n\n## Цикл оптимизации\n\nИзмерить (мониторинг) → найти узкое место → посмотреть план (EXPLAIN ANALYZE) → добавить или поправить индекс / переписать запрос → снова измерить.\n\n## Коротко\n\npg_stat_statements находит самые дорогие запросы, системные представления показывают использование индексов; оптимизация — это цикл «измерил → нашёл → поправил → проверил».\n\n## Литература\n\n- [Документация: pg_stat_statements](https://postgrespro.ru/docs/postgresql/current/pgstatstatements)\n- [PostgreSQL 16. Оптимизация запросов](https://postgrespro.ru/education/books/qptbook)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
81651146-f428-4ee5-8483-4610b7778d4a	ca457d41-474f-425b-b52c-1d74751f00d0	Установка PostgreSQL и psql	PostgreSQL — свободная объектно-реляционная СУБД. Прежде чем писать запросы, её нужно установить и научиться подключаться. Основной консольный клиент — **psql**.\n\n## Установка\n\nPostgreSQL ставят из официального дистрибутива (для Windows — установщик, в Linux — пакет) или через Docker. Вместе с сервером ставится клиент `psql` и графический pgAdmin.\n\n## psql — консоль СУБД\n\n`psql` — интерактивная оболочка для SQL-команд и служебных команд (начинаются с обратной косой черты):\n- `\\l` — список баз;\n- `\\c имя_бд` — подключиться к базе;\n- `\\dt` — список таблиц;\n- `\\d таблица` — структура таблицы;\n- `\\q` — выход.\n\n## Пример\n\n```\npsql -U postgres -d dataedu\ndataedu=# \\dt\n```\n\n## Коротко\n\nPostgreSQL ставят из дистрибутива или Docker; psql — консольный клиент, где служебные команды начинаются с `\\` (\\l, \\dt, \\d, \\q).\n\n## Литература\n\n- [Документация: psql](https://postgrespro.ru/docs/postgresql/current/app-psql)\n- [Postgres: первое знакомство](https://postgrespro.ru/education/books/introbook)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих» (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	0	20	10
a83b1194-5806-41ca-96ee-c6eae3b76c69	4f7c50f2-af4f-453a-927c-034623a2f694	Что такое оконная функция и OVER()	**Оконные функции** выполняют вычисления по набору строк, связанных с текущей, но — в отличие от агрегатов с GROUP BY — **не схлопывают строки**. Каждая строка остаётся в результате, а рядом появляется вычисленное по «окну» значение.\n\n## Окно и OVER()\n\n«Окно» — это множество строк, по которым считается функция. Его задают конструкцией `OVER(...)`. Пустые скобки `OVER ()` означают окно из всех строк результата.\n\n```\nSELECT full_name, avg_grade,\n       AVG(avg_grade) OVER () AS overall_avg\nFROM students;\n```\n\nЗдесь у каждой строки выводятся её балл и общий средний балл — при этом ни одна строка не исчезает.\n\n## Чем отличается от GROUP BY\n\n`GROUP BY` возвращает по одной строке на группу; оконная функция оставляет все строки и добавляет к ним агрегат. Это удобно, когда нужно показать строку **и** её отношение к группе одновременно.\n\n## Коротко\n\nОконная функция считает значение по «окну» строк через OVER(), не схлопывая строки (в отличие от GROUP BY).\n\n## Литература\n\n- [Документация: оконные функции (учебник)](https://postgrespro.ru/docs/postgresql/current/tutorial-window)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
42487a06-725b-48e1-a85d-9933d35a3b4b	bd1d6e65-392c-47e4-8fd1-045217c779db	Аналитика данных оконными функциями	Соберём приёмы вместе: оконные функции — основной инструмент аналитических запросов, отчётов и витрин данных.\n\n## Типовые задачи\n\n- **Рейтинги и топ-N** в каждой категории (ROW_NUMBER + PARTITION BY);\n- **Динамика** относительно прошлого периода (LAG/LEAD);\n- **Нарастающие итоги** и скользящие средние (SUM/AVG с рамкой);\n- **Доли** от общего (агрегат OVER ()).\n\n## Пример: рейтинг внутри группы\n\n```\nSELECT group_name, full_name, avg_grade,\n       RANK() OVER (PARTITION BY group_name ORDER BY avg_grade DESC) AS place_in_group\nFROM students;\n```\n\nОдин запрос сразу даёт место каждого студента в его группе — без подзапросов и самосоединений.\n\n## Почему это удобно\n\nРаньше такие задачи решали громоздкими подзапросами и соединением таблицы с самой собой. Оконные функции выражают ту же логику короче, читаемее и обычно быстрее.\n\n## Коротко\n\nОконные функции — ядро аналитики: рейтинги, динамика, нарастающие итоги и доли выражаются коротко и без самосоединений.\n\n## Литература\n\n- [Документация: оконные функции (учебник)](https://postgrespro.ru/docs/postgresql/current/tutorial-window)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n- [PostgreSQL Exercises](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
3e61acfb-9f0d-4355-9275-c9c5e13639b5	b951683f-55d5-4b76-8e75-152bcbd2419a	Функциональные зависимости	Теория нормализации опирается на понятие **функциональной зависимости** (ФЗ). Понимание ФЗ позволяет формально решать, как разбивать таблицы.\n\n## Что такое функциональная зависимость\n\nАтрибут Y **функционально зависит** от X (пишут X → Y), если каждому значению X соответствует ровно одно значение Y. Пример: номер зачётки → ФИО (по зачётке однозначно определяется имя). А «группа → студент» неверно: в группе много студентов.\n\n## Виды зависимостей\n\n- **Полная**: Y зависит от всего составного ключа, а не от его части.\n- **Частичная**: Y зависит лишь от части составного ключа (нарушает 2НФ).\n- **Транзитивная**: X → Y и Y → Z, значит X → Z через промежуточный атрибут (нарушает 3НФ).\n\n## Пример\n\nВ таблице (студент, группа, куратор): студент → группа, группа → куратор, значит студент → куратор **транзитивно**. От этой транзитивной зависимости избавляется 3НФ.\n\n## Коротко\n\nX → Y означает «по X однозначно определяется Y»; зависимости бывают полные, частичные и транзитивные — на них опираются нормальные формы.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих» (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	1	30	10
31051ef3-f4d3-45a4-af33-e8bcb08edc46	6e25b2e3-aaee-4e08-aed9-3bcc74cf67f6	Подзапросы	Подзапрос — это запрос внутри другого запроса. Он помогает, когда результат одного запроса нужен как условие или источник данных для другого.\n\n## Где применяют\n\nПодзапрос можно поставить:\n- в WHERE — отобрать строки относительно вычисленного значения;\n- после FROM — как временную таблицу (производную таблицу);\n- в списке SELECT — посчитать связанное значение для каждой строки.\n\n## Пример\n\nСтуденты, чей балл выше среднего по всем:\n\n```\nSELECT full_name, avg_grade\nFROM students\nWHERE avg_grade > (SELECT AVG(avg_grade) FROM students);\n```\n\nВнутренний запрос в скобках выполняется первым и возвращает одно число — средний балл, с которым затем сравнивается каждая строка.\n\n## Скалярные и многострочные подзапросы\n\nЕсли подзапрос возвращает **одно** значение (как выше), его сравнивают через `=`, `>`, `<`. Если он возвращает **список** значений — используют `IN (...)`, `EXISTS (...)`, `ANY`/`ALL`. Например, `WHERE group_id IN (SELECT id FROM groups WHERE year = 1)` отберёт студентов всех групп первого курса. Часто такой подзапрос можно переписать через JOIN — выбирайте тот вариант, что читается понятнее.\n\n## Коротко\n\nПодзапрос — вложенный SELECT; скалярный сравнивают через `=/>/<`, многострочный — через IN/EXISTS/ANY.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — подзапросы](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: подзапросные выражения](https://postgrespro.ru/docs/postgresql/current/functions-subquery)\n- [PostgreSQL Exercises — подзапросы](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
5d1a6e20-fd15-4a96-8790-2bd1e75d75f3	b951683f-55d5-4b76-8e75-152bcbd2419a	Аномалии вставки, обновления и удаления	Нормализация — это процесс проектирования таблиц, при котором устраняют **избыточность** данных и связанные с ней ошибки. Чтобы понять, зачем она нужна, посмотрим, что бывает без неё.\n\n## Избыточность\n\nЕсли хранить всё в одной «плоской» таблице, одни и те же данные повторяются во многих строках. Например, в таблице со столбцами *студент, группа, куратор группы* имя куратора дублируется у каждого студента группы.\n\n## Три вида аномалий\n\n- **Аномалия вставки**: нельзя добавить новую группу без студента — некуда записать куратора.\n- **Аномалия обновления**: при смене куратора группы придётся менять его во всех строках студентов этой группы; забудешь одну — данные противоречивы.\n- **Аномалия удаления**: удалив последнего студента группы, потеряешь сведения и о самой группе.\n\n## Пример\n\n```\nстудент   | группа | куратор\nИванов    | П-101  | Петрова\nСидоров   | П-101  | Петрова   -- куратор дублируется\n```\n\nРешение — разнести данные по разным таблицам (студенты и группы) и связать их ключом. К этому и ведёт нормализация.\n\n## Коротко\n\nИзбыточность порождает аномалии вставки, обновления и удаления; нормализация устраняет их, разнося данные по связанным таблицам.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
f0098687-3382-4359-9591-afe24241dbfa	f387a0d1-8bc0-4865-b0db-cc0e316c5d2c	Аномалии параллельного доступа	Когда транзакции работают параллельно, без должной изоляции возникают **аномалии** — некорректные результаты чтения. Уровни изоляции различаются именно тем, какие аномалии они допускают.\n\n## Основные аномалии\n\n- **Грязное чтение (dirty read)** — транзакция видит чужие ещё не зафиксированные изменения, которые могут откатиться.\n- **Неповторяющееся чтение (non-repeatable read)** — повторный SELECT той же строки в одной транзакции даёт другое значение.\n- **Фантомное чтение (phantom read)** — повторный запрос по условию возвращает новые строки, добавленные другой транзакцией.\n- **Потерянное обновление (lost update)** — два параллельных обновления одной строки, и одно «затирает» другое.\n\n## Пример\n\nДве транзакции одновременно читают баланс 100, обе прибавляют 10 и пишут 110 — итог 110 вместо 120. Это потерянное обновление.\n\n## Коротко\n\nБез изоляции возможны грязное, неповторяющееся и фантомное чтения, а также потерянное обновление.\n\n## Литература\n\n- [Документация: изоляция транзакций](https://postgrespro.ru/docs/postgresql/current/transaction-iso)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
7f9e2412-4a74-41d1-8d1e-f3027de00a03	0d61ac1b-37ee-4150-bf3d-f862cd47d50e	Оптимистичные блокировки	Альтернатива — **оптимистичная** блокировка: мы предполагаем, что конфликты редки, не блокируем строку, а проверяем при записи, не изменил ли её кто-то другой.\n\n## Как это работает\n\nВ таблицу добавляют столбец-версию (`version` или метку времени). При обновлении проверяют, что версия не изменилась с момента чтения:\n\n```\n-- прочитали строку с version = 7, затем:\nUPDATE courses\nSET seats = seats - 1, version = version + 1\nWHERE id = 5 AND version = 7;\n```\n\nЕсли строку уже кто-то обновил (version стал 8), запрос изменит **0 строк** — значит, был конфликт, и операцию нужно повторить, перечитав данные.\n\n## Когда что выбирать\n\n- **Оптимистичная** — когда конфликты редки (больше параллельности, не держим блокировки).\n- **Пессимистичная (FOR UPDATE)** — когда конфликты вероятны и важно не допустить даже одной повторной попытки.\n\n## Коротко\n\nОптимистичная блокировка не держит строку, а проверяет version при записи; конфликт виден по «0 изменённых строк» и решается повтором.\n\n## Литература\n\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n- [Документация: изоляция транзакций](https://postgrespro.ru/docs/postgresql/current/transaction-iso)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
e9367415-e853-436d-be15-3068f343afdc	a91b48e1-85e5-49d2-968a-0ae47a581a36	Блокировки строк и таблиц	Несмотря на MVCC, блокировки всё же нужны — когда несколько транзакций хотят **изменять** одни и те же данные.\n\n## Зачем блокировки\n\nБлокировка не даёт двум транзакциям одновременно поменять одну строку и тем самым предотвращает потерянное обновление и нарушение целостности.\n\n## Уровни блокировок\n\n- **Блокировки строк** — самые частые; PostgreSQL автоматически блокирует строку, которую транзакция изменяет (UPDATE/DELETE), пока та не завершится.\n- **Блокировки таблиц** — более грубые; нужны для DDL (например, изменения структуры таблицы). Их можно запросить явно через `LOCK TABLE`, но без необходимости этого избегают.\n\n## Важно\n\nЧем грубее и дольше блокировка, тем меньше параллельность. Хорошая практика — держать транзакции короткими, чтобы блокировки снимались быстрее.\n\n## Коротко\n\nБлокировки нужны при конкурентном изменении данных; строковые ставятся автоматически при UPDATE/DELETE, табличные — грубые и применяются редко.\n\n## Литература\n\n- [Документация: явные блокировки](https://postgrespro.ru/docs/postgresql/current/explicit-locking)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
f36928df-0bd6-41d1-bc55-6b17f50c02ae	cc106b14-5e26-4e65-8c79-6e40ee1bb56e	Условия и оператор LIKE	Кроме точных сравнений, часто нужен поиск по шаблону текста — например, «фамилии на С» или «почты на @edu.ru». Для этого служит оператор **LIKE**.\n\n## Шаблоны\n\nВ шаблоне два специальных символа: `%` — любое число любых символов (в том числе ноль), `_` — ровно один любой символ. Для поиска без учёта регистра в PostgreSQL есть `ILIKE` (это расширение PostgreSQL, в стандарте SQL его нет).\n\n## Пример\n\nСтуденты, чьё имя начинается на «Ив», и группы, заканчивающиеся на «01»:\n\n```\nSELECT full_name, group_name\nFROM students\nWHERE full_name LIKE 'Ив%' AND group_name LIKE '%01';\n```\n\n- `'Ив%'` — начинается на «Ив»;\n- `'%сон'` — заканчивается на «сон»;\n- `'%баз%'` — содержит «баз» где угодно;\n- `'_ва'` — три символа, заканчивается на «ва».\n\n## Полезно знать\n\nПоиск по `'%текст%'` не может опираться на обычный индекс и на больших таблицах работает медленно. Для полнотекстового и более «умного» поиска в PostgreSQL есть отдельные средства (tsvector, триграммы), но это уже продвинутая тема.\n\n## Коротко\n\nLIKE ищет по шаблону: `%` — любые символы, `_` — один символ; ILIKE игнорирует регистр.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — поиск по шаблону](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: сопоставление с шаблоном (LIKE)](https://postgrespro.ru/docs/postgresql/current/functions-matching)\n- [PostgreSQL Exercises — фильтрация строк](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	2	40	10
4458ddc8-4ef9-4805-a633-958e704b916d	d3ec801e-8b74-43f2-bf41-8dfcb9b85b86	Составные и частичные индексы	Индекс можно строить по нескольким столбцам сразу или только по части строк таблицы.\n\n## Составной (многоколоночный) индекс\n\nИндекс по нескольким столбцам полезен для запросов, фильтрующих сразу по ним:\n\n```\nCREATE INDEX idx_students_group_grade ON students (group_id, avg_grade);\n```\n\nВажен **порядок столбцов**: такой индекс помогает запросам по `group_id` и по `group_id` + `avg_grade`, но почти бесполезен для запроса только по `avg_grade`. Правило: сначала столбцы для равенства, потом для диапазона.\n\n## Частичный индекс\n\nИндекс только по строкам, удовлетворяющим условию — компактнее и быстрее:\n\n```\nCREATE INDEX idx_active_students ON students (group_id) WHERE is_active;\n```\n\nПолезен, когда запросы почти всегда обращаются к подмножеству (например, только к активным записям).\n\n## Коротко\n\nСоставной индекс ускоряет фильтрацию по нескольким столбцам (важен порядок); частичный индексирует лишь нужное подмножество строк, экономя место.\n\n## Литература\n\n- [Документация: многоколоночные индексы](https://postgrespro.ru/docs/postgresql/current/indexes-multicolumn)\n- [Документация: частичные индексы](https://postgrespro.ru/docs/postgresql/current/indexes-partial)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	2	40	10
4dc39f00-ef2c-4ccb-a5ba-e1299250e494	d3ec801e-8b74-43f2-bf41-8dfcb9b85b86	B-tree — основной индекс	По умолчанию `CREATE INDEX` создаёт индекс типа **B-tree** (сбалансированное дерево) — самый универсальный и используемый тип.\n\n## Что умеет B-tree\n\nB-tree хранит значения в отсортированном виде, поэтому эффективно поддерживает:\n- поиск по равенству (`=`);\n- диапазоны (`<`, `>`, `BETWEEN`);\n- сортировку (ORDER BY по индексированному столбцу);\n- поиск по префиксу строки (`LIKE 'абв%'`).\n\n## Пример\n\n```\nCREATE INDEX idx_students_grade ON students (avg_grade);\n-- ускорит и WHERE avg_grade > 4, и ORDER BY avg_grade\n```\n\n## Когда B-tree не подходит\n\nB-tree бесполезен для поиска «содержит подстроку» (`LIKE '%абв%'`), для полнотекстового поиска и для данных вроде JSON/массивов — там нужны другие типы индексов (следующий урок).\n\n## Коротко\n\nB-tree — универсальный индекс по умолчанию; хорош для равенства, диапазонов и сортировки, но не для поиска подстроки в середине и полнотекста.\n\n## Литература\n\n- [Документация: типы индексов](https://postgrespro.ru/docs/postgresql/current/indexes-types)\n- [Markus Winand. Use The Index, Luke!](https://use-the-index-luke.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
112dadaa-f5a0-4827-a5b0-74403dc9974b	ca457d41-474f-425b-b52c-1d74751f00d0	Подключение и первые команды	Попрактикуемся в базовых действиях: создать базу и таблицу, наполнить и прочитать данные — весь цикл в psql.\n\n## Создание базы и таблицы\n\n```\nCREATE DATABASE school;\n\\c school\nCREATE TABLE students (\n  id serial PRIMARY KEY,\n  full_name text NOT NULL\n);\n```\n\n## Наполнение и чтение\n\n```\nINSERT INTO students (full_name) VALUES ('Иванов'), ('Петров');\nSELECT * FROM students;\n```\n\n## Полезные служебные команды\n\n- `\\dt` — какие есть таблицы;\n- `\\d students` — столбцы и ограничения;\n- `\\x` — расширенный вывод (удобно для «широких» строк);\n- `\\timing` — показывать время выполнения.\n\n## Коротко\n\nБазовый цикл: CREATE DATABASE → CREATE TABLE → INSERT → SELECT; ориентироваться в базе помогают \\dt и \\d.\n\n## Литература\n\n- [Документация: psql](https://postgrespro.ru/docs/postgresql/current/app-psql)\n- [Postgres: первое знакомство](https://postgrespro.ru/education/books/introbook)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
077f0df8-d46e-4041-be74-2873406970e9	de23741e-cedb-4a46-b0fc-f89d498082e8	Импорт и экспорт: COPY	Когда данных много, вставлять их по одной строке через INSERT медленно. Для массовой загрузки и выгрузки есть команда **COPY**.\n\n## COPY\n\n`COPY` переносит данные между таблицей и файлом (обычно CSV) на стороне сервера — это самый быстрый способ массовой загрузки:\n\n```\nCOPY students (full_name, group_name)\nFROM '/data/students.csv' WITH (FORMAT csv, HEADER true);\n\nCOPY students TO '/data/dump.csv' WITH (FORMAT csv, HEADER true);\n```\n\n## \\copy в psql\n\nСерверный COPY требует доступа к файлам сервера. В psql есть клиентская версия `\\copy` — она читает/пишет файл на стороне клиента, что удобнее и безопаснее:\n\n```\n\\copy students FROM 'students.csv' WITH (FORMAT csv, HEADER true)\n```\n\n## Коротко\n\nCOPY — быстрый массовый импорт/экспорт между таблицей и CSV; \\copy в psql работает с файлами на стороне клиента.\n\n## Литература\n\n- [Документация: команда COPY](https://postgrespro.ru/docs/postgresql/current/sql-copy)\n- [Документация: наполнение базы данными](https://postgrespro.ru/docs/postgresql/current/populate)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
c7c614c9-2bd4-42f1-bf16-5d5b24872c00	cc106b14-5e26-4e65-8c79-6e40ee1bb56e	Группировка: GROUP BY и HAVING	Агрегаты становятся по-настоящему полезными вместе с группировкой. **GROUP BY** разбивает строки на группы по значению столбца, и тогда агрегат считается отдельно для каждой группы — например, средний балл по каждой учебной группе.\n\n## Правило столбцов\n\nЕсли в SELECT есть и обычные столбцы, и агрегаты, то все «необычные» столбцы обязаны присутствовать в GROUP BY. Иначе СУБД не знает, какое из значений столбца показать для группы, и вернёт ошибку.\n\n## WHERE или HAVING\n\nЭто ключевое различие урока. **WHERE** фильтрует строки **до** группировки, **HAVING** — готовые группы **после** агрегирования. Условие на агрегат (например, «средний балл группы ≥ 4») можно написать только в HAVING.\n\n## Пример\n\nСредний балл по каждой группе, где он не ниже 4:\n\n```\nSELECT group_name, ROUND(AVG(avg_grade), 2) AS avg_grade\nFROM students\nWHERE avg_grade IS NOT NULL\nGROUP BY group_name\nHAVING AVG(avg_grade) >= 4\nORDER BY avg_grade DESC;\n```\n\nЛогический порядок: WHERE отбирает строки → GROUP BY группирует → HAVING отбирает группы → ORDER BY сортирует.\n\n## Коротко\n\nGROUP BY группирует строки для агрегатов; «обычные» столбцы из SELECT должны быть в GROUP BY; HAVING фильтрует уже посчитанные группы (в отличие от WHERE).\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — группировка](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: GROUP BY и HAVING](https://postgrespro.ru/docs/postgresql/current/queries-table-expressions)\n- [PostgreSQL Exercises — группировка](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
082331df-9b45-4e81-a326-9805f3fe3902	de23741e-cedb-4a46-b0fc-f89d498082e8	INSERT, UPDATE, DELETE на практике	Практический разбор изменения данных с приёмами, которые часто нужны в реальной работе.\n\n## Множественная вставка\n\n```\nINSERT INTO students (full_name, group_name)\nVALUES ('Иванов', 'П-101'),\n       ('Петров', 'П-102');\n```\n\n## RETURNING\n\nПолезная возможность PostgreSQL — вернуть данные изменённых строк (например, сгенерированный id):\n\n```\nINSERT INTO students (full_name) VALUES ('Сидоров') RETURNING id;\n```\n\n## UPSERT (ON CONFLICT)\n\n«Вставить или обновить, если уже есть» — частый сценарий:\n\n```\nINSERT INTO settings (key, value) VALUES ('theme', 'dark')\nON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;\n```\n\n## Коротко\n\nPostgreSQL умеет множественный INSERT, RETURNING (вернуть изменённые строки) и UPSERT через ON CONFLICT — это упрощает типовые операции.\n\n## Литература\n\n- [Документация: изменение данных (DML)](https://postgrespro.ru/docs/postgresql/current/dml)\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
729750c4-de0f-4e63-acf0-9726989134c3	8da79b56-5f63-4c57-8cc6-80999f553fb5	Сущности, атрибуты и связи	Проектирование базы данных начинается не с таблиц, а с анализа предметной области. Сначала строят **инфологическую модель** — описывают, какие объекты есть в задаче и как они связаны, на языке, понятном и заказчику. Три базовых понятия: **сущность**, **атрибут** и **связь**.\n\n## Сущности и атрибуты\n\n**Сущность** — это класс объектов, о которых мы храним данные (Студент, Группа, Курс). Конкретный объект — **экземпляр** сущности. **Атрибут** — свойство сущности (у Студента: ФИО, дата рождения, номер зачётки).\n\nСреди атрибутов выделяют **ключевой** — он однозначно отличает один экземпляр от другого (номер зачётки уникален у каждого студента).\n\n## Связи\n\n**Связь** показывает, как сущности относятся друг к другу: Студент *учится в* Группе, Преподаватель *ведёт* Курс. У связи есть **степень** (сколько экземпляров одной сущности соответствует другой) — её подробно разберём в уроке про виды связей.\n\n## Пример\n\nДля учебного портала выделим:\n- **Студент**: ФИО, зачётка, дата рождения;\n- **Группа**: название, курс обучения;\n- связь: студент *входит в* группу.\n\n## Коротко\n\nСущность — класс объектов, атрибут — его свойство, ключевой атрибут различает экземпляры, связь описывает отношение между сущностями.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
9cc46e04-4a89-44e1-8db3-6052d926f644	8da79b56-5f63-4c57-8cc6-80999f553fb5	ER-диаграммы и нотации (Чен, Crow's Foot)	ER-модель (Entity-Relationship, «сущность-связь») — графическое представление инфологической модели. Она наглядно показывает сущности, их атрибуты и связи. Существует несколько нотаций; разберём две самые распространённые.\n\n## Нотация Чена\n\nКлассическая нотация Питера Чена (1976): сущность — прямоугольник, атрибут — овал, связь — ромб, всё соединено линиями. Нотация нагляднa для обучения, но громоздкa для больших схем.\n\n## Crow's Foot («вороньи лапки»)\n\nСамая популярная на практике. Сущность — прямоугольник со списком атрибутов внутри; связь — линия между сущностями. Кратность показывают значками на концах линии: «вороньей лапкой» (много), чёрточкой (один), кружком (ноль, необязательно). Её поддерживает большинство инструментов проектирования.\n\n## Что показывают на диаграмме\n\n- сущности и их атрибуты;\n- первичные ключи (обычно помечены PK);\n- связи и их кратность (1:1, 1:М, М:М);\n- обязательность участия в связи.\n\n## Пример\n\nСвязь «Группа — Студенты» в Crow's Foot: со стороны Группы — «один», со стороны Студентов — «много» (вороньи лапки): в одной группе много студентов.\n\n## Коротко\n\nER-диаграмма визуализирует сущности, атрибуты и связи; нотация Чена нагляднее для учёбы, Crow's Foot — практичнее и поддерживается инструментами.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих» (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	1	30	10
6cabc30f-64b0-42d9-b09c-793df65ee478	78cd78a6-0f85-4727-ad68-9c0c48a96006	Функции для строк и дат	PostgreSQL богат встроенными функциями. Разберём самые ходовые — для работы со строками и датами.\n\n## Строковые функции\n\n- `length(s)` — длина;\n- `lower(s)`, `upper(s)` — регистр;\n- `trim(s)` — убрать пробелы по краям;\n- `s1 || s2` — конкатенация;\n- `substring(s FROM 1 FOR 3)` — подстрока;\n- `split_part(s, ',', 1)` — часть по разделителю.\n\n## Функции даты и времени\n\n- `now()` / `current_date` — текущие момент и дата;\n- `age(d)` — разница во времени;\n- `date_trunc('month', ts)` — округление до месяца;\n- `extract(year FROM d)` — выделить часть;\n- интервалы: `now() - interval '7 days'`.\n\n## Пример\n\n```\nSELECT upper(full_name), extract(year FROM enrolled_at) AS year\nFROM students;\n```\n\n## Коротко\n\nСтроки обрабатывают length/lower/trim/||/substring, даты — now/age/date_trunc/extract и интервалы; это покрывает большинство задач.\n\n## Литература\n\n- [Документация: строковые функции](https://postgrespro.ru/docs/postgresql/current/functions-string)\n- [Документация: функции даты и времени](https://postgrespro.ru/docs/postgresql/current/functions-datetime)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
31e9b78d-8b76-4fb4-9556-d18193ee7b3b	6e25b2e3-aaee-4e08-aed9-3bcc74cf67f6	Изменение данных: INSERT, UPDATE, DELETE	До сих пор мы только читали данные. Менять их позволяют три команды языка изменения данных (DML): **INSERT** (добавить), **UPDATE** (изменить), **DELETE** (удалить).\n\n## Три команды\n\n- `INSERT` добавляет новые строки;\n- `UPDATE` меняет значения в существующих строках;\n- `DELETE` удаляет строки.\n\n## Пример\n\n```\nINSERT INTO students (full_name, group_name, avg_grade)\nVALUES ('Иванов Пётр', 'П-101', 4.5);\n\nUPDATE students SET avg_grade = 5.0\nWHERE full_name = 'Иванов Пётр';\n\nDELETE FROM students\nWHERE avg_grade IS NULL;\n```\n\n## WHERE решает всё\n\nУ UPDATE и DELETE почти всегда должен быть **WHERE**. Без него `UPDATE students SET avg_grade = 5` поставит пятёрку **всем**, а `DELETE FROM students` удалит **всю** таблицу. Хорошая привычка: сначала выполнить `SELECT` с тем же условием и убедиться, что под него попадают именно нужные строки, и только потом менять SELECT на UPDATE/DELETE.\n\n## Откат изменений\n\nЕсли работать внутри транзакции (`BEGIN ... ROLLBACK`), ошибочное изменение можно отменить, пока оно не зафиксировано через `COMMIT`. Подробно транзакции разбираются в отдельном курсе.\n\n## Коротко\n\nINSERT добавляет, UPDATE меняет, DELETE удаляет строки; у UPDATE/DELETE почти всегда нужен WHERE, иначе изменятся все строки.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — изменение данных](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: изменение данных (DML)](https://postgrespro.ru/docs/postgresql/current/dml)\n- [PostgreSQL Exercises — изменение данных](https://pgexercises.com/)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
12f8a209-f08e-4629-91d2-cdaa4af53c53	aabba830-2e2f-4803-81db-816ed5e40415	Проектирование схемы: разбор кейса	Соберём всё вместе на сквозном примере — спроектируем схему небольшого учебного портала, где студенты записываются на курсы и получают оценки.\n\n## Шаг 1. Сущности\n\nВыделяем: **Группа**, **Студент**, **Курс**, **Запись на курс** (с оценкой). Для каждой определяем атрибуты и ключ.\n\n## Шаг 2. Связи\n\n- Группа — Студент: 1:М;\n- Студент — Курс: М:М (через «Запись»);\n- запись хранит оценку студента по курсу.\n\n## Шаг 3. Ключи и ограничения\n\nБерём суррогатные первичные ключи, внешние ключи для связей, `CHECK` на диапазон оценки.\n\n## Итоговая схема\n\n```\nCREATE TABLE groups (\n  id serial PRIMARY KEY,\n  title text NOT NULL\n);\nCREATE TABLE students (\n  id serial PRIMARY KEY,\n  full_name text NOT NULL,\n  group_id int REFERENCES groups(id) ON DELETE SET NULL\n);\nCREATE TABLE courses (\n  id serial PRIMARY KEY,\n  title text NOT NULL\n);\nCREATE TABLE enrollments (\n  student_id int REFERENCES students(id) ON DELETE CASCADE,\n  course_id  int REFERENCES courses(id) ON DELETE CASCADE,\n  grade numeric CHECK (grade BETWEEN 2 AND 5),\n  PRIMARY KEY (student_id, course_id)\n);\n```\n\nТакую схему уже можно наполнять данными. Дальше её проверяют на аномалии (курс «Нормализация») и ускоряют запросы (курс «Индексы»).\n\n## Коротко\n\nПроектирование идёт по шагам: сущности → связи → ключи и ограничения → SQL-схема; составной ключ связующей таблицы защищает от дублей.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n- [Документация: создание таблиц (DDL)](https://postgrespro.ru/docs/postgresql/current/ddl)\n- [PostgreSQL Exercises](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
600decf7-2d3a-4f65-9342-a7b4b4a02675	78cd78a6-0f85-4727-ad68-9c0c48a96006	CASE, COALESCE и условные выражения	Часто прямо в запросе нужно ветвление или обработка пустых значений — для этого есть условные выражения.\n\n## CASE\n\n`CASE` — аналог if/else внутри SQL:\n\n```\nSELECT full_name,\n  CASE\n    WHEN avg_grade >= 4.5 THEN 'отлично'\n    WHEN avg_grade >= 3.5 THEN 'хорошо'\n    ELSE 'удовлетворительно'\n  END AS level\nFROM students;\n```\n\n## Работа с NULL\n\n- `COALESCE(a, b, ...)` — вернуть первое не-NULL значение (удобно для значений по умолчанию);\n- `NULLIF(a, b)` — вернуть NULL, если a = b;\n- `GREATEST`/`LEAST` — максимум/минимум из списка.\n\n```\nSELECT COALESCE(avg_grade, 0) AS grade FROM students;  -- NULL → 0\n```\n\n## Коротко\n\nCASE даёт ветвление в запросе, COALESCE подставляет значение вместо NULL, NULLIF превращает значение в NULL по условию.\n\n## Литература\n\n- [Документация: условные выражения](https://postgrespro.ru/docs/postgresql/current/functions-conditional)\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
e9228693-dede-4cd6-b401-1a23aacef807	aabba830-2e2f-4803-81db-816ed5e40415	Ограничения целостности (CHECK, FK, UNIQUE)	Ограничения (constraints) — правила, которые СУБД проверяет автоматически при каждом изменении данных. Они переносят часть бизнес-логики в саму базу и не дают занести некорректные данные.\n\n## Виды ограничений\n\n- **NOT NULL** — значение обязательно;\n- **UNIQUE** — значения не повторяются (например, email);\n- **PRIMARY KEY** — уникальность + NOT NULL, идентификатор строки;\n- **FOREIGN KEY** — ссылка на существующую строку другой таблицы;\n- **CHECK** — произвольное условие на значение.\n\n## Пример\n\n```\nCREATE TABLE students (\n  id        serial PRIMARY KEY,\n  email     text UNIQUE,\n  full_name text NOT NULL,\n  avg_grade numeric CHECK (avg_grade BETWEEN 2 AND 5),\n  group_id  int REFERENCES groups(id) ON DELETE SET NULL\n);\n```\n\n## Поведение при удалении\n\nУ внешнего ключа задают реакцию на удаление «родителя»: `ON DELETE CASCADE` удалит связанные строки, `SET NULL` обнулит ссылку, `RESTRICT` (по умолчанию) запретит удаление, пока есть ссылки. Это важная часть проектирования целостности.\n\n## Коротко\n\nОграничения (NOT NULL, UNIQUE, CHECK, PK, FK) проверяются базой автоматически; у FK поведение при удалении задаётся через ON DELETE.\n\n## Литература\n\n- [Документация: ограничения целостности](https://postgrespro.ru/docs/postgresql/current/ddl-constraints)\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n- [PostgreSQL Exercises](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
5b71f05a-3af0-4c16-8974-2aa0e78eb75e	a967fcbe-701f-4fc0-92f1-1b649a31f713	Первичные и внешние ключи	Ключи — основа целостности реляционной модели. Они связывают таблицы и гарантируют, что каждую строку можно однозначно найти.\n\n## Первичный ключ (PRIMARY KEY)\n\nСтолбец (или набор столбцов), однозначно определяющий строку. Он обязателен, уникален и не может быть NULL. У каждой таблицы должен быть ровно один первичный ключ (он может быть составным).\n\n## Внешний ключ (FOREIGN KEY)\n\nСтолбец, который ссылается на первичный ключ другой (или той же) таблицы. Реализует связь 1:М и обеспечивает **ссылочную целостность**: нельзя записать студента в несуществующую группу.\n\n```\nCREATE TABLE groups (\n  id    serial PRIMARY KEY,\n  title text NOT NULL\n);\nCREATE TABLE students (\n  id        serial PRIMARY KEY,\n  full_name text NOT NULL,\n  group_id  int REFERENCES groups(id)\n);\n```\n\n## Естественные и суррогатные ключи\n\n**Естественный** ключ — осмысленный атрибут (номер зачётки). **Суррогатный** — искусственный идентификатор (`serial`, UUID) без смысла. На практике чаще берут суррогатные: они компактны, стабильны и не меняются, даже если меняются данные.\n\n## Коротко\n\nPRIMARY KEY однозначно определяет строку; FOREIGN KEY ссылается на PK другой таблицы и обеспечивает ссылочную целостность; суррогатные ключи обычно удобнее естественных.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: внешние ключи](https://postgrespro.ru/docs/postgresql/current/tutorial-fk)\n- [Документация: ограничения](https://postgrespro.ru/docs/postgresql/current/ddl-constraints)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
8c275646-25f1-4e32-b229-c74e3fd3b193	0bb51c3a-f221-44a4-911f-d07bb32e53a7	Третья форма (3НФ) и НФБК	**Третья нормальная форма (3НФ)** убирает **транзитивные** зависимости, а **НФБК** (нормальная форма Бойса–Кодда) усиливает требование.\n\n## Третья нормальная форма\n\nТаблица в 3НФ, если:\n- она в 2НФ;\n- нет транзитивных зависимостей: неключевой атрибут не зависит от другого неключевого.\n\n## Пример\n\n```\n-- студент → группа → куратор:\n-- куратор зависит от группы (неключевой), а не от студента\nстудент | группа | куратор\n```\n\nЭто транзитивная зависимость. Исправление — вынести группы:\n\n```\nstudents(студент, группа)\ngroups(группа, куратор)\n```\n\n## НФБК (нормальная форма Бойса–Кодда)\n\nУсиленная 3НФ: **любой** детерминант (левая часть ФЗ) должен быть ключом-кандидатом. На практике большинство таблиц после приведения к 3НФ удовлетворяют и НФБК; различия проявляются в редких случаях с несколькими перекрывающимися ключами.\n\n## Коротко\n\n3НФ убирает транзитивные зависимости (неключевой не зависит от неключевого); НФБК — усиленная версия, где любой детерминант является ключом.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих» (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	2	40	10
94a373ed-f6ac-4ada-af0b-6d64d94c7c19	720171ae-9ba0-4777-a9e1-8d53f6881e54	Представления (VIEW)	Если один и тот же сложный запрос нужен часто, его удобно сохранить под именем — это **представление (VIEW)**.\n\n## Что такое VIEW\n\nПредставление — сохранённый именованный запрос. Обращаются к нему как к таблице, но данные оно не хранит — вычисляет «на лету» при каждом обращении.\n\n```\nCREATE VIEW group_stats AS\nSELECT group_name, COUNT(*) AS students, ROUND(AVG(avg_grade), 2) AS avg\nFROM students\nGROUP BY group_name;\n\nSELECT * FROM group_stats WHERE avg > 4;\n```\n\n## Зачем нужны\n\n- скрыть сложность запроса за простым именем;\n- переиспользовать логику;\n- разграничить доступ (дать права на VIEW, а не на таблицу).\n\n## Материализованные представления\n\n`MATERIALIZED VIEW` физически хранит результат и обновляется командой `REFRESH` — полезно для тяжёлых отчётов, которые не нужны в реальном времени.\n\n## Коротко\n\nVIEW — сохранённый запрос, к которому обращаются как к таблице (данные не хранятся); MATERIALIZED VIEW хранит результат и обновляется по REFRESH.\n\n## Литература\n\n- [Документация: представления (учебник)](https://postgrespro.ru/docs/postgresql/current/tutorial-views)\n- [Документация: CREATE VIEW](https://postgrespro.ru/docs/postgresql/current/sql-createview)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	0	20	10
fdf77ac5-0d32-4f2d-b75d-c255d4dcf6a5	720171ae-9ba0-4777-a9e1-8d53f6881e54	Общие табличные выражения (CTE)	**CTE** (Common Table Expression), или конструкция `WITH`, позволяет вынести подзапрос в начало и дать ему имя — запрос становится читаемее.\n\n## Синтаксис WITH\n\n```\nWITH active AS (\n  SELECT * FROM students WHERE is_active\n)\nSELECT group_name, COUNT(*)\nFROM active\nGROUP BY group_name;\n```\n\nCTE `active` работает как временная именованная таблица в пределах запроса. Несколько CTE перечисляют через запятую.\n\n## Рекурсивные CTE\n\n`WITH RECURSIVE` умеет обходить иерархии (дерево разделов, граф) — например, развернуть все подкатегории из дерева. Это мощный инструмент для древовидных данных.\n\n## CTE и читаемость\n\nCTE особенно полезны, когда запрос состоит из нескольких логических шагов: каждый шаг выносят в отдельный WITH и собирают финальный результат — вместо громоздкой вложенности подзапросов.\n\n## Коротко\n\nCTE (WITH) даёт имя подзапросу и улучшает читаемость; WITH RECURSIVE обходит иерархические данные.\n\n## Литература\n\n- [Документация: запросы WITH (CTE)](https://postgrespro.ru/docs/postgresql/current/queries-with)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
504c6e26-6106-4db5-8ab2-80a42c7a5159	a967fcbe-701f-4fc0-92f1-1b649a31f713	Виды связей: 1:1, 1:М, М:М	Связи различают по **кратности** — сколько экземпляров одной сущности соответствует экземплярам другой. Это ключевое решение: от него зависит структура будущих таблиц.\n\n## Один-к-одному (1:1)\n\nОдному экземпляру соответствует не более одного экземпляра другой сущности. Встречается редко — обычно это признак того, что данные можно объединить в одну таблицу или вынести часть атрибутов (Студент — Зачётная книжка).\n\n## Один-ко-многим (1:М)\n\nСамая частая связь. Одному экземпляру соответствует много экземпляров другой сущности, но не наоборот: одна Группа — много Студентов, но студент учится в одной группе. Реализуется внешним ключом в таблице на стороне «много».\n\n## Многие-ко-многим (М:М)\n\nМногим соответствует много: Студент записан на много Курсов, на Курс записано много Студентов. Напрямую в реляционной БД такую связь хранить нельзя — её разбивают на две связи 1:М через **связующую (ассоциативную) таблицу** (например, «Записи на курс» с парой студент+курс).\n\n## Пример\n\n- Группа → Студенты: 1:М;\n- Студенты ↔ Курсы: М:М через таблицу записей.\n\n## Коротко\n\n1:1 — редко (часто сливают в одну таблицу), 1:М — внешним ключом на стороне «много», М:М — только через связующую таблицу.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n- [Документация: учебник по внешним ключам](https://postgrespro.ru/docs/postgresql/current/tutorial-fk)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	ec8b8164-455f-4903-87be-0522e01d7663	Нормализация на реальном примере	Пройдём весь путь от «плоской» таблицы до 3НФ на сквозном примере — учёте оценок студентов.\n\n## Исходная таблица\n\n```\nстудент | группа | куратор | курс | оценка\n```\n\nЗдесь есть и список (много курсов у студента), и дублирование куратора, и транзитивная зависимость.\n\n## Шаг к 1НФ\n\nДелаем значения атомарными: одна строка на пару студент+курс (убираем списки).\n\n## Шаг к 2НФ\n\nВыносим то, что зависит от части ключа: характеристики курса — в таблицу `courses`.\n\n## Шаг к 3НФ\n\nУбираем транзитивную зависимость «студент → группа → куратор»: группы — в отдельную таблицу.\n\n## Итоговая схема\n\n```\ngroups(id, название, куратор)\nstudents(id, ФИО, group_id → groups)\ncourses(id, название)\nenrollments(student_id → students, course_id → courses, оценка)\n```\n\nТеперь каждое сведение хранится один раз, аномалии исчезли, а связи поддержаны внешними ключами.\n\n## Коротко\n\nНормализацию ведут пошагово (1НФ → 2НФ → 3НФ), на каждом шаге вынося в отдельные таблицы то, что нарушает текущую форму.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
7c482ced-9808-4c6e-b0f0-914380542c54	5ddec0ed-61e9-43a4-b0d5-4e605c6e35fa	Объединение таблиц: JOIN	Данные обычно разнесены по нескольким таблицам, чтобы не дублировать информацию (это и есть нормализация). Чтобы собрать их в одном запросе, используют соединение — **JOIN**.\n\n## Внутреннее соединение\n\n`INNER JOIN` (или просто JOIN) оставляет только те пары строк, для которых нашлось совпадение по условию соединения (`ON`). Обычно соединяют внешний ключ одной таблицы с первичным ключом другой.\n\n## Пример\n\nПокажем студентов вместе с названием их группы из таблицы `groups`:\n\n```\nSELECT s.full_name, g.title AS group_title\nFROM students AS s\nJOIN groups AS g ON g.id = s.group_id;\n```\n\nПсевдонимы таблиц (`s`, `g`) делают запрос короче и убирают двусмысленность, если в обеих таблицах есть столбцы с одинаковым именем.\n\n## ON или WHERE\n\n`ON` описывает **как связаны** таблицы (условие соединения), а `WHERE` — **какие строки оставить** в результате. Их легко перепутать: связь всегда пишут в ON, а дополнительный отбор — в WHERE. Соединять можно сколько угодно таблиц, добавляя новые JOIN.\n\n## Коротко\n\nJOIN объединяет таблицы по условию ON; INNER JOIN оставляет только совпавшие строки; условие связи — в ON, дополнительный отбор — в WHERE.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — соединения](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: учебник по соединениям таблиц](https://postgrespro.ru/docs/postgresql/current/tutorial-join)\n- [PostgreSQL Exercises — JOIN](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
4aff43ad-be28-4469-8215-ccbd3c0b1a45	0bb51c3a-f221-44a4-911f-d07bb32e53a7	Первая нормальная форма (1НФ)	**Первая нормальная форма (1НФ)** — базовое требование к таблице в реляционной модели.\n\n## Требование 1НФ\n\nТаблица в 1НФ, если:\n- все значения **атомарны** (в одной ячейке одно значение, а не список);\n- нет **повторяющихся групп** (нельзя столбцы телефон1, телефон2, телефон3);\n- у каждой строки есть ключ.\n\n## Нарушение и исправление\n\n```\n-- НЕ в 1НФ: в одной ячейке список курсов\nстудент | курсы\nИванов  | SQL, Индексы, ER\n\n-- в 1НФ: одна строка на пару студент+курс\nстудент | курс\nИванов  | SQL\nИванов  | Индексы\nИванов  | ER\n```\n\nСписки и «многозначные» поля выносят в отдельную таблицу со связью. Именно так связь «многие-ко-многим» получает связующую таблицу.\n\n## Коротко\n\n1НФ требует атомарных значений и отсутствия повторяющихся групп; списки выносят в отдельные строки/таблицу.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
a4d4ab36-87cc-4727-a1f1-07e5a216adbb	f387a0d1-8bc0-4865-b0db-cc0e316c5d2c	MVCC в PostgreSQL	PostgreSQL обеспечивает изоляцию без массовых блокировок благодаря **MVCC** — многоверсионному управлению конкурентным доступом.\n\n## Идея MVCC\n\nПри изменении строки PostgreSQL не перезаписывает её на месте, а создаёт **новую версию**, помечая старую как устаревшую. Каждая транзакция видит **снимок** данных, согласованный на момент её начала (или запроса).\n\n## Читатели не блокируют писателей\n\nГлавное следствие: **чтение никогда не блокирует запись, а запись — чтение**. Пока одна транзакция меняет строку, другие продолжают видеть её прежнюю версию. Это резко повышает параллельность по сравнению с блокировочными СУБД.\n\n## VACUUM\n\nУстаревшие версии строк («мёртвые кортежи») со временем накапливаются — их убирает процесс **VACUUM** (обычно автоматический, autovacuum), освобождая место.\n\n## Коротко\n\nMVCC хранит несколько версий строк и даёт каждой транзакции согласованный снимок; читатели и писатели не блокируют друг друга, а старые версии чистит VACUUM.\n\n## Литература\n\n- [Документация: MVCC](https://postgrespro.ru/docs/postgresql/current/mvcc)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
656a356d-8ad7-4bb5-b5b5-3597d30936f8	13b76285-eb0b-4105-843e-f6aaaceceda5	Первый запрос: SELECT и FROM	SQL (Structured Query Language) — язык запросов к реляционным базам данных. Он **декларативный**: мы описываем, *какой* результат хотим получить, а не *как* его вычислять — за это отвечает сама СУБД. Самая частая задача — получить данные из таблицы, и за неё отвечает оператор **SELECT**, который говорит «какие столбцы вернуть», а ключевое слово **FROM** — «из какой таблицы».\n\n## Синтаксис\n\nПосле SELECT перечисляют нужные столбцы через запятую, после FROM указывают таблицу. Звёздочка `*` означает «все столбцы». Псевдоним через `AS` переименовывает столбец в результате.\n\n## Пример\n\nВыберем имена и группы всех студентов:\n\n```\nSELECT full_name AS student, group_name\nFROM students;\n```\n\nЕсли нужны все столбцы — пишут `SELECT * FROM students;`. Запрос завершается точкой с запятой.\n\n## Сколько строк вернётся\n\nSELECT обрабатывает каждую строку таблицы. Если в `students` 30 записей, то `SELECT group_name FROM students` вернёт **30 строк** — по одной на студента, и значения групп будут повторяться. Чтобы убрать повторы, добавляют `DISTINCT`: `SELECT DISTINCT group_name FROM students`.\n\n## Частые ошибки\n\n- Забытая точка с запятой в конце команды.\n- Ожидание, что строки придут в каком-то порядке: без `ORDER BY` порядок строк **не гарантирован**.\n- Опечатка в имени столбца — запрос завершится ошибкой, а не вернёт пустой столбец.\n\n## Коротко\n\nSELECT задаёт столбцы, FROM — таблицу, `*` — все столбцы, `DISTINCT` убирает дубликаты, `AS` переименовывает столбец.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — «Выборка данных»](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: запросы (SELECT)](https://postgrespro.ru/docs/postgresql/current/queries)\n- [PostgreSQL Exercises — практика](https://pgexercises.com/)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих»: #1 — Основы SQL (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	13b76285-eb0b-4105-843e-f6aaaceceda5	Фильтрация строк: WHERE	Чаще всего нужны не все строки таблицы, а только подходящие под условие. За отбор отвечает ключевое слово **WHERE**: оно идёт после FROM и оставляет лишь те строки, для которых условие истинно. Важно понимать: WHERE работает **до** группировки и сортировки и проверяет каждую строку по отдельности.\n\n## Операторы сравнения\n\nВ условии используют сравнения: `=` (равно), `<>` (не равно), `<`, `>`, `<=`, `>=`. Условия объединяют через **AND** и **OR**, отрицают через **NOT**. Скобки задают приоритет, как в математике.\n\n## Пример\n\nСтуденты группы «П-101» со средним баллом не ниже 4:\n\n```\nSELECT full_name, avg_grade\nFROM students\nWHERE group_name = 'П-101' AND avg_grade >= 4;\n```\n\nТекстовые значения берут в одинарные кавычки. Полезны также `IN (...)` — проверка на вхождение в список, и `BETWEEN a AND b` — попадание в диапазон включительно.\n\n## Особый случай — NULL\n\nNULL означает «значение неизвестно». Поэтому `avg_grade = NULL` **не работает**: сравнение с неизвестным даёт не «истину», а «неизвестно». Для проверки пустоты есть отдельные операторы: `IS NULL` и `IS NOT NULL`. Если у 5 из 30 студентов балл не выставлен, то `WHERE avg_grade IS NULL` вернёт именно эти 5 строк.\n\n## Коротко\n\nWHERE отбирает строки по условию; условия комбинируют AND/OR/NOT; пустые значения проверяют только через IS NULL / IS NOT NULL.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — условия выборки](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: операторы сравнения](https://postgrespro.ru/docs/postgresql/current/functions-comparison)\n- [PostgreSQL Exercises — задачи на WHERE](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
5e596545-cfe5-420d-8ecf-c2b5a15f1122	5ddec0ed-61e9-43a4-b0d5-4e605c6e35fa	Внешние соединения: LEFT/RIGHT JOIN	Внутренний JOIN отбрасывает строки без пары. Но иногда нужно сохранить все строки одной таблицы, даже если совпадения нет — например, показать все группы, включая те, где пока нет студентов. Для этого есть внешние соединения.\n\n## LEFT и RIGHT JOIN\n\n`LEFT JOIN` сохраняет все строки левой таблицы; там, где справа совпадения нет, столбцы правой таблицы будут `NULL`. `RIGHT JOIN` — наоборот, сохраняет правую таблицу. На практике почти всегда пользуются LEFT JOIN, ставя «главную» таблицу слева.\n\n## Пример\n\nВсе группы и число студентов в каждой (включая пустые группы):\n\n```\nSELECT g.title, COUNT(s.id) AS students\nFROM groups AS g\nLEFT JOIN students AS s ON s.group_id = g.id\nGROUP BY g.title\nORDER BY students DESC;\n```\n\n## Важная тонкость\n\nЗдесь нужно считать `COUNT(s.id)`, а не `COUNT(*)`. Для пустой группы LEFT JOIN всё равно даёт одну строку, но с `s.id = NULL`; `COUNT(*)` посчитал бы её за 1, а `COUNT(s.id)` пропустит NULL и даст честный **0**. Это классическая ошибка при подсчётах по внешнему соединению.\n\n## Коротко\n\nLEFT JOIN сохраняет все строки левой таблицы, подставляя NULL при отсутствии пары справа; при подсчётах считайте столбец правой таблицы, а не `*`.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — внешние соединения](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: соединённые таблицы](https://postgrespro.ru/docs/postgresql/current/queries-table-expressions)\n- [PostgreSQL Exercises — JOIN](https://pgexercises.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
803cf9c4-1f4a-4eab-b50a-31ab05d57840	6e25b2e3-aaee-4e08-aed9-3bcc74cf67f6	Итоговая практика по SQL	Соберём вместе всё, что прошли: выборку, фильтрацию, сортировку, агрегаты с группировкой, соединения и подзапросы. Хороший запрос обычно строится по частям и проверяется по шагам.\n\n## Порядок выполнения запроса\n\nСУБД выполняет части в таком порядке (он отличается от порядка написания): `FROM` и JOIN → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`. Понимание этого порядка объясняет, почему, например, псевдоним из SELECT нельзя использовать в WHERE, но можно в ORDER BY.\n\n## Пример\n\nТоп-3 группы по среднему баллу, считая только сданные экзамены и группы хотя бы с 5 оценками:\n\n```\nSELECT g.title, ROUND(AVG(e.grade), 2) AS avg_grade\nFROM groups AS g\nJOIN students AS s ON s.group_id = g.id\nJOIN exams AS e ON e.student_id = s.id\nWHERE e.grade IS NOT NULL\nGROUP BY g.title\nHAVING COUNT(e.id) >= 5\nORDER BY avg_grade DESC\nLIMIT 3;\n```\n\nРазберём по шагам: соединяем три таблицы → оставляем только сданные экзамены → группируем по группе → берём группы с ≥5 оценками → сортируем по среднему → оставляем три верхних.\n\n## Как закреплять\n\nЛучший способ освоить SQL — решать задачи. Начните с интерактивных тренажёров, разбирайте чужие запросы и постепенно усложняйте свои. Возвращайтесь к этой шпаргалке по порядку выполнения, когда запрос ведёт себя неожиданно.\n\n## Коротко\n\nСложные запросы собирают по частям; помните порядок выполнения FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL (учебник целиком)](https://postgrespro.ru/education/books/sqlprimer)\n- [PostgreSQL Exercises — задачи всех уровней](https://pgexercises.com/)\n- [Документация: учебник по SQL](https://postgrespro.ru/docs/postgresql/current/tutorial-sql)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
c857e472-55b9-4ba4-8612-8e81cf5f42be	a967fcbe-701f-4fc0-92f1-1b649a31f713	Преобразование ER-модели в таблицы	Когда ER-модель готова, её переводят в реляционную схему — набор таблиц. Для этого есть чёткие правила.\n\n## Правила преобразования\n\n- **сущность → таблица**, её атрибуты → столбцы;\n- ключевой атрибут → **PRIMARY KEY**;\n- связь **1:М** → **внешний ключ** в таблице на стороне «много»;\n- связь **М:М** → отдельная **связующая таблица** с двумя внешними ключами;\n- связь **1:1** → внешний ключ с ограничением `UNIQUE` (или объединение в одну таблицу).\n\n## Пример\n\nСвязь Студенты ↔ Курсы (М:М) превращается в связующую таблицу:\n\n```\nCREATE TABLE enrollments (\n  student_id int REFERENCES students(id),\n  course_id  int REFERENCES courses(id),\n  PRIMARY KEY (student_id, course_id)\n);\n```\n\nЗдесь первичный ключ **составной** (пара студент+курс) — это заодно запрещает дважды записать студента на один курс.\n\n## Частые ошибки\n\n- Хранить М:М без связующей таблицы (списком в одном поле) — это нарушает первую нормальную форму;\n- забыть внешний ключ и потерять ссылочную целостность.\n\n## Коротко\n\nСущность → таблица, 1:М → внешний ключ, М:М → связующая таблица с составным ключом.\n\n## Литература\n\n- [Документация: создание таблиц (DDL)](https://postgrespro.ru/docs/postgresql/current/ddl)\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих» (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	2	40	10
a76e62b1-ed81-4666-ab21-3ee82561ec15	0d61ac1b-37ee-4150-bf3d-f862cd47d50e	Транзакции в реальных сценариях	Соберём практические правила работы с транзакциями, которые делают приложение надёжным и быстрым.\n\n## Короткие транзакции\n\nДержите транзакции как можно короче: не открывайте BEGIN перед долгими вычислениями или ожиданием пользователя. Длинные транзакции дольше держат блокировки и мешают VACUUM убирать старые версии строк.\n\n## Повтор при сбое сериализации\n\nНа уровнях Repeatable Read и Serializable PostgreSQL может откатить транзакцию с ошибкой сериализации. Это нормально — приложение должно **повторить** такую транзакцию. Поэтому код транзакции желательно делать идемпотентным и оборачивать в цикл повторов.\n\n## Практические советы\n\n- одна логическая операция — одна транзакция;\n- не делайте сетевых запросов внутри открытой транзакции;\n- выбирайте минимально достаточный уровень изоляции;\n- обрабатывайте deadlock и ошибки сериализации повтором.\n\n## Коротко\n\nТранзакции должны быть короткими и по возможности идемпотентными; ошибки сериализации и взаимоблокировки решают повтором, а уровень изоляции берут минимально достаточный.\n\n## Литература\n\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n- [Документация: изоляция транзакций](https://postgrespro.ru/docs/postgresql/current/transaction-iso)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
b269811c-16b7-451b-982a-e859036655a2	1d3e6738-fbfa-481c-a347-e7c868aa4cf2	План запроса: EXPLAIN и EXPLAIN ANALYZE	Чтобы понять, как СУБД выполняет запрос и использует ли индекс, смотрят **план выполнения** командой EXPLAIN.\n\n## EXPLAIN\n\n`EXPLAIN` показывает план без выполнения запроса: какие сканирования и соединения будут применены и какова оценочная стоимость.\n\n```\nEXPLAIN SELECT * FROM students WHERE group_id = 5;\n```\n\nВ плане видно, например, `Seq Scan` (полный перебор) или `Index Scan` (поиск по индексу).\n\n## EXPLAIN ANALYZE\n\n`EXPLAIN ANALYZE` действительно выполняет запрос и показывает **реальное** время и число строк — это главный инструмент диагностики медленных запросов. Сравнивая оценку планировщика с фактом, находят проблемы.\n\n## Ключевые узлы плана\n\n- **Seq Scan** — последовательное чтение всей таблицы;\n- **Index Scan** / **Index Only Scan** — поиск по индексу;\n- **Bitmap Scan** — компромисс при множестве совпадений;\n- **Nested Loop / Hash Join / Merge Join** — способы соединения.\n\n## Коротко\n\nEXPLAIN показывает план запроса, EXPLAIN ANALYZE — ещё и реальное время; по узлам плана видно, используется ли индекс.\n\n## Литература\n\n- [Документация: использование EXPLAIN](https://postgrespro.ru/docs/postgresql/current/using-explain)\n- [PostgreSQL 16. Оптимизация запросов](https://postgrespro.ru/education/books/qptbook)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
01671e10-6ef0-47ea-87c8-901dc1e2f2fb	f387a0d1-8bc0-4865-b0db-cc0e316c5d2c	Уровни изоляции транзакций	Стандарт SQL определяет четыре **уровня изоляции** — компромисс между корректностью и параллельностью: чем строже уровень, тем меньше аномалий, но больше блокировок и откатов.\n\n## Четыре уровня\n\n- **Read Uncommitted** — допускает грязное чтение (самый слабый).\n- **Read Committed** — видит только зафиксированные данные; возможны неповторяющиеся и фантомные чтения.\n- **Repeatable Read** — повторные чтения стабильны; PostgreSQL на этом уровне исключает и фантомы.\n- **Serializable** — результат как при последовательном выполнении транзакций (самый строгий).\n\n## Особенности PostgreSQL\n\nВ PostgreSQL уровень по умолчанию — **Read Committed**, а грязное чтение не возникает **никогда** (даже Read Uncommitted ведёт себя как Read Committed). Уровень задают так:\n\n```\nBEGIN ISOLATION LEVEL REPEATABLE READ;\n-- ...\nCOMMIT;\n```\n\n## Коротко\n\nЧетыре уровня (Read Uncommitted → Serializable) различаются допустимыми аномалиями; в PostgreSQL по умолчанию Read Committed, грязного чтения нет вовсе.\n\n## Литература\n\n- [Документация: изоляция транзакций](https://postgrespro.ru/docs/postgresql/current/transaction-iso)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
c3342223-7064-48a9-871c-809ed3b36cef	052a6e65-41b9-4fcb-adcd-964ca39508b5	Почему индекс не используется	Частая ситуация: индекс создан, а запрос всё равно идёт через Seq Scan. Разберём типичные причины.\n\n## Функция или преобразование над столбцом\n\nЕсли в условии столбец «завёрнут» в функцию, обычный индекс не применяется:\n\n```\nWHERE lower(email) = 'a@b.ru'   -- индекс по email не сработает\n```\n\nРешение — индекс по выражению: `CREATE INDEX ... ON students (lower(email))`.\n\n## Малая таблица или много совпадений\n\nЕсли таблица маленькая или запрос возвращает большую долю строк, планировщику **дешевле** прочитать всю таблицу, чем прыгать по индексу. Это нормальное поведение.\n\n## Несовпадение типов и устаревшая статистика\n\nСравнение разных типов (`WHERE id = '5'`) и устаревшая статистика тоже мешают. После массовых изменений полезно выполнить `ANALYZE` (следующий урок).\n\n## Коротко\n\nИндекс игнорируется, если столбец обёрнут в функцию, таблица мала, совпадений слишком много, не совпадают типы или устарела статистика.\n\n## Литература\n\n- [Markus Winand. Use The Index, Luke!](https://use-the-index-luke.com/)\n- [Документация: использование EXPLAIN](https://postgrespro.ru/docs/postgresql/current/using-explain)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	0	20	10
109a7e19-2fe6-41f1-a344-f02a732b310c	d3ec801e-8b74-43f2-bf41-8dfcb9b85b86	Hash, GIN и GiST	Кроме B-tree, PostgreSQL поддерживает специализированные типы индексов под особые задачи.\n\n## Hash\n\nИндекс по хэшу значения. Поддерживает только поиск по равенству (`=`), зато компактен. На практике B-tree почти всегда предпочтительнее, поэтому Hash используют редко.\n\n## GIN (обобщённый инвертированный индекс)\n\nДля «составных» значений, где в одном поле много элементов: массивы, JSONB, полнотекстовый поиск (tsvector). GIN отвечает на вопросы вида «содержит ли документ слово», «есть ли элемент в массиве».\n\n## GiST\n\nОбобщённое дерево поиска — для данных, где важна близость или пересечение: геометрия, диапазоны, полнотекст. Например, «какие интервалы пересекаются».\n\n## Пример\n\n```\nCREATE INDEX idx_doc_search\n  ON lessons USING gin (to_tsvector('russian', theory_content));\n```\n\n## Коротко\n\nHash — только равенство (редко нужен); GIN — массивы/JSONB/полнотекст; GiST — близость и пересечения (геометрия, диапазоны).\n\n## Литература\n\n- [Документация: типы индексов](https://postgrespro.ru/docs/postgresql/current/indexes-types)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
216f012b-02e7-49c4-81e1-08e8a9af6dcd	cc106b14-5e26-4e65-8c79-6e40ee1bb56e	Сортировка и агрегатные функции	Чтобы упорядочить результат, используют **ORDER BY**, а чтобы получить сводные числа по множеству строк — **агрегатные функции**.\n\n## Сортировка\n\nORDER BY указывает столбец (или несколько) для сортировки; `ASC` — по возрастанию (по умолчанию), `DESC` — по убыванию. Можно сортировать по нескольким столбцам: `ORDER BY group_name, avg_grade DESC`.\n\n## Агрегаты\n\nОсновные функции: `COUNT` — количество, `SUM` — сумма, `AVG` — среднее, `MIN` и `MAX` — минимум и максимум. Агрегат «сворачивает» множество строк в одно значение.\n\n## Пример\n\nСколько студентов и какой у них средний балл:\n\n```\nSELECT COUNT(*) AS students, ROUND(AVG(avg_grade), 2) AS avg_grade\nFROM students;\n```\n\n## COUNT(*) против COUNT(столбец)\n\nЭто частый источник ошибок. `COUNT(*)` считает **все** строки. `COUNT(avg_grade)` считает только строки, где `avg_grade` **не NULL**. Поэтому если у части студентов балл не выставлен, эти два запроса дадут разные числа — и обычно нужен именно второй вариант.\n\n## Коротко\n\nORDER BY сортирует строки (ASC/DESC); агрегаты COUNT/SUM/AVG/MIN/MAX считают сводные значения; COUNT(столбец) пропускает NULL.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — агрегатные функции](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: агрегатные функции](https://postgrespro.ru/docs/postgresql/current/functions-aggregate)\n- [PostgreSQL Exercises — агрегаты](https://pgexercises.com/)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих»: основы SQL (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	0	20	10
4af74a77-d15e-4068-a521-ee54d84fb942	b6ca775f-7a9c-455c-8099-49f8fc187f96	Индексы для JOIN и сортировки	Индексы ускоряют не только WHERE, но и соединения и сортировку — частые источники медленных запросов.\n\n## Индексы для JOIN\n\nПри соединении таблиц по внешнему ключу индекс на столбце-ссылке позволяет использовать быстрые стратегии (Nested Loop с Index Scan, Merge Join) вместо перебора всех пар.\n\n```\nCREATE INDEX idx_enrollments_student ON enrollments (student_id);\n```\n\nПолезное правило: **столбцы внешних ключей почти всегда стоит индексировать**, потому что по ним постоянно соединяют.\n\n## Индексы для сортировки\n\nПоскольку B-tree хранит значения отсортированными, индекс может вернуть строки уже в нужном порядке — тогда отдельный шаг Sort в плане исчезает:\n\n```\nCREATE INDEX idx_students_grade ON students (avg_grade DESC);\n-- ORDER BY avg_grade DESC обойдётся без сортировки\n```\n\n## Коротко\n\nИндексы на столбцах внешних ключей ускоряют JOIN, а индекс с нужным порядком убирает шаг сортировки для ORDER BY.\n\n## Литература\n\n- [Markus Winand. Use The Index, Luke!](https://use-the-index-luke.com/)\n- [Документация: использование EXPLAIN](https://postgrespro.ru/docs/postgresql/current/using-explain)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	0	20	10
9058ccbe-0dd4-4d78-8bf6-d39b08e5187b	a91b48e1-85e5-49d2-968a-0ae47a581a36	Взаимоблокировки (deadlock)	**Взаимоблокировка (deadlock)** — ситуация, когда две транзакции ждут друг друга и ни одна не может продолжиться.\n\n## Как возникает\n\nТранзакция A заблокировала строку 1 и ждёт строку 2; транзакция B заблокировала строку 2 и ждёт строку 1. Обе застряли навсегда.\n\n```\n-- A:                        -- B:\nUPDATE ... WHERE id = 1;     UPDATE ... WHERE id = 2;\nUPDATE ... WHERE id = 2;     UPDATE ... WHERE id = 1;   -- deadlock\n```\n\n## Что делает PostgreSQL\n\nPostgreSQL **автоматически обнаруживает** взаимоблокировки и принудительно откатывает одну из транзакций с ошибкой — приложение должно её повторить.\n\n## Как избегать\n\nГлавный приём — захватывать ресурсы в **едином порядке** во всех транзакциях (например, всегда по возрастанию id) и держать транзакции короткими.\n\n## Коротко\n\nDeadlock — взаимное ожидание транзакций; PostgreSQL обнаруживает его и откатывает одну из них; предотвращают единым порядком захвата ресурсов.\n\n## Литература\n\n- [Документация: явные блокировки и взаимоблокировки](https://postgrespro.ru/docs/postgresql/current/explicit-locking)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	1	30	10
d88c153c-0b2b-4ed1-ad34-ce9835fdd9db	0d61ac1b-37ee-4150-bf3d-f862cd47d50e	SELECT FOR UPDATE и пессимистичные блокировки	Когда нужно прочитать строку и тут же гарантированно её изменить, не дав другим вмешаться, применяют **пессимистичную** блокировку через `SELECT ... FOR UPDATE`.\n\n## Пессимистичный подход\n\n«Пессимистичный» — потому что мы заранее предполагаем конфликт и блокируем строку сразу при чтении, до изменения.\n\n## SELECT FOR UPDATE\n\n```\nBEGIN;\nSELECT seats FROM courses WHERE id = 5 FOR UPDATE;  -- строка заблокирована\n-- проверяем, есть ли места, и если да:\nUPDATE courses SET seats = seats - 1 WHERE id = 5;\nCOMMIT;\n```\n\nПока транзакция не завершится, другая транзакция с таким же `FOR UPDATE` будет ждать. Это надёжно решает проблему «двойной записи на последнее место».\n\n## Коротко\n\nSELECT ... FOR UPDATE блокирует прочитанные строки до конца транзакции — пессимистичный способ безопасно «прочитать и изменить».\n\n## Литература\n\n- [Документация: явные блокировки (FOR UPDATE)](https://postgrespro.ru/docs/postgresql/current/explicit-locking)\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
15c8f256-1ec2-43e9-bb50-0509160c3d8b	052a6e65-41b9-4fcb-adcd-964ca39508b5	Статистика и ANALYZE	Планировщик выбирает план не наугад, а по **статистике** о данных: сколько строк в таблице, насколько разнообразны значения столбцов. От её актуальности напрямую зависит качество планов.\n\n## Что собирает статистика\n\nДля каждого столбца хранятся оценки: доля NULL, число различных значений, самые частые значения, гистограмма распределения. По ним планировщик оценивает, сколько строк вернёт условие, и выбирает Seq Scan или Index Scan.\n\n## Команда ANALYZE\n\n`ANALYZE` пересобирает статистику:\n\n```\nANALYZE students;\n```\n\nОбычно её собирает автоматически процесс **autovacuum**, но после массовой загрузки данных полезно запустить ANALYZE вручную, иначе планы строятся по устаревшим оценкам.\n\n## Коротко\n\nПланировщик опирается на статистику распределения данных; её обновляет ANALYZE (и autovacuum) — без свежей статистики планы получаются плохими.\n\n## Литература\n\n- [Документация: статистика для планировщика](https://postgrespro.ru/docs/postgresql/current/planner-stats)\n- [PostgreSQL 16. Оптимизация запросов](https://postgrespro.ru/education/books/qptbook)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
0d066443-46e1-4505-a7e6-bcaed42de2e1	1d3e6738-fbfa-481c-a347-e7c868aa4cf2	Что такое индекс и зачем он нужен	Индекс — это вспомогательная структура данных, которая ускоряет поиск строк по значению столбца. Без индекса СУБД вынуждена просматривать всю таблицу (последовательное сканирование, *seq scan*); индекс позволяет находить нужные строки почти сразу, как алфавитный указатель в книге.\n\n## Аналогия\n\nЧтобы найти слово в книге, не листают все страницы подряд — смотрят в указатель в конце. Индекс в БД работает так же: хранит отсортированные значения столбца и ссылки на строки.\n\n## Цена индекса\n\nИндексы ускоряют чтение, но замедляют запись: при каждом INSERT/UPDATE/DELETE индекс нужно обновлять, и он занимает место на диске. Поэтому индексируют не всё подряд, а столбцы, по которым реально часто ищут и соединяют.\n\n## Пример\n\n```\nCREATE INDEX idx_students_group ON students (group_id);\n```\n\nТеперь запрос `WHERE group_id = 5` сможет использовать индекс вместо полного перебора.\n\n## Коротко\n\nИндекс ускоряет поиск по значению ценой замедления записи и расхода места; создают его на часто используемых в WHERE/JOIN столбцах.\n\n## Литература\n\n- [Документация: индексы](https://postgrespro.ru/docs/postgresql/current/indexes)\n- [Markus Winand. Use The Index, Luke!](https://use-the-index-luke.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
79cfafe9-a52d-43b9-b488-150641e6fbb7	de23741e-cedb-4a46-b0fc-f89d498082e8	Типы данных PostgreSQL	Правильный выбор типа столбца — основа корректной и компактной схемы. PostgreSQL предлагает богатый набор типов.\n\n## Основные типы\n\n- **Числа**: `integer`, `bigint`, `numeric(p, s)` (точные дроби — для денег и оценок), `double precision`.\n- **Строки**: `text` (универсальный), `varchar(n)` (с ограничением длины).\n- **Дата и время**: `date`, `time`, `timestamp`, `timestamptz` (с часовым поясом — обычно предпочтительнее).\n- **Логический**: `boolean`.\n- **Прочее**: `uuid`, `json`/`jsonb`, массивы.\n\n## serial и идентификаторы\n\n`serial`/`bigserial` — это `integer`/`bigint` с автоинкрементом, удобно для первичных ключей.\n\n## Пример\n\n```\nCREATE TABLE exams (\n  id bigserial PRIMARY KEY,\n  grade numeric(2,1) CHECK (grade BETWEEN 2 AND 5),\n  taken_at timestamptz DEFAULT now()\n);\n```\n\n## Коротко\n\nВыбирайте тип по смыслу: numeric для точных дробей, text для строк, timestamptz для времени, boolean для флагов; serial удобен для ключей.\n\n## Литература\n\n- [Документация: типы данных](https://postgrespro.ru/docs/postgresql/current/datatype)\n- [PostgreSQL. Основы языка SQL](https://postgrespro.ru/education/books/sqlprimer)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
1a340833-305a-415a-aab5-08d5e36d17c8	720171ae-9ba0-4777-a9e1-8d53f6881e54	JSON и массивы в PostgreSQL	PostgreSQL умеет хранить не только «плоские» значения, но и полуструктурированные данные — массивы и JSON. Это делает его гибким для современных приложений.\n\n## Массивы\n\nСтолбец может быть массивом значений:\n\n```\nCREATE TABLE posts (id serial, tags text[]);\nINSERT INTO posts (tags) VALUES (ARRAY['sql', 'postgres']);\nSELECT * FROM posts WHERE 'sql' = ANY(tags);\n```\n\n## JSON и JSONB\n\n`json` хранит текст как есть, `jsonb` — в разобранном бинарном виде (быстрее для поиска и поддерживает индексы GIN). На практике используют **jsonb**:\n\n```\nCREATE TABLE events (id serial, data jsonb);\nINSERT INTO events (data) VALUES ('{"type":"login","ok":true}');\nSELECT data->>'type' FROM events WHERE data->>'ok' = 'true';\n```\n\nОператоры: `->` (вернуть JSON), `->>` (вернуть текст), `@>` (содержит).\n\n## Когда применять\n\nПолуструктурированные типы хороши для редких и переменных полей. Но если данные регулярные — лучше обычные столбцы и нормализация: они строже и эффективнее.\n\n## Коротко\n\nPostgreSQL хранит массивы и JSON (предпочтителен jsonb с операторами -> / ->> / @> и GIN-индексом); применяют для переменных данных, а регулярные лучше держать в обычных столбцах.\n\n## Литература\n\n- [Документация: типы JSON](https://postgrespro.ru/docs/postgresql/current/datatype-json)\n- [Документация: массивы](https://postgrespro.ru/docs/postgresql/current/arrays)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
65a44718-3541-4b58-ae6e-20130d170308	04815cf9-0c0a-4b20-b3d6-9ff860f7e2c3	Смещение: LAG и LEAD	Иногда нужно сравнить строку с **соседней** — предыдущей или следующей. Для этого служат функции смещения LAG и LEAD.\n\n## LAG и LEAD\n\n- **LAG(столбец)** — значение из предыдущей строки окна;\n- **LEAD(столбец)** — значение из следующей строки.\n\nИм важен `ORDER BY` в окне — он определяет, какая строка «предыдущая».\n\n## Пример\n\nСравним балл студента с предыдущим в рейтинге:\n\n```\nSELECT full_name, avg_grade,\n       LAG(avg_grade) OVER (ORDER BY avg_grade DESC) AS prev,\n       avg_grade - LAG(avg_grade) OVER (ORDER BY avg_grade DESC) AS diff\nFROM students;\n```\n\nУ первой строки `prev` будет NULL (предыдущей строки нет). Можно задать значение по умолчанию: `LAG(avg_grade, 1, 0)`.\n\n## Где применяют\n\nДинамика во времени: рост или падение показателя относительно прошлого периода, разрывы между соседними значениями.\n\n## Коротко\n\nLAG берёт значение из предыдущей строки, LEAD — из следующей (по ORDER BY окна); удобно для сравнения с соседями и анализа динамики.\n\n## Литература\n\n- [Документация: оконные функции (справочник)](https://postgrespro.ru/docs/postgresql/current/functions-window)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
a462d37f-b543-4513-93cb-9048887b090b	04815cf9-0c0a-4b20-b3d6-9ff860f7e2c3	Агрегаты как оконные функции	Любую агрегатную функцию (SUM, AVG, COUNT, MIN, MAX) можно использовать как оконную — добавив OVER(). Это открывает мощные приёмы аналитики.\n\n## Агрегат + OVER()\n\nБез ORDER BY агрегат считается по всему окну (или секции). С ORDER BY получается **нарастающий итог** (running total) — агрегат от начала окна до текущей строки.\n\n## Пример: нарастающий итог\n\n```\nSELECT taken_at, points,\n       SUM(points) OVER (ORDER BY taken_at) AS running_total\nFROM transactions;\n```\n\nКаждая строка показывает сумму всех баллов с начала и до неё включительно.\n\n## Доля от общего\n\n```\nSELECT group_name, students,\n       ROUND(100.0 * students / SUM(students) OVER (), 1) AS percent\nFROM group_sizes;\n```\n\nЗдесь `SUM(...) OVER ()` — общее число, а рядом сразу доля каждой группы.\n\n## Коротко\n\nАгрегаты с OVER() считают по окну без схлопывания строк; с ORDER BY дают нарастающий итог, без него — общую сумму для расчёта долей.\n\n## Литература\n\n- [Документация: оконные функции (учебник)](https://postgrespro.ru/docs/postgresql/current/tutorial-window)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	2	40	10
5bfd53b9-1c56-46c0-993e-fd7614f85bbd	bd1d6e65-392c-47e4-8fd1-045217c779db	Рамки окна: ROWS и RANGE	По умолчанию при наличии ORDER BY окно «растёт» от начала до текущей строки. Но границы окна можно задать явно — это **рамка** (frame).\n\n## Зачем нужны рамки\n\nРамка определяет, какие именно строки вокруг текущей входят в расчёт: все предыдущие, скользящее окно из N строк, всё до конца секции и т. д.\n\n## ROWS и RANGE\n\n- **ROWS** считает рамку в строках (физически);\n- **RANGE** — по значениям ORDER BY (логически; строки с равным значением попадают вместе).\n\n```\n-- скользящее среднее по 3 последним строкам\nAVG(points) OVER (\n  ORDER BY taken_at\n  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n)\n```\n\nГраницы задают словами: `UNBOUNDED PRECEDING` (с начала), `N PRECEDING`, `CURRENT ROW`, `N FOLLOWING`, `UNBOUNDED FOLLOWING` (до конца).\n\n## Коротко\n\nРамка (ROWS/RANGE BETWEEN ...) задаёт точные границы окна вокруг текущей строки — например, скользящее среднее по последним N строкам.\n\n## Литература\n\n- [Документация: оконные функции (справочник)](https://postgrespro.ru/docs/postgresql/current/functions-window)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
67fd2b21-adf0-4cba-af96-30c691d48c56	0bb51c3a-f221-44a4-911f-d07bb32e53a7	Вторая нормальная форма (2НФ)	**Вторая нормальная форма (2НФ)** борется с **частичными** зависимостями и важна для таблиц с **составным** ключом.\n\n## Требование 2НФ\n\nТаблица в 2НФ, если:\n- она уже в 1НФ;\n- каждый неключевой атрибут зависит от **всего** составного ключа, а не от его части.\n\nЕсли ключ состоит из одного столбца, 2НФ выполняется автоматически.\n\n## Пример\n\n```\n-- ключ (студент, курс); оценка зависит от обоих,\n-- а название курса — только от курса\nстудент | курс | название_курса | оценка\n```\n\n`название_курса` зависит лишь от части ключа (`курс`) — это частичная зависимость, нарушение 2НФ. Исправление — вынести курсы в отдельную таблицу:\n\n```\nenrollments(студент, курс, оценка)\ncourses(курс, название_курса)\n```\n\n## Коротко\n\n2НФ: таблица в 1НФ и нет частичных зависимостей — неключевые атрибуты зависят от всего составного ключа, а не от его части.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
c6961546-24cc-4c8c-9ab5-11dc836974a4	ec8b8164-455f-4903-87be-0522e01d7663	Денормализация: когда оправдана	Нормализация убирает избыточность, но иногда её сознательно нарушают ради скорости — это **денормализация**.\n\n## Что это\n\nДенормализация — намеренное добавление избыточных данных (дублирование столбца, хранение предвычисленного итога), чтобы ускорить чтение и упростить запросы.\n\n## Когда оправдана\n\n- тяжёлые **аналитические отчёты**, где JOIN множества таблиц дороги;\n- редко меняющиеся справочные данные;\n- хранение агрегатов (например, «число студентов в группе»), чтобы не считать их каждый раз.\n\n## Риски\n\nЗа скорость чтения платят целостностью: продублированные данные нужно поддерживать в согласованном состоянии (триггерами, фоновым пересчётом). Поэтому денормализуют **осознанно и точечно**, начав с нормализованной схемы, а не наоборот.\n\n## Коротко\n\nДенормализация — намеренная избыточность ради скорости чтения; применяется точечно, ценой усложнения поддержки целостности.\n\n## Литература\n\n- [Основы технологий баз данных](https://postgrespro.ru/education/books/dbtech)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
908c3e39-6910-48f7-81e2-2a5059fb346e	6ba31548-cc5b-4aa0-8e9a-712eb3b40e47	ACID — свойства транзакций	**Транзакция** — это группа операций над данными, которая выполняется как единое целое: либо целиком, либо никак. Транзакции — основа надёжности базы данных; их свойства описывают аббревиатурой **ACID**.\n\n## Зачем нужны транзакции\n\nКлассический пример — перевод: списать баллы у одного студента и начислить другому. Если между двумя операциями случится сбой, баллы «потеряются». Транзакция гарантирует, что либо пройдут обе операции, либо ни одной.\n\n## ACID\n\n- **Atomicity (атомарность)** — все операции применяются целиком или откатываются.\n- **Consistency (согласованность)** — транзакция переводит базу из одного корректного состояния в другое, не нарушая ограничений.\n- **Isolation (изоляция)** — параллельные транзакции не мешают друг другу так, будто выполняются по очереди.\n- **Durability (долговечность)** — после фиксации изменения сохранятся даже при сбое питания.\n\n## Коротко\n\nТранзакция — неделимая группа операций; её свойства — атомарность, согласованность, изоляция и долговечность (ACID).\n\n## Литература\n\n- [PostgreSQL 17 изнутри (Е. Рогов)](https://postgrespro.ru/education/books/internals)\n- [Документация: введение в MVCC](https://postgrespro.ru/docs/postgresql/current/mvcc-intro)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	0	20	10
a09899eb-977c-44ed-8212-a0ae9af37084	6ba31548-cc5b-4aa0-8e9a-712eb3b40e47	BEGIN, COMMIT, ROLLBACK	Транзакцией управляют тремя командами: **BEGIN** (начать), **COMMIT** (зафиксировать), **ROLLBACK** (откатить).\n\n## Управление транзакцией\n\n```\nBEGIN;\nUPDATE accounts SET points = points - 10 WHERE student_id = 1;\nUPDATE accounts SET points = points + 10 WHERE student_id = 2;\nCOMMIT;   -- обе операции зафиксированы вместе\n```\n\nЕсли на любом шаге что-то пошло не так, вместо COMMIT выполняют `ROLLBACK` — и база возвращается в состояние до BEGIN.\n\n## Автокоммит\n\nПо умолчанию каждый одиночный запрос выполняется в своей неявной транзакции (автокоммит). Явные BEGIN/COMMIT нужны, когда несколько операций должны быть неделимы.\n\n## Коротко\n\nBEGIN открывает транзакцию, COMMIT фиксирует изменения, ROLLBACK отменяет их; одиночные запросы фиксируются автоматически.\n\n## Литература\n\n- [PostgreSQL. Основы языка SQL — транзакции](https://postgrespro.ru/education/books/sqlprimer)\n- [Документация: учебник по транзакциям](https://postgrespro.ru/docs/postgresql/current/tutorial-transactions)\n\n## Видео\n\n- [Курс «PostgreSQL для начинающих» (Habr)](https://habr.com/ru/companies/tensor/articles/779698/)	1	30	10
9c7d1d3d-d4ee-4499-b44d-9b360a1b7a38	b6ca775f-7a9c-455c-8099-49f8fc187f96	Покрывающие индексы (INCLUDE)	Иногда запрос можно выполнить, вообще не обращаясь к таблице — только по индексу. Этот приём называется **index-only scan**, а индекс — **покрывающим**.\n\n## Идея\n\nЕсли все нужные запросу столбцы есть в индексе, СУБД берёт данные прямо из него, не читая строки таблицы. Это заметно быстрее.\n\n## INCLUDE\n\nС PostgreSQL 11 можно добавить в индекс «полезную нагрузку» — столбцы, по которым не ищут, но которые нужны в результате:\n\n```\nCREATE INDEX idx_students_group_inc\n  ON students (group_id) INCLUDE (full_name);\n-- SELECT full_name WHERE group_id = 5 пойдёт index-only\n```\n\n`group_id` участвует в поиске, `full_name` лежит в индексе как нагрузка — таблицу читать не нужно.\n\n## Коротко\n\nПокрывающий индекс содержит все столбцы запроса, что даёт index-only scan без чтения таблицы; дополнительные столбцы добавляют через INCLUDE.\n\n## Литература\n\n- [Документация: index-only сканирование](https://postgrespro.ru/docs/postgresql/current/indexes-index-only-scans)\n- [Markus Winand. Use The Index, Luke!](https://use-the-index-luke.com/)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
d5958c5c-05d6-4093-981f-bb8c27da8491	4f7c50f2-af4f-453a-927c-034623a2f694	PARTITION BY и ORDER BY в окне	Окно можно сузить и упорядочить — для этого внутри OVER() используют PARTITION BY и ORDER BY.\n\n## PARTITION BY\n\n`PARTITION BY` разбивает строки на секции, и функция считается отдельно в каждой — аналог GROUP BY, но без схлопывания строк:\n\n```\nSELECT full_name, group_name, avg_grade,\n       AVG(avg_grade) OVER (PARTITION BY group_name) AS group_avg\nFROM students;\n```\n\nТеперь рядом с каждым студентом — средний балл его группы.\n\n## ORDER BY в окне\n\n`ORDER BY` внутри OVER() задаёт порядок строк в окне. Он нужен функциям, которым важна последовательность (ранжирование, нарастающий итог):\n\n```\nSELECT full_name, avg_grade,\n       RANK() OVER (ORDER BY avg_grade DESC) AS place\nFROM students;\n```\n\n## Коротко\n\nPARTITION BY делит окно на секции (как GROUP BY, но без схлопывания), ORDER BY задаёт порядок строк внутри окна.\n\n## Литература\n\n- [Документация: оконные функции (учебник)](https://postgrespro.ru/docs/postgresql/current/tutorial-window)\n- [Документация: оконные функции (справочник)](https://postgrespro.ru/docs/postgresql/current/functions-window)\n\n## Видео\n\n- [Видеоуроки по SQL и PostgreSQL (sqlcode.ru)](https://www.sqlcode.ru/index.php/all-video-lessons/video-lessons-pgsql)	1	30	10
74d2bdb5-6663-41c3-8f2d-f491bcb750b5	04815cf9-0c0a-4b20-b3d6-9ff860f7e2c3	Ранжирование: ROW_NUMBER, RANK, DENSE_RANK	Самая частая задача для оконных функций — пронумеровать или проранжировать строки в нужном порядке.\n\n## Три функции ранжирования\n\n- **ROW_NUMBER()** — сквозной номер строки (1, 2, 3, 4...), всегда уникальный.\n- **RANK()** — ранг с «пропусками»: при равенстве значений ранг одинаков, а следующий пропускается (1, 2, 2, 4).\n- **DENSE_RANK()** — ранг без пропусков (1, 2, 2, 3).\n\n## Пример\n\n```\nSELECT full_name, avg_grade,\n       ROW_NUMBER() OVER (ORDER BY avg_grade DESC) AS num,\n       RANK()       OVER (ORDER BY avg_grade DESC) AS rank,\n       DENSE_RANK() OVER (ORDER BY avg_grade DESC) AS dense\nFROM students;\n```\n\n## Топ-N в каждой группе\n\nКомбинируя PARTITION BY и ROW_NUMBER, получают «топ-N в каждой секции» — например, лучшего студента каждой группы (взять строки с num = 1).\n\n## Коротко\n\nROW_NUMBER — уникальный номер; RANK — ранг с пропусками при равенстве; DENSE_RANK — без пропусков; вместе с PARTITION BY дают «топ-N в группе».\n\n## Литература\n\n- [Документация: оконные функции (справочник)](https://postgrespro.ru/docs/postgresql/current/functions-window)\n- [PostgreSQL. Профессиональный SQL](https://postgrespro.ru/education/books/advancedsql)\n\n## Видео\n\n- [RUTUBE: видеоуроки по СУБД](https://rutube.ru/u/reddatabase/)	0	20	10
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (id, sender_id, recipient_id, course_id, body, created_at, read_at) FROM stdin;
17f6c85f-3ba4-4cbb-a19b-9f88b35e9670	0a000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000005	\N	test	2026-06-18 22:31:26.346+03	2026-06-18 22:31:36.051+03
27cb99ce-46cd-4645-8d76-4b68d7f3ad5b	0a000000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000005	758a89c8-4b2a-44c5-9156-200aaa59fcbe	Что именно вас интересует?	2026-06-19 05:45:36.041+03	2026-06-19 05:45:47.855+03
eb1ad8ca-e942-42b9-ac7d-9abc6e52158c	0a000000-0000-0000-0000-000000000005	0a000000-0000-0000-0000-000000000001	758a89c8-4b2a-44c5-9156-200aaa59fcbe	Здравствуйте! Подскажите по теме JOIN, не до конца понял внешние соединения.	2026-06-18 22:27:08.66+03	\N
c1c526e0-54e4-4210-8101-2afd1735d243	0a000000-0000-0000-0000-000000000005	0a000000-0000-0000-0000-000000000001	0c000000-0000-0000-0000-000000000001	Здравствуйте	2026-06-19 05:44:50.939+03	\N
6a2fb1cb-2a1d-4e46-9898-4bdc168052e0	0a000000-0000-0000-0000-000000000005	0a000000-0000-0000-0000-000000000001	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	По нормализации: чем 2НФ отличается от 3НФ?	2026-06-19 05:00:55.224+03	\N
\.


--
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.modules (id, course_id, title, description, order_index, week_number) FROM stdin;
0d000000-0000-0000-0000-000000000001	0c000000-0000-0000-0000-000000000001	Данные и таблицы	Что такое данные и как они хранятся в таблицах.	1	1
0d000000-0000-0000-0000-000000000002	0c000000-0000-0000-0000-000000000001	Сущности, связи, ER-модель	Моделирование предметной области.	2	3
0d000000-0000-0000-0000-000000000003	0c000000-0000-0000-0000-000000000001	SQL: создание и выборка	Первые запросы в PostgreSQL.	3	7
0d000000-0000-0000-0000-000000000004	0c000000-0000-0000-0000-000000000001	SQL: фильтрация и сортировка	Отбор нужных строк и наведение порядка в выборке.	4	8
0d000000-0000-0000-0000-000000000005	0c000000-0000-0000-0000-000000000001	SQL: изменение данных	Добавление, изменение и удаление записей.	5	9
0d000000-0000-0000-0000-000000000006	0c000000-0000-0000-0000-000000000001	Агрегация и группировка	Подсчёты, средние и сводки по группам.	6	10
0d000000-0000-0000-0000-000000000007	0c000000-0000-0000-0000-000000000001	Связывание таблиц (JOIN)	Объединение данных из нескольких таблиц.	7	12
0d000000-0000-0000-0000-000000000008	0c000000-0000-0000-0000-000000000001	Проектирование: нормализация	Как избавиться от избыточности и аномалий.	8	14
0d000000-0000-0000-0000-000000000009	0c000000-0000-0000-0000-000000000001	Целостность и производительность	Ограничения, индексы и представления.	9	15
ca457d41-474f-425b-b52c-1d74751f00d0	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	Запуск и окружение	\N	0	1
de23741e-cedb-4a46-b0fc-f89d498082e8	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	Работа с данными	\N	1	2
78cd78a6-0f85-4727-ad68-9c0c48a96006	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	Выражения и функции	\N	2	3
720171ae-9ba0-4777-a9e1-8d53f6881e54	838f794f-2700-49ed-86f3-6f2a4ddbf5e0	Расширенные возможности	\N	3	4
1d3e6738-fbfa-481c-a347-e7c868aa4cf2	f21476f6-df52-474c-88ca-b20c8e79eb71	Как работает планировщик	\N	0	1
d3ec801e-8b74-43f2-bf41-8dfcb9b85b86	f21476f6-df52-474c-88ca-b20c8e79eb71	Виды индексов	\N	1	2
052a6e65-41b9-4fcb-adcd-964ca39508b5	f21476f6-df52-474c-88ca-b20c8e79eb71	Оптимизация запросов	\N	2	3
b6ca775f-7a9c-455c-8099-49f8fc187f96	f21476f6-df52-474c-88ca-b20c8e79eb71	Производительность на практике	\N	3	4
b951683f-55d5-4b76-8e75-152bcbd2419a	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	Зачем нормализовать	\N	0	1
0bb51c3a-f221-44a4-911f-d07bb32e53a7	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	Нормальные формы	\N	1	2
ec8b8164-455f-4903-87be-0522e01d7663	1cb6b85b-ecfb-45b6-99bc-286ff90bc0c6	Баланс и практика	\N	2	3
4f7c50f2-af4f-453a-927c-034623a2f694	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	Основы оконных функций	\N	0	1
04815cf9-0c0a-4b20-b3d6-9ff860f7e2c3	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	Виды функций	\N	1	2
bd1d6e65-392c-47e4-8fd1-045217c779db	9320eb85-1c9e-42ef-8863-a4de7d4e38d8	Рамки и практика	\N	2	3
8da79b56-5f63-4c57-8cc6-80999f553fb5	9e37f28b-b379-49b9-9aa2-d90d8a801c04	Основы проектирования	\N	0	1
a967fcbe-701f-4fc0-92f1-1b649a31f713	9e37f28b-b379-49b9-9aa2-d90d8a801c04	От модели к схеме	\N	1	2
aabba830-2e2f-4803-81db-816ed5e40415	9e37f28b-b379-49b9-9aa2-d90d8a801c04	Целостность и практика	\N	2	3
6ba31548-cc5b-4aa0-8e9a-712eb3b40e47	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	Основы транзакций	\N	0	1
f387a0d1-8bc0-4865-b0db-cc0e316c5d2c	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	Изоляция	\N	1	2
a91b48e1-85e5-49d2-968a-0ae47a581a36	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	Блокировки	\N	2	3
0d61ac1b-37ee-4150-bf3d-f862cd47d50e	f96f77bb-8a04-469b-82b3-9ad4fb5e6bcb	Надёжность на практике	\N	3	4
13b76285-eb0b-4105-843e-f6aaaceceda5	758a89c8-4b2a-44c5-9156-200aaa59fcbe	Первые запросы	\N	0	1
cc106b14-5e26-4e65-8c79-6e40ee1bb56e	758a89c8-4b2a-44c5-9156-200aaa59fcbe	Сортировка и группировка	\N	1	2
5ddec0ed-61e9-43a4-b0d5-4e605c6e35fa	758a89c8-4b2a-44c5-9156-200aaa59fcbe	Соединение таблиц	\N	2	3
6e25b2e3-aaee-4e08-aed9-3bcc74cf67f6	758a89c8-4b2a-44c5-9156-200aaa59fcbe	Продвинутое и практика	\N	3	4
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.questions (id, test_id, text, type, points, order_index) FROM stdin;
0ba00000-0000-0000-0000-000000000001	0fa00000-0000-0000-0000-000000000001	Что такое база данных?	single	1	1
0ba00000-0000-0000-0000-000000000002	0fa00000-0000-0000-0000-000000000001	Как называется одна запись в таблице?	single	1	2
0ba00000-0000-0000-0000-000000000004	0fa00000-0000-0000-0000-000000000002	Что делает первичный ключ?	single	1	1
0ba00000-0000-0000-0000-000000000005	0fa00000-0000-0000-0000-000000000002	Внешний ключ нужен для того, чтобы...	single	1	2
53ef5e70-13b4-4d11-b3f2-5e93445832eb	0f000000-0000-0000-0000-000000000002	Что такое строка (запись) в таблице?	single	1	1
c2cfb6a1-8bda-4653-9c2a-9c4a28802e66	0f000000-0000-0000-0000-000000000002	Зачем столбцу нужен тип данных?	single	1	2
56f2fed4-1b45-4db8-814d-2e8c200cb3f3	0f000000-0000-0000-0000-000000000002	Чем таблица базы данных надёжнее обычного листа Excel?	single	1	3
b44e3951-8ee3-4f7d-96ec-0fe60858a652	0f000000-0000-0000-0000-000000000003	Что такое сущность?	single	1	1
db1b41f5-35dd-47bd-86e8-121d317af45f	0f000000-0000-0000-0000-000000000003	Атрибут — это…	single	1	2
42a753ac-23e7-484a-b3b4-5c02c03fe1d6	0f000000-0000-0000-0000-000000000003	Как удобно находить сущности в описании задачи?	single	1	3
3d3a4faa-5610-44a3-b4d3-8216979fbd35	0f000000-0000-0000-0000-000000000005	Какая команда создаёт таблицу в SQL?	single	1	1
90c909b8-fcad-44a9-96d7-836edc53316b	0f000000-0000-0000-0000-000000000005	Что делает ограничение NOT NULL?	single	1	2
8dbef985-44c0-4edd-bdfa-0804b2326f4e	0f000000-0000-0000-0000-000000000005	Что означает PRIMARY KEY у столбца?	single	1	3
13c0a935-26f8-4852-a072-bdb28bc7fa10	0f000000-0000-0000-0000-000000000006	Какая команда читает (выбирает) данные из таблицы?	single	1	1
ff192d35-dd59-4b66-9174-9c6583303086	0f000000-0000-0000-0000-000000000006	Что вернёт запрос SELECT * FROM students;?	single	1	2
c39985e7-39de-4642-adb4-85e537180625	0f000000-0000-0000-0000-000000000006	Для чего нужно условие WHERE?	single	1	3
0ba00000-0000-0000-0000-000000000003	0fa00000-0000-0000-0000-000000000001	Что из перечисленного — пример базы данных в образовании?	single	2	3
2f587621-79fd-454a-8024-8707d781a4c1	0f000000-0000-0000-0000-000000000007	Для чего нужно условие WHERE?	single	1	1
f09ee98f-8cc6-4b24-bd38-5935d0708a48	0f000000-0000-0000-0000-000000000007	Как в SQL правильно записать текстовое значение в условии?	single	1	2
5d13e0bb-d1f1-47be-aeb8-69579afda898	0f000000-0000-0000-0000-000000000007	Что вернёт условие WHERE xp >= 60 AND group_name = 'Б-101'?	single	1	3
05ec09c4-7d1c-4ebb-9222-6ffa64f55bff	0f000000-0000-0000-0000-000000000007	Какой оператор проверяет вхождение значения в список?	single	1	4
93cb2db4-7ba0-4a60-8d92-2a2d18cd691b	0f000000-0000-0000-0000-000000000007	Как корректно проверить, что значение в столбце отсутствует (пустое)?	single	1	5
906743ba-69ce-4c97-9f9a-b547a0812e61	0f000000-0000-0000-0000-000000000008	Что делает ORDER BY xp DESC?	single	1	1
55fb5f8c-e0c3-4359-b946-f3de1f352c20	0f000000-0000-0000-0000-000000000008	Для чего нужен LIMIT?	single	1	2
6ca5ee17-2595-47c7-8ef1-928f96f8b696	0f000000-0000-0000-0000-000000000008	Как получить тройку студентов с наибольшим баллом?	single	1	3
3f3b4a1a-af3f-43ba-952a-bb156a125068	0f000000-0000-0000-0000-000000000008	Что делает DISTINCT в SELECT DISTINCT group_name?	single	1	4
de50745d-f109-4874-93c8-08b1fa8cfdd9	0f000000-0000-0000-0000-000000000008	В каком порядке должны идти части запроса?	single	1	5
d2cdde62-eb4f-4303-8e54-70a34e4508f0	0f000000-0000-0000-0000-000000000009	Какая команда добавляет новые строки в таблицу?	single	1	1
1f4fff6f-347c-45bc-bb7b-2efdb318138c	0f000000-0000-0000-0000-000000000009	Почему полезно явно перечислять столбцы в INSERT?	single	1	2
8b0caabb-904d-4f46-ba08-965a5a149aa3	0f000000-0000-0000-0000-000000000009	Как добавить несколько строк одной командой?	single	1	3
0d4b2b99-b0d1-41be-a512-8c4652b5f9e9	0f000000-0000-0000-0000-000000000009	Если у столбца id задан DEFAULT (автонумерация), то в INSERT его...	single	1	4
a4261771-7e74-4c1c-99c4-79ab04cd7591	0f000000-0000-0000-0000-000000000009	Что делает RETURNING id в команде INSERT?	single	1	5
a070ca37-90c9-43d5-ad24-22ad083448c4	0f000000-0000-0000-0000-00000000000a	Какая команда изменяет значения в существующих строках?	single	1	1
e239c29f-fd06-4ca6-b894-98d81b15f9e7	0f000000-0000-0000-0000-00000000000a	Что произойдёт, если в UPDATE забыть условие WHERE?	single	1	2
5b2c2fad-ed08-4d6b-8081-94c1e42ba363	0f000000-0000-0000-0000-00000000000a	Что делает запрос: UPDATE students SET xp = xp + 10 WHERE id = 5?	single	1	3
d47d5bde-a499-4c73-93b6-c9dfec6c5b58	0f000000-0000-0000-0000-00000000000a	Что разумно сделать перед удалением строк командой DELETE?	single	1	4
a8373ce9-7321-4c08-abbe-edc464b45e41	0f000000-0000-0000-0000-00000000000a	Для чего нужны транзакции (BEGIN ... COMMIT/ROLLBACK)?	single	1	5
411968e1-2e18-40f4-90fb-e1f3bee1d16b	0f000000-0000-0000-0000-00000000000b	Что делает функция AVG(xp)?	single	1	1
8fe277ac-2405-4bbe-b58b-a2d427c5d0df	0f000000-0000-0000-0000-00000000000b	Чем COUNT(*) отличается от COUNT(столбец)?	single	1	2
41920440-682d-4da1-8adc-b2a54f245706	0f000000-0000-0000-0000-00000000000b	Что вернёт COUNT(DISTINCT group_name)?	single	1	3
30394892-b435-4ff9-9b5f-328e10817a63	0f000000-0000-0000-0000-00000000000b	Зачем в запросе используют AS (например, AVG(xp) AS средний_балл)?	single	1	4
e6d347cc-2ddb-4b6c-8c8f-b005660ea176	0f000000-0000-0000-0000-00000000000b	Сколько строк обычно возвращает SELECT AVG(xp) FROM students; (без группировки)?	single	1	5
38407d26-9f17-4dbf-88ed-83daca46f8c7	0f000000-0000-0000-0000-00000000000c	Что делает GROUP BY group_name?	single	1	1
cbfbacdb-2e37-417b-83f8-f471a17d2945	0f000000-0000-0000-0000-00000000000c	Какие столбцы можно выводить в SELECT при группировке по group_name?	single	1	2
6e58dec4-f01b-4dbd-b312-a4cff7758276	0f000000-0000-0000-0000-00000000000c	Чем HAVING отличается от WHERE?	single	1	3
d54a7e5a-8791-45c3-9043-648f5493703a	0f000000-0000-0000-0000-00000000000c	Что вернёт: GROUP BY group_name HAVING AVG(xp) < 50?	single	1	4
27e9581c-bfd4-4bbf-9ca2-edf66eb9b944	0f000000-0000-0000-0000-00000000000c	В каком порядке выполняются части запроса?	single	1	5
8143f4cb-b1f6-44f2-80f2-7affc223d8ec	0f000000-0000-0000-0000-00000000000d	Зачем нужна команда JOIN?	single	1	1
54b440d7-9115-407c-9d88-91291e5f6371	0f000000-0000-0000-0000-00000000000d	Что оставляет в результате INNER JOIN?	single	1	2
3a9d1967-27f3-48d6-a485-43b63d3915b8	0f000000-0000-0000-0000-00000000000d	Что записывают в условии ON при соединении students и grades?	single	1	3
828140f3-b07e-4941-bf59-03eff42b11e3	0f000000-0000-0000-0000-00000000000d	Зачем таблицам дают псевдонимы (students s, grades g)?	single	1	4
d1e62523-810b-4577-b4ae-89fdca1d9d01	0f000000-0000-0000-0000-00000000000d	Если у студента Вики нет ни одной оценки, попадёт ли она в результат INNER JOIN со grades?	single	1	5
40e6c47f-5fbe-4ad3-8446-6d2a289cdc34	0f000000-0000-0000-0000-00000000000e	Что делает LEFT JOIN?	single	1	1
635c7305-f0f9-4852-a7ea-199f0e09adfb	0f000000-0000-0000-0000-00000000000e	Чем заполнятся поля правой таблицы, если пары не нашлось?	single	1	2
593fa247-4127-4274-817b-b92db3f368fb	0f000000-0000-0000-0000-00000000000e	Как найти студентов, у которых вообще нет оценок?	single	1	3
f96be62a-fa21-4ce0-b527-0e16798654c9	0f000000-0000-0000-0000-00000000000e	Какое соединение сохраняет строки обеих таблиц, даже без пары?	single	1	4
fba5ca96-cf9f-4358-85f7-f81b60ac7f8e	0f000000-0000-0000-0000-00000000000e	Когда уместнее INNER JOIN, а не LEFT JOIN?	single	1	5
4ec9a30e-b191-4a48-847a-fa8aad000416	0f000000-0000-0000-0000-00000000000f	Что такое нормализация?	single	1	1
0201f609-7035-4379-8421-2fb22e54c165	0f000000-0000-0000-0000-00000000000f	Что нарушает первую нормальную форму (1НФ)?	single	1	2
c3881aa8-41b0-4988-90c3-e5e4490e8884	0f000000-0000-0000-0000-00000000000f	Что такое аномалия обновления?	single	1	3
2ac33c62-2141-44a4-8e2d-51d4651df661	0f000000-0000-0000-0000-00000000000f	Почему избыточность (дублирование данных) — это плохо?	single	1	4
4374d4d0-5378-4fc3-9747-19903d4edb11	0f000000-0000-0000-0000-00000000000f	Что значит «атомарное значение» в ячейке?	single	1	5
ecbb9e8c-3775-49bd-8450-456725f26934	0f000000-0000-0000-0000-000000000010	Когда становится важна вторая нормальная форма (2НФ)?	single	1	1
fae4743d-b137-4122-b867-6b7d20b1a762	0f000000-0000-0000-0000-000000000010	Что устраняет третья нормальная форма (3НФ)?	single	1	2
9fd151d7-9afd-486a-8833-df32634a60d9	0f000000-0000-0000-0000-000000000010	Куратор группы повторяется у каждого студента группы. Как это исправить по 3НФ?	single	1	3
b8656a4b-aadb-4109-b473-35a6d895ba8b	0f000000-0000-0000-0000-000000000010	Главная выгода нормализованной базы:	single	1	4
de0187e9-f36d-4a11-8f05-dc679a7afab1	0f000000-0000-0000-0000-000000000010	Что такое денормализация?	single	1	5
c825b791-73ad-440d-b906-e0a969c250c9	0f000000-0000-0000-0000-000000000011	Что гарантирует ограничение PRIMARY KEY?	single	1	1
abedd9bf-4174-42a1-a242-014995d2f7aa	0f000000-0000-0000-0000-000000000011	Что делает ограничение NOT NULL?	single	1	2
7ffc08ac-6d90-447b-98d3-3e7a36bb3ba6	0f000000-0000-0000-0000-000000000011	Для чего нужен внешний ключ (FOREIGN KEY)?	single	1	3
52a765d7-07f7-4a86-950a-19eac1bca3a7	0f000000-0000-0000-0000-000000000011	Что задаёт ON DELETE CASCADE для внешнего ключа?	single	1	4
87b7c455-7b1a-42ff-8d59-c4613cc9d5cc	0f000000-0000-0000-0000-000000000011	Почему правила целостности лучше задавать в самой базе, а не только в программе?	single	1	5
fc56d41d-e7d6-45c2-8fb4-98c69163a111	0f000000-0000-0000-0000-000000000012	Что такое индекс в базе данных?	single	1	1
37074ade-642b-4419-98db-f2e6101082db	0f000000-0000-0000-0000-000000000012	Для каких столбцов индекс особенно полезен?	single	1	2
6c924639-70a8-4bdb-807d-682912f4bd3e	0f000000-0000-0000-0000-000000000012	В чём «цена» индекса?	single	1	3
4a86e893-9cb9-41b4-9f7b-96f35cc2e9d4	0f000000-0000-0000-0000-000000000012	Что такое представление (VIEW)?	single	1	4
b676a51d-0432-4000-933d-b4283d286b51	0f000000-0000-0000-0000-000000000012	Хранит ли обычное представление (VIEW) собственные данные?	single	1	5
6c206b42-d436-4937-92e8-428266117a87	330d453f-8fcb-4579-b941-5e35d1ac5a35	В таблице 30 студентов из 3 групп. Сколько строк вернёт SELECT group_name FROM students?	single	1	0
7c5df4cd-b1c1-4fb8-b1b9-a69abb7a98e1	330d453f-8fcb-4579-b941-5e35d1ac5a35	Что произойдёт, если указать в SELECT столбец, которого нет в таблице?	single	1	1
2021684f-ec30-4b62-b24c-b62c0c45d351	330d453f-8fcb-4579-b941-5e35d1ac5a35	Как убрать из результата повторяющиеся значения группы?	single	1	2
274978a3-7443-4516-98b8-a81a1df46b38	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	У 5 из 30 студентов балл не выставлен. Сколько строк вернёт WHERE avg_grade IS NULL?	single	1	0
3828b5ec-f126-4eae-bdf8-d159c446f1a9	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	Почему условие WHERE avg_grade = NULL не находит пустые значения?	single	1	1
79129577-4bb9-407a-b75f-59182dfff0ef	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	Что вернёт условие WHERE group_name = 'П-101' OR avg_grade > 4?	single	1	2
57085e9e-1172-41dd-b553-1b9ede0f45c5	9ae38d39-0a6e-47a8-929f-60e48f7311c9	Чем COUNT(avg_grade) отличается от COUNT(*)?	single	1	0
8d905a71-a150-4a3d-ae83-dd6619fbf1fb	9ae38d39-0a6e-47a8-929f-60e48f7311c9	Что вернёт SELECT AVG(avg_grade) FROM students без GROUP BY?	single	1	1
281cbfde-fc59-417c-a26c-a26750c9ffc7	9ae38d39-0a6e-47a8-929f-60e48f7311c9	Как отсортировать студентов по баллу от большего к меньшему?	single	1	2
21570212-319a-42d0-a88d-8ef3e848c9a3	6b604fc2-d9b2-4091-90f2-ac047f9f794d	Сколько первичных ключей может быть у одной таблицы?	single	1	0
d4a3ab54-5c0c-4cc9-9986-13501cfcef5f	6b604fc2-d9b2-4091-90f2-ac047f9f794d	Как в реляционной БД реализуют связь «многие-ко-многим»?	single	1	1
5462fb3b-8c5d-4c6e-abcc-c231a2d0ccc8	6b604fc2-d9b2-4091-90f2-ac047f9f794d	Что обеспечивает внешний ключ (FOREIGN KEY)?	single	1	2
bf58f4fa-11a2-4890-8282-de57b6886991	6b604fc2-d9b2-4091-90f2-ac047f9f794d	Связь «одна группа — много студентов» (1:М) реализуется как:	single	1	3
73961e85-87a7-4e52-9471-a91b87d56b97	6b604fc2-d9b2-4091-90f2-ac047f9f794d	Почему чаще берут суррогатный ключ (serial/UUID), а не естественный?	single	1	4
b19b875e-34ef-4803-b1e6-e8830b2216ca	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	Что в первую очередь устраняет нормализация?	single	1	0
72ef060a-ef88-48ea-9aea-eb85c3b0db1e	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	Список значений в одной ячейке — это нарушение:	single	1	1
3faa7ed1-20e7-4584-b567-de45a858e0a6	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	Частичная зависимость от части составного ключа нарушает:	single	1	2
22ddc903-87d8-4ef0-b50d-13815b3a9fea	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	Транзитивная зависимость «студент → группа → куратор» нарушает:	single	1	3
bd79a2c5-fa6b-4d76-94e3-6d35ff23f557	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	Денормализацию применяют, чтобы:	single	1	4
8830c3fa-2dfe-42a7-894c-a57cc1e88598	a47b8287-9a6e-4dd1-a150-e67096053cfb	Что гарантирует свойство атомарности (Atomicity)?	single	1	0
1467d970-0d52-4d24-bc46-5a304049b5bf	a47b8287-9a6e-4dd1-a150-e67096053cfb	Какой уровень изоляции в PostgreSQL используется по умолчанию?	single	1	1
4fb1ed42-6579-448c-80a9-80d60efa9b55	a47b8287-9a6e-4dd1-a150-e67096053cfb	Что даёт MVCC в PostgreSQL?	single	1	2
9bdc19f8-b247-4cb9-b942-9e4a57b6351f	a47b8287-9a6e-4dd1-a150-e67096053cfb	Что делает PostgreSQL при взаимоблокировке (deadlock)?	single	1	3
b45f71fc-f02a-436c-ad77-c9aff83da125	a47b8287-9a6e-4dd1-a150-e67096053cfb	Как оптимистичная блокировка обнаруживает конфликт?	single	1	4
0385aa1d-9eca-437f-b7d9-7e2ab3293ddd	9e8d13a1-a6eb-4646-bcf0-766022bd8189	Как наличие индекса влияет на операции записи (INSERT/UPDATE/DELETE)?	single	1	0
b06828c8-31f6-4bac-9430-f369e5f104a4	9e8d13a1-a6eb-4646-bcf0-766022bd8189	Какая команда показывает реальное время выполнения запроса?	single	1	1
e217a42d-636d-45bc-92ed-addcc56b4db7	9e8d13a1-a6eb-4646-bcf0-766022bd8189	Для какого условия обычный B-tree индекс бесполезен?	single	1	2
3b23312f-f34f-41c5-bf90-4cab5989c8af	9e8d13a1-a6eb-4646-bcf0-766022bd8189	Для каких запросов эффективен составной индекс (group_id, avg_grade)?	single	1	3
ec3fcb95-9e6a-497a-ab8c-a2fc2af0253e	9e8d13a1-a6eb-4646-bcf0-766022bd8189	Зачем нужна команда ANALYZE?	single	1	4
094ffddf-f429-4b8c-90e8-cd88d4789eb0	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	Какая служебная команда psql покажет список таблиц текущей базы?	single	1	0
03afd3fa-fa28-4953-bff2-cf59386cbc97	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	Какой тип выбрать для точного хранения оценки вроде 4.5?	single	1	1
3144f678-6efa-4037-a089-53a6484cae43	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	Что вернёт COALESCE(avg_grade, 0)?	single	1	2
1299e0dd-b153-46a1-8a32-8ec70877a4c6	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	Чем VIEW отличается от обычной таблицы?	single	1	3
f014541c-9b76-4e6b-bd30-814fb530e34f	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	Зачем нужна конструкция WITH (CTE)?	single	1	4
1d71b18a-562a-42ed-97d2-b0f515ed8b30	f3057118-3a60-49bf-ab23-b15fdde27457	Чем оконная функция отличается от агрегата с GROUP BY?	single	1	0
0f06a907-24b1-4b9b-8ba8-15b79786445a	f3057118-3a60-49bf-ab23-b15fdde27457	Что делает PARTITION BY внутри OVER()?	single	1	1
65d6850b-f3f0-45c2-a4e0-d7a37b3ab478	f3057118-3a60-49bf-ab23-b15fdde27457	Чем RANK() отличается от DENSE_RANK() при равных значениях?	single	1	2
7f6f4fde-693d-4977-b2fb-fed71c2d3dda	f3057118-3a60-49bf-ab23-b15fdde27457	Что вернёт LAG(avg_grade) для самой первой строки окна?	single	1	3
24a18078-b33b-41fe-a689-cfa05324c386	f3057118-3a60-49bf-ab23-b15fdde27457	Что даёт SUM(x) OVER (ORDER BY t) — агрегат с ORDER BY в окне?	single	1	4
\.


--
-- Data for Name: reflections; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reflections (id, user_id, lesson_id, clarity_rating, difficulty_rating, comment, created_at) FROM stdin;
028faa4c-8159-426b-b9b1-1ba7b683f3bc	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000001	5	2	Всё понятно, примеры из журнала помогли.	2025-09-05 18:32:00+03
8c780c70-1396-4fc4-90a5-34969b846fbf	0a000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000001	4	3	В целом ясно.	2025-09-06 12:29:00+03
93b20a2b-22b5-4fd6-9cbb-68f59bf8f3de	0a000000-0000-0000-0000-000000000004	0e000000-0000-0000-0000-000000000001	2	4	Сложновато, нужно больше примеров.	2025-09-07 11:25:00+03
f48b86e5-96bd-4b2d-a8ef-832a0c26d3d6	0a000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000004	4	3	Связи поняла, ключи чуть труднее.	2025-09-22 18:42:00+03
f80018ea-5854-49c7-b31f-16be4ac1e2c9	0a000000-0000-0000-0000-000000000005	0e000000-0000-0000-0000-000000000001	5	5	Все супер!	2026-06-09 16:11:44.683+03
4e686dff-2925-4625-94a9-2d9ecc74a807	0a000000-0000-0000-0000-000000000001	0e000000-0000-0000-0000-000000000001	5	1	\N	2026-06-10 16:42:31.515+03
a2bc0811-d51b-4564-befd-3bd501fea34e	0a000000-0000-0000-0000-000000000002	656a356d-8ad7-4bb5-b5b5-3597d30936f8	5	2	\N	2026-06-03 07:21:59.282+03
05af2964-7dea-4c1a-8fca-89f55e3254a0	0a000000-0000-0000-0000-000000000003	656a356d-8ad7-4bb5-b5b5-3597d30936f8	5	1	\N	2026-06-04 07:21:59.284+03
75188c8b-5ad8-4cd2-9dbe-c3c5bf690e44	0a000000-0000-0000-0000-000000000004	656a356d-8ad7-4bb5-b5b5-3597d30936f8	4	2	\N	2026-06-05 07:21:59.284+03
eab9323e-0b78-4db6-b878-c51509138a6f	0a000000-0000-0000-0000-000000000005	656a356d-8ad7-4bb5-b5b5-3597d30936f8	5	2	\N	2026-06-06 07:21:59.285+03
b8cd1269-eb0d-4c82-a709-54b938123959	0a000000-0000-0000-0000-000000000010	656a356d-8ad7-4bb5-b5b5-3597d30936f8	4	3	\N	2026-06-07 07:21:59.285+03
14c09595-d544-4232-9456-98908e275381	0a000000-0000-0000-0000-000000000011	656a356d-8ad7-4bb5-b5b5-3597d30936f8	5	2	\N	2026-06-08 07:21:59.286+03
fa212471-f01a-4920-a8bd-a24e4ef60d4e	0a000000-0000-0000-0000-000000000002	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	4	3	\N	2026-06-03 07:21:59.286+03
7377c3b3-867b-4a15-a2b0-2788c9f55430	0a000000-0000-0000-0000-000000000003	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	3	4	\N	2026-06-04 07:21:59.287+03
2aafbd82-90a8-4efd-9874-7777eecd1cc5	0a000000-0000-0000-0000-000000000004	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	4	3	\N	2026-06-05 07:21:59.287+03
c46eccf2-4ae2-4f88-8833-63bb9aa537bc	0a000000-0000-0000-0000-000000000005	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	4	3	\N	2026-06-06 07:21:59.287+03
fb92d3d2-6b1c-4247-b4d3-dc2ee41d731a	0a000000-0000-0000-0000-000000000010	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	3	4	\N	2026-06-07 07:21:59.288+03
884257e2-65c9-48b7-97d3-3ae6fbd9878a	0a000000-0000-0000-0000-000000000002	216f012b-02e7-49c4-81e1-08e8a9af6dcd	3	4	\N	2026-06-03 07:21:59.288+03
677327bc-cd80-4e9b-b689-f90a3c68af6e	0a000000-0000-0000-0000-000000000003	216f012b-02e7-49c4-81e1-08e8a9af6dcd	3	4	\N	2026-06-04 07:21:59.289+03
12a6bb23-1e53-4a5d-8e6e-16f51b4f522c	0a000000-0000-0000-0000-000000000004	216f012b-02e7-49c4-81e1-08e8a9af6dcd	2	5	\N	2026-06-05 07:21:59.289+03
49e1ed7e-8bd9-4843-811d-0cb78ea25fcd	0a000000-0000-0000-0000-000000000005	216f012b-02e7-49c4-81e1-08e8a9af6dcd	4	3	\N	2026-06-06 07:21:59.29+03
803d6ac1-9656-47f5-bddd-7f73bb08163c	0a000000-0000-0000-0000-000000000010	216f012b-02e7-49c4-81e1-08e8a9af6dcd	3	4	\N	2026-06-07 07:21:59.29+03
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (id, code, name, description) FROM stdin;
481e965b-f5bf-4689-a7f5-836edf9adfd1	student	Студент	Проходит курс, выполняет задания и тесты
b2ea6708-47d9-4c87-bd35-90a3c8c89444	teacher	Преподаватель	Создаёт контент, проверяет работы, видит аналитику
49b27c2a-4b82-458f-9dac-03ec55bf3f37	admin	Администратор	Управляет платформой и пользователями
\.


--
-- Data for Name: submissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.submissions (id, assignment_id, user_id, sql_query, file_url, text_answer, score, feedback, status, graded_by, submitted_at, graded_at) FROM stdin;
6f5b3a36-fc00-42c4-b84a-c60ffc8d3475	0aa00000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000002	CREATE TABLE students (id serial PRIMARY KEY, full_name text, group_name text);	\N	\N	100.00	Отлично, всё верно.	graded	0a000000-0000-0000-0000-000000000001	2025-10-14 19:00:00+03	2025-10-15 10:00:00+03
e11f4abf-d697-4ecb-956f-d03cc48dca1c	0aa00000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000003	CREATE TABLE students (id int, full_name text);	\N	\N	80.00	Не хватает первичного ключа и группы.	graded	0a000000-0000-0000-0000-000000000001	2025-10-15 16:00:00+03	2025-10-16 09:30:00+03
1d458b5f-c68b-4b1f-a66e-817dbd4f88c7	0aa00000-0000-0000-0000-000000000002	0a000000-0000-0000-0000-000000000002	SELECT * FROM students;	\N	\N	95.00	Верно.	graded	0a000000-0000-0000-0000-000000000001	2025-10-16 19:00:00+03	2025-10-17 11:00:00+03
5032ee87-b7b5-46b4-a973-2e9d5d81c272	0aa00000-0000-0000-0000-000000000003	0a000000-0000-0000-0000-000000000010	\N	\N	\N	100.00	\N	graded	0a000000-0000-0000-0000-000000000001	2026-06-11 12:26:06.51+03	2026-06-11 12:26:06.509+03
4caa8e61-478e-4165-8f0d-b4b83d71b3b1	0aa00000-0000-0000-0000-000000000002	0a000000-0000-0000-0000-000000000005	select * from students;	\N	\N	100.00	Результат совпадает с эталоном (5 строк).	graded	\N	2026-06-10 09:14:21.504+03	2026-06-18 22:01:35.983+03
f5c196ed-32b7-4f30-8b2d-af8c390cde43	0aa00000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000004	CREATE TABLE students (id int);	\N	\N	\N	\N	submitted	\N	2025-10-05 12:00:00+03	\N
\.


--
-- Data for Name: test_attempts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.test_attempts (id, user_id, test_id, score, is_passed, started_at, finished_at) FROM stdin;
0fb00000-0000-0000-0000-000000000001	0a000000-0000-0000-0000-000000000002	0fa00000-0000-0000-0000-000000000001	90.00	t	2025-09-05 18:32:00+03	2025-09-05 18:40:00+03
0fb00000-0000-0000-0000-000000000002	0a000000-0000-0000-0000-000000000003	0fa00000-0000-0000-0000-000000000001	70.00	t	2025-09-06 12:30:00+03	2025-09-06 12:39:00+03
0fb00000-0000-0000-0000-000000000003	0a000000-0000-0000-0000-000000000004	0fa00000-0000-0000-0000-000000000001	40.00	f	2025-09-07 11:25:00+03	2025-09-07 11:35:00+03
0fb00000-0000-0000-0000-000000000004	0a000000-0000-0000-0000-000000000002	0fa00000-0000-0000-0000-000000000002	85.00	t	2025-09-22 18:42:00+03	2025-09-22 18:50:00+03
0fb00000-0000-0000-0000-000000000005	0a000000-0000-0000-0000-000000000003	0fa00000-0000-0000-0000-000000000002	55.00	f	2025-10-01 13:00:00+03	2025-10-01 13:09:00+03
1ab4905d-5140-4d01-8660-2714849536c7	0a000000-0000-0000-0000-000000000005	0fa00000-0000-0000-0000-000000000001	100.00	t	2026-06-09 11:41:02.262+03	2026-06-09 11:41:02.257+03
66ab8adf-963b-4912-951c-e3731fedfe5d	0a000000-0000-0000-0000-000000000005	0fa00000-0000-0000-0000-000000000001	100.00	t	2026-06-09 11:46:51.94+03	2026-06-09 11:46:51.94+03
34f7cfe2-3a34-4042-ad88-c1d8a84d1f5a	0a000000-0000-0000-0000-000000000010	0fa00000-0000-0000-0000-000000000001	96.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
1b1c9d60-1680-4cc4-aefb-951aeed2d017	0a000000-0000-0000-0000-000000000011	0fa00000-0000-0000-0000-000000000001	88.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
82a791e1-4bad-43bf-9bec-a57f5d07b432	0a000000-0000-0000-0000-000000000012	0fa00000-0000-0000-0000-000000000001	92.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
0af90410-2b9a-46f2-853a-b20584ce2aed	0a000000-0000-0000-0000-000000000013	0fa00000-0000-0000-0000-000000000001	80.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
8babdbfc-e44c-47a8-8990-ed1c2e00702d	0a000000-0000-0000-0000-000000000014	0fa00000-0000-0000-0000-000000000001	70.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
66fa2a36-7460-40a0-872f-3fd088617384	0a000000-0000-0000-0000-000000000015	0fa00000-0000-0000-0000-000000000001	65.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
9f3817b3-de66-449e-b801-86aae27672f3	0a000000-0000-0000-0000-000000000016	0fa00000-0000-0000-0000-000000000001	72.00	t	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
4d0ee30a-0003-48f5-98ba-2b6010cb6b06	0a000000-0000-0000-0000-000000000017	0fa00000-0000-0000-0000-000000000001	55.00	f	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
b724c89e-84e7-4dda-b39d-7f9908df5a12	0a000000-0000-0000-0000-000000000018	0fa00000-0000-0000-0000-000000000001	45.00	f	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
da0fe154-8895-4ca5-8cb5-a334a13a7c3e	0a000000-0000-0000-0000-00000000001a	0fa00000-0000-0000-0000-000000000001	38.00	f	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
9dbf2370-a78f-4853-ac04-b24aada01883	0a000000-0000-0000-0000-00000000001b	0fa00000-0000-0000-0000-000000000001	40.00	f	2026-06-09 23:23:49.263196+03	2026-06-09 23:23:49.263196+03
0681590e-e373-4756-8ac2-fdb4002acda8	0a000000-0000-0000-0000-000000000010	0f000000-0000-0000-0000-00000000000b	90.00	t	2026-06-09 23:48:37.152473+03	2026-06-03 23:48:37.152473+03
7fd0f45d-83bd-4595-a4ff-b4dda8e50edb	0a000000-0000-0000-0000-000000000010	0f000000-0000-0000-0000-000000000007	95.00	t	2026-06-09 23:48:37.152473+03	2026-06-03 23:48:37.152473+03
7551cef6-9a1f-447d-ad15-20150b3efc28	0a000000-0000-0000-0000-000000000011	0f000000-0000-0000-0000-000000000007	76.00	t	2026-06-09 23:48:37.152473+03	2026-06-03 23:48:37.152473+03
850b60e0-0b10-45d8-89ac-c0cd1ae1359d	0a000000-0000-0000-0000-000000000012	0f000000-0000-0000-0000-000000000007	91.00	t	2026-06-09 23:48:37.152473+03	2026-06-03 23:48:37.152473+03
08ff4037-7b1d-4d53-850a-3bc820e528ce	0a000000-0000-0000-0000-000000000002	0f000000-0000-0000-0000-00000000000b	82.00	t	2026-06-09 23:48:37.152473+03	2026-06-03 23:48:37.152473+03
4311949e-b4b1-4458-a709-7d83cf183942	0a000000-0000-0000-0000-000000000002	0f000000-0000-0000-0000-000000000007	88.00	t	2026-06-09 23:48:37.152473+03	2026-06-03 23:48:37.152473+03
d581ccb3-6f92-4fad-a8f1-35f87215e8e3	0a000000-0000-0000-0000-000000000002	6b604fc2-d9b2-4091-90f2-ac047f9f794d	40.00	f	2026-06-07 16:30:10.662+03	2026-06-07 16:30:10.662+03
bfea2af4-fd2e-40ce-83de-d649c6103e8f	0a000000-0000-0000-0000-000000000003	6b604fc2-d9b2-4091-90f2-ac047f9f794d	80.00	t	2026-06-08 16:30:10.688+03	2026-06-08 16:30:10.688+03
4c5e6452-8f32-4a12-8146-fb734f8b021c	0a000000-0000-0000-0000-000000000004	6b604fc2-d9b2-4091-90f2-ac047f9f794d	60.00	t	2026-06-09 16:30:10.692+03	2026-06-09 16:30:10.692+03
496db3f9-e66d-438f-91cd-f9d157af1d91	0a000000-0000-0000-0000-000000000005	6b604fc2-d9b2-4091-90f2-ac047f9f794d	40.00	f	2026-06-10 16:30:10.696+03	2026-06-10 16:30:10.696+03
f68e9838-1d4a-43b9-90ad-feef347483a0	0a000000-0000-0000-0000-000000000010	6b604fc2-d9b2-4091-90f2-ac047f9f794d	60.00	t	2026-06-11 16:30:10.7+03	2026-06-11 16:30:10.7+03
78828310-33f0-4114-b083-7f35b00e8aad	0a000000-0000-0000-0000-000000000011	6b604fc2-d9b2-4091-90f2-ac047f9f794d	60.00	t	2026-06-12 16:30:10.703+03	2026-06-12 16:30:10.703+03
019407f4-2317-464e-88e1-a329b4bd5429	0a000000-0000-0000-0000-000000000002	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	20.00	f	2026-06-07 16:30:10.722+03	2026-06-07 16:30:10.722+03
24befe89-4b98-41ef-8ebb-0bc7bea3d4d7	0a000000-0000-0000-0000-000000000003	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	0.00	f	2026-06-08 16:30:10.725+03	2026-06-08 16:30:10.725+03
86bb7325-6555-4f31-af51-3d9b8ac3b424	0a000000-0000-0000-0000-000000000004	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	60.00	t	2026-06-09 16:30:10.728+03	2026-06-09 16:30:10.728+03
5c49c681-b5e1-44a0-9aed-49e8315ff24e	0a000000-0000-0000-0000-000000000005	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	80.00	t	2026-06-10 16:30:10.731+03	2026-06-10 16:30:10.731+03
12cecddd-5572-4c35-8cf8-4e6d6b9564c8	0a000000-0000-0000-0000-000000000010	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	40.00	f	2026-06-11 16:30:10.735+03	2026-06-11 16:30:10.735+03
6b817e58-fdc5-415b-a181-4c9af823bfcd	0a000000-0000-0000-0000-000000000011	c24a5c67-01fe-4274-8b7d-d12325d9f4f5	40.00	f	2026-06-12 16:30:10.738+03	2026-06-12 16:30:10.738+03
1946718b-eb30-44f3-94f1-8b1072634175	0a000000-0000-0000-0000-000000000002	a47b8287-9a6e-4dd1-a150-e67096053cfb	40.00	f	2026-06-07 16:30:10.756+03	2026-06-07 16:30:10.756+03
eb4f667d-8efc-4299-977a-3290c6880410	0a000000-0000-0000-0000-000000000003	a47b8287-9a6e-4dd1-a150-e67096053cfb	0.00	f	2026-06-08 16:30:10.757+03	2026-06-08 16:30:10.757+03
dec6dd7e-1a61-47f0-bbee-6374ae2cbb41	0a000000-0000-0000-0000-000000000004	a47b8287-9a6e-4dd1-a150-e67096053cfb	40.00	f	2026-06-09 16:30:10.759+03	2026-06-09 16:30:10.759+03
f32d1267-a4e2-465d-9ded-7502737d2608	0a000000-0000-0000-0000-000000000005	a47b8287-9a6e-4dd1-a150-e67096053cfb	20.00	f	2026-06-10 16:30:10.762+03	2026-06-10 16:30:10.762+03
4f23ae45-5ec6-42f7-a5e7-be946f549f38	0a000000-0000-0000-0000-000000000010	a47b8287-9a6e-4dd1-a150-e67096053cfb	80.00	t	2026-06-11 16:30:10.764+03	2026-06-11 16:30:10.764+03
2893d822-6b5a-431a-ae04-23cab221f2ca	0a000000-0000-0000-0000-000000000011	a47b8287-9a6e-4dd1-a150-e67096053cfb	60.00	t	2026-06-12 16:30:10.767+03	2026-06-12 16:30:10.767+03
a0fa7c27-fed4-4377-b1c3-309e4e002f6a	0a000000-0000-0000-0000-000000000002	9e8d13a1-a6eb-4646-bcf0-766022bd8189	20.00	f	2026-06-07 16:30:10.782+03	2026-06-07 16:30:10.782+03
2ef4a297-0c55-4b7c-807d-75495b8df71d	0a000000-0000-0000-0000-000000000003	9e8d13a1-a6eb-4646-bcf0-766022bd8189	60.00	t	2026-06-08 16:30:10.785+03	2026-06-08 16:30:10.785+03
523842f2-b2eb-4e66-86b9-555c80a6b8eb	0a000000-0000-0000-0000-000000000004	9e8d13a1-a6eb-4646-bcf0-766022bd8189	40.00	f	2026-06-09 16:30:10.787+03	2026-06-09 16:30:10.787+03
aa360042-86bc-49dc-9d1b-1714704e6fd8	0a000000-0000-0000-0000-000000000005	9e8d13a1-a6eb-4646-bcf0-766022bd8189	60.00	t	2026-06-10 16:30:10.789+03	2026-06-10 16:30:10.789+03
e269fdde-91d6-4ab4-b6d0-52e3baa38ce6	0a000000-0000-0000-0000-000000000010	9e8d13a1-a6eb-4646-bcf0-766022bd8189	60.00	t	2026-06-11 16:30:10.791+03	2026-06-11 16:30:10.791+03
3d46bfc0-f9e5-455d-a813-f01de69a3d48	0a000000-0000-0000-0000-000000000011	9e8d13a1-a6eb-4646-bcf0-766022bd8189	60.00	t	2026-06-12 16:30:10.793+03	2026-06-12 16:30:10.793+03
e02962ed-74ad-4464-a8c9-ea5dccf62739	0a000000-0000-0000-0000-000000000002	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	60.00	t	2026-06-07 16:30:10.809+03	2026-06-07 16:30:10.809+03
075b1e6b-17a9-4602-a434-990d737649b4	0a000000-0000-0000-0000-000000000003	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	60.00	t	2026-06-08 16:30:10.811+03	2026-06-08 16:30:10.811+03
cee70db0-b351-4ec0-8fb3-db83930daf8f	0a000000-0000-0000-0000-000000000004	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	60.00	t	2026-06-09 16:30:10.813+03	2026-06-09 16:30:10.813+03
8913de42-9d4b-470a-8c1d-d5ea0060572e	0a000000-0000-0000-0000-000000000005	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	60.00	t	2026-06-10 16:30:10.815+03	2026-06-10 16:30:10.815+03
fd55f7bb-028e-4391-8780-9121cc81b669	0a000000-0000-0000-0000-000000000010	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	80.00	t	2026-06-11 16:30:10.817+03	2026-06-11 16:30:10.817+03
21a5e40e-cc90-40d0-babf-5ce913a335b3	0a000000-0000-0000-0000-000000000002	330d453f-8fcb-4579-b941-5e35d1ac5a35	100.00	t	2026-06-01 07:21:59.174+03	2026-06-01 07:21:59.174+03
3118f442-68d3-4eb8-8f56-da8493743655	0a000000-0000-0000-0000-000000000003	330d453f-8fcb-4579-b941-5e35d1ac5a35	33.00	f	2026-06-02 07:21:59.191+03	2026-06-02 07:21:59.191+03
0eff89f0-e4c7-42c3-8803-598be0ba7dd4	0a000000-0000-0000-0000-000000000004	330d453f-8fcb-4579-b941-5e35d1ac5a35	67.00	t	2026-06-03 07:21:59.195+03	2026-06-03 07:21:59.195+03
2e4e0e03-9f01-42e3-a944-7d9ead45cc74	0a000000-0000-0000-0000-000000000005	330d453f-8fcb-4579-b941-5e35d1ac5a35	33.00	f	2026-06-04 07:21:59.2+03	2026-06-04 07:21:59.2+03
ba45956c-17cc-42cd-8e51-bd3fbbd5d813	0a000000-0000-0000-0000-000000000010	330d453f-8fcb-4579-b941-5e35d1ac5a35	100.00	t	2026-06-05 07:21:59.204+03	2026-06-05 07:21:59.204+03
648d5891-3996-4173-8147-58c8f19ce281	0a000000-0000-0000-0000-000000000011	330d453f-8fcb-4579-b941-5e35d1ac5a35	33.00	f	2026-06-06 07:21:59.208+03	2026-06-06 07:21:59.208+03
e6e446fd-967e-4401-a1ca-f080c59bff0a	0a000000-0000-0000-0000-000000000012	330d453f-8fcb-4579-b941-5e35d1ac5a35	33.00	f	2026-06-07 07:21:59.211+03	2026-06-07 07:21:59.211+03
be305657-8326-45de-9166-8476ac7e02bb	0a000000-0000-0000-0000-000000000013	330d453f-8fcb-4579-b941-5e35d1ac5a35	33.00	f	2026-06-08 07:21:59.215+03	2026-06-08 07:21:59.215+03
bc8f4bb1-83ca-4ed3-b297-31b917cb2d94	0a000000-0000-0000-0000-000000000002	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	100.00	t	2026-06-01 07:21:59.223+03	2026-06-01 07:21:59.223+03
05c4a323-efc8-4281-bee1-ad8460e03e39	0a000000-0000-0000-0000-000000000003	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	0.00	f	2026-06-02 07:21:59.226+03	2026-06-02 07:21:59.226+03
2fb54e31-0a8d-4bdc-b196-e2dcdcf19ea5	0a000000-0000-0000-0000-000000000004	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	67.00	t	2026-06-03 07:21:59.23+03	2026-06-03 07:21:59.23+03
d4cf5862-076b-46a3-8d57-be286cb32cb6	0a000000-0000-0000-0000-000000000005	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	33.00	f	2026-06-04 07:21:59.234+03	2026-06-04 07:21:59.234+03
15442db2-0fdf-461d-87f5-8ef24665e63c	0a000000-0000-0000-0000-000000000010	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	33.00	f	2026-06-05 07:21:59.239+03	2026-06-05 07:21:59.239+03
a3233a1e-366f-4f54-8492-363dc9843806	0a000000-0000-0000-0000-000000000011	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	33.00	f	2026-06-06 07:21:59.243+03	2026-06-06 07:21:59.243+03
916bae6d-32b6-4bbf-98db-2d8e632bdf91	0a000000-0000-0000-0000-000000000012	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	100.00	t	2026-06-07 07:21:59.246+03	2026-06-07 07:21:59.246+03
38663c7f-dae3-4088-bfe9-c088cdff9c93	0a000000-0000-0000-0000-000000000013	f13a5b8e-3a15-4d17-b2c8-7cca0b814626	33.00	f	2026-06-08 07:21:59.249+03	2026-06-08 07:21:59.249+03
0ed8b0cc-3420-440d-ac85-b724791b9b61	0a000000-0000-0000-0000-000000000002	9ae38d39-0a6e-47a8-929f-60e48f7311c9	67.00	t	2026-06-01 07:21:59.256+03	2026-06-01 07:21:59.256+03
85c00fbd-bb63-4656-b2ed-1d5541635d87	0a000000-0000-0000-0000-000000000003	9ae38d39-0a6e-47a8-929f-60e48f7311c9	100.00	t	2026-06-02 07:21:59.259+03	2026-06-02 07:21:59.259+03
12267ead-50cf-4a3b-a80a-9aaa0fecffd4	0a000000-0000-0000-0000-000000000004	9ae38d39-0a6e-47a8-929f-60e48f7311c9	67.00	t	2026-06-03 07:21:59.264+03	2026-06-03 07:21:59.264+03
b07973a3-a2bb-490c-a76e-b6fce3f2a316	0a000000-0000-0000-0000-000000000005	9ae38d39-0a6e-47a8-929f-60e48f7311c9	67.00	t	2026-06-04 07:21:59.269+03	2026-06-04 07:21:59.269+03
8da19b6a-2596-4e6f-a1b2-8f7bcf141491	0a000000-0000-0000-0000-000000000010	9ae38d39-0a6e-47a8-929f-60e48f7311c9	100.00	t	2026-06-05 07:21:59.272+03	2026-06-05 07:21:59.272+03
d4a91558-0239-4150-a2ea-ed33048ba508	0a000000-0000-0000-0000-000000000011	9ae38d39-0a6e-47a8-929f-60e48f7311c9	100.00	t	2026-06-06 07:21:59.275+03	2026-06-06 07:21:59.275+03
be5715fc-1a02-4474-b573-bbf2b22bd416	0a000000-0000-0000-0000-000000000012	9ae38d39-0a6e-47a8-929f-60e48f7311c9	67.00	t	2026-06-07 07:21:59.277+03	2026-06-07 07:21:59.277+03
6c54a6cd-c17c-46bc-ae61-9ec7a226f3e9	0a000000-0000-0000-0000-000000000013	9ae38d39-0a6e-47a8-929f-60e48f7311c9	67.00	t	2026-06-08 07:21:59.279+03	2026-06-08 07:21:59.279+03
09bcbf4a-e1d5-4527-a177-949d79c5c997	0a000000-0000-0000-0000-000000000011	0f1b7f21-0b1f-4248-9997-504c4e32e1a1	60.00	t	2026-06-12 16:30:10.819+03	2026-06-12 16:30:10.819+03
ef4d2102-7442-4b64-9050-44d3e358ed90	0a000000-0000-0000-0000-000000000002	f3057118-3a60-49bf-ab23-b15fdde27457	20.00	f	2026-06-07 16:30:10.834+03	2026-06-07 16:30:10.834+03
e2fc4a2b-d28b-4270-a621-c4801463e426	0a000000-0000-0000-0000-000000000003	f3057118-3a60-49bf-ab23-b15fdde27457	60.00	t	2026-06-08 16:30:10.843+03	2026-06-08 16:30:10.843+03
1006bebb-169e-4d39-833d-58dc36007052	0a000000-0000-0000-0000-000000000004	f3057118-3a60-49bf-ab23-b15fdde27457	80.00	t	2026-06-09 16:30:10.845+03	2026-06-09 16:30:10.845+03
e97b2d34-4d16-49b8-8a59-16f038b6c0bc	0a000000-0000-0000-0000-000000000005	f3057118-3a60-49bf-ab23-b15fdde27457	40.00	f	2026-06-10 16:30:10.847+03	2026-06-10 16:30:10.847+03
22c3b553-c22a-426f-aa26-af56d807022b	0a000000-0000-0000-0000-000000000010	f3057118-3a60-49bf-ab23-b15fdde27457	40.00	f	2026-06-11 16:30:10.849+03	2026-06-11 16:30:10.849+03
a962b64c-08b0-4746-b65b-6bfefcaa97a0	0a000000-0000-0000-0000-000000000011	f3057118-3a60-49bf-ab23-b15fdde27457	20.00	f	2026-06-12 16:30:10.851+03	2026-06-12 16:30:10.851+03
\.


--
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tests (id, lesson_id, title, pass_score, time_limit_sec) FROM stdin;
0fa00000-0000-0000-0000-000000000001	0e000000-0000-0000-0000-000000000001	Тест: основы баз данных	60	600
0fa00000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000004	Тест: связи и ключи	60	600
0f000000-0000-0000-0000-000000000002	0e000000-0000-0000-0000-000000000002	Тест: строки и столбцы	60	\N
0f000000-0000-0000-0000-000000000003	0e000000-0000-0000-0000-000000000003	Тест: сущности и атрибуты	60	\N
0f000000-0000-0000-0000-000000000005	0e000000-0000-0000-0000-000000000005	Тест: CREATE TABLE	60	\N
0f000000-0000-0000-0000-000000000006	0e000000-0000-0000-0000-000000000006	Тест: команда SELECT	60	\N
0f000000-0000-0000-0000-000000000007	0e000000-0000-0000-0000-000000000007	Тест: фильтрация (WHERE)	60	\N
0f000000-0000-0000-0000-000000000008	0e000000-0000-0000-0000-000000000008	Тест: сортировка и ограничение	60	\N
0f000000-0000-0000-0000-000000000009	0e000000-0000-0000-0000-000000000009	Тест: добавление данных (INSERT)	60	\N
0f000000-0000-0000-0000-00000000000a	0e000000-0000-0000-0000-00000000000a	Тест: изменение и удаление	60	\N
0f000000-0000-0000-0000-00000000000b	0e000000-0000-0000-0000-00000000000b	Тест: агрегатные функции	60	\N
0f000000-0000-0000-0000-00000000000c	0e000000-0000-0000-0000-00000000000c	Тест: GROUP BY и HAVING	60	\N
0f000000-0000-0000-0000-00000000000d	0e000000-0000-0000-0000-00000000000d	Тест: INNER JOIN	60	\N
0f000000-0000-0000-0000-00000000000e	0e000000-0000-0000-0000-00000000000e	Тест: LEFT JOIN и виды соединений	60	\N
0f000000-0000-0000-0000-00000000000f	0e000000-0000-0000-0000-00000000000f	Тест: аномалии и 1НФ	60	\N
0f000000-0000-0000-0000-000000000010	0e000000-0000-0000-0000-000000000010	Тест: 2НФ и 3НФ	60	\N
0f000000-0000-0000-0000-000000000011	0e000000-0000-0000-0000-000000000011	Тест: ограничения целостности	60	\N
0f000000-0000-0000-0000-000000000012	0e000000-0000-0000-0000-000000000012	Тест: индексы и представления	60	\N
330d453f-8fcb-4579-b941-5e35d1ac5a35	656a356d-8ad7-4bb5-b5b5-3597d30936f8	Проверка: первые запросы SELECT	60	\N
f13a5b8e-3a15-4d17-b2c8-7cca0b814626	131ee2bd-dc3d-47a5-a51b-dab0deb28e2f	Проверка: фильтрация WHERE	60	\N
9ae38d39-0a6e-47a8-929f-60e48f7311c9	216f012b-02e7-49c4-81e1-08e8a9af6dcd	Проверка: сортировка и агрегаты	60	\N
6b604fc2-d9b2-4091-90f2-ac047f9f794d	12f8a209-f08e-4629-91d2-cdaa4af53c53	Итоговый тест: проектирование БД	60	\N
c24a5c67-01fe-4274-8b7d-d12325d9f4f5	fa880b3b-f5bc-4dec-b343-ea5bebc2ab0a	Итоговый тест: нормализация	60	\N
a47b8287-9a6e-4dd1-a150-e67096053cfb	a76e62b1-ed81-4666-ab21-3ee82561ec15	Итоговый тест: транзакции и блокировки	60	\N
9e8d13a1-a6eb-4646-bcf0-766022bd8189	8dae3fac-b120-4fa6-b46b-c166f2c1965f	Итоговый тест: индексы и производительность	60	\N
0f1b7f21-0b1f-4248-9997-504c4e32e1a1	1a340833-305a-415a-aab5-08d5e36d17c8	Итоговый тест: PostgreSQL на практике	60	\N
f3057118-3a60-49bf-ab23-b15fdde27457	42487a06-725b-48e1-a85d-9933d35a3b4b	Итоговый тест: оконные функции	60	\N
\.


--
-- Data for Name: topics; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.topics (id, code, name) FROM stdin;
8c2acdbe-c962-46fd-9c1a-89b8890a0b37	sql	SQL
15f929ac-53d5-4891-b073-c7fff41fc581	postgresql	PostgreSQL
f99935dd-5cf0-487b-9efa-3b885d136fec	design	Проектирование БД
b2271f85-242b-45c3-a2f2-3c6989578471	modeling	ER-моделирование
854bb4bc-a757-47c0-94b1-8de546f4bb6f	normalization	Нормализация
2a12d38d-4cd6-4622-8e3b-a6c50c43db37	transactions	Транзакции
3a11bf6f-cd97-4024-97c2-38afdeafcd33	indexing	Индексы
c496bbb5-fbda-4b1a-a8c8-8e34fab0a9ef	performance	Производительность
\.


--
-- Data for Name: user_achievements; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_achievements (id, user_id, achievement_id, awarded_at) FROM stdin;
5b3a61ef-ffcc-460b-aa40-cd8746325dd2	0a000000-0000-0000-0000-000000000002	0ac00000-0000-0000-0000-000000000001	2025-09-05 18:31:00+03
09769f07-7757-4ec2-bcb3-af5b061610be	0a000000-0000-0000-0000-000000000002	0ac00000-0000-0000-0000-000000000002	2025-10-14 19:05:00+03
39fd43d9-a69a-4066-98b5-6ea306f883fe	0a000000-0000-0000-0000-000000000002	0ac00000-0000-0000-0000-000000000003	2025-09-05 18:40:00+03
c7a29550-f90a-4408-a683-484155480127	0a000000-0000-0000-0000-000000000003	0ac00000-0000-0000-0000-000000000001	2025-09-06 12:28:00+03
81a27420-d9b1-4c7b-a23a-710f3022407c	0a000000-0000-0000-0000-000000000003	0ac00000-0000-0000-0000-000000000002	2025-10-15 16:05:00+03
da67f5c2-cd4b-4f24-9977-8aa73180266a	0a000000-0000-0000-0000-000000000004	0ac00000-0000-0000-0000-000000000001	2025-09-07 11:24:00+03
82112d25-1937-4e4b-aa37-3481cb22e3a8	0a000000-0000-0000-0000-000000000013	0ac00000-0000-0000-0000-000000000001	2026-06-02 23:48:37.152+03
ee7a410f-ae13-4866-9d89-2933ffa6de78	0a000000-0000-0000-0000-000000000017	0ac00000-0000-0000-0000-000000000001	2026-06-09 23:23:44.059+03
cecdd5f4-0b4f-460b-a697-0d0a4c8a4eca	0a000000-0000-0000-0000-000000000005	0ac00000-0000-0000-0000-000000000001	2026-06-09 11:46:51.947+03
24fc6e45-e36c-4d74-a6d4-f74bdfd86670	0a000000-0000-0000-0000-000000000018	0ac00000-0000-0000-0000-000000000001	2026-06-09 23:23:44.059+03
9a5fc340-761a-4178-9c75-fea50ab88142	0a000000-0000-0000-0000-000000000012	0ac00000-0000-0000-0000-000000000001	2026-06-02 23:48:37.152+03
e717c976-c122-4c3f-a8de-bf1867432566	0a000000-0000-0000-0000-000000000010	0ac00000-0000-0000-0000-000000000001	2026-06-02 23:48:37.152+03
f458589e-634a-4171-a525-769f9c59e882	0a000000-0000-0000-0000-000000000016	0ac00000-0000-0000-0000-000000000001	2026-06-02 23:48:37.152+03
8feba523-a614-4eb4-88b3-f2e5d6e53694	0a000000-0000-0000-0000-000000000011	0ac00000-0000-0000-0000-000000000001	2026-06-02 23:48:37.152+03
5495ad34-557b-4ac3-997a-af97e694a0ca	0a000000-0000-0000-0000-000000000014	0ac00000-0000-0000-0000-000000000001	2026-06-02 23:48:37.152+03
2e6ad6fd-7895-47df-8351-e57267658bcc	0a000000-0000-0000-0000-00000000001a	0ac00000-0000-0000-0000-000000000001	2026-06-09 23:23:44.059+03
7e3d4bf8-c0f4-44f5-a5d9-3f2b35db2bd4	0a000000-0000-0000-0000-000000000015	0ac00000-0000-0000-0000-000000000001	2026-06-09 23:23:44.059+03
ea4fa66b-33c8-454c-b860-aaad1f15320c	0a000000-0000-0000-0000-000000000010	0ac00000-0000-0000-0000-000000000003	2026-06-03 23:48:37.152+03
074afe65-db49-46e5-9f03-0980df997dc9	0a000000-0000-0000-0000-000000000005	0ac00000-0000-0000-0000-000000000003	2026-06-09 11:41:02.257+03
0d31706f-ea9d-4aad-863f-68ffcb8a0ca6	0a000000-0000-0000-0000-000000000011	0ac00000-0000-0000-0000-000000000003	2026-06-09 23:23:49.263+03
202a7ed3-3982-4e3f-84bc-ac2cb6fd2a0b	0a000000-0000-0000-0000-000000000012	0ac00000-0000-0000-0000-000000000003	2026-06-03 23:48:37.152+03
d05205d3-4ee0-4793-8400-3b6df9acbd00	0a000000-0000-0000-0000-000000000013	0ac00000-0000-0000-0000-000000000003	2026-06-09 23:23:49.263+03
7ebe62cb-bcfc-473c-b03a-1c70fd3821b0	0a000000-0000-0000-0000-000000000005	0ac00000-0000-0000-0000-000000000002	2026-06-10 09:40:05.833+03
b39f417e-da4c-4770-b215-cd16cc939a6a	0a000000-0000-0000-0000-000000000001	0ac00000-0000-0000-0000-000000000002	2026-06-10 16:41:16.344+03
af189b4e-ab24-483f-ab8a-c4068150eaea	0a000000-0000-0000-0000-000000000010	0ac00000-0000-0000-0000-000000000005	2026-06-11 12:26:06.517+03
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, password_hash, full_name, role_id, avatar_url, xp, level, is_active, last_seen_at, created_at, updated_at) FROM stdin;
0a000000-0000-0000-0000-000000000013	alina@stud.ru	scrypt$5de3564f38926a47376e5115dacaeec2$68e7b63f43108d47debebd46e873906e795b83fb4fd2a28e81c86ce6fa3d380629862a574837044654366645215eebb02ad3483dd7b695fbac28c116bff1bd7a	Борисова Алина	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	190	3	t	2026-06-06 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000017	gleb@stud.ru	scrypt$2375abbc54966b24ed15eb1caa3dd2fe$681921a0848073519d72603a52623446fcf56fda889b6d056cd0523e88cd139cdae9eeb6b999292f320c821d9e71b8927ecd3d13169680681a869d4189532b56	Тимофеев Глеб	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	75	2	t	2026-05-30 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000018	olga2@stud.ru	scrypt$cf62f594d0d618adde9f5c4400570713$8890fdeab27acd7194bb7995b0d12f1ddd50a7faca315c3690723b98f12fa805ce5f609c0b5b7a2628efd4d93be95dbdedaa309d6513542f229db9756910aaf6	Попова Ольга	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	60	2	t	2026-05-22 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000012	darya@stud.ru	scrypt$1a09abc8114b8cb207fada12d3878513$51a5233bb64a257857e2a55b3004d62af3e632c56b1a8d2810a3bf9a3dd1e683b6863c742ffced7a27aaf9e5fb80e660c7ccee64e49b4eaca1db3f20f6f5aced	Новикова Дарья	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	260	4	t	2026-06-08 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000015	maria@stud.ru	scrypt$0f69a41174691aa59e58c955dadaf717$bc23a3b4f88fbf3a02a318d1e6c224aecf21d52556bb9862e19ec7002df123a902f967438911f85fc2f5dee5024985e972388934d6bf4e5ac6cc4296e1d9e550	Алексеева Мария	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	100	2	t	2026-06-02 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000010	elena@stud.ru	scrypt$729a480a1a3b219c3a1f74be63247cec$71fb33eb4be8704902a17d7066233ece874c72228c541d2d1de8628587b4b4e3b20caeb7691e67e3a3c23c57a134c60abf80daaa780b5462dd7f4db0d8bd0941	Морозова Елена	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	380	5	t	2026-06-08 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000016	nikita@stud.ru	scrypt$d30643c40bba499c0d8e60a7a2bdabd6$5baf58bbfd0328fc0d3c34dcdc6576c5dccb449622e8d3423c33143e8c27a9f398d8c77ef7adff505e9e44daa2fc056202f2436b895f0c76645e22ab2444d5ee	Сергеев Никита	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	120	3	t	2026-06-05 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000011	pavel@stud.ru	scrypt$a84ae5549ba2e619dbb9a6b174adafdb$94722f32f5e6a91b90037f81b9b0834195db555a6cfc5e48f00f08748c7f29e73eb1a9e10e1c2f75a94705fc7b498989b7400fa876215da8e5dc847f587b6020	Васильев Павел	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	220	4	t	2026-06-07 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000014	ilya@stud.ru	scrypt$f8d36676c04e0317a18402a7f9b2c2eb$5400f192488d5b3ea59f06e604b409e20b74d2ebfb814016390bfb97e4a326c5da1a4a402931e3a0a741ee18d7aef323ed6750f9640a70341afe4267a9b6d002	Фёдоров Илья	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	115	2	t	2026-06-04 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-00000000001a	polina@stud.ru	scrypt$847993736b5db380d859d298071ae422$1098317222d0eeb2c068e0c52c17bfc226abb1552d41341f306a5748acb55399c225c63494e4adc6049149f6acb37d882f92b6970549c46e419c050713d91641	Захарова Полина	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	55	1	t	2026-05-20 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000001	petrova@dataedu.ru	scrypt$ca46c2a0e8adb8a8dec1cac911d3759b$9a316fd282861341d13f140f696a967954bce767734f52cf45dcdf1b2538c36600d35294b0b8abb83a53bc8eba9d693d0bdef7c00344ded90bc2aca7f4a38ae2	Петрова Ольга Ивановна	b2ea6708-47d9-4c87-bd35-90a3c8c89444	\N	20	1	t	2025-10-20 09:00:00+03	2025-09-01 08:00:00+03	2026-06-07 21:32:31.893381+03
96a9242b-7429-4a6d-bfc3-0bdad53a8a73	admin@dataedu.ru	scrypt$0ad3d0a37757e3b03d959d1d8d7e37ab$5704b84e0df8395302e43dbb8d901e4d3005458cfdeb2d49384d75a86e91238e0e0cd1486107fb95e63c530eca16bc9f168326ef970f6a312e27d223b7ff81a4	Администратор Системы	49b27c2a-4b82-458f-9dac-03ec55bf3f37	\N	0	1	t	\N	2026-06-11 14:19:19.834513+03	2026-06-11 14:19:19.834513+03
0a000000-0000-0000-0000-000000000005	dmitry@stud.ru	scrypt$00da948e679fc5548dc5ea0c75f17b4c$74966456e42e5c459bc0e6d4cc1bddc728cda5c8daf8f0396350b86c51d08dd7b9bc82f8b7e9225146c80896052c1e4ab83a61c371ba8ac0ecf940b298a40676	Соколов Дмитрий	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	80	2	t	2026-06-07 23:23:49.263196+03	2025-09-10 11:00:00+03	2026-06-07 21:32:31.893381+03
0a000000-0000-0000-0000-000000000019	artem@stud.ru	scrypt$c7adf183628bda0ab71dac79eb7c6d43$9ab3519ea55c902d4f4164c8296621c62588db936b33ce06ba2a5c94220113088a6831b6e6141a51332c52bdf51ea9ed50af900627e8cc3f6924358f7f656386	Михайлов Артём	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	10	1	t	2026-05-18 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
dac3fbb0-f253-4492-a731-27496f3ed123	achertovikov@edu.ru	scrypt$776d04bc8f9cbd507de42709f6bcd23a$5c629c0357a68e5059ea892b9f4d9006a03fd13c4eb2ec71d007162187a6cb5b2a62799ca3a5947136b5f7ca958edea5777bd52494ab7e49f6fcd7b52987856a	Чертовиков Алексей Витальевич	49b27c2a-4b82-458f-9dac-03ec55bf3f37	\N	0	1	t	\N	2026-06-12 07:40:38.662+03	2026-06-12 07:40:38.662+03
0a000000-0000-0000-0000-00000000001b	denis@stud.ru	scrypt$c6c5359223125b2a14b6d543fb0e1b85$ea6ef60c91d3e94961a7ece6bcfafaa598bf54d66e913039efe9d03f3af84466caaf37cd1dd1696733de6409d284276a680b7a96ac48f5cb3ec582539e3693bd	Григорьев Денис	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	20	1	t	2026-05-15 23:23:49.263196+03	2026-06-09 23:23:44.059174+03	2026-06-09 23:23:44.059174+03
0a000000-0000-0000-0000-000000000002	anna@stud.ru	scrypt$3c061fb1bd74d00898aa9c50cc178c07$3f8adcaf1b10d286dcf22ad506bf631c72bdfc72e74120d9085b07951d07d7757728da7ed4687f2c880a065a644f1d9e001870fe76e21408a9cb8658cb2f0e59	Смирнова Анна	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	180	3	t	2026-06-08 23:23:49.263196+03	2025-09-02 10:00:00+03	2026-06-07 21:32:31.893381+03
0a000000-0000-0000-0000-000000000003	boris@stud.ru	scrypt$3f52613f7f3ba908b153cbd439ec8797$466651e6f10d64a5a7ff1ccf4336efeaeddeb1a10a536590becead7990aa6933d5eb0e50fb012e3d606e82753519fb40c327a94fa605220e5c4b19ac58a83bf4	Кузнецов Борис	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	90	2	t	2026-06-06 23:23:49.263196+03	2025-09-02 10:05:00+03	2026-06-07 21:32:31.893381+03
0a000000-0000-0000-0000-000000000004	vika@stud.ru	scrypt$5f01074856eb2f06977e835a95c22d03$010f531de1ec030e0cb45010aec9cde99cf299098cbced4d197281cdba3fc737b15e195ac6dee28489bfa702c920670e5b8adbc6bc5725132ab31f0cc6c86fb7	Иванова Виктория	481e965b-f5bf-4689-a7f5-836edf9adfd1	\N	30	1	t	2026-05-24 23:23:49.263196+03	2025-09-02 10:08:00+03	2026-06-07 21:32:31.893381+03
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: sandbox; Owner: -
--

COPY sandbox.students (id, full_name, group_name, xp) FROM stdin;
1	Смирнова Анна	Б-101	180
2	Кузнецов Борис	Б-101	90
3	Иванова Виктория	Б-102	30
4	Соколов Дмитрий	Б-102	10
5	Петров Олег	Б-103	0
\.


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: sandbox; Owner: -
--

SELECT pg_catalog.setval('sandbox.students_id_seq', 5, true);


--
-- Name: achievements achievements_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_code_key UNIQUE (code);


--
-- Name: achievements achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_pkey PRIMARY KEY (id);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: answer_options answer_options_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer_options
    ADD CONSTRAINT answer_options_pkey PRIMARY KEY (id);


--
-- Name: answer_submissions answer_submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer_submissions
    ADD CONSTRAINT answer_submissions_pkey PRIMARY KEY (id);


--
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);


--
-- Name: course_ratings course_ratings_course_id_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_ratings
    ADD CONSTRAINT course_ratings_course_id_user_id_key UNIQUE (course_id, user_id);


--
-- Name: course_ratings course_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_ratings
    ADD CONSTRAINT course_ratings_pkey PRIMARY KEY (id);


--
-- Name: course_topics course_topics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_topics
    ADD CONSTRAINT course_topics_pkey PRIMARY KEY (course_id, topic_id);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: courses courses_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_slug_key UNIQUE (slug);


--
-- Name: enrollments enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_pkey PRIMARY KEY (id);


--
-- Name: enrollments enrollments_user_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_user_id_course_id_key UNIQUE (user_id, course_id);


--
-- Name: lesson_progress lesson_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lesson_progress
    ADD CONSTRAINT lesson_progress_pkey PRIMARY KEY (id);


--
-- Name: lesson_progress lesson_progress_user_id_lesson_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lesson_progress
    ADD CONSTRAINT lesson_progress_user_id_lesson_id_key UNIQUE (user_id, lesson_id);


--
-- Name: lessons lessons_module_id_order_index_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_module_id_order_index_key UNIQUE (module_id, order_index);


--
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: modules modules_course_id_order_index_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_course_id_order_index_key UNIQUE (course_id, order_index);


--
-- Name: modules modules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: reflections reflections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reflections
    ADD CONSTRAINT reflections_pkey PRIMARY KEY (id);


--
-- Name: reflections reflections_user_id_lesson_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reflections
    ADD CONSTRAINT reflections_user_id_lesson_id_key UNIQUE (user_id, lesson_id);


--
-- Name: roles roles_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_code_key UNIQUE (code);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: submissions submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_pkey PRIMARY KEY (id);


--
-- Name: test_attempts test_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.test_attempts
    ADD CONSTRAINT test_attempts_pkey PRIMARY KEY (id);


--
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- Name: topics topics_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_code_key UNIQUE (code);


--
-- Name: topics topics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_pkey PRIMARY KEY (id);


--
-- Name: user_achievements user_achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_pkey PRIMARY KEY (id);


--
-- Name: user_achievements user_achievements_user_id_achievement_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_user_id_achievement_id_key UNIQUE (user_id, achievement_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: sandbox; Owner: -
--

ALTER TABLE ONLY sandbox.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: idx_activities_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_activities_type ON public.activities USING btree (type);


--
-- Name: idx_activities_user_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_activities_user_time ON public.activities USING btree (user_id, created_at DESC);


--
-- Name: idx_answer_options_question; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_answer_options_question ON public.answer_options USING btree (question_id);


--
-- Name: idx_answer_submissions_attempt; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_answer_submissions_attempt ON public.answer_submissions USING btree (attempt_id);


--
-- Name: idx_assignments_course; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_assignments_course ON public.assignments USING btree (course_id);


--
-- Name: idx_enrollments_course; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_enrollments_course ON public.enrollments USING btree (course_id);


--
-- Name: idx_lesson_progress_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_lesson_progress_user ON public.lesson_progress USING btree (user_id);


--
-- Name: idx_lessons_module; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_lessons_module ON public.lessons USING btree (module_id);


--
-- Name: idx_messages_pair; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_messages_pair ON public.messages USING btree (sender_id, recipient_id, created_at);


--
-- Name: idx_messages_recipient; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_messages_recipient ON public.messages USING btree (recipient_id, read_at);


--
-- Name: idx_modules_course; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_modules_course ON public.modules USING btree (course_id);


--
-- Name: idx_questions_test; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_questions_test ON public.questions USING btree (test_id);


--
-- Name: idx_submissions_assignment; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_assignment ON public.submissions USING btree (assignment_id);


--
-- Name: idx_submissions_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_user ON public.submissions USING btree (user_id);


--
-- Name: idx_test_attempts_test; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_test_attempts_test ON public.test_attempts USING btree (test_id);


--
-- Name: idx_test_attempts_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_test_attempts_user ON public.test_attempts USING btree (user_id);


--
-- Name: idx_tests_lesson; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tests_lesson ON public.tests USING btree (lesson_id);


--
-- Name: idx_users_role; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_role ON public.users USING btree (role_id);


--
-- Name: activities activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: answer_options answer_options_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer_options
    ADD CONSTRAINT answer_options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;


--
-- Name: answer_submissions answer_submissions_answer_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer_submissions
    ADD CONSTRAINT answer_submissions_answer_option_id_fkey FOREIGN KEY (answer_option_id) REFERENCES public.answer_options(id) ON DELETE SET NULL;


--
-- Name: answer_submissions answer_submissions_attempt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer_submissions
    ADD CONSTRAINT answer_submissions_attempt_id_fkey FOREIGN KEY (attempt_id) REFERENCES public.test_attempts(id) ON DELETE CASCADE;


--
-- Name: answer_submissions answer_submissions_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer_submissions
    ADD CONSTRAINT answer_submissions_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;


--
-- Name: assignments assignments_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- Name: assignments assignments_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: course_ratings course_ratings_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_ratings
    ADD CONSTRAINT course_ratings_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- Name: course_ratings course_ratings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_ratings
    ADD CONSTRAINT course_ratings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: course_topics course_topics_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_topics
    ADD CONSTRAINT course_topics_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- Name: course_topics course_topics_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_topics
    ADD CONSTRAINT course_topics_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(id) ON DELETE CASCADE;


--
-- Name: courses courses_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: enrollments enrollments_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- Name: enrollments enrollments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: lesson_progress lesson_progress_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lesson_progress
    ADD CONSTRAINT lesson_progress_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: lesson_progress lesson_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lesson_progress
    ADD CONSTRAINT lesson_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: lessons lessons_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(id) ON DELETE CASCADE;


--
-- Name: messages messages_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE SET NULL;


--
-- Name: messages messages_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: modules modules_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- Name: questions questions_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE CASCADE;


--
-- Name: reflections reflections_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reflections
    ADD CONSTRAINT reflections_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: reflections reflections_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reflections
    ADD CONSTRAINT reflections_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: submissions submissions_assignment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_assignment_id_fkey FOREIGN KEY (assignment_id) REFERENCES public.assignments(id) ON DELETE CASCADE;


--
-- Name: submissions submissions_graded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_graded_by_fkey FOREIGN KEY (graded_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: submissions submissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: test_attempts test_attempts_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.test_attempts
    ADD CONSTRAINT test_attempts_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.tests(id) ON DELETE CASCADE;


--
-- Name: test_attempts test_attempts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.test_attempts
    ADD CONSTRAINT test_attempts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: tests tests_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- Name: user_achievements user_achievements_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievements(id) ON DELETE CASCADE;


--
-- Name: user_achievements user_achievements_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict ReUPFuVPhi9n7g6WuL00QMwE4vPXQSQCKd7APtBR3ax456zQUCdzPbHjci8A6Zg

