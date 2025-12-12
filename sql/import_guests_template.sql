-- =====================================================
-- BULK IMPORT GUESTS INTO PostgreSQL
-- =====================================================
-- This template shows how to import your 550 guests
-- 
-- Option 1: Copy from CSV (recommended for large imports)
-- Option 2: Individual INSERT statements
-- =====================================================

-- =====================================================
-- OPTION 1: COPY FROM CSV (Fastest method)
-- =====================================================
-- First, create your CSV file with these columns (no header):
-- rsvp_code,name,email,phone,party_name,max_guests,invited_mendhi,invited_vidhi,invited_wedding,invited_reception

-- Generate RSVP codes first in Excel/Sheets using: =UPPER(RANDBETWEEN(CONCAT(CHAR(RANDBETWEEN(65,90)),CHAR(RANDBETWEEN(50,57))))...)
-- Or leave blank and use the function below

-- Run this COPY command (update the path to your CSV):
/*
COPY wedding_guest (name, email, phone, party_name, max_guests, invited_mendhi, invited_vidhi, invited_wedding, invited_reception)
FROM '/path/to/your/guests.csv'
WITH (FORMAT csv, HEADER true);

-- Then generate RSVP codes for any that don't have them:
UPDATE wedding_guest 
SET rsvp_code = generate_rsvp_code() 
WHERE rsvp_code IS NULL OR rsvp_code = '';
*/

-- =====================================================
-- OPTION 2: INSERT STATEMENTS
-- =====================================================
-- Use this format to add guests individually or in batches

-- Guests invited to ALL events (Family & Close Friends)
INSERT INTO wedding_guest (rsvp_code, name, email, phone, party_name, max_guests, invited_mendhi, invited_vidhi, invited_wedding, invited_reception)
VALUES
    (generate_rsvp_code(), 'Sharma Family', 'sharma@email.com', '9876543210', 'The Sharma Family', 4, TRUE, TRUE, TRUE, TRUE),
    (generate_rsvp_code(), 'Patel Family', 'patel@email.com', '9876543211', 'The Patel Family', 5, TRUE, TRUE, TRUE, TRUE),
    (generate_rsvp_code(), 'Mehta Family', 'mehta@email.com', '9876543212', 'The Mehta Family', 4, TRUE, TRUE, TRUE, TRUE),
    (generate_rsvp_code(), 'Desai Family', 'desai@email.com', '9876543213', 'The Desai Family', 3, TRUE, TRUE, TRUE, TRUE),
    (generate_rsvp_code(), 'Kumar Family', 'kumar@email.com', '9876543214', 'The Kumar Family', 4, TRUE, TRUE, TRUE, TRUE);

-- Guests invited to WEDDING & RECEPTION only (Extended Family/Friends)
INSERT INTO wedding_guest (rsvp_code, name, email, phone, party_name, max_guests, invited_mendhi, invited_vidhi, invited_wedding, invited_reception)
VALUES
    (generate_rsvp_code(), 'John Smith', 'john.smith@email.com', '9876543220', '', 2, FALSE, FALSE, TRUE, TRUE),
    (generate_rsvp_code(), 'Priya Verma', 'priya.verma@email.com', '9876543221', '', 2, FALSE, FALSE, TRUE, TRUE),
    (generate_rsvp_code(), 'Raj Kapoor', 'raj.kapoor@email.com', '9876543222', '', 2, FALSE, FALSE, TRUE, TRUE),
    (generate_rsvp_code(), 'Anita Gupta', 'anita.gupta@email.com', '9876543223', '', 1, FALSE, FALSE, TRUE, TRUE);

-- Guests invited to RECEPTION only (Colleagues/Acquaintances)
INSERT INTO wedding_guest (rsvp_code, name, email, phone, party_name, max_guests, invited_mendhi, invited_vidhi, invited_wedding, invited_reception)
VALUES
    (generate_rsvp_code(), 'Office Team Lead', 'lead@company.com', '9876543230', '', 1, FALSE, FALSE, FALSE, TRUE),
    (generate_rsvp_code(), 'College Friend', 'friend@email.com', '9876543231', '', 2, FALSE, FALSE, FALSE, TRUE);

-- =====================================================
-- VERIFY IMPORT
-- =====================================================
-- Check total count
SELECT COUNT(*) as total_guests FROM wedding_guest;

-- Check by invitation type
SELECT 
    SUM(CASE WHEN invited_mendhi AND invited_vidhi AND invited_wedding AND invited_reception THEN 1 ELSE 0 END) as all_events,
    SUM(CASE WHEN NOT invited_mendhi AND NOT invited_vidhi AND invited_wedding AND invited_reception THEN 1 ELSE 0 END) as wedding_reception_only,
    SUM(CASE WHEN NOT invited_mendhi AND NOT invited_vidhi AND NOT invited_wedding AND invited_reception THEN 1 ELSE 0 END) as reception_only
FROM wedding_guest;

-- Verify all have unique RSVP codes
SELECT rsvp_code, COUNT(*) 
FROM wedding_guest 
GROUP BY rsvp_code 
HAVING COUNT(*) > 1;

-- =====================================================
-- USEFUL QUERIES
-- =====================================================

-- Get all RSVP codes with names (for invitation printing)
SELECT name, rsvp_code, email, 
       CONCAT(
           CASE WHEN invited_mendhi THEN 'M' ELSE '' END,
           CASE WHEN invited_vidhi THEN 'V' ELSE '' END,
           CASE WHEN invited_wedding THEN 'W' ELSE '' END,
           CASE WHEN invited_reception THEN 'R' ELSE '' END
       ) as invited_to
FROM wedding_guest
ORDER BY name;

-- Export for mail merge
SELECT name, email, rsvp_code,
       CONCAT('https://yourwebsite.com/rsvp/', rsvp_code, '/') as rsvp_link
FROM wedding_guest
WHERE email IS NOT NULL AND email != ''
ORDER BY name;

-- Check RSVP summary
SELECT * FROM rsvp_summary;

-- View pending responses
SELECT * FROM pending_rsvps;

-- View recent responses  
SELECT * FROM recent_rsvps;

