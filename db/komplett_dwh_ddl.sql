/*
DDL for the dimensional model for the komplett data warehouse.
Will focus on sales transactions, on the product level.
*/


DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
	id serial PRIMARY KEY,
	date date UNIQUE NOT null,
    day_of_week int NOT null,
    day_of_month int NOT null,
    day_of_year int NOT null,
    week_number int NOT null,
    YEAR int NOT null,
    name_of_day varchar(10) NOT null,
    name_of_month varchar(10) NOT null,
    month_number int NOT null,
    quarter_number int NOT null,
    full_date_description TEXT NOT null,
    month_end_flag TEXT NOT null,
    weekday_flag TEXT NOT null,
    holiday_flag TEXT NOT NULL
    );
   


DROP TABLE IF EXISTS dim_payment_method ;
CREATE TABLE dim_payment_method (
	id serial PRIMARY KEY,
	payment_method_description varchar(10)
	);


DROP TABLE IF EXISTS dim_product;
CREATE TABLE dim_product (
	id serial PRIMARY KEY,
	product_sku_number int UNIQUE NOT null,
	product_mpn_number TEXT UNIQUE NOT null,
	product_name TEXT UNIQUE NOT null,
	product_category varchar(20) NOT null,
	product_type_category varchar(20) NOT null,
	product_main_category varchar(20) NOT null,
	product_producer_name varchar(35) NOT null
	);


DROP TABLE IF EXISTS dim_discount;
CREATE TABLE dim_discount (
	id serial PRIMARY KEY,
	discount_name TEXT UNIQUE NOT null,
	discount_type varchar(15) NOT null,
	discount_amount decimal(4, 2) NOT null,
	start_date date NOT null,
	end_date date NOT null
	);


DROP TABLE IF EXISTS dim_location;
CREATE TABLE dim_location (
	id serial PRIMARY KEY,
	zip_code int NOT null,
	city_name TEXT NOT null,
	state_name TEXT NOT NULL
	);


DROP TABLE IF EXISTS fact_product_sale;
CREATE TABLE fact_product_sale (
	id serial PRIMARY KEY,
	product_id int NOT NULL REFERENCES dim_product (id),
	payment_method_id int NOT NULL REFERENCES dim_payment_method (id),
	date_id int NOT NULL REFERENCES dim_date (id),
	location_id int NOT NULL REFERENCES dim_location (id),
	discount_id int NOT NULL REFERENCES dim_discount (id),
	quantity int NOT null,
	regular_unit_price decimal(8, 2),
	discount_unit_price decimal(8, 2),
	net_unit_price decimal(8, 2)
	);
	

SELECT * FROM dim_date;
SELECT * FROM dim_discount;
SELECT * FROM dim_location;
SELECT * FROM dim_payment_method;
SELECT * FROM dim_product;
SELECT * FROM fact_product_sale;