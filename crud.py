# crud.py
from sqlalchemy.orm import Session
from models import Product, Customer, Order, OrderItem
import schemas
from decimal import Decimal

# Products
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = Product(
        sku=product.sku,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_qty=product.stock_qty,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, updates: dict):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for k, v in updates.items():
        setattr(db_product, k, v)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True

# Customers
def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def list_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, updates: dict):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    for k, v in updates.items():
        setattr(db_customer, k, v)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True

# Orders
def create_order(db: Session, order_in: schemas.OrderCreate):
    # compute totals and unit prices from products
    customer = db.query(Customer).filter(Customer.id == order_in.customer_id).first()
    if not customer:
        raise ValueError("Customer not found")
    order = Order(customer_id=order_in.customer_id, shipping_address=order_in.shipping_address, status="pending")
    db.add(order)
    db.flush()  # get order.id

    total = Decimal("0.00")
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        if not product:
            raise ValueError(f"Product id {item.product_id} not found")
        unit_price = product.price
        if product.stock_qty < item.quantity:
            raise ValueError(f"Not enough stock for product id {product.id}")
        line_total = Decimal(unit_price) * item.quantity
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=unit_price, line_total=line_total)
        db.add(order_item)

        # decrement stock
        product.stock_qty = product.stock_qty - item.quantity

        total += line_total

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def list_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()
