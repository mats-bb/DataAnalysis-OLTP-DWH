DROP PROCEDURE insert_product_data(TEXT, TEXT, TEXT, TEXT, TEXT, TEXT, NUMERIC, JSONB, TEXT, TEXT, INT);
-- STORED PROCEDURE for inserting product data
CREATE OR REPLACE PROCEDURE insert_product_data(
    main_category_name_param TEXT,
    type_category_name_param TEXT,
    product_category_name_param TEXT,
    producer_name_param TEXT,
    product_name_param TEXT,
    product_description_param TEXT,
    price_param DECIMAL(8,2),
    specs_param JSONB,
    sku_param TEXT,
    mpn_param TEXT,
    quantity_param INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_main_cat_id INT := 0;
    new_type_cat_id INT := 0;
    new_prod_cat_id INT := 0;
    new_producer_id INT := 0;
    new_product_id INT := 0;
BEGIN
    -- Start transaction
    BEGIN
        -- Main category
        new_main_cat_id := (
            SELECT id FROM main_category WHERE category_name = main_category_name_param
        );

        IF new_main_cat_id IS NULL THEN
            INSERT INTO main_category (category_name)
            VALUES (main_category_name_param) RETURNING id INTO new_main_cat_id;
        END IF;

        -- Type category
        new_type_cat_id := (
            SELECT id FROM type_category WHERE category_name = type_category_name_param
        );

        IF new_type_cat_id IS NULL THEN
            INSERT INTO type_category (category_name, main_cat_id)
            VALUES (type_category_name_param, new_main_cat_id) RETURNING id INTO new_type_cat_id;
        END IF;

        -- Product category
        new_prod_cat_id := (
            SELECT id FROM product_category WHERE category_name = product_category_name_param
        );

        IF new_prod_cat_id IS NULL THEN
            INSERT INTO product_category (category_name, type_cat_id)
            VALUES (product_category_name_param, new_type_cat_id) RETURNING id INTO new_prod_cat_id;
        END IF;

        -- Producer
        new_producer_id := (
            SELECT id FROM producer WHERE producer_name = producer_name_param
        );

        IF new_producer_id IS NULL THEN
            INSERT INTO producer (producer_name)
            VALUES (producer_name_param) RETURNING id INTO new_producer_id;
        END IF;

        -- Product
        new_product_id := (
            SELECT id FROM product WHERE product_name = product_name_param
        );

        IF new_product_id IS NULL THEN
            INSERT INTO product (product_name, description, product_cat_id, producer_id)
            VALUES (product_name_param, product_description_param, new_prod_cat_id, new_producer_id) RETURNING id INTO new_product_id;
        
            INSERT INTO price_history (price, product_id)
            VALUES (price_param, new_product_id);
        
            INSERT INTO product_specs (spec_body, product_id)
            VALUES (specs_param, new_product_id);
            
            INSERT INTO product_inventory (sku, mpn, quantity, product_id)
            VALUES (sku_param, mpn_param, quantity_param, new_product_id);
        
        END IF;
       
    END;

END;
$$;