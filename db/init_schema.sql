CREATE TABLE
    sources (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL, -- e.g. 'avito', 'mubawab'
        url TEXT, -- optional: base URL of site
        created_at TIMESTAMP DEFAULT now ()
    );

-- Insert example sources
INSERT INTO
    sources (name, url)
VALUES
    ('avito', 'https://www.avito.ma'),
    ('mubawab', 'https://www.mubawab.ma');

-- Cities table
CREATE TABLE
    cities (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );

-- Neighborhoods table
CREATE TABLE
    neighborhoods (
        id SERIAL PRIMARY KEY,
        city_id INT NOT NULL REFERENCES cities (id) ON DELETE CASCADE,
        name VARCHAR(100) NOT NULL,
        UNIQUE (city_id, name) -- prevent duplicate neighborhood names in the same city
    );

-- Listings table
CREATE TABLE
    listings (
        id UUID PRIMARY KEY,
        source_id INT NOT NULL REFERENCES sources (id) ON DELETE CASCADE,
        title TEXT,
        description TEXT,
        price NUMERIC,
        currency VARCHAR(10) DEFAULT 'MAD',
        property_type VARCHAR(50),
        rooms INT,
        surface_m2 NUMERIC,
        city_id INT REFERENCES cities (id) ON DELETE SET NULL,
        neighborhood_id INT REFERENCES neighborhoods (id) ON DELETE SET NULL,
        publication_date TIMESTAMP, -- date of ad on Avito/Mubawab
        url TEXT
    );

-- Listings history table
CREATE TABLE
    listing_history (
        id UUID PRIMARY KEY,
        listing_id UUID NOT NULL REFERENCES listings (id) ON DELETE CASCADE,
        price NUMERIC,
        is_active BOOLEAN,
        scraped_at TIMESTAMP DEFAULT now ()
    );