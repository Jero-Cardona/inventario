--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8
-- Dumped by pg_dump version 15.8

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
-- Name: categoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categoria (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    depreciacion real
);


ALTER TABLE public.categoria OWNER TO postgres;

--
-- Name: categoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categoria_id_seq OWNER TO postgres;

--
-- Name: categoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categoria_id_seq OWNED BY public.categoria.id;


--
-- Name: mantenimiento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mantenimiento (
    id integer NOT NULL,
    fecha_mantenimiento date NOT NULL,
    observacion text NOT NULL,
    id_usuarios integer NOT NULL,
    id_producto integer NOT NULL
);


ALTER TABLE public.mantenimiento OWNER TO postgres;

--
-- Name: mantenimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mantenimiento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mantenimiento_id_seq OWNER TO postgres;

--
-- Name: mantenimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mantenimiento_id_seq OWNED BY public.mantenimiento.id;


--
-- Name: producto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producto (
    id integer NOT NULL,
    id_responsable integer NOT NULL,
    codigo character varying(200) NOT NULL,
    id_sede integer NOT NULL,
    cantidad integer NOT NULL,
    uso text NOT NULL,
    estado character varying(100) NOT NULL,
    fecha_mantenimiento date NOT NULL,
    costo_inicial real NOT NULL,
    observacion text NOT NULL,
    id_categoria integer NOT NULL,
    id_proveedor integer,
    modo character varying(200) NOT NULL,
    fecha_ingreso date NOT NULL
);


ALTER TABLE public.producto OWNER TO postgres;

--
-- Name: producto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.producto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.producto_id_seq OWNER TO postgres;

--
-- Name: producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.producto_id_seq OWNED BY public.producto.id;


--
-- Name: producto_proveedores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producto_proveedores (
    id integer NOT NULL,
    id_producto integer NOT NULL,
    id_proveedor integer NOT NULL
);


ALTER TABLE public.producto_proveedores OWNER TO postgres;

--
-- Name: producto_proveedores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.producto_proveedores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.producto_proveedores_id_seq OWNER TO postgres;

--
-- Name: producto_proveedores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.producto_proveedores_id_seq OWNED BY public.producto_proveedores.id;


--
-- Name: proveedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proveedor (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    direccion character varying(200) NOT NULL,
    telefono character varying(20) NOT NULL
);


ALTER TABLE public.proveedor OWNER TO postgres;

--
-- Name: proveedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proveedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.proveedor_id_seq OWNER TO postgres;

--
-- Name: proveedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proveedor_id_seq OWNED BY public.proveedor.id;


--
-- Name: proveedormantenimiento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proveedormantenimiento (
    id integer NOT NULL,
    contacto character varying(250) NOT NULL,
    id_producto integer NOT NULL,
    id_proveedor integer
);


ALTER TABLE public.proveedormantenimiento OWNER TO postgres;

--
-- Name: proveedormantenimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proveedormantenimiento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.proveedormantenimiento_id_seq OWNER TO postgres;

--
-- Name: proveedormantenimiento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proveedormantenimiento_id_seq OWNED BY public.proveedormantenimiento.id;


--
-- Name: responsable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.responsable (
    id integer NOT NULL,
    nombre character varying(100),
    correo character varying(200),
    telefono character varying(20)
);


ALTER TABLE public.responsable OWNER TO postgres;

--
-- Name: responsable_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.responsable_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.responsable_id_seq1 OWNER TO postgres;

--
-- Name: responsable_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.responsable_id_seq1 OWNED BY public.responsable.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    nombre character varying(250) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: sede; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sede (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    direccion character varying(200) NOT NULL,
    telefono character varying(20) NOT NULL
);


ALTER TABLE public.sede OWNER TO postgres;

--
-- Name: sede_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sede_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sede_id_seq OWNER TO postgres;

--
-- Name: sede_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sede_id_seq OWNED BY public.sede.id;


--
-- Name: ubicacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicacion (
    id integer NOT NULL,
    nombre character varying(250) NOT NULL,
    id_sede integer NOT NULL,
    id_producto integer
);


ALTER TABLE public.ubicacion OWNER TO postgres;

--
-- Name: ubicacion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ubicacion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ubicacion_id_seq OWNER TO postgres;

--
-- Name: ubicacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicacion_id_seq OWNED BY public.ubicacion.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    nombre character varying(250) NOT NULL,
    correo character varying(250) NOT NULL,
    hashed_password character varying(100) NOT NULL,
    estado character varying(250) NOT NULL,
    fecha_creacion date NOT NULL,
    id_rol integer NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: categoria id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria ALTER COLUMN id SET DEFAULT nextval('public.categoria_id_seq'::regclass);


--
-- Name: mantenimiento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimiento ALTER COLUMN id SET DEFAULT nextval('public.mantenimiento_id_seq'::regclass);


--
-- Name: producto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto ALTER COLUMN id SET DEFAULT nextval('public.producto_id_seq'::regclass);


--
-- Name: producto_proveedores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto_proveedores ALTER COLUMN id SET DEFAULT nextval('public.producto_proveedores_id_seq'::regclass);


--
-- Name: proveedor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor ALTER COLUMN id SET DEFAULT nextval('public.proveedor_id_seq'::regclass);


--
-- Name: proveedormantenimiento id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedormantenimiento ALTER COLUMN id SET DEFAULT nextval('public.proveedormantenimiento_id_seq'::regclass);


--
-- Name: responsable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responsable ALTER COLUMN id SET DEFAULT nextval('public.responsable_id_seq1'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: sede id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sede ALTER COLUMN id SET DEFAULT nextval('public.sede_id_seq'::regclass);


--
-- Name: ubicacion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion ALTER COLUMN id SET DEFAULT nextval('public.ubicacion_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categoria (id, nombre, depreciacion) FROM stdin;
30	dasdasdasd	18
2	Equipo Tecnologico	15
3	Categoría A	8
4	Materia Prima	2.25
18	Alquilado	16
19	Comprado	30
29	categoria producto pequeño	22
11	prueba 	4.2
34	tecnologia	1.6
35	categoria	1.8
38	Prueba categoría 	1.666
39	Categoria Prueba Editada h	1.666
40	inmueble	0.83
41	inmueble ca 2	0.8333333
1	Categoría Inmueble	15
\.


--
-- Data for Name: mantenimiento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mantenimiento (id, fecha_mantenimiento, observacion, id_usuarios, id_producto) FROM stdin;
15	2024-09-15	producto prueba de cargue 	9	20
16	2024-10-01	producto prueba de cargue 	9	20
17	2024-10-01	producto prueba de cargue 	9	20
20	2024-09-12	dsadasdas	1	57
21	2024-12-06	asdasdasdasdsad aleluya	22	78
22	2024-09-14	DASDSADAS	24	81
23	2024-09-11	dasdasd	24	3
11	2024-08-21	observacion del producto o descripcion detallada	7	14
10	2024-10-11	Descripcion detallada de un productos sobre su mantenimiento y demas solicitudes sobre el mismo, y ayuda con esta prueba de codigo prueba\n                                	10	14
8	2026-03-20	mantenimiento editado prueba	10	79
24	2024-11-12	Producto nuevo con daños	10	79
25	2024-09-25	Mantenimiento equipo	6	78
26	2024-11-01	Observacion del mantenimiento como deseee el usuario del aplicativo final, Observacion del mantenimiento como deseee el usuario del aplicativo final, Observacion del mantenimiento 	10	97
27	2024-12-15	producto prueba de cargue 	9	97
28	2024-12-15	producto prueba de cargue 	9	97
29	2024-12-15	producto prueba de cargue 	9	97
30	2024-12-15	producto prueba de cargue 	9	97
\.


--
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.producto (id, id_responsable, codigo, id_sede, cantidad, uso, estado, fecha_mantenimiento, costo_inicial, observacion, id_categoria, id_proveedor, modo, fecha_ingreso) FROM stdin;
83	2	h	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
84	2	3213b	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
85	1	dasdasd21	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
76	2	pruebacantidad	1	1000	Cualquiera	Cualquiera	2024-10-09	1	prueba cantidad de datos	2	3	Cualquiera	2024-09-17
77	2	pruebaestado	1	212	Activo	Dañado	2024-09-26	30000	Producto nuevo que necesita ser arreglado	3	1	Alquilado	2024-09-18
78	2	a	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
79	2	b	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
80	1	d	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
81	2	t	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
9	2	ADA3	2	2	Cualquiera	Activo\n	2024-07-01	31000	dasdas	3	1	Cualquiera	2024-06-01
56	2	CODIGO2232	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
57	2	CODIGO2203	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
58	1	CODIGO2123123	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
59	2	CODIGO22332	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
5	3	P0090	3	200	Uso General	Activo	2024-06-25	64000.535	Producto nuevo en el inventario	3	1	Propio	2024-06-01
46	2	2215g \n	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
47	2	275gc	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
48	2	338b\n	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
49	2	2215gdf	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
50	2	2324ab	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
51	1	365cd	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
62	2	Prueba 1 Nulo	1	1	Uso General	Activo	2024-09-03	31000	Producto lenovo nuevo ingreso 	3	\N	Cualquiera	2024-09-16
66	4	Prueba nulo 34	3	1	Uso General	Cualquiera	2024-10-12	31000	Producto portátil lenovo	19	7	Cualquiera	2024-09-16
68	33	Prueba nulo 36	3	1	Uso General	Cualquiera	2024-10-12	31000	Producto portátil lenovo	19	2	Cualquiera	2024-09-16
69	2	Producto null 1	1	1	Cualquiera	Cualquiera	2024-09-03	31000	Observacion del producto de mesa computador con procesador ryzen 5	19	7	Cualquiera	2024-09-16
70	2	Producto null 2	1	1	Cualquiera	Cualquiera	2024-09-03	31000	Observacion del producto de mesa computador con procesador ryzen 5	19	7	Cualquiera	2024-09-16
96	2	codigo prueba	1	1	asdasdasd	Cualquiera	2024-09-11	123123	adasdsad	11	2	sdadsad	2024-09-19
142	2	11EDIT	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
14	2	A31450	3	1	Produccion	Activo	2024-08-30	85600	Observación producto prueba bugs editado de nuevo	3	2	Alquilado	2024-08-22
3	1	A	2	100	Uso General	Activo	2024-06-25	320000.53	Producto nuevo	2	1	Propioaqs	2024-06-01
98	2	75675a	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
99	2	423443a	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
100	1	7657567a	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
101	2	312312a	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
4	1	P090	2	532	Uso General	Inactivo	2024-06-25	100000	Nueva descripción detallada del producto, como prueba de funcionamiento del mismo	3	2	valor_por_defecto	2024-06-01
107	2	75673123123	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
108	2	888888888	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
109	1	76575675435	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
131	2	123213	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
132	2	54645645d	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
133	1	5555555555	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
134	2	4444444444	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
135	2	4	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
136	2	3	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
137	1	2	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
138	2	1	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
139	2	10	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
140	2	12	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
141	1	211	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
97	2	SINPRO2	1	1	asdasdad	dasasdasd	2024-09-11	323232.2	dasdasdasdad	1	\N	Alquilado	2024-07-24
20	2	CODIGO2	4	1	Cualquiera	Cualquiera	2024-09-10	31000	observación del producto, si editado cualquiera editado, observación del producto, si editado cualquiera editado, observación del producto, si editado cualquiera editado, observación del producto, si editado cualquiera editadoobservación del producto, si editado cualquiera editadoobservación del producto, si editado cualquiera editadoobservación del producto, si editado cualquiera editadoobservación del producto, si editado cualquiera editadoobservación del producto, si editado cualquiera editadoobservación del product	3	1	Cualquiera	2024-09-05
143	1	PDEPRE2	1	1	Uso General	Activo	2024-10-24	2e+07	Producto ingreso hace mas de 4 años	34	\N	Alquilado	2020-10-07
144	2	DEPRE21	1	1	Cualquiera	Cualquiera	2024-09-25	2e+07	Producto ya depreciado	34	1	Cualquiera	2020-09-09
145	2	32183d	1	1	Cualquiera	activo	2024-10-10	2e+06	producto nuevo	35	1	Cualquiera	2020-07-31
146	2	producto2312	1	1	uso	activo	2024-10-30	4.5e+06	producto	34	\N	Cualquiera	2015-07-07
150	2	13245457	1	1	Cualquiera	Cualquiera	2024-10-01	300000	h	39	1	Cualquiera	2022-06-15
151	3	3123123123	1	1	Cualquiera	Cualquiera	2024-10-08	5e+06	hola	40	1	Cualquiera	2024-09-01
155	2	P002	1	1	Produccion	Activo	2024-11-19	85600	dfdfd	41	\N	Alquilado	2024-10-16
157	2	Nm	1	20	uso general	activo	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
158	2	Nm1	1	4	uso general	inactivo	2025-12-30	20000	Producto antiguo	2	2	propio	2024-09-15
159	1	Emm	1	10	uso general	activo	2024-05-20	5000.59	Producto guardado	2	2	valoor por defecto	2023-07-28
160	2	Em11	1	1	uso general	prueba	2024-07-26	30000	Producto nuevo	2	2	Alquilado	2024-04-26
161	2	0000hola	1	1	En produccion arriba	dasd	2024-11-01	160000	Hola asdsad	40	\N	Alquilado	2024-10-30
\.


--
-- Data for Name: producto_proveedores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.producto_proveedores (id, id_producto, id_proveedor) FROM stdin;
3	3	1
4	4	2
9	76	3
10	77	1
13	96	2
14	14	2
5	5	1
16	20	1
18	131	2
19	132	2
20	133	2
21	134	2
22	135	2
23	136	2
24	137	2
25	138	2
26	139	2
27	140	2
28	141	2
29	142	2
30	144	1
31	145	1
32	150	1
33	151	1
37	157	2
38	158	2
39	159	2
40	160	2
\.


--
-- Data for Name: proveedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proveedor (id, nombre, direccion, telefono) FROM stdin;
2	Biotecs SAS	Calle #41a 25-05	312834212
6	Proveedor editado 	calle 41a #25c05	3123213213
12	Proveedor Prueba	cll37#56a65	3125432789
14	Proveedor Prueba	cr37#29-50	3122564388
3	prueba proveedor	direccion calle31a #25c05	31232131876
1	Compañia tecnologica	Calle #41a 25-15	3289768987
7	Proveedor C	calle 41a #25c05	312312316547
16	sadasd	asdasdasd	213123
\.


--
-- Data for Name: proveedormantenimiento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proveedormantenimiento (id, contacto, id_producto, id_proveedor) FROM stdin;
16	312312312312	4	2
18	12312312123	20	1
\.


--
-- Data for Name: responsable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.responsable (id, nombre, correo, telefono) FROM stdin;
2	Jeronimo Cardona Henao	jeronimo@example.com	31142949
3	Samuel Betancur Velasquez	Samuel@example.com	3128352
4	Emmanuel Echeverry Arboleda	Emmanuel@example.com	31152332
33	Santiago Cardona Morales	ejemplo@ejemplo.mx	3128452150
37	Responsable File	responsable@gmail.com	3125432789
38	File	responsable@gmail.com	3016667544
39	Responsable prueba	responsable@gmail.com	3122564388
43	Jeronimo	aasdasdads@hola.com	21312312
1	Brian Cardona	brian@gmail.com	340578626
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, nombre) FROM stdin;
2	Operador
30	Operacion de prueba
1	Administrador
\.


--
-- Data for Name: sede; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sede (id, nombre, direccion, telefono) FROM stdin;
1	Sede Ceja	La Ceja - Via el Tambo	6045537
3	Sede Rionegro	Rionegro - Parque Empresarial	604541
4	Sede Bogota	Bogota	6041244
2	Sede Editada	calle 41a #25c05	987654321
40	La ceja	cll37#56a65	3125432789
41	Rionegro	cll28#56a65	3016667544
42	Medellín	cr37#29-50	3122564388
47	La ceja	cll37#56a65	3125432789
48	Rionegro	cll28#56a65	3016667544
51	Medellín	calle 41a #25c10	3825754328
53	Jeronimo Cardona	asdasd	231323
\.


--
-- Data for Name: ubicacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicacion (id, nombre, id_sede, id_producto) FROM stdin;
16	Prueba	2	4
30	Cafeteria	1	5
40	Cafeteria	1	3
41	Operacion rionegro bodega	3	3
42	operacion ceja cesde 	1	4
43	operacion medellin auteco	42	5
44	operacion medellin auteco	2	20
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, nombre, correo, hashed_password, estado, fecha_creacion, id_rol) FROM stdin;
8	Jeronimo Henao	jeronimocardona@gmail.com	$2b$12$Y7a0w1i3EDROYE0lBC.SYO7QrUkkveVvtxrjZyXnSOe97TnrYOU9K	activo	2024-07-31	1
36	User File	user@gmai.com	$2b$12$YOGiDJobJM1Za2lqn4con.qHNTm1Ej7Sjrw0bMUor83p3j8bjIuVW	inactivo	2024-04-26	2
10	Daniel	dani@gmail.com	$2b$12$N1sWgcgeVfR4LWELhcfn8.a3tCYTHiC9V/rWRv0Bsoc9FQKWiZFLy	inactivo	2024-08-16	2
24	Santiago Cardona Moreno	jeronimocardona@gmail.com	$2b$12$bBxqzYq0KgemLUlcpR3yp.y6Zu14Q8l0F7bG8A1ISzrkdYdTU5YV2	inactivo	2024-08-30	2
22	Sergio Andre Editado	prueba@gmail.com	$2b$12$KZamtbSxOVHu/XsLo/lNXO/VhM7rgLwl05I7XtyvBjYO4Va2ucvKq	inactivo	2024-09-09	1
1	Jeronimo Cardona edit	corre@exmaple.com	$2b$12$fND5LOKICmmWLKLKFvAGo.W5oEg/eMHqTXbemZqVAVZGYOmOrzoA.	inactivo	2024-07-05	1
56	Prueba User New	user@gmail.com	$2b$12$.zOREQyJopaMWhV4p64Do.Ff5RRKyJypbvRe6A0SEnBhWP9RQAHhW	activo	2024-10-18	1
32	Usuario prueba edit	prueba@gmail.com	$2b$12$Wya8Ij/HiqxDfFvtTbTkdufaHkZ.YK4yDBBPcG5PIvGZNGPCJC1US	inactivo	2024-09-04	1
37	User test	user@gmail.com	$2b$12$p3b47O/E7Ahm7m.8C0j3wORWb5L7MkRZMfrA5xIFMUTnXaFK9iiKa	activo	2024-04-26	2
6	Jeronimo Henaods	peluche@gmail.com	$2b$12$OXcVL007scpFv9QUwsj94eEySv79Vq0OR6e4SKVLlbCmmHsFRlHoy	inactivo	2024-07-31	2
54	Jeronimo Cardona G	jeronimocardona@gmail.com	$2b$12$zjG9l7IvkvQ7hGqPmC3pR.Twqjiomrhhbb7gPKLPHocSW5ijErH22	inactivo	2024-10-02	2
53	Jeronimo Cardona	jeronimocardona@gmail.com	$2b$12$VL3Gq/zL1PasQjdBjpvhC.lE/Fo2WIEzzL2FY.nG/zevo18PKoNBC	inactivo	2024-10-02	1
7	pelucheuno	peluche1@gmail.com	$2b$12$U9AHeJqfTEJA8bG4nlmKPeDFzgPCz4dVIpvg9wWSscPJJYuv7z75.	inactivo	2024-07-31	1
9	UsuarioTest	test@gmail.com	$2b$12$ik4CLmbC9gU.Io6aa.0GaeAajKMaKJBlsPBuDCY6n/FmMSgVQgXqK	inactivo	2024-07-31	2
52	Joir	corre@gmail.com	$2b$12$LnXSliP9GAgnmE.4ef8a3uys/pGLk4l6mDl8XCq9IqoA3shKwd2Pe	activo	2024-09-25	2
55	nallely	nallelymarin@gmail.com	$2b$12$fRyuDdgnK1yUK9F6cM4xsOOZKJAtY.d11XvYMJk.5fC34SCUJcUSe	activo	2024-10-17	1
\.


--
-- Name: categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categoria_id_seq', 44, true);


--
-- Name: mantenimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mantenimiento_id_seq', 31, true);


--
-- Name: producto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.producto_id_seq', 161, true);


--
-- Name: producto_proveedores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.producto_proveedores_id_seq', 40, true);


--
-- Name: proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proveedor_id_seq', 16, true);


--
-- Name: proveedormantenimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proveedormantenimiento_id_seq', 22, true);


--
-- Name: responsable_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.responsable_id_seq1', 44, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 40, true);


--
-- Name: sede_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sede_id_seq', 53, true);


--
-- Name: ubicacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicacion_id_seq', 46, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 56, true);


--
-- Name: categoria categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (id);


--
-- Name: mantenimiento mantenimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimiento
    ADD CONSTRAINT mantenimiento_pkey PRIMARY KEY (id);


--
-- Name: producto producto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (id);


--
-- Name: producto_proveedores producto_proveedores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto_proveedores
    ADD CONSTRAINT producto_proveedores_pkey PRIMARY KEY (id);


--
-- Name: proveedor proveedor_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_pkey1 PRIMARY KEY (id);


--
-- Name: proveedormantenimiento proveedormantenimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedormantenimiento
    ADD CONSTRAINT proveedormantenimiento_pkey PRIMARY KEY (id);


--
-- Name: responsable responsable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responsable
    ADD CONSTRAINT responsable_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: sede sede_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sede
    ADD CONSTRAINT sede_pkey PRIMARY KEY (id);


--
-- Name: ubicacion ubicacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT ubicacion_pkey PRIMARY KEY (id);


--
-- Name: producto_proveedores unique_id_producto; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto_proveedores
    ADD CONSTRAINT unique_id_producto UNIQUE (id_producto);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: producto fk_categorias; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT fk_categorias FOREIGN KEY (id_categoria) REFERENCES public.categoria(id);


--
-- Name: producto fk_id_proveedor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT fk_id_proveedor FOREIGN KEY (id_proveedor) REFERENCES public.proveedor(id) ON DELETE CASCADE;


--
-- Name: producto_proveedores fk_id_proveedor_producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto_proveedores
    ADD CONSTRAINT fk_id_proveedor_producto FOREIGN KEY (id_proveedor) REFERENCES public.proveedor(id) ON DELETE CASCADE;


--
-- Name: producto fk_id_sede; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT fk_id_sede FOREIGN KEY (id_sede) REFERENCES public.sede(id);


--
-- Name: mantenimiento fk_id_usuarios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimiento
    ADD CONSTRAINT fk_id_usuarios FOREIGN KEY (id_usuarios) REFERENCES public.usuarios(id);


--
-- Name: producto_proveedores fk_producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto_proveedores
    ADD CONSTRAINT fk_producto FOREIGN KEY (id_producto) REFERENCES public.producto(id) ON DELETE CASCADE;


--
-- Name: proveedormantenimiento fk_producto_refered; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedormantenimiento
    ADD CONSTRAINT fk_producto_refered FOREIGN KEY (id_producto) REFERENCES public.producto_proveedores(id_producto) ON DELETE CASCADE;


--
-- Name: ubicacion fk_producto_u_refered; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT fk_producto_u_refered FOREIGN KEY (id_producto) REFERENCES public.producto(id) ON DELETE CASCADE;


--
-- Name: mantenimiento fk_productos; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mantenimiento
    ADD CONSTRAINT fk_productos FOREIGN KEY (id_producto) REFERENCES public.producto(id);


--
-- Name: proveedormantenimiento fk_proveedor_m_refered; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedormantenimiento
    ADD CONSTRAINT fk_proveedor_m_refered FOREIGN KEY (id_proveedor) REFERENCES public.proveedor(id) ON DELETE CASCADE;


--
-- Name: producto fk_responsables; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT fk_responsables FOREIGN KEY (id_responsable) REFERENCES public.responsable(id) ON DELETE CASCADE;


--
-- Name: usuarios fk_roles; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_roles FOREIGN KEY (id_rol) REFERENCES public.roles(id);


--
-- Name: ubicacion fk_sedes; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicacion
    ADD CONSTRAINT fk_sedes FOREIGN KEY (id_sede) REFERENCES public.sede(id);


--
-- PostgreSQL database dump complete
--

