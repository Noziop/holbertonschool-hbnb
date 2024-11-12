-- schema.sql : Where haunted tables come to life! 👻
-- This SQLite database will be created at: part3/instance/hbnb.db

-- Create Enums (en SQLite on utilise CHECK constraints)
CREATE TABLE IF NOT EXISTS user (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    address VARCHAR(200),
    postal_code VARCHAR(20),
    city VARCHAR(100),
    phone VARCHAR(20),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS place (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    owner_id VARCHAR(36) NOT NULL,
    price_by_night FLOAT NOT NULL,
    number_rooms INTEGER NOT NULL DEFAULT 1,
    number_bathrooms INTEGER NOT NULL DEFAULT 1,
    max_guest INTEGER NOT NULL DEFAULT 2,
    latitude FLOAT,
    longitude FLOAT,
    city VARCHAR(100),
    country VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'active' 
        CHECK (status IN ('active', 'maintenance', 'blocked')),
    property_type VARCHAR(20) NOT NULL DEFAULT 'apartment'
        CHECK (property_type IN ('house', 'apartment', 'villa')),
    minimum_stay INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (owner_id) REFERENCES user(id)
);

-- Reviews table with rating enum
CREATE TABLE IF NOT EXISTS review (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36),  -- Nullable pour l'anonymisation
    text TEXT NOT NULL,
    rating VARCHAR(1) CHECK (rating IN ('1', '2', '3', '4', '5')),
    FOREIGN KEY (place_id) REFERENCES place(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Amenities table with category enum
CREATE TABLE IF NOT EXISTS amenity (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category VARCHAR(20) NOT NULL DEFAULT 'supernatural'
        CHECK (category IN ('safety', 'comfort', 'entertainment', 'supernatural', 'blocked'))
);

-- Place-Amenity association table
CREATE TABLE IF NOT EXISTS placeamenity (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES place(id),
    FOREIGN KEY (amenity_id) REFERENCES amenity(id),
    UNIQUE(place_id, amenity_id)
);