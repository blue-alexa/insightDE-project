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

CREATE INDEX cik_form_index ON filing_index (cik, form_type);

CREATE INDEX accession_no_index ON filing_index (accession_number);
