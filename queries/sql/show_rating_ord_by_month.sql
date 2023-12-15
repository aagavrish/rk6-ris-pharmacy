SELECT
    med_code,
    med_name,
    med_group,
    med_company,
    med_country,
    SUM(amount) as sum,
    price,
    MAX(conclusion_date) as conclusion_date,
    YEAR(conclusion_date) as year,
    MONTH(conclusion_date) as month
FROM
    orders
    JOIN order_list USING(or_id)
    JOIN medicines ON(med_ID = med_code)
WHERE
    YEAR(conclusion_date) = YEAR('$date-01')
    AND MONTH(conclusion_date) = MONTH('$date-01')
GROUP BY
    med_code,
    med_name,
    med_group,
    med_company,
    med_country
ORDER BY
    sum DESC
LIMIT
    $limit