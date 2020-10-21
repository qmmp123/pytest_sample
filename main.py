from typing import Optional, List

from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session

import schemas
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_product/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create product with specified params
    See params in schemas.ProductCreate
    """
    product = models.Product(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.delete("/delete_product/{product_id}", status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete product by given product_id
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(product)
    db.commit()


@app.patch("/change_product_in_stock/{product_id}/{left}", response_model=schemas.Product)
def patch_product(product_id: int, left: int, db: Session = Depends(get_db)):
    """
    Change product in stock
    """
    product: schemas.Product = db.query(models.Product).filter(models.Product.id == product_id).first()
    product.in_stock = left
    db.commit()


@app.get("/get_products/", response_model=List[schemas.Product])
def get_products(product_group: Optional[str] = None, min_cost: Optional[int] = None, max_cost: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get all products or filtered products
    """
    filters = []
    if product_group:
        filters.append(models.Product.group == product_group)
    if min_cost:
        filters.append(models.Product.cost > min_cost)
    if max_cost:
        filters.append(models.Product.cost < max_cost)
    return db.query(models.Product).filter(*filters).all()
