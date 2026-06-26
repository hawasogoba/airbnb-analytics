SELECT
    *,
    TRY_CAST(REPLACE(REPLACE(price, '$', ''), ',', '') AS DOUBLE) AS price_clean
FROM {{ source('bronze', 'bronze_listings') }}
WHERE id IS NOT NULL