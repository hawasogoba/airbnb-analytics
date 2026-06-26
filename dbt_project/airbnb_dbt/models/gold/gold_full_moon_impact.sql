SELECT
    is_full_moon_night,
    sentiment,
    COUNT(*) AS nb_reviews
FROM {{ ref('silver_reviews') }}
GROUP BY is_full_moon_night, sentiment
ORDER BY is_full_moon_night, sentiment