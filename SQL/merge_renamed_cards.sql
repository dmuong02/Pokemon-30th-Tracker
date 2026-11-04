CREATE TABLE card_id_map (
  old_id TEXT PRIMARY KEY,
  new_id TEXT NOT NULL
);

INSERT INTO card_id_map (old_id, new_id) VALUES
('pokemon-me-30th-celebration-greninja-ex-double-rare', 'pokemon-me-30th-celebration-greninja-ex-021-128-double-rare'),
('pokemon-me-30th-celebration-sylveon-ex-double-rare', 'pokemon-me-30th-celebration-sylveon-ex-071-128-double-rare'),
('pokemon-me-30th-celebration-gengar-ex', 'pokemon-me-30th-celebration-gengar-ex-090-128-double-rare'),
('pokemon-me-30th-celebration-kommo-o', 'pokemon-me-30th-celebration-kommo-o-112-128-common'),
('pokemon-me-30th-celebration-lapras-illustration-rare', 'pokemon-me-30th-celebration-lapras-131-128-illustration-rare'),
('pokemon-me-30th-celebration-drifloon-illustration-rare', 'pokemon-me-30th-celebration-drifloon-136-128-illustration-rare'),
('pokemon-me-30th-celebration-lycanroc-illustration-rare', 'pokemon-me-30th-celebration-lycanroc-138-128-illustration-rare'),
('pokemon-me-30th-celebration-alolan-meowth-139-128-common', 'pokemon-me-30th-celebration-alolan-meowth-139-128-illustration-rare'),
('pokemon-me-30th-celebration-hisuian-zorua-illustration-rare', 'pokemon-me-30th-celebration-hisuian-zorua-145-128-illustration-rare'),
('pokemon-me-30th-celebration-mewtwo-ex-futuristic-rare', 'pokemon-me-30th-celebration-mewtwo-ex-157-128-futuristic-rare'),
('pokemon-me-30th-celebration-mew-ex-futuristic-rare', 'pokemon-me-30th-celebration-mew-ex-158-128-futuristic-rare'),
('pokemon-me-30th-celebration-mew-b-rgb-holo-rare', 'pokemon-me-30th-celebration-mew-b-rgb-rgb-rare'),
('pokemon-me-30th-celebration-mew-g-rgb-holo-rare', 'pokemon-me-30th-celebration-mew-g-rgb-rgb-rare'),
('pokemon-me-30th-celebration-mew-r-rgb-holo-rare', 'pokemon-me-30th-celebration-mew-r-rgb-rgb-rare'),
('pokemon-me-30th-celebration-classic-collection-n-classic-collection', 'pokemon-me-30th-celebration-classic-collection-n-supporter-classic-collection');

BEGIN;

-- 1. Copy the clean name, number, and illustrator from each old ID to its new ID
UPDATE cards AS new_card
SET card_name   = old_card.card_name,
    card_number = old_card.card_number,
    illustrator = old_card.illustrator
FROM card_id_map AS m
JOIN cards AS old_card ON old_card.card_id = m.old_id
WHERE new_card.card_id = m.new_id;

-- 2. Move over the price days only the old ID has (skip days the new ID already covers)
INSERT INTO price_history (card_id, price_date, price_usd)
SELECT m.new_id, ph.price_date, ph.price_usd
FROM price_history AS ph
JOIN card_id_map AS m ON m.old_id = ph.card_id
ON CONFLICT (card_id, price_date) DO NOTHING;

-- 3. Delete the old IDs (prices first, then the cards)
DELETE FROM price_history WHERE card_id IN (SELECT old_id FROM card_id_map);
DELETE FROM cards WHERE card_id IN (SELECT old_id FROM card_id_map);

COMMIT;