-- PRODUCT

DROP TABLE IF EXISTS producer CASCADE;
CREATE TABLE producer (
	id serial PRIMARY KEY,
	producer_name varchar(50) UNIQUE NOT NULL
	);

DROP TABLE IF EXISTS main_category CASCADE;
CREATE TABLE main_category (
	id serial PRIMARY KEY,
	category_name varchar(50) UNIQUE NOT NULL
	);

DROP TABLE IF EXISTS type_category CASCADE;
CREATE TABLE type_category (
	id serial PRIMARY KEY,
	category_name varchar(50) UNIQUE NOT NULL,
	main_cat_id int NOT NULL REFERENCES main_category (id)
	);

DROP TABLE IF EXISTS product_category CASCADE;
CREATE TABLE product_category (
	id serial PRIMARY KEY,
	category_name varchar(50) UNIQUE NOT NULL,
	type_cat_id int NOT NULL REFERENCES type_category (id)
	);

DROP TABLE IF EXISTS discount CASCADE;
CREATE TABLE discount (
	id serial PRIMARY KEY,
	discount_name varchar(50) UNIQUE NOT NULL,
	discount_info text NOT NULL,
	discount_type text NOT NULL,
	amount int NOT NULL,
	start_date date,
	end_date date 
	);
	
DROP TABLE IF EXISTS product CASCADE;
CREATE TABLE product (
	id serial PRIMARY KEY,
	product_name varchar(75) UNIQUE NOT NULL,
	description text NOT NULL,
	product_cat_id int NOT NULL REFERENCES product_category (id),
	producer_id int NOT NULL REFERENCES producer (id)
	);

DROP TABLE IF EXISTS discount_product CASCADE;
CREATE TABLE discount_product (
	id serial PRIMARY KEY,
	product_id int UNIQUE NOT NULL REFERENCES product (id),
	discount_id int NOT NULL REFERENCES discount (id)
	);

DROP TABLE IF EXISTS price_history CASCADE;
CREATE TABLE price_history (
	id serial PRIMARY KEY,
	price int NOT NULL,
	effective_date date DEFAULT current_date NOT NULL,
	product_id int NOT NULL REFERENCES product (id)
	);

DROP TABLE IF EXISTS product_image CASCADE;
CREATE TABLE product_image (
	id serial PRIMARY KEY,
	img_path text UNIQUE NOT NULL,
	product_id int NOT NULL REFERENCES product (id)
	);

DROP TABLE IF EXISTS product_info CASCADE;
CREATE TABLE product_info (
	id serial PRIMARY KEY,
	info_body jsonb NOT NULL,
	product_id int NOT NULL REFERENCES product (id)
	);

DROP TABLE IF EXISTS product_specs CASCADE;
CREATE TABLE product_specs (
	id serial PRIMARY KEY,
	spec_body jsonb NOT NULL,
	product_id int NOT NULL REFERENCES product (id)
	);

DROP TABLE IF EXISTS product_inventory CASCADE;
CREATE TABLE product_inventory (
	id serial PRIMARY KEY,
	SKU varchar(50) UNIQUE NOT NULL,
	MPN varchar(50) NOT NULL,
	quantity int DEFAULT 0 NOT NULL,
	CREATEd_date date DEFAULT current_date NOT NULL,
	product_id int NOT NULL REFERENCES product (id)
	);

-- ORDERS

DROP TABLE IF EXISTS payment_provider CASCADE;
CREATE TABLE payment_provider (
	id serial PRIMARY KEY,
	name varchar(30) UNIQUE NOT NULL
	);

DROP TABLE IF EXISTS delivery_option CASCADE;
CREATE TABLE delivery_option (
	id serial PRIMARY KEY,
	type varchar(30) UNIQUE NOT NULL,
	price int NOT NULL
	);

DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
	id serial PRIMARY KEY,
	order_date date NOT NULL,
	shipped_date date DEFAULT NULL,
	ip_address varchar(20) NOT NULL,
	last_update date DEFAULT NULL,
	payment_method TEXT NOT NULL,
	pickup_msg text DEFAULT NULL,
	delivery_note text NOT NULL,
	delivery_option_id int NOT NULL REFERENCES delivery_option (id),
	customer_id int NOT NULL REFERENCES customer (id)
	);

DROP TABLE IF EXISTS orders_payment CASCADE;
CREATE TABLE orders_payment (
	id serial PRIMARY KEY,
	total_amount decimal(6, 2) NOT NULL,
	payment_date date NOT NULL,
	status varchar(20) DEFAULT NULL,
	orders_id int NOT NULL REFERENCES orders (id),
	card_id int NOT NULL REFERENCES card_info (id)
	);

DROP TABLE IF EXISTS orders_product CASCADE;
CREATE TABLE orders_product (
	id serial PRIMARY KEY,
	quantity int NOT NULL,
	orders_id int NOT NULL REFERENCES orders (id),
	product_id int NOT NULL REFERENCES product (id),
	discount_id int DEFAULT 1 REFERENCES discount (id)
	);

-- CUSTOMER

DROP TABLE IF EXISTS customer CASCADE;
CREATE TABLE customer (
	id serial PRIMARY KEY,
	first_name varchar(20) NOT NULL,
	middle_name varchar(20) DEFAULT NULL,
	last_name varchar(20) NOT NULL,
	DOB date NOT NULL,
	email varchar(50) UNIQUE NOT NULL,
	password varchar(50) NOT NULL,
	mobile_num varchar(8) UNIQUE NOT NULL,
	CREATEd_date date DEFAULT current_date NOT NULL,
	last_modified date DEFAULT current_date NOT NULL 
	);


DROP TABLE IF EXISTS state CASCADE;
CREATE TABLE state (
	id serial PRIMARY KEY,
	state_name varchar(40) UNIQUE NOT NULL
	);

DROP TABLE IF EXISTS city CASCADE;
CREATE TABLE city (
	id serial PRIMARY KEY,
	city_name varchar(20) UNIQUE NOT NULL,
	state_id int NOT NULL REFERENCES state (id)
	);

DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
	id serial PRIMARY KEY,
	street_address varchar(50) NOT NULL,
	zip_code int NOT NULL,
	city_id int NOT NULL REFERENCES city (id)
	);

DROP TABLE IF EXISTS customer_address CASCADE;
CREATE TABLE customer_address (
	id serial PRIMARY KEY,
	customer_id int NOT NULL REFERENCES customer (id),
	address_id int NOT NULL REFERENCES address (id)
	);

DROP TABLE IF EXISTS card_info CASCADE;
CREATE TABLE card_info (
	id serial PRIMARY KEY,
	card_number varchar(19) UNIQUE NOT NULL,
	cardholder_first_name varchar(20) NOT NULL,
	cardholder_last_name varchar(20) NOT NULL,
	expiration_date text NOT NULL,
	cvv text NOT NULL,
	payment_provider_id int NOT NULL REFERENCES payment_provider (id),
	customer_id int NOT NULL REFERENCES customer (id)
	);

-- CART

DROP TABLE IF EXISTS cart CASCADE;
CREATE TABLE cart (
	id serial PRIMARY KEY,
	CREATEd_date date NOT NULL,
	customer_id int NOT NULL REFERENCES customer (id)
	);

DROP TABLE IF EXISTS cart_product CASCADE;
CREATE TABLE cart_product (
	id serial PRIMARY KEY,
	quantity int NOT NULL,
	cart_id int NOT NULL REFERENCES cart (id),
	product_id int NOT NULL REFERENCES product (id)
	);

-- WISHLIST

DROP TABLE IF EXISTS wishlist CASCADE;
CREATE TABLE wishlist (
	id serial PRIMARY KEY,
	wishlist_name varchar(70) NOT NULL,
	CREATEd_date date NOT NULL,
	note text DEFAULT NULL,
	customer_id int NOT NULL REFERENCES customer (id)
	);

DROP TABLE IF EXISTS wishlist_product CASCADE;
CREATE TABLE wishlist_product (
	id serial PRIMARY KEY,
	quantity int NOT NULL,
	wishlist_id int NOT NULL REFERENCES wishlist (id),
	product_id int NOT NULL REFERENCES product (id)
	);

-- CUSTOMER_PRODUCT

DROP TABLE IF EXISTS product_review CASCADE;
CREATE TABLE product_review (
	id serial PRIMARY KEY,
	title text NOT NULL,
	rating int NOT NULL check (rating between 0 and 5),
	review_date date NOT NULL,
	review_text text DEFAULT NULL,
	product_id int NOT NULL REFERENCES product (id),
	customer_id int NOT NULL REFERENCES customer (id)
	);