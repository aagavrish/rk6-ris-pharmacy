SELECT
    rep_year,
    rep_month
FROM
    reports_orders
WHERE
    rep_year = '$date-01'
    AND rep_month = '$date-01'