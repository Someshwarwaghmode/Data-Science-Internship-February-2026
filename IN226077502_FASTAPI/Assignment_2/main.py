from fastapi import FastAPI,Query
from typing import List
from pydantic import BaseModel,Field


# -----------------------------------------------------------------------------------

# day 1

# ----------------------------- Q 1 -----------------------------------------------------
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




# -----------------------------------------------------------------------------------

# day 2

# ----------------------------- Q 1 -----------------------------------------------------
@app.get("/products/filter")
def filter_products(
    category: str = Query(None, description="electronics and stationary"),
    min_price: int = Query(None, description="minimum price"),
    max_price: int = Query(None, description="max price")
):
    filtered_list = products

    if category:
        filtered_list = [p for p in filtered_list if p["category"].lower() == category.lower()]
    if min_price:
        filtered_list = [p for p in filtered_list if p["price"] >= min_price]
    if max_price:
        filtered_list = [p for p in filtered_list if p["price"] <= max_price]
    
    return filtered_list


# --------------------------Q 2 ---------------------------------------------------------------------

@app.get("/products/{product_id}/price")
def product_name_with_price(product_id: int):
    for p in products:
        if p["id"]==product_id:
            return {
                "name":p["name"],
                "price":p["price"]
            }
    
    return {"product not found"}



# -----------------------------Q 3 -----------------------------------------------------------------------


feedback = []
class CustomerFeedbback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    produuct_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(None, max_length=300)

@app.post("/feedback")
def customer_feedback(data: CustomerFeedbback):
    feedback.append(data.model_dump())

    return {
        "message": "Feedback Submited scsscefully",
        "feedback":data,
        "total_feedback":len(feedback)
    }


# ----------------------------- Q 4 ------------------------------------------------
@app.get("/products/summary")
def products_summary_dashbord():

    in_stock = products
    in_stock = [p for p in in_stock if p["in_stock"]]
    out_stock = len(products)-len(in_stock)

    expensive = max(products, key=lambda x: x["price"])
    cheapest = min(products, key=lambda x: x["price"])

    categories = list(set(p["category"] for p in products))

    return{
        "Total Products ": len(products),
        "In Stock ":len(in_stock),
        "Out Stock ": out_stock,
        "Most Expensive ":{"name ": expensive["name"], "price ": expensive["price"]},
        "Most Cheapest ":{"name ":cheapest["name"], "price ":cheapest["price"]},
        "categories ": categories
    }

# ----------------------------------- Q 5 ------------------------------------------------



class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem]

@app.post("/order/bulk")
def bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:
        product = next((p for p in products if p["id"]==item.product_id), None)

        if not product:
            failed.append({"product_id":item.product_id, "reason" : "product not found"})
            continue
        if not product["in_stock"]:
            failed.append({"product_id":item.product_id, "reason" : f"{product["name"]} is out of stock"})
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append(
            {
                "product":product["name"],
                "qty":item.quantity,
                "subtotal":subtotal
            }
        )

    return {
        "Company Name" :order.company_name,
        "confirmed": confirmed,
        "faild": failed,
        "Garnd total": grand_total
    }
        

# ---------------------------- Bonus Question ---------------------------------------------------

orders = []

class Order(BaseModel):
    product_id: int
    qunatity: int

@app.post("/orders")
def place_order(order: Order):
    order_data = {
        "id": len(orders)+1,
        "product_id": order.product_id,
        "quantity": order.qunatity,
        "status": "pending"
    }

    orders.append(order_data)
    
    return order_data

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["id"]==order_id:
            return order
        
    return {"Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["id"]==order_id:
            order["status"] = "confirmed"
            return order
        
    return {"Order not found"}
