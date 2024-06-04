SELECT * FROM dim_date;
SELECT * FROM dim_product;
SELECT * FROM dim_customer;
SELECT * FROM dim_location;
SELECT * FROM dim_discount;
SELECT * FROM fact_product_sale;


DROP TABLE IF EXISTS dim_date CASCADE;
CREATE TABLE dim_date (
	id serial PRIMARY KEY,
	date date UNIQUE NOT NULL,
    day_of_week int NOT NULL,
    day_of_month int NOT NULL,
    day_of_year int NOT NULL,
    week_number int NOT NULL,
    year int NOT NULL,
    name_of_day varchar(10) NOT NULL,
    name_of_month varchar(10) NOT NULL,
    month_number int NOT NULL,
    quarter_number int NOT NULL,
    full_date_description TEXT NOT NULL,
    month_end_flag TEXT NOT NULL,
    weekday_flag TEXT NOT NULL,
    holiday_flag TEXT NOT NULL
    );


DROP TABLE IF EXISTS dim_product CASCADE;
CREATE TABLE dim_product (
	id int NOT NULL PRIMARY KEY,
	product_sku_number int UNIQUE NOT NULL,
	product_mpn_number TEXT NOT NULL,
	product_name TEXT NOT NULL,
	product_category varchar(30) NOT NULL,
	product_type_category varchar(30) NOT NULL,
	product_main_category varchar(30) NOT NULL,
	product_producer_name varchar(35) NOT NULL
	);


DROP TABLE IF EXISTS dim_discount CASCADE;
CREATE TABLE dim_discount (
	id int PRIMARY KEY,
	discount_name TEXT UNIQUE NOT NULL,
	discount_type varchar(15) NOT NULL,
	discount_amount int NOT NULL,
	start_date date,
	end_date date
	);


DROP TABLE IF EXISTS dim_location CASCADE;
CREATE TABLE dim_location (
	id int PRIMARY KEY,
	street_address TEXT NOT NULL,
	zip_code int NOT NULL,
	city_name TEXT NOT NULL,
	state_name TEXT NOT NULL
	);


DROP TABLE IF EXISTS dim_customer CASCADE;
CREATE TABLE dim_customer (
	id int PRIMARY KEY,
	first_name varchar(30) NOT NULL,
	last_name varchar(30) NOT NULL,
	full_name varchar(60) NOT NULL,
	date_of_birth date NOT NULL,
	email TEXT UNIQUE NOT NULL,
	mobile_number varchar(8) UNIQUE NOT NULL,
	account_created_date date NOT NULL
	);


DROP TABLE IF EXISTS fact_product_sale CASCADE;
CREATE TABLE fact_product_sale (
	id serial PRIMARY KEY,
	product_id int NOT NULL REFERENCES dim_product (id),
	date_id int NOT NULL REFERENCES dim_date (id),
	location_id int NOT NULL REFERENCES dim_location (id),
	discount_id int NOT NULL REFERENCES dim_discount (id),
	customer_id int NOT NULL REFERENCES dim_customer (id),
	payment_method varchar(20) NOT NULL,
	delivery_method varchar(20) NOT NULL,
	quantity int NOT NULL,
	regular_unit_price int NOT NULL,
	discount_unit_price int DEFAULT 0,
	net_unit_price int NOT NULL,
	extended_sales_amount int NOT NULL,
	extended_discount_amount int DEFAULT 0
	);
