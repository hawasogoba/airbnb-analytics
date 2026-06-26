SELECT
    room_type,
    COUNT(*) AS nb_listings,
    AVG(price_clean) AS avg_price
FROM {{ ref('silver_listings') }}
GROUP BY room_type