PGDMP                         {            db_diulliosantos    14.7    15.2     s           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            t           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            u           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            v           1262    41030    db_diulliosantos    DATABASE     {   CREATE DATABASE db_diulliosantos WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
     DROP DATABASE db_diulliosantos;
                pgadmin    false            w           0    0    DATABASE db_diulliosantos    ACL     �   GRANT ALL ON DATABASE db_diulliosantos TO diulliosantos WITH GRANT OPTION;
SET SESSION AUTHORIZATION diulliosantos;
GRANT ALL ON DATABASE db_diulliosantos TO PUBLIC;
RESET SESSION AUTHORIZATION;
                   pgadmin    false    3958                        2615    45972    rfv    SCHEMA        CREATE SCHEMA rfv;
    DROP SCHEMA rfv;
                diulliosantos    false            x           0    0 
   SCHEMA rfv    ACL     >   GRANT ALL ON SCHEMA rfv TO olgaalexopoulos WITH GRANT OPTION;
                   diulliosantos    false    6            �            1259    45974    rfv_analysis    TABLE     S  CREATE TABLE rfv.rfv_analysis (
    id integer NOT NULL,
    rede_uf character varying NOT NULL,
    canal character varying NOT NULL,
    recencia integer NOT NULL,
    frequencia integer NOT NULL,
    score_frequencia integer NOT NULL,
    score_valor integer NOT NULL,
    score_recencia integer NOT NULL,
    valor double precision
);
    DROP TABLE rfv.rfv_analysis;
       rfv         heap    diulliosantos    false    6            �            1259    45973    rfv_analysis_id_seq    SEQUENCE     y   CREATE SEQUENCE rfv.rfv_analysis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE rfv.rfv_analysis_id_seq;
       rfv          diulliosantos    false    6    231            y           0    0    rfv_analysis_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE rfv.rfv_analysis_id_seq OWNED BY rfv.rfv_analysis.id;
          rfv          diulliosantos    false    230            �           2604    45977    rfv_analysis id    DEFAULT     l   ALTER TABLE ONLY rfv.rfv_analysis ALTER COLUMN id SET DEFAULT nextval('rfv.rfv_analysis_id_seq'::regclass);
 ;   ALTER TABLE rfv.rfv_analysis ALTER COLUMN id DROP DEFAULT;
       rfv          diulliosantos    false    231    230    231            p          0    45974    rfv_analysis 
   TABLE DATA           �   COPY rfv.rfv_analysis (id, rede_uf, canal, recencia, frequencia, score_frequencia, score_valor, score_recencia, valor) FROM stdin;
    rfv          diulliosantos    false    231   �       z           0    0    rfv_analysis_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('rfv.rfv_analysis_id_seq', 1, false);
          rfv          diulliosantos    false    230            �           2606    45981    rfv_analysis rfv_analysis_pk 
   CONSTRAINT     W   ALTER TABLE ONLY rfv.rfv_analysis
    ADD CONSTRAINT rfv_analysis_pk PRIMARY KEY (id);
 C   ALTER TABLE ONLY rfv.rfv_analysis DROP CONSTRAINT rfv_analysis_pk;
       rfv            diulliosantos    false    231            p      x������ � �     