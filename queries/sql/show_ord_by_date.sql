SELECT
    MONTH(conclusion_date) as month,
    YEAR(conclusion_date) as year,
    conclusion_date,
    sup_name,
    med_code,
    med_name,
    amount,
    price
FROM
    orders
    JOIN order_list USING (or_ID)
    JOIN suppliers ON (sup_id = sup_code)
    JOIN medicines ON (med_id = med_code)
WHERE
    MONTH(conclusion_date) = MONTH('$conclusion_date-01')
    AND YEAR(conclusion_date) = YEAR('$conclusion_date-01')