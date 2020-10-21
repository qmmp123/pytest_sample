import logging
import pytest
from typing import List

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from pydantic import parse_obj_as

from main import app, get_db
from database import Base
from schemas import Product


DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db/postgres"
engine = create_engine(DATABASE_URL)
TestSessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
logger = logging.getLogger(__name__)
client = TestClient(app)


@pytest.fixture(scope="module")
def create_products():
    id1 = client.post("/create_product/", json={"name": "qwe", "sku": "asd", "group": "zxc", "in_stock": "123", "cost": 123})
    id2 = client.post("/create_product/", json={"name": "qwer", "sku": "asdf", "group": "zxcv", "in_stock": "123", "cost": 1234})
    yield id1, id2
    client.delete(f"/delete_product/{id1}")
    client.delete(f"/delete_product/{id2}")


def test_get_products(create_products):
    r = client.get("/get_products/")
    assert len(r.json()) == 2
    r = client.get("/get_products/", params={"product_group": "zxc"})
    assert len(r.json()) == 1
    r = client.get("/get_products/", params={"product_group": "zxc", "min_cost": "100"})
    assert len(r.json()) == 1
    r = client.get("/get_products/", params={"product_group": "zxc", "min_cost": "1000"})
    assert len(r.json()) == 0
    r = client.get("/get_products/", params={"product_group": "zxc", "min_cost": "100", "max_cost": "1000"})
    assert len(r.json()) == 1


def test_patch_product(create_products):
    client.patch(f"/change_product_in_stock/{create_products[0]}/321")
    client.patch(f"/change_product_in_stock/{create_products[1]}/322")
    r = client.get("/get_products/")
    products: List[Product] = parse_obj_as(List[Product], r.json())
    for product in products:
        if product.id == create_products[0]:
            assert product.in_stock == 321
        elif product.id == create_products[1]:
            assert product.in_stock == 322


def test_delete_products(create_products):
    r = client.get("/get_products/")
    products: List[Product] = parse_obj_as(List[Product], r.json())
    assert len(products) == 2
    for product in products:
        client.delete(f"/delete_product/{product.id}")
    r = client.get("/get_products/")
    assert len(r.json()) == 0
