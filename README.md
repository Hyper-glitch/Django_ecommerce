# Django_ecommerce
This pet project allows you to buy digital and non digital products like in online-shops.
At this very moment users can add any products to their cart, also here is possibility to checkout their order with PayPal.
Products are created through Django Admin.

## Technologies
Project is created with:
* Python version: 3.10
* Django version: 4.0
* Bootstrap version: 4.4.1
* Docker version: 20.10.12
* Docker-compose version: 1.29.2

## Setup
To run this project, install it locally using:
1. git clone https://github.com/Hyper-glitch/Django_ecommerce.git
2. docker-compose -f ./ecommerce/docker-compose.yml up -d (if you are in /Django_ecommerce)
3. go to the http://0.0.0.0:7000/

![Algorithm schema](ecom.png)

## Here is the application on the Linux server
You can test my application in a docker containers (web_app and postgresql) on a Linux server
http://139.162.137.249:7000/
