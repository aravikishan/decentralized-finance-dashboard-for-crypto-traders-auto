# app.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uvicorn
from datetime import datetime
import os

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crypto_symbol = Column(String)
    amount = Column(Float)
    transaction_type = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

class Portfolio(Base):
    __tablename__ = "portfolios"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    crypto_symbol = Column(String, primary_key=True)
    quantity = Column(Float)
    average_purchase_price = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    crypto_symbol = Column(String)
    condition = Column(String)
    threshold = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/portfolio", response_class=HTMLResponse)
async def read_portfolio():
    with open("templates/portfolio.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/transactions", response_class=HTMLResponse)
async def read_transactions():
    with open("templates/transactions.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/alerts", response_class=HTMLResponse)
async def read_alerts():
    with open("templates/alerts.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/profile", response_class=HTMLResponse)
async def read_profile():
    with open("templates/profile.html") as f:
        return HTMLResponse(content=f.read())

# Seed data
def seed_data():
    db = SessionLocal()
    if not db.query(User).first():
        user = User(username="demo", email="demo@example.com", password_hash="hashedpassword")
        db.add(user)
        db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
    uvicorn.run(app, host="0.0.0.0", port=8000)
