# About
In this repo I've built an operational database for an ecommerce platform, using popular tech-shop "Komplett.no" as a reference. 
The database contains real product data scraped from komplett, as well as other generated data for table population.
Finally I've built a data warehouse using a star schema approach, used for doing BI analysis.

The project will be updated continously. This is not it's final form.

![Alt Text](https://github.com/mats-bb/Reverse-engineered-Komplett-DB/blob/master/imgs/overview_1.png)


# Table of contents
- [The idea](#the-idea)
- [The process](#the-process)
- [Tools](#tools)
- [Future work](#future-work)


# The idea
The idea for this project came to be because I wanted to dig deeper into data modeling. Typically you'd be given a set of instructions on what data processes the system will handle. In order to get some "instructions" for the project, I decided to use a website I know and love for inspiration, popular webshop, Komplett.no.
From there the idea only grew. I wanted to build the actual system itself and populate it with real data, hence the web scraping. Of course, I needed a data warehouse too, on which I would run analysis. I concluded the project would provide a good foundation for future learning, that I could add new functionalities as I learn about new technologies. A good part of the groundwork has been done in this current iteration of the project, and I will detail it all, step by step.

# The process
## 1. Exploring the website
In order to get the required instructions for building the data model, some exploration was needed. I clicked around on the webpage, checking out the different categories and products, different functions like the shoppingcart and wishlist, customer pages and more. After getting a good overview of the core functions I wanted the system to support I could start the actual modeling.

## 2. Building the ERD
At the heart of every webshop is the products they offer. Customers buy the products, and everything gets recorded in an order. I decided to focus on these aspects for the data model as they are the most "important", and most fun to work with, in my opinion. The process itself was pretty straightforward: explore each aspect in depth, break them down into logical pieces, build the tables and relations, and iterate. Some data, of course, is not avaiable by just looking at a webpage, so some actual thinking was involved in designing parts of the schema, like the product inventory table, for example. You can see the current ERD [here](imgs/operations_ERD.drawio.png).

## 3. Building the operational database
There is not very much to say about the actual creation of the database. The ERD is complete, just follow the recipe. The [DDL](sql/operations_DDL.sql) for the operations database. Don't worry about the cascades, I've deliberately kept them as they were a part of the process. Do be careful in a real environment though!

## 4. Scraping the data
The data scraping process was way more involved, using browser dev tools to inspect the HTML of each webpage to get the actual data. Product data was the target here, and I chose to focus on computer parts only. The process simply described, extract the URL for each product and extract the relevant data from these URLs HTML. This was a lengthy process, and a lot of debugging and manual labour had to be done finding the correct HTML elements and writing the actual code for it. Ultimately though, scraping the data would be a one-time operation.

## 5. Generating data
Next I needed some data for the customers and their orders. I will not go into the details here, 
## 6. ETL
## 7. Building the data warehouse
## 8. Generating data
## 9. ETL
## 10. Power Bi

## Ideas
- Build operational database
- Build dimensional data warehouse
- Scrape product data
- Generate dummy data
- Write ETL processes
- Do analysis with Power Bi

## Tools
- Python
- Dbeaver (postgreSQL)
- Power Bi
- Draw.io (ERD design)
- APIs (https://randomuser.me/)

## Future work
- Scrape all product data
- Generate more sales data for deeper analysis
- Implement big data tools (Kafka, Spark)
- Automate with Airflow
- Migrate to Snowflake
- Build a GUI or web solution to interact with DBs
