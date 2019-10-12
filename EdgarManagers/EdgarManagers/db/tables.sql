DROP TABLE IF EXISTS filing_index;
CREATE TABLE filing_index(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cik VARCHAR(20),
    company_name VARCHAR(200),
    form_type VARCHAR(30),
    date_filed DATE,
    accession_number VARCHAR(100),
    url VARCHAR(200)
);

CREATE INDEX date_index ON filing_index (date_filed);

CREATE INDEX formtype_index ON filing_index (form_type);

CREATE INDEX cik_form_index ON filing_index (cik, form_type);

CREATE UNIQUE INDEX accession_no_index ON filing_index (accession_number);

DROP TABLE IF EXISTS history;
CREATE TABLE history(
    download_date DATE PRIMARY KEY,
    date_created DATE,
    date_modified DATE
);

##########################################
CREATE TABLE filing_index_copy(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cik VARCHAR(20),
    company_name VARCHAR(200),
    form_type VARCHAR(30),
    date_filed DATE,
    accession_number VARCHAR(100),
    url VARCHAR(200)
);
CREATE INDEX date_index ON filing_index_copy (date_filed);

CREATE INDEX formtype_index ON filing_index_copy (form_type);

CREATE INDEX cik_form_index ON filing_index_copy (cik, form_type);

CREATE UNIQUE INDEX accession_no_index ON filing_index_copy (accession_number);

INSERT IGNORE INTO filing_index_copy SELECT * FROM filing_index;
COMMIT
SELECT count(id) from filing_index;
SELECT count(id) from filing_index_copy;

RENAME TABLE filing_index TO dup, filing_index_copy TO filing_index;
DROP TABLE dup;

CREATE TABLE tmp SELECT *
FROM filing_index
GROUP BY accession_number;