DROP TABLE IF EXISTS history;
CREATE TABLE history(
    download_date DATE PRIMARY KEY,
    date_created DATE,
    date_modified DATE
);

DROP TABLE IF EXISTS form_parsers;
CREATE TABLE form_parsers(
    form_type VARCHAR(30) PRIMARY KEY,
    code TEXT,
    date_created DATE,
    date_modified DATE
);