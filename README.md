# shopify-backend-internship-challenge-fall-2022

<h2>Background</h2>

This is a FastAPI application created for Shopify's Fall 2022 Backend Developer Intern Challenge. It is backend server
for an online Product Inventory Application. Lets start off with some basic details about the project.

<b>Replit web app</b> - https://shopify-backend-internship-challenge-fall-4.sumitdadwal1.repl.co/docs

<b>Replit code</b> - https://replit.com/@sumitdadwal1/shopify-backend-internship-challenge-fall-4?v=1<b>

<h2>Project Structure</h2>

This application is initiated through the `main.py` file in apps folder. This file contains the entry point for the
application. 

The db folder contains `database.py` where we conntect to our database and `models.py` which ensures format in which out data is going to be stored in database.

Then we have routers folder in which we have `products.py` where all the endpoints for productsare define, `warehouses.py` where all the endpoints for warehouses are defined
and `manager.py` where all the endpoints for managers are defined. We also have `schemas.py` in routers folder which is used to validate data we receive as well as to reformat the data that we want to send to the client/browser.

<h2>Running the Application Locally</h2>
Now that we have a good understading of the project lets run it in your local machine by following the commands below:

First you need to have Python installed in your machine - https://www.python.org/downloads/

1. git clone https://github.com/sumitdadwal/shopify-backend-internship-challenge-fall-2022
2. cd shopify-backend-internship-challenge-fall-2022
3. python -m venv env (to create virtual environment)
4. env\scripts\activate (to activate virtual environement)
5. pip install -r requirements.txt (to install all the packahes)
6. uvicorn app.main:app --reload (to run the ap in `localhost`)

Once your app is up and running go to `localhost:8000/docs` to access all the endpoints.


<h2>Testing</h2>
We also have tests folder in which all the tests are difined for products, warehouses and managers endpoints.

You can run tests by simply using:

`pytest -v -s`.

for Coverage reports you can use:
`coverage run --source=routers -m pytest -v tests &&coverage report -m`

![coverage](https://user-images.githubusercontent.com/84678969/169150488-bcc01eed-7db4-4e6f-971b-7eec5eba3cf0.jpg)


<h2>API Documentation</h2>

<h2> For managers:</h2>


<h3>POST: /manager/create</h3>

Used to create new managers

Requires `first_name`, `last_name`, `manager_email`and `manager_phone` in the body.

Example:

https://user-images.githubusercontent.com/84678969/169151047-f9918be2-ae1f-4927-bfc8-73642aa43a4a.mp4

<h3>GET: /manager/all</h3>

Used to get all the managers.

Query accepts `limit`, `skip`, `search_first_name`, `search_last_name` and `search_email`.


https://user-images.githubusercontent.com/84678969/169151513-553a7b1c-21d4-443d-a1ba-799138ad7cc8.mp4

<h3>GET: /manager/{id}</h3>

Used to get manager with specific `manager_id`.

Query requires `manager_id`.

<h3>PUT: /manager/update/{id}</h3>

Used to update existing manager.

Query requires `manager_id`.

https://user-images.githubusercontent.com/84678969/169151835-0ab76752-78a8-46cf-a3dd-1d088d267140.mp4


<h3>DELETE: /manager/delete/{id}</h3>

Used to delete manager with specific `manager_id`.

Query requires `manager_id`.


Now that we have managers. Lets create warehouses than assign them these managers.

<h2>For warehouses</h2>

<h3>POST: /warehouse/create</h3>

Used to create new Warehouses.

Request Body:
![request body warehouse](https://user-images.githubusercontent.com/84678969/169152749-2e39d9dc-1df0-49b0-8df2-36fbed5a7527.jpg)

Response Body: 

![createwarehouse](https://user-images.githubusercontent.com/84678969/169152825-2402e751-afe3-4fd5-89b5-49502b9cd5ea.jpg)


<h3>GET: /warehouse/all</h3>

Used to get all the warehouse.

Query accepts `search_name`, `search_type`, `search_address` and `search_by_manager_id`.


<h3>GET: /warehouse/{id}</h3>

Used to get warehouse with specific `manager_id`.

Query requres `manager_id`.

Then we have <b>`UPDATE: /warehouse/update/{id}`</b> and <b>`DELETE: /warehouse/delete/{id}`</b> works similar to the managers.

UPDATE WAREHOUSE:


https://user-images.githubusercontent.com/84678969/169155126-77fa8931-9146-43f1-acc5-24ca0f4a0fea.mp4




<h2>For Products:</h2>

<h3>POST: /product/create</h3>


Request Body:

![request body](https://user-images.githubusercontent.com/84678969/169154639-bf8fc323-0500-42ed-aed1-d4cce51df6f0.jpg)

Response Body:

![response body](https://user-images.githubusercontent.com/84678969/169154708-171d1b93-bb56-4145-92a7-a379a60d1a85.jpg)

<b>NOTE:
  There are two ways you can upload image of product. If you wish to pass an <i>`Image_URL`</i> directly into the <i>`image_url'</i> field
  you can do that but the you need to put `image_url_type` as absolute
  
  OR
  
  If you want to a upload an image from your computer, you can do that as well but then you need to pass `relative` in `image_url_type`. Take a look at the video below.
  </b>
  
<h3>POST: /product/image</h3>
Used to upload product image.

if you choose to upload image, make sure copy the path in the <b>RESPONSE BODY</b> and paste it in `image_url` under `/product/create/`. and pass  `relative` as `image_url_type`.



https://user-images.githubusercontent.com/84678969/169156664-02ccd1de-c501-4fa0-880a-fb5b7250a65f.mp4




<h3>GET: /product/all</h3>

Used to get all the products.

Query accepts `limit`, `skip`, `search_name`, `search_description`, `search_count`, `search_warehouseID` and `search_unit_price`.

<h3>GET: /product/{id}</h3>

Used to get product with specific `product_id`.

Query requires `product_id`.

<h3><h3>GET: /product/warehouse/{warehouse_id}</h3>

Used to get all products under specific `warehouse_id`.

Query requires `warehouse_id`.
  
  
<h3>PUT: /product/update/{id}</h3>

Used to update existing product.

Query requires `product_id`.
  
<h3>DELETE: /product/delete/{id}</h3>

Used to delete existing product.

Query requires `product_id`.
  
  
  
 
  
  





