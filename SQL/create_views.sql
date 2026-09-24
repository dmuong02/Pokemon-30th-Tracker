-- One row per card per day, with all card details attached
CREATE OR REPLACE VIEW v_card_prices AS
SELECT
    p.price_date,
    c.card_id,
    c.card_name,
    c.card_number,
    c.rarity,
    c.illustrator,
    s.set_name,
    p.price_usd,
    p.price_date - s.release_date AS days_since_release
FROM price_history p
JOIN cards c ON c.card_id = p.card_id
JOIN sets s ON s.set_id = c.set_id;

-- One row per card: first price on or after release day vs. latest price
CREATE OR REPLACE VIEW v_card_summary AS
WITH ranked AS (
    SELECT
        p.card_id,
        p.price_date,
        p.price_usd,
        ROW_NUMBER() OVER (PARTITION BY p.card_id ORDER BY p.price_date ASC)  AS first_rank,
        ROW_NUMBER() OVER (PARTITION BY p.card_id ORDER BY p.price_date DESC) AS last_rank
    FROM price_history p
    JOIN cards c ON c.card_id = p.card_id
    JOIN sets s ON s.set_id = c.set_id
    WHERE p.price_date >= s.release_date
)
SELECT
    c.card_id,
    c.card_name,
    c.card_number,
    c.rarity,
    c.illustrator,
    s.set_name,
    f.price_usd AS release_price,
    l.price_usd AS latest_price,
    l.price_date AS latest_date,
    l.price_usd - f.price_usd AS change_usd,
    ROUND((l.price_usd - f.price_usd) / NULLIF(f.price_usd, 0) * 100, 1) AS change_pct
FROM cards c
JOIN sets s ON s.set_id = c.set_id
JOIN ranked f ON f.card_id = c.card_id AND f.first_rank = 1
JOIN ranked l ON l.card_id = c.card_id AND l.last_rank = 1;