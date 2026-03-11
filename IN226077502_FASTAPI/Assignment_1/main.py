from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"This is home page. thank you for Visiting.."}

products = [
    {"id": 1, "name": "Samsung Galaxy A33", "price": 23999, "category": "electronics", "in_stock": True},
    {"id": 2, "name": "Oppo F17 Pro", "price": 21999, "category": "electronics", "in_stock": True},
    {"id": 3, "name": "Apple iPhone 14", "price": 69999, "category": "electronics", "in_stock": True},
    {"id": 4, "name": "HP Pavilion Laptop", "price": 58999, "category": "electronics", "in_stock": True},

    #add 3 more
    {"id": 5, "name": "Classmate Notebook", "price": 120, "category": "stationery", "in_stock": True},
    {"id": 6, "name": "Boat Rockerz 255 Earphones", "price": 1499, "category": "electronics", "in_stock": False},
    {"id": 7, "name": "Wooden Study Table", "price": 4500, "category": "furniture", "in_stock": True}
    ]

@app.get("/products")
def show_all_products():
    return {
        "products":products,
        "total":len(products)
    }


@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filter_product = [
        product for product in products
        if product["category"].lower() == category_name.lower() 
    ]

    if not filter_product:
        return {"error": "No products found in this category"}
    
    return {
        "category":category_name,
        "products":filter_product
    }


@app.get("/products/in_stock")
def in_stock_products():
    filter_product = [
        product for product in products
        if product["in_stock"] == True
    ]

    if not filter_product:
        return{"All product are out of stock"}
    
    return{
        "in_stock_products":filter_product,
        "count":len(filter_product)
    }


@app.get("/store/summary")
def store_info():

    in_stock_product = [
        product for product in products
        if product["in_stock"] == True
    ]

    out_stock_product = [
        product for product in products
        if product["in_stock"] != True
    ]

    categories = list(set([p["category"] for p in products]))

    return{
        "store_name":"My E-commerce store",
        "total":len(products),
        "in_stock":len(in_stock_product),
        "out_stock":len(out_stock_product),
        "category":categories
    }


@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    result = [
        product for product in products
        if keyword.lower() in product["name"].lower()
    ]

    if not result:
        return {"message": "No products matched your search"}
    
    return {
        "keyword":keyword,
        "result":result,
        "total":len(result)
    }

@app.get("/products/deals")
def products_deals():
    
    best_deal = min(products, key=lambda x: x["price"])
    pre_pick = max(products, key=lambda x: x["price"])

    return{
        "best_deal":best_deal,
        "premium_pick":pre_pick
    }

