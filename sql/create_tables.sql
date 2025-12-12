-- =====================================================
-- Wedding RSVP System - PostgreSQL Database Setup
-- =====================================================
-- Run this script in pgAdmin to set up your database
-- After running, update your Django settings.py with the connection info
-- =====================================================

-- Create the wedding database (run this separately if needed)
-- CREATE DATABASE wedding_db;

-- Connect to the database before running the rest
-- \c wedding_db

-- =====================================================
-- GUESTS TABLE - Main table for 550 guests
-- =====================================================
CREATE TABLE IF NOT EXISTS wedding_guest (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rsvp_code VARCHAR(8) UNIQUE NOT NULL,
    
    -- Guest Information
    name VARCHAR(200) NOT NULL,
    email VARCHAR(254),
    phone VARCHAR(20),
    party_name VARCHAR(200),
    max_guests INTEGER DEFAULT 1,
    
    -- Event Invitations (which events they're invited to)
    invited_mendhi BOOLEAN DEFAULT FALSE,
    invited_vidhi BOOLEAN DEFAULT FALSE,
    invited_wedding BOOLEAN DEFAULT FALSE,
    invited_reception BOOLEAN DEFAULT FALSE,
    
    -- RSVP Responses
    rsvp_mendhi VARCHAR(20) DEFAULT 'pending',
    rsvp_vidhi VARCHAR(20) DEFAULT 'pending',
    rsvp_wedding VARCHAR(20) DEFAULT 'pending',
    rsvp_reception VARCHAR(20) DEFAULT 'pending',
    
    -- Guest counts for each event
    guests_mendhi INTEGER DEFAULT 0,
    guests_vidhi INTEGER DEFAULT 0,
    guests_wedding INTEGER DEFAULT 0,
    guests_reception INTEGER DEFAULT 0,
    
    -- Additional Information
    dietary_requirements TEXT,
    message TEXT,
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    rsvp_submitted_at TIMESTAMP WITH TIME ZONE,
    last_viewed_at TIMESTAMP WITH TIME ZONE,
    
    -- Status
    has_responded BOOLEAN DEFAULT FALSE,
    
    -- Constraints
    CONSTRAINT rsvp_mendhi_check CHECK (rsvp_mendhi IN ('pending', 'attending', 'not_attending')),
    CONSTRAINT rsvp_vidhi_check CHECK (rsvp_vidhi IN ('pending', 'attending', 'not_attending')),
    CONSTRAINT rsvp_wedding_check CHECK (rsvp_wedding IN ('pending', 'attending', 'not_attending')),
    CONSTRAINT rsvp_reception_check CHECK (rsvp_reception IN ('pending', 'attending', 'not_attending'))
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_guest_rsvp_code ON wedding_guest(rsvp_code);
CREATE INDEX IF NOT EXISTS idx_guest_name ON wedding_guest(name);
CREATE INDEX IF NOT EXISTS idx_guest_email ON wedding_guest(email);
CREATE INDEX IF NOT EXISTS idx_guest_has_responded ON wedding_guest(has_responded);

-- =====================================================
-- EVENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS wedding_event (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(10),
    date DATE NOT NULL,
    time VARCHAR(50),
    venue_name VARCHAR(200),
    venue_address VARCHAR(300),
    description TEXT,
    dress_code VARCHAR(100),
    is_featured BOOLEAN DEFAULT FALSE,
    "order" INTEGER DEFAULT 0
);

-- Insert default events
INSERT INTO wedding_event (slug, name, icon, date, time, venue_name, venue_address, description, dress_code, is_featured, "order")
VALUES 
    ('mendhi', 'Mendhi', '✿', '2025-12-25', '4:00 PM onwards', 'The Garden Pavilion', '123 Celebration Lane, Mumbai', 'Join us for an evening of beautiful henna designs, music, and dance. Wear your brightest colors and get ready to celebrate!', 'Colorful Indian Attire', FALSE, 1),
    ('vidhi', 'Vidhi', '🪔', '2025-12-26', '10:00 AM - 2:00 PM', 'Family Residence', '456 Heritage Road, Mumbai', 'A sacred ceremony filled with traditional rituals and blessings. Join our families as we perform the pre-wedding ceremonies.', 'Traditional Indian Wear', FALSE, 2),
    ('wedding', 'Wedding', '💒', '2025-12-27', '6:00 PM onwards', 'The Grand Ballroom', '789 Royal Palace Hotel, Mumbai', 'The main event! Watch us exchange vows and become partners for life in a beautiful ceremony followed by dinner and celebrations.', 'Formal Indian / Western', TRUE, 3),
    ('reception', 'Reception', '🎉', '2025-12-28', '7:00 PM onwards', 'Starlight Terrace', '789 Royal Palace Hotel, Mumbai', 'Let''s dance the night away! Join us for an evening of dinner, drinks, music, and endless dancing as we celebrate our new beginning.', 'Glamorous Evening Wear', FALSE, 4)
ON CONFLICT (slug) DO NOTHING;

-- =====================================================
-- WEDDING INFO TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS wedding_weddinginfo (
    id SERIAL PRIMARY KEY,
    partner1_name VARCHAR(100) DEFAULT 'Sarah',
    partner2_name VARCHAR(100) DEFAULT 'Michael',
    wedding_date DATE NOT NULL,
    location VARCHAR(200) DEFAULT 'Mumbai, India',
    hashtag VARCHAR(100) DEFAULT '#SarahAndMichaelForever',
    welcome_title VARCHAR(200) DEFAULT 'Welcome to Our Wedding',
    welcome_message TEXT
);

-- =====================================================
-- STORY MILESTONES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS wedding_storymilestone (
    id SERIAL PRIMARY KEY,
    year VARCHAR(10) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    "order" INTEGER DEFAULT 0
);

-- Insert default story milestones
INSERT INTO wedding_storymilestone (year, title, description, "order")
VALUES 
    ('2018', 'How We Met', 'It all started at a mutual friend''s birthday party. Across a crowded room, our eyes met, and we knew something magical was beginning.', 1),
    ('2019', 'The First Date', 'Our first official date was at a cozy café downtown. We were both so nervous, but within minutes, it felt like we had known each other forever.', 2),
    ('2021', 'Moving In Together', 'After two wonderful years of dating, we decided to take the next step. We found our perfect little apartment and started building our life together.', 3),
    ('2024', 'The Proposal', 'On a beautiful sunset evening at our favorite beach, Michael got down on one knee and asked the question that would change our lives forever.', 4),
    ('2025', 'Forever Begins', 'And now, we''re ready to begin our forever journey together. We can''t wait to celebrate this new chapter with all of you.', 5)
ON CONFLICT DO NOTHING;

-- =====================================================
-- FUNCTION: Generate RSVP Code
-- =====================================================
CREATE OR REPLACE FUNCTION generate_rsvp_code()
RETURNS VARCHAR(8) AS $$
DECLARE
    chars VARCHAR := 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
    result VARCHAR(8) := '';
    i INTEGER;
BEGIN
    FOR i IN 1..8 LOOP
        result := result || substr(chars, floor(random() * length(chars) + 1)::integer, 1);
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- VIEWS FOR REPORTING
-- =====================================================

-- View: RSVP Summary by Event
CREATE OR REPLACE VIEW rsvp_summary AS
SELECT 
    'Mendhi' as event_name,
    COUNT(*) FILTER (WHERE invited_mendhi = TRUE) as total_invited,
    COUNT(*) FILTER (WHERE invited_mendhi = TRUE AND rsvp_mendhi = 'attending') as attending,
    COUNT(*) FILTER (WHERE invited_mendhi = TRUE AND rsvp_mendhi = 'not_attending') as declined,
    COUNT(*) FILTER (WHERE invited_mendhi = TRUE AND rsvp_mendhi = 'pending') as pending,
    COALESCE(SUM(guests_mendhi) FILTER (WHERE rsvp_mendhi = 'attending'), 0) as total_guests
FROM wedding_guest
UNION ALL
SELECT 
    'Vidhi',
    COUNT(*) FILTER (WHERE invited_vidhi = TRUE),
    COUNT(*) FILTER (WHERE invited_vidhi = TRUE AND rsvp_vidhi = 'attending'),
    COUNT(*) FILTER (WHERE invited_vidhi = TRUE AND rsvp_vidhi = 'not_attending'),
    COUNT(*) FILTER (WHERE invited_vidhi = TRUE AND rsvp_vidhi = 'pending'),
    COALESCE(SUM(guests_vidhi) FILTER (WHERE rsvp_vidhi = 'attending'), 0)
FROM wedding_guest
UNION ALL
SELECT 
    'Wedding',
    COUNT(*) FILTER (WHERE invited_wedding = TRUE),
    COUNT(*) FILTER (WHERE invited_wedding = TRUE AND rsvp_wedding = 'attending'),
    COUNT(*) FILTER (WHERE invited_wedding = TRUE AND rsvp_wedding = 'not_attending'),
    COUNT(*) FILTER (WHERE invited_wedding = TRUE AND rsvp_wedding = 'pending'),
    COALESCE(SUM(guests_wedding) FILTER (WHERE rsvp_wedding = 'attending'), 0)
FROM wedding_guest
UNION ALL
SELECT 
    'Reception',
    COUNT(*) FILTER (WHERE invited_reception = TRUE),
    COUNT(*) FILTER (WHERE invited_reception = TRUE AND rsvp_reception = 'attending'),
    COUNT(*) FILTER (WHERE invited_reception = TRUE AND rsvp_reception = 'not_attending'),
    COUNT(*) FILTER (WHERE invited_reception = TRUE AND rsvp_reception = 'pending'),
    COALESCE(SUM(guests_reception) FILTER (WHERE rsvp_reception = 'attending'), 0)
FROM wedding_guest;

-- View: Pending RSVPs
CREATE OR REPLACE VIEW pending_rsvps AS
SELECT name, email, rsvp_code, party_name, max_guests,
       invited_mendhi, invited_vidhi, invited_wedding, invited_reception,
       created_at
FROM wedding_guest
WHERE has_responded = FALSE
ORDER BY name;

-- View: Recent RSVPs
CREATE OR REPLACE VIEW recent_rsvps AS
SELECT name, email, rsvp_code, 
       rsvp_mendhi, rsvp_vidhi, rsvp_wedding, rsvp_reception,
       guests_mendhi, guests_vidhi, guests_wedding, guests_reception,
       rsvp_submitted_at, message
FROM wedding_guest
WHERE has_responded = TRUE
ORDER BY rsvp_submitted_at DESC
LIMIT 50;

-- =====================================================
-- SAMPLE: Import guests (modify and run as needed)
-- =====================================================
-- Example of inserting a guest directly:
/*
INSERT INTO wedding_guest (
    rsvp_code, name, email, phone, party_name, max_guests,
    invited_mendhi, invited_vidhi, invited_wedding, invited_reception
) VALUES (
    generate_rsvp_code(),
    'Guest Name',
    'guest@email.com',
    '9876543210',
    'The Guest Family',
    4,
    TRUE, TRUE, TRUE, TRUE
);
*/

-- =====================================================
-- GRANT PERMISSIONS (adjust username as needed)
-- =====================================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_django_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_django_user;

