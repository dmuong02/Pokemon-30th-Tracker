CREATE TABLE sets (
    set_id        TEXT PRIMARY KEY,
    set_name      TEXT NOT NULL,
    release_date  DATE
);

CREATE TABLE cards (
    card_id       TEXT PRIMARY KEY,
    set_id        TEXT NOT NULL REFERENCES sets(set_id),
    card_name     TEXT NOT NULL,
    card_number   TEXT,
    rarity        TEXT,
    printing      TEXT,
    illustrator   TEXT,
    tcgplayer_id  TEXT
);

CREATE TABLE price_history (
    card_id     TEXT NOT NULL REFERENCES cards(card_id),
    price_date  DATE NOT NULL,
    price_usd   NUMERIC(10, 2) NOT NULL,
    loaded_at   TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (card_id, price_date)
);