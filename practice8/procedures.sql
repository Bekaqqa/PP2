--  Upsert
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE full_name = p_name) THEN
        UPDATE contacts SET phone_number = p_phone WHERE full_name = p_name;
    ELSE
        INSERT INTO contacts(full_name, phone_number)
        VALUES(p_name, p_phone);
    END IF;
END;
$$;


--  Delete
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE full_name = p_value OR phone_number = p_value;
END;
$$;


--  Bulk insert
CREATE OR REPLACE PROCEDURE insert_many(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^[0-9]+$' THEN
            INSERT INTO contacts(full_name, phone_number)
            VALUES(names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %', phones[i];
        END IF;
    END LOOP;
END;
$$;