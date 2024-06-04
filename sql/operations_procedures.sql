-- INSERT CUSTOMER DATA
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
    dob_param DATE;
    created_date_param DATE;
BEGIN
    -- Extract JSON fields
    address_name_param := json_data->>'address';
    city_name_param := json_data->>'city';
    state_name_param := json_data->>'state';
   	zip_code_param := json_data->>'zip';
    dob_param := json_data->>'DOB';
    created_date_param := json_data->>'account_created_date';
    
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
	INSERT INTO customer (first_name, last_name, dob, email, PASSWORD, mobile_num, created_date)
	VALUES (json_data->>'first_name', json_data->>'last_name', dob_param, json_data->>'email', json_data->>'password', json_data->>'mobile_num', created_date_param)
	RETURNING id INTO customer_id_param;

	-- Insert customer_address
	INSERT INTO customer_address (customer_id, address_id)
	VALUES (customer_id_param, address_id_param);
	
	-- Insert card_info
	INSERT INTO card_info (card_number, cardholder_first_name, cardholder_last_name, expiration_date, cvv, payment_provider_id, customer_id)
	VALUES (json_data->'card_info'->>'card_number', json_data->>'first_name', json_data->>'last_name', json_data->'card_info'->>'expr_date'::text, json_data->'card_info'->>'cvv', 1, customer_id_param);
   
END;
$$;


-- INSERT PRODUCT DATA
DROP PROCEDURE insert_product_data(jsonb);

CREATE OR REPLACE PROCEDURE insert_product_data(json_data jsonb)
LANGUAGE plpgsql
AS $$
DECLARE
    main_cat_id_param INT;
    type_cat_id_param INT;
    prod_cat_id_param INT;
    producer_id_param INT;
    product_id_param INT;
    main_category_name_param TEXT;
    type_category_name_param TEXT;
    product_category_name_param TEXT;
    producer_name_param TEXT;
    product_name_param TEXT;
    product_description_param TEXT;
    price_param INT;
    specs_param JSONB;
    sku_param TEXT;
    mpn_param TEXT;
    quantity_param INT;
  
   
BEGIN
    -- Extract json data fields
	main_category_name_param = json_data->>'main_category_name';
    type_category_name_param = json_data->>'type_category_name';
    product_category_name_param = json_data->>'product_category_name';
    producer_name_param = json_data->>'producer_name';
    product_name_param = json_data->>'product_name';
    product_description_param = json_data->>'product_description';
    price_param = json_data->>'price';
    specs_param = json_data->>'specs';
    sku_param = json_data->>'sku';
    mpn_param = json_data->>'mpn';
    quantity_param = json_data->>'quantity';
  
    -- Main category
    SELECT id INTO main_cat_id_param FROM main_category WHERE category_name = main_category_name_param;
       
    IF main_cat_id_param IS NULL THEN
        INSERT INTO main_category (category_name)
        VALUES (main_category_name_param) RETURNING id INTO main_cat_id_param;
    END IF;

    -- Type category
    SELECT id INTO type_cat_id_param FROM type_category WHERE category_name = type_category_name_param;

    IF type_cat_id_param IS NULL THEN
        INSERT INTO type_category (category_name, main_cat_id)
        VALUES (type_category_name_param, main_cat_id_param) RETURNING id INTO type_cat_id_param;
    END IF;

    -- Product category
    SELECT id INTO prod_cat_id_param FROM product_category WHERE category_name = product_category_name_param;

    IF prod_cat_id_param IS NULL THEN
        INSERT INTO product_category (category_name, type_cat_id)
        VALUES (product_category_name_param, type_cat_id_param) RETURNING id INTO prod_cat_id_param;
    END IF;

    -- Producer
    SELECT id INTO producer_id_param FROM producer WHERE producer_name = producer_name_param;

    IF producer_id_param IS NULL THEN
        INSERT INTO producer (producer_name)
        VALUES (producer_name_param) RETURNING id INTO producer_id_param;
    END IF;

    -- Product
    SELECT id INTO product_id_param FROM product WHERE product_name = product_name_param;

    IF product_id_param IS NULL THEN
        INSERT INTO product (product_name, description, product_cat_id, producer_id)
        VALUES (product_name_param, product_description_param, prod_cat_id_param, producer_id_param) RETURNING id INTO product_id_param;
    
        INSERT INTO price_history (price, product_id)
        VALUES (price_param, product_id_param);
    
        INSERT INTO product_specs (spec_body, product_id)
        VALUES (specs_param, product_id_param);
        
        INSERT INTO product_inventory (sku, mpn, quantity, product_id)
        VALUES (sku_param, mpn_param, quantity_param, product_id_param);
    
    END IF;     
END;
$$;
