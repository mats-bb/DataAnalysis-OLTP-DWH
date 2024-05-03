DROP PROCEDURE insert_customer_data(jsonb);

CREATE OR REPLACE PROCEDURE insert_customer_data(json_data JSONB)
LANGUAGE plpgsql
AS $$
DECLARE	
    address_name_param TEXT;
    city_name_param TEXT;
    state_name_param TEXT;
    state_id_param INT;
    city_id_param INT;
    address_id_param INT;
   	zip_code_param INT;
   	customer_id_param INT;
BEGIN
    -- Extract JSON fields
    address_name_param := json_data->>'address';
    city_name_param := json_data->>'city';
    state_name_param := json_data->>'state';
   	zip_code_param := json_data->>'zip';
    
	-- Check if state exists, if not, insert
	SELECT id INTO state_id_param FROM state
	WHERE state_name = state_name_param;

	IF state_id_param IS NULL THEN
		INSERT INTO state (state_name)
		VALUES (state_name_param)
		RETURNING id INTO state_id_param;
	END IF;
	   
	-- Check if city exists, if not, insert
	SELECT id INTO city_id_param FROM city
	WHERE city_name = city_name_param;

	IF city_id_param IS NULL THEN
		INSERT INTO city (city_name, state_id)
		VALUES (city_name_param, state_id_param)
		RETURNING id INTO city_id_param;
	END IF;

	-- Check if address exists, if not, insert
	SELECT id INTO address_id_param FROM address
	WHERE street_address = address_name_param;

	IF address_id_param IS NULL THEN
		INSERT INTO address (street_address, zip_code, city_id)
		VALUES (address_name_param, zip_code_param, city_id_param)
		RETURNING id INTO address_id_param;
	END IF;

	-- Insert customer
	INSERT INTO customer (first_name, last_name, email, PASSWORD, mobile_num)
	VALUES (json_data->>'first_name' , json_data->>'last_name', json_data->>'email', json_data->>'password', json_data->>'mobile_num')
	RETURNING id INTO customer_id_param;

	-- Insert customer_address
	INSERT INTO customer_address (customer_id, address_id)
	VALUES (customer_id_param, address_id_param);
	
	-- Insert card_info
	INSERT INTO card_info (card_number, cardholder_first_name, cardholder_last_name, expiration_date, cvv, payment_provider_id, customer_id)
	VALUES (json_data->'card_info'->>'card_number', json_data->>'first_name', json_data->>'last_name', json_data->'card_info'->>'expr_date'::text, json_data->'card_info'->>'cvv', 1, customer_id_param);
   
END;
$$;

