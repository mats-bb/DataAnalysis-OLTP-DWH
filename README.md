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


## The idea
The idea for this project came to be because I wanted to dig deeper into data modeling. Typically you'd be given a set of instructions on what data processes the system will handle. In order to get some "instructions" for the project, I decided to use a website I know and love for inspiration, popular webshop, Komplett.no.
From there the idea only grew. I wanted to build the actual system itself and populate it with real data, hence the web scraping. Of course, I needed a data warehouse too, on which I would run analysis. I concluded the project would provide a good foundation for future learning, that I could add new functionalities as I learn about new technologies. A good part of the groundwork has been done in this current iteration of the project, and I will detail it all, step by step.

## The process
1. Exploring the website
  -  Test
2. Building the ERD
3. Building the operational database
4. Scraping the data
5. Generating data
6. ETL
7. Building the data warehouse
8. Generating data
9. ETL
10. Power Bi

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
