--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.24
-- Dumped by pg_dump version 9.1.24
-- Started on 2017-05-02 00:13:00 BRT

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 199 (class 1259 OID 24723)
-- Dependencies: 8
-- Name: categories_subcategories; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE categories_subcategories (
    id integer NOT NULL,
    sub_categories_text character varying(220) NOT NULL,
    categories_id integer NOT NULL
);


ALTER TABLE public.categories_subcategories OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 24721)
-- Dependencies: 199 8
-- Name: categories_subcategories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE categories_subcategories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_subcategories_id_seq OWNER TO postgres;

--
-- TOC entry 3690 (class 0 OID 0)
-- Dependencies: 198
-- Name: categories_subcategories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE categories_subcategories_id_seq OWNED BY categories_subcategories.id;


--
-- TOC entry 3571 (class 2604 OID 24726)
-- Dependencies: 198 199 199
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categories_subcategories ALTER COLUMN id SET DEFAULT nextval('categories_subcategories_id_seq'::regclass);


--
-- TOC entry 3685 (class 0 OID 24723)
-- Dependencies: 199 3686
-- Data for Name: categories_subcategories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY categories_subcategories (id, sub_categories_text, categories_id) FROM stdin;
2	OTHER	1
3	TRAVEL	1
4	GARDEN	1
5	CLOTHES & ACESSORIES	1
6	FILM & MOVIES	1
7	PETS & ANIMALS	1
8	ELECTRONICS	1
9	FOOD & KITCHEN	1
10	CAMPING & OUTDOORS	1
11	FURNITURE	1
12	GAMES & TOYS	1
13	BOOKS & MAGAZINES	1
14	MUSIC	1
15	SPORTS	1
16	TOOLS	1
\.


--
-- TOC entry 3691 (class 0 OID 0)
-- Dependencies: 198
-- Name: categories_subcategories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('categories_subcategories_id_seq', 1, false);


--
-- TOC entry 3574 (class 2606 OID 24728)
-- Dependencies: 199 199 3687
-- Name: categories_subcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY categories_subcategories
    ADD CONSTRAINT categories_subcategories_pkey PRIMARY KEY (id);


--
-- TOC entry 3572 (class 1259 OID 24734)
-- Dependencies: 199 3687
-- Name: categories_subcategories_09c55841; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX categories_subcategories_09c55841 ON categories_subcategories USING btree (categories_id);


--
-- TOC entry 3575 (class 2606 OID 24729)
-- Dependencies: 199 197 3687
-- Name: cate_categories_id_5ce3763741fd3ceb_fk_categories_categories_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categories_subcategories
    ADD CONSTRAINT cate_categories_id_5ce3763741fd3ceb_fk_categories_categories_id FOREIGN KEY (categories_id) REFERENCES categories_categories(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2017-05-02 00:13:00 BRT

--
-- PostgreSQL database dump complete
--

