
DROP DATABASE IF EXISTS authdb_dev;

ALTER USER postgres WITH PASSWORD 'password';
-- DDL
CREATE DATABASE authdb_dev
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\c authdb_dev;

CREATE TABLE public.clients
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "ClientId" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "ClientSecret" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "IsAdmin" boolean NOT NULL,
    CONSTRAINT clients_pkey PRIMARY KEY ("Id"),
    CONSTRAINT "ClientId" UNIQUE ("ClientId")
)

-- CREATE TABLE public.blacklist
-- (
--     token character varying(256) COLLATE pg_catalog."default" NOT NULL
-- )