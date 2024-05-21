
CREATE MATERIALIZED VIEW IF NOT EXISTS public.mv_currency_exchange_rate_monthly_agg
AS
 SELECT currency_symbol,
    EXTRACT(year FROM currency_date) AS currency_year,
    EXTRACT(month FROM currency_date) AS currency_month,
    min(currency_rate) AS currency_rate_min,
    max(currency_rate) AS currency_rate_max,
    avg(currency_rate) AS currency_rate_avg
   FROM currency_exchange_rate
  GROUP BY currency_symbol, (EXTRACT(year FROM currency_date)), (EXTRACT(month FROM currency_date))