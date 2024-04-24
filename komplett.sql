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

--

drop table if exists producer;
create table producer (
	id serial primary key,
	producer_name varchar(50) unique not null
	);

drop table if exists main_category;
create table main_category (
	id serial primary key,
	category_name varchar(50) unique not null
	);

drop table if exists type_category;
create table type_category (
	id serial primary key,
	category_name varchar(50) unique not null,
	main_cat_id int not null references main_category (id)
	);

drop table if exists product_category;
create table product_category (
	id serial primary key,
	category_name varchar(50) unique not null,
	type_cat_id int not null references type_category (id)
	);

drop table if exists discount;
create table discount (
	id serial primary key,
	discount_name varchar(50) unique not null,
	discount_info text not null,
	discount_type text not null,
	amount int not null,
	start_date date not null,
	end_date date not null
	);
	
drop table if exists product;
create table product (
	id serial primary key,
	product_name varchar(75) unique not null,
	description text not null,
	product_cat_id int references product_category (id),
	producer_id int references producer (id)
	);

drop table if exists product_discount;
create table product_discount (
	id serial primary key,
	product_id int references product (id),
	discount_id int references discount (id)
	);

drop table if exists price_history;
create table price_history (
	id serial primary key,
	price decimal(6, 2) not null,
	effective_date date not null,
	product_id int references product (id)
	);

drop table if exists product_image;
create table product_image (
	id serial primary key,
	img_path text unique not null,
	product_id int references product (id)
	);

drop table if exists product_info;
create table product_info (
	id serial primary key,
	info_body jsonb not null,
	product_id int not null references product (id)
	);

drop table if exists product_specs;
create table product_specs (
	id serial primary key,
	spec_body jsonb not null,
	product_id int not null references product (id)
	);

drop table if exists product_inventory;
create table product_inventory (
	id serial primary key,
	SKU varchar(50) unique not null,
	quantity int default 0,
	created_date date not null,
	product_id int references product (id)
	);