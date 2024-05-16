/*
product
producer
product_category
type_category
main_category
product_discount
discount
price_history
product_image
product_info
product_specs
product_inventory

order
order_product
order_payment
payment_provider
delivery_option

user
user_address
address
user_review
cart
cart_product
wishlist
wishlist_product
card_info
*/

-- PRODUCT

drop table if exists producer cascade;
create table producer (
	id serial primary key,
	producer_name varchar(50) unique not null
	);

drop table if exists main_category cascade;
create table main_category (
	id serial primary key,
	category_name varchar(50) unique not null
	);

drop table if exists type_category cascade;
create table type_category (
	id serial primary key,
	category_name varchar(50) unique not null,
	main_cat_id int not null references main_category (id)
	);

drop table if exists product_category cascade;
create table product_category (
	id serial primary key,
	category_name varchar(50) unique not null,
	type_cat_id int not null references type_category (id)
	);

drop table if exists discount cascade;
create table discount (
	id serial primary key,
	discount_name varchar(50) unique not null,
	discount_info text not null,
	discount_type text not null,
	amount int not null,
	start_date date not null,
	end_date date not null
	);
	
drop table if exists product cascade;
create table product (
	id serial primary key,
	product_name varchar(75) unique not null,
	description text not null,
	product_cat_id int not null references product_category (id),
	producer_id int not null references producer (id)
	);

drop table if exists product_discount cascade;
create table product_discount (
	id serial primary key,
	product_id int not null references product (id),
	discount_id int not null references discount (id)
	);

drop table if exists price_history cascade;
create table price_history (
	id serial primary key,
	price decimal(8, 2) not null,
	effective_date date default current_date not null,
	product_id int not null references product (id)
	);

drop table if exists product_image cascade;
create table product_image (
	id serial primary key,
	img_path text unique not null,
	product_id int not NULL references product (id)
	);

drop table if exists product_info cascade;
create table product_info (
	id serial primary key,
	info_body jsonb not null,
	product_id int not null references product (id)
	);

drop table if exists product_specs cascade;
create table product_specs (
	id serial primary key,
	spec_body jsonb not null,
	product_id int not null references product (id)
	);

drop table if exists product_inventory cascade;
create table product_inventory (
	id serial primary key,
	SKU varchar(50) unique not null,
	MPN varchar(50) not null,
	quantity int default 0,
	created_date date DEFAULT current_date not null,
	product_id int not null references product (id)
	);

-- ORDERS

drop table if exists payment_provider cascade;
create table payment_provider (
	id serial primary key,
	name varchar(30) unique not null
	);

drop table if exists delivery_option cascade;
create table delivery_option (
	id serial primary key,
	type varchar(30) unique not null,
	price decimal(3, 2) not null
	);

drop table if exists orders cascade;
create table orders (
	id serial primary key,
	order_date date not null,
	shipped_date date default null,
	ip_address varchar(20) not null,
	last_update date default null,
	pickup_msg text default null,
	delivery_note text not null,
	delivery_option_id int not null references delivery_option (id),
	customer_id int not null references customer (id)
	);

drop table if exists orders_payment cascade;
create table orders_payment (
	id serial primary key,
	total_amount decimal(6, 2) not null,
	payment_date date not null,
	status varchar(20) default null,
	orders_id int not null references orders (id),
	card_id int NOT NULL REFERENCES card_info (id)
	);

drop table if exists orders_product cascade;
create table orders_product (
	id serial primary key,
	quantity int not null,
	orders_id int not null references orders (id),
	product_id int not null references product (id)
	);

-- CUSTOMER

drop table if exists customer cascade;
create table customer (
	id serial primary key,
	first_name varchar(20) not null,
	middle_name varchar(20) default null,
	last_name varchar(20) not null,
	email varchar(50) unique not null,
	password varchar(50) not null,
	mobile_num varchar(8) unique not null,
	created_date date DEFAULT current_date NOT null,
	last_modified date DEFAULT current_date NOT null 
	);

drop table if exists state cascade;
create table state (
	id serial primary key,
	state_name varchar(40) unique not null
	);

drop table if exists city cascade;
create table city (
	id serial primary key,
	city_name varchar(20) unique not NULL,
	state_id int NOT NULL REFERENCES state (id)
	);

drop table if exists address cascade;
create table address (
	id serial primary key,
	street_address varchar(35) not null,
	zip_code int not null,
	city_id int not null references city (id)
	);

drop table if exists customer_address cascade;
create table customer_address (
	id serial primary key,
	customer_id int not null references customer (id),
	address_id int not null references address (id)
	);

drop table if exists card_info cascade;
create table card_info (
	id serial primary key,
	card_number varchar(19) unique not null,
	cardholder_first_name varchar(20) not null,
	cardholder_last_name varchar(20) not null,
	expiration_date text not null,
	cvv text not null,
	payment_provider_id int NOT NULL REFERENCES payment_provider (id),
	customer_id int not null references customer (id)
	);

-- CART

drop table if exists cart cascade;
create table cart (
	id serial primary key,
	created_date date not null,
	customer_id int not null references customer (id)
	);

drop table if exists cart_product cascade;
create table cart_product (
	id serial primary key,
	quantity int not null,
	cart_id int not null references cart (id),
	product_id int not null references product (id)
	);

-- WISHLIST

drop table if exists wishlist cascade;
create table wishlist (
	id serial primary key,
	wishlist_name varchar(70) not null,
	created_date date not null,
	note text default null,
	customer_id int not null references customer (id)
	);

drop table if exists wishlist_product cascade;
create table wishlist_product (
	id serial primary key,
	quantity int not null,
	wishlist_id int not null references wishlist (id),
	product_id int not null references product (id)
	);

-- CUSTOMER_PRODUCT

drop table if exists product_review cascade;
create table product_review (
	id serial primary key,
	title text not null,
	rating int not null check (rating between 0 and 5),
	review_date date not null,
	review_text text default null,
	product_id int not null references product (id),
	customer_id int not null references customer (id)
	);