CREATE TABLE IF NOT EXISTS public.currency_exchange_rate
(
    currency_symbol character varying COLLATE pg_catalog."default" NOT NULL,
    currency_date date NOT NULL,
    currency_rate double precision NOT NULL,
    load_timestamp timestamp without time zone NOT NULL,
    CONSTRAINT currency_exchange_rate_pkey PRIMARY KEY (currency_symbol, currency_date)
)
