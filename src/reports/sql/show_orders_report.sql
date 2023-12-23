SELECT
    rep_year,
    rep_month,
    sup_name,
    med_ID,
    amount,
    price
FROM
    reports_orders
    JOIN orders USING(or_id)
    JOIN order_list USING(or_id)
    JOIN suppliers ON(sup_id = sup_code)
    JOIN medicines ON(med_id = med_code)
WHERE
    rep_year = YEAR('$date-01')
    AND rep_month = MONTH('$date-01')
GROUP BY
    sup_ID,
    med_id,
    price