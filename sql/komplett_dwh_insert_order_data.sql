-- Procedure for inserting order data into the DWH
DROP PROCEDURE insert_order_data(jsonb);

CREATE OR REPLACE PROCEDURE insert_order_data(json_data JSONB)
LANGUAGE plpgsql
AS $$
DECLARE
	product_id_param INT;
	date_id_param INT;
	location_id_param INT;
	discount_id_param INT;
	payment_method_param TEXT;
	delivery_method_param TEXT;
	quantity_param INT;
	regular_unit_price_param DECIMAL;
	discount_unit_price_param DECIMAL;
	net_unit_price_param DECIMAL;
	extended_sales_amount_param INT;
	extended_discount_amount_param INT;
BEGIN
	-- Date ID
	SELECT id INTO date_id_param
	FROM dim_date
	WHERE "date" = (json_data->>'order_date')::date;

	-- Location ID
	SELECT id INTO location_id_param
	FROM dim_location
	WHERE zip_code = (json_data->>'zip_code')::int AND city_name = json_data->>'city_name';

	-- Extract json data fields
	product_id_param = json_data->>'product_id';
	discount_id_param = json_data->>'discount_id';
	payment_method_param = json_data->>'payment_method'; 
	delivery_method_param = json_data->>'delivery_method';
	quantity_param = json_data->>'quantity';
	regular_unit_price_param = json_data->>'regular_unit_price';
	discount_unit_price_param = json_data->>'discounted_price';
	net_unit_price_param = json_data->>'net_price';
	extended_sales_amount_param = json_data->>'extended_sales_amount';
	extended_discount_amount_param = json_data->>'extended_discount_amount';

	-- Insert the data
	INSERT INTO fact_product_sale (product_id, date_id, location_id, discount_id, payment_method, delivery_method,
	quantity, regular_unit_price, discount_unit_price, net_unit_price, extended_sales_amount , extended_discount_amount)
	VALUES (product_id_param, date_id_param, location_id_param, discount_id_param, payment_method_param, delivery_method_param,
			quantity_param, regular_unit_price_param, discount_unit_price_param, net_unit_price_param, extended_sales_amount_param, extended_discount_amount_param);
END; 
$$;