# Online Shop

This project is a fully featured online platform. it allows customers to browse products, add them to cart, apply discount codes, go through the checkout process, pay with credit card and obtain an invoice.

Additionally it have a recomendation engine to recommend products to customers and internalization to offer site in multiple languages.

#### Versions

- V1.0
  - added product catalog models. (**category** and **product**),
  - added product catalog models to adminstration site,
  - built views and templates to display product catalog.

*Concepts used: **models**, **admin site**, **views**, **urls** and **templates** in Django.*

- V2.0
  - added a new app for managing shopping carts,
  - built functionlaity to create carts, (Initialized a **Cart** class inside *cart.py* file.),
  - built functionality to construct cart dictionaries, (*save()*, *add()* and *remove()* methods.),
  - built functionality to iterate through the items conatined in the cart and access the related product instances, (*__iter*__*()* method.),
  - added methods to return count of total products, total price of products in the cart and a method to remove the cart from session, (*__len*__*()*, *get_total_price()* and *clear()* methods respectively.),

*Concepts used: **Django sessions**

#### Sitemap

- **'/'** - *product list*
- **'/category_slug/'** - *list products by category*
- **'/product_id/product_slug/'** - *product detail*
