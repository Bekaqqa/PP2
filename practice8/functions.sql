--  Поиск
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT contact_id, full_name, phone_number
    FROM contacts
    WHERE full_name ILIKE '%' || p_pattern || '%'
       OR phone_number ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;


--  Пагинация
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT contact_id, full_name, phone_number
    FROM contacts
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;