-- seed.sql : Initial data for our haunted realm! 👻

-- Create admin user (password: admin1234)
INSERT INTO user (
    id, 
    username,
    email, 
    password_hash,
    first_name,
    last_name,
    is_admin,
    is_active,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin',
    'admin@hbnb.io',
    '$2b$12$MI0/rfWswl7cNCR8NP7gaOIEYmGeIdaX4GvoVExhU2xlH8mQW.8Qq',
    'Admin',
    'HBnB',
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Create initial amenities
INSERT INTO amenity (
    id, 
    name, 
    description, 
    category,
    created_at,
    updated_at
) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 
     'WiFi', 
     'High-speed wireless internet', 
     'comfort',
     CURRENT_TIMESTAMP,
     CURRENT_TIMESTAMP),
    ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 
     'Swimming Pool', 
     'Outdoor swimming pool', 
     'entertainment',
     CURRENT_TIMESTAMP,
     CURRENT_TIMESTAMP),
    ('6ba7b811-9dad-11d1-80b4-00c04fd430c9', 
     'Air Conditioning', 
     'Climate control system', 
     'comfort',
     CURRENT_TIMESTAMP,
     CURRENT_TIMESTAMP);