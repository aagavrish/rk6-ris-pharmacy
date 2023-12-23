SELECT
    rep_year,
    rep_month,
    med_name,
    med_company,
    SUM(quantity) as amount,
    price
FROM
    reports_sales
    JOIN orders_by_users USING(order_id)
    JOIN medicines ON(med_ID = med_code)
WHERE
    rep_year = YEAR('$date-01')
    AND rep_month = MONTH('$date-01')
GROUP BY
    med_id,
    price
ORDER BY
    amount DESC