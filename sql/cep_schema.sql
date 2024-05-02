
CREATE TABLE IF NOT EXISTS public.ect_pais
(
    pai_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    pai_sg_alternativa character varying(3) COLLATE pg_catalog."default",
    pai_no_portugues character varying(72) COLLATE pg_catalog."default",
    pai_no_ingles character varying(72) COLLATE pg_catalog."default",
    pai_no_frances character varying(72) COLLATE pg_catalog."default",
    pai_abreviatura character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT ect_pais_pkey PRIMARY KEY (pai_sg)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.ect_pais OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_bairro
(
    bai_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    bai_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    bai_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT log_bairro_pkey PRIMARY KEY (bai_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_bairro OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_cpc
(
    cpc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    cpc_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    cpc_endereco character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cep character varying(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_cpc_pkey PRIMARY KEY (cpc_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_cpc OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_faixa_bairro
(
    bai_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    fcb_cep_ini character varying(8) COLLATE pg_catalog."default" NOT NULL,
    fcb_cep_fim character varying(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_faixa_bairro_pkey PRIMARY KEY (bai_nu, fcb_cep_ini)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_faixa_bairro OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_faixa_cpc
(
    cpc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    cpc_inicial character varying(6) COLLATE pg_catalog."default" NOT NULL,
    cpc_final character varying(6) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_faixa_cpc_pkey PRIMARY KEY (cpc_nu, cpc_inicial)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_faixa_cpc OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_faixa_localidade
(
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    loc_cep_ini character varying(8) COLLATE pg_catalog."default" NOT NULL,
    loc_cep_fim character varying(8) COLLATE pg_catalog."default",
    loc_tipo_faixa character varying(1) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_faixa_localidade_pkey PRIMARY KEY (loc_nu, loc_cep_ini, loc_tipo_faixa)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_faixa_localidade OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_faixa_uf
(
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    ufe_cep_ini character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_cep_fim character varying(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_faixa_uf_pkey PRIMARY KEY (ufe_sg, ufe_cep_ini, ufe_cep_fim)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_faixa_uf OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_faixa_uop
(
    uop_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    fnc_inicial character varying(8) COLLATE pg_catalog."default" NOT NULL,
    fnc_final character varying(8) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_faixa_uop_pkey PRIMARY KEY (uop_nu, fnc_inicial)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_faixa_uop OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_grande_usuario
(
    gru_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    bai_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    log_nu character varying(8) COLLATE pg_catalog."default",
    gru_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    gru_endereco character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cep character varying(8) COLLATE pg_catalog."default" NOT NULL,
    gru_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT log_grande_usuario_pkey PRIMARY KEY (gru_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_grande_usuario OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_localidade
(
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    loc_no character varying(72) COLLATE pg_catalog."default" NOT NULL,
    cep character varying(8) COLLATE pg_catalog."default",
    loc_in_sit character varying(1) COLLATE pg_catalog."default" NOT NULL,
    loc_in_tipo_loc character varying(1) COLLATE pg_catalog."default" NOT NULL,
    loc_nu_sub character varying(8) COLLATE pg_catalog."default",
    loc_no_abrev character varying(36) COLLATE pg_catalog."default",
    mun_nu character varying(7) COLLATE pg_catalog."default",
    CONSTRAINT log_localidade_pkey PRIMARY KEY (loc_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_localidade OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_logradouro
(
    log_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    bai_nu_ini character varying(8) COLLATE pg_catalog."default" NOT NULL,
    bai_nu_fim character varying(8) COLLATE pg_catalog."default",
    log_no character varying(100) COLLATE pg_catalog."default" NOT NULL,
    log_complemento character varying(100) COLLATE pg_catalog."default",
    cep character varying(8) COLLATE pg_catalog."default" NOT NULL,
    tlo_tx character varying(36) COLLATE pg_catalog."default" NOT NULL,
    log_sta_tlo character varying(1) COLLATE pg_catalog."default",
    log_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT log_logradouro_pkey PRIMARY KEY (log_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_logradouro OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_num_sec
(
    log_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    sec_nu_ini character varying(10) COLLATE pg_catalog."default" NOT NULL,
    sec_nu_fim character varying(10) COLLATE pg_catalog."default" NOT NULL,
    sec_in_lado character varying(1) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_num_sec_pkey PRIMARY KEY (log_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_num_sec OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_unid_oper
(
    uop_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    ufe_sg character varying(2) COLLATE pg_catalog."default" NOT NULL,
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    bai_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    log_nu character varying(8) COLLATE pg_catalog."default",
    uop_no character varying(100) COLLATE pg_catalog."default" NOT NULL,
    uop_endereco character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cep character varying(8) COLLATE pg_catalog."default" NOT NULL,
    uop_in_cp character varying(1) COLLATE pg_catalog."default" NOT NULL,
    uop_no_abrev character varying(36) COLLATE pg_catalog."default",
    CONSTRAINT log_unid_oper_pkey PRIMARY KEY (uop_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_unid_oper OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_var_bai
(
    bai_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    vdb_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    vdb_tx character varying(72) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_var_bai_pkey PRIMARY KEY (bai_nu, vdb_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_var_bai OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_var_loc
(
    loc_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    val_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    val_txt character varying(72) COLLATE pg_catalog."default",
    CONSTRAINT log_var_loc_pkey PRIMARY KEY (loc_nu, val_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_var_loc OWNER to airflow;

CREATE TABLE IF NOT EXISTS public.log_var_log
(
    log_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    vlo_nu character varying(8) COLLATE pg_catalog."default" NOT NULL,
    tlo_tx character varying(36) COLLATE pg_catalog."default" NOT NULL,
    vlo_no character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT log_var_log_pkey PRIMARY KEY (log_nu, vlo_nu)
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.log_var_log OWNER to airflow;

TRUNCATE log_bairro;
TRUNCATE log_cpc;
TRUNCATE log_faixa_bairro;
TRUNCATE log_faixa_cpc;
TRUNCATE log_faixa_localidade;
TRUNCATE log_faixa_uf;
TRUNCATE log_faixa_uop;
TRUNCATE log_grande_usuario;
TRUNCATE log_localidade;
TRUNCATE log_logradouro;
TRUNCATE log_num_sec;
TRUNCATE log_unid_oper;
TRUNCATE log_var_bai;
TRUNCATE log_var_loc;
TRUNCATE log_var_log;
TRUNCATE ect_pais;
