DROP TABLE IF EXISTS filing_index;
CREATE TABLE filing_index(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cik VARCHAR(20),
    company_name VARCHAR(200),
    form_type VARCHAR(30),
    date_filed DATE,
    accession_number VARCHAR(100) UNIQUE KEY,
    url VARCHAR(200)
);

CREATE INDEX date_index ON filing_index (date_filed);

CREATE INDEX formtype_index ON filing_index (form_type);

CREATE INDEX cik_index ON filing_index (cik);

DROP TABLE IF EXISTS history;
CREATE TABLE history(
    download_date DATE PRIMARY KEY,
    date_created DATE,
    date_modified DATE
);

