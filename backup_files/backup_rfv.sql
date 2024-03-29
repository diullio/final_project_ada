PGDMP         0                {            db_diulliosantos    14.7    15.2     ~           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    41030    db_diulliosantos    DATABASE     {   CREATE DATABASE db_diulliosantos WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
     DROP DATABASE db_diulliosantos;
                pgadmin    false            �           0    0    DATABASE db_diulliosantos    ACL     �   GRANT ALL ON DATABASE db_diulliosantos TO diulliosantos WITH GRANT OPTION;
SET SESSION AUTHORIZATION diulliosantos;
GRANT ALL ON DATABASE db_diulliosantos TO PUBLIC;
RESET SESSION AUTHORIZATION;
                   pgadmin    false    3969                        2615    46101    rfv    SCHEMA        CREATE SCHEMA rfv;
    DROP SCHEMA rfv;
                diulliosantos    false            �            1259    46102    analysis    TABLE     �  CREATE TABLE rfv.analysis (
    id_analysis integer NOT NULL,
    rede_uf character varying(500) NOT NULL,
    uf character(2) NOT NULL,
    canal character varying(500) NOT NULL,
    recencia integer NOT NULL,
    frequencia integer NOT NULL,
    valor double precision NOT NULL,
    score_frequencia integer NOT NULL,
    score_valor integer NOT NULL,
    score_recencia integer NOT NULL,
    score integer NOT NULL
);
    DROP TABLE rfv.analysis;
       rfv         heap    diulliosantos    false    6            �            1259    46107    analysis_id_analysis_seq    SEQUENCE     ~   CREATE SEQUENCE rfv.analysis_id_analysis_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE rfv.analysis_id_analysis_seq;
       rfv          diulliosantos    false    230    6            �           0    0    analysis_id_analysis_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE rfv.analysis_id_analysis_seq OWNED BY rfv.analysis.id_analysis;
          rfv          diulliosantos    false    231            �            1259    46108    evolucao    TABLE     c  CREATE TABLE rfv.evolucao (
    id_evolucao integer NOT NULL,
    id_analysis integer NOT NULL,
    date date NOT NULL,
    recencia integer NOT NULL,
    frequencia integer NOT NULL,
    valor double precision NOT NULL,
    score_freq integer NOT NULL,
    score_valor integer NOT NULL,
    score_recencia integer NOT NULL,
    score integer NOT NULL
);
    DROP TABLE rfv.evolucao;
       rfv         heap    diulliosantos    false    6            �            1259    46111    evolucao_id_evolucao_seq    SEQUENCE     ~   CREATE SEQUENCE rfv.evolucao_id_evolucao_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE rfv.evolucao_id_evolucao_seq;
       rfv          diulliosantos    false    232    6            �           0    0    evolucao_id_evolucao_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE rfv.evolucao_id_evolucao_seq OWNED BY rfv.evolucao.id_evolucao;
          rfv          diulliosantos    false    233            �           2604    46112    analysis id_analysis    DEFAULT     v   ALTER TABLE ONLY rfv.analysis ALTER COLUMN id_analysis SET DEFAULT nextval('rfv.analysis_id_analysis_seq'::regclass);
 @   ALTER TABLE rfv.analysis ALTER COLUMN id_analysis DROP DEFAULT;
       rfv          diulliosantos    false    231    230            �           2604    46113    evolucao id_evolucao    DEFAULT     v   ALTER TABLE ONLY rfv.evolucao ALTER COLUMN id_evolucao SET DEFAULT nextval('rfv.evolucao_id_evolucao_seq'::regclass);
 @   ALTER TABLE rfv.evolucao ALTER COLUMN id_evolucao DROP DEFAULT;
       rfv          diulliosantos    false    233    232            x          0    46102    analysis 
   TABLE DATA           �   COPY rfv.analysis (id_analysis, rede_uf, uf, canal, recencia, frequencia, valor, score_frequencia, score_valor, score_recencia, score) FROM stdin;
    rfv          diulliosantos    false    230   �       z          0    46108    evolucao 
   TABLE DATA           �   COPY rfv.evolucao (id_evolucao, id_analysis, date, recencia, frequencia, valor, score_freq, score_valor, score_recencia, score) FROM stdin;
    rfv          diulliosantos    false    232   �       �           0    0    analysis_id_analysis_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('rfv.analysis_id_analysis_seq', 1, false);
          rfv          diulliosantos    false    231            �           0    0    evolucao_id_evolucao_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('rfv.evolucao_id_evolucao_seq', 1, false);
          rfv          diulliosantos    false    233            �           2606    46115    analysis analysis_pk 
   CONSTRAINT     X   ALTER TABLE ONLY rfv.analysis
    ADD CONSTRAINT analysis_pk PRIMARY KEY (id_analysis);
 ;   ALTER TABLE ONLY rfv.analysis DROP CONSTRAINT analysis_pk;
       rfv            diulliosantos    false    230            �           2606    46117    evolucao evolucao_pk 
   CONSTRAINT     e   ALTER TABLE ONLY rfv.evolucao
    ADD CONSTRAINT evolucao_pk PRIMARY KEY (id_evolucao, id_analysis);
 ;   ALTER TABLE ONLY rfv.evolucao DROP CONSTRAINT evolucao_pk;
       rfv            diulliosantos    false    232    232            �           2606    46118 !   evolucao rfv_analysis_evolucao_fk    FK CONSTRAINT     �   ALTER TABLE ONLY rfv.evolucao
    ADD CONSTRAINT rfv_analysis_evolucao_fk FOREIGN KEY (id_analysis) REFERENCES rfv.analysis(id_analysis);
 H   ALTER TABLE ONLY rfv.evolucao DROP CONSTRAINT rfv_analysis_evolucao_fk;
       rfv          diulliosantos    false    3817    230    232            x      x������ � �      z      x������ � �     