import databases
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = "postgresql+asyncpg://compare_user:compare_user_pass@localhost:5432/django_vs_fast_api"

database = databases.Database(DATABASE_URL)

app = FastAPI()

class Customer(BaseModel):
    id: int
    name: str
    email: str

class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    id: int
    customer_id: int
    created_at: str
    customer: Customer

class CombinedData(BaseModel):
    order: Order
    products: List[Product]

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/api/orders/{order_id}/", response_model=CombinedData)
async def get_order(order_id: int):
    order_query = """
        SELECT 
            o.id, 
            o.customer_id, 
            o.created_at, 
            c.id AS customer_id, 
            c.name AS customer_name, 
            c.email AS customer_email
        FROM 
            myapp_order o
        INNER JOIN 
            myapp_customer c 
        ON 
            o.customer_id = c.id
        WHERE 
            o.id = :order_id
        LIMIT 21;
    """
    order_row = await database.fetch_one(query=order_query, values={"order_id": order_id})

    if not order_row:
        raise HTTPException(status_code=404, detail="Order not found")

    order_instance = {
        'id': order_row['id'],
        'customer_id': order_row['customer_id'],
        'created_at': str(order_row['created_at']),
        'customer': {
            'id': order_row['customer_id'],
            'name': order_row['customer_name'],
            'email': order_row['customer_email'],
        }
    }

    products_query = """
        SELECT 
            p.id, 
            p.name, 
            p.price
        FROM 
            myapp_product p
        INNER JOIN 
            myapp_order_products op 
        ON 
            p.id = op.product_id
        WHERE 
            op.order_id IN (:order_id);
    """
    products_rows = await database.fetch_all(query=products_query, values={"order_id": order_id})

    product_data = [
        {'id': row['id'], 'name': row['name'], 'price': row['price']} for row in products_rows
    ]

    combined_data = {
        'order': order_instance,
        'products': product_data,
    }

    return combined_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
