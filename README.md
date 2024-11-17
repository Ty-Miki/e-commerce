# Online Shop

This project is a fully featured online platform. it allows customers to browse products, add them to cart, apply discount codes, go through the checkout process, pay with credit card and obtain an invoice.

Additionally it have a recomendation engine to recommend products to customers and internalization to offer site in multiple languages.

#### Apps

- Shop
  - added product catalog models. (**category** and **product**),
  - added product catalog models to adminstration site,
  - built views and templates to display product catalog.

*Concepts used: **models**, **admin site**, **views**, **urls** and **templates** in Django.*

- Cart
  - added a new app for managing shopping carts,
  - built functionlaity to create carts, (Initialized a **Cart** class inside *cart.py* file.),
  - built functionality to construct cart dictionaries, (*save()*, *add()* and *remove()* methods.),
  - built functionality to iterate through the items conatined in the cart and access the related product instances, (*__iter*__*()* method.),
  - added methods to return count of total products, total price of products in the cart and a method to remove the cart from session, (*__len*__*()*, *get_total_price()* and *clear()* methods respectively.),
  - Appropriate views, forms, urls and templates are added to enable users add, remove, update and view their cart items.

*New Concepts used: **Django sessions***

- Orders
  - This app handles the checkout process and is used to persist the cart items to the database as an order instance once users click checkout and fill in the appropraite data.
  - Appropriate models, forms, views, urls and templates are implemented for this purpose.
  - Used Celery with RabbitMQ to send email notification to users after an order is successfully placed.

  *New Concepts used: **Celery** and **RabbitMQ***

- Payment
  - This app handles the payment process through stripe
  - Requires a .env file inside the same directory as *settings.py* and needs to have **STRIPE_PUBLISHABLE_KEY**, **STRIPE_SECRET_KEY** and **STRIPE_API_VERSION** variables. I used the 2022-08-01 stripe API version.
  - Now orders can have the paid flag on using stripe webhooks and the admin can reference back to the stripe payment url using the stripe ID for the payment of that order. For this the .env file should be updated to have **STRIPE_WEBHOOK_SECRET** variable.

#### Sitemap

- **'/'** - *product list*
- **'/category_slug/'** - *list products by category*
- **'/product_id/product_slug/'** - *product detail*
- **'/cart/'** - *cart detail*
- **'/orders/create/'** - *orders create*

#### Requirements

- A **messaage borker for celery**, I used the official **RabbitMQ docker image**.
- A **.env** file inside the **same directory as settings.py** and it should contain the configuration for the email server. (See the bottom of settings.py for further info).