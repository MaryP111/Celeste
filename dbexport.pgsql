PGDMP     &    '                u           Celeste    9.3.18    9.3.18     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            �           1262    16395    Celeste    DATABASE     {   CREATE DATABASE "Celeste" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
    DROP DATABASE "Celeste";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    6            �           0    0    public    ACL     �   REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
                  postgres    false    6                        3079    11789    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            �           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16405    people    TABLE     �   CREATE TABLE people (
    id integer NOT NULL,
    name text,
    color text,
    music text,
    gender text,
    category text
);
    DROP TABLE public.people;
       public         postgres    false    6            �            1259    16397    settings    TABLE     t   CREATE TABLE settings (
    id integer NOT NULL,
    name character varying(80),
    value character varying(80)
);
    DROP TABLE public.settings;
       public         postgres    false    6            �            1259    16400    settings_id_seq    SEQUENCE     q   CREATE SEQUENCE settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.settings_id_seq;
       public       postgres    false    6    171            �           0    0    settings_id_seq    SEQUENCE OWNED BY     5   ALTER SEQUENCE settings_id_seq OWNED BY settings.id;
            public       postgres    false    172            J           2604    16402    id    DEFAULT     \   ALTER TABLE ONLY settings ALTER COLUMN id SET DEFAULT nextval('settings_id_seq'::regclass);
 :   ALTER TABLE public.settings ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    172    171            �          0    16405    people 
   TABLE DATA               C   COPY people (id, name, color, music, gender, category) FROM stdin;
    public       postgres    false    173          �          0    16397    settings 
   TABLE DATA               ,   COPY settings (id, name, value) FROM stdin;
    public       postgres    false    171   ^       �           0    0    settings_id_seq    SEQUENCE SET     7   SELECT pg_catalog.setval('settings_id_seq', 1, false);
            public       postgres    false    172            N           2606    16412    pkey 
   CONSTRAINT     B   ALTER TABLE ONLY people
    ADD CONSTRAINT pkey PRIMARY KEY (id);
 5   ALTER TABLE ONLY public.people DROP CONSTRAINT pkey;
       public         postgres    false    173    173            L           2606    16404    settings_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.settings DROP CONSTRAINT settings_pkey;
       public         postgres    false    171    171            �   5   x�3�L�L��L/JM���ͯJ,*��M�I�L���2�LJ����#�=... ���      �      x�3�L�,*.Q(��M�4����� >�     