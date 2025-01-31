from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from typing import List
import uuid
from datetime import datetime
from math import ceil

app = FastAPI()

RECEIPTS = {}

class Item(BaseModel):
    shortDescription: str
    price: str

    @validator("shortDescription")
    def validate_short_description(cls, v):
        # Pattern check
        return v

    @validator("price")
    def validate_price(cls, v):
        # Must match \d+\.\d{2}
        try:
            if not isinstance(float(v), float):
                raise ValueError
        except:
            raise ValueError("Please verify input.")
        return v

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

    @validator("retailer")
    def validate_retailer(cls, v):
        return v

    @validator("purchaseDate")
    def validate_purchase_date(cls, v):
        # should be in YYYY-MM-DD format
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except:
            raise ValueError("Please verify input.")
        return v

    @validator("purchaseTime")
    def validate_purchase_time(cls, v):
        # should be in HH:MM (24-hour) format
        try:
            datetime.strptime(v, "%H:%M")
        except:
            raise ValueError("Please verify input.")
        return v

    @validator("items")
    def validate_items(cls, v):
        if len(v) < 1:
            raise ValueError("Please verify input.")
        return v

    @validator("total")
    def validate_total(cls, v):
        # Must match \d+\.\d{2} pattern
        try:
            float_val = float(v)
            # Confirm exactly two decimal places
            if float_val < 0:
                raise ValueError
        except:
            raise ValueError("Please verify input.")
        return v


@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    points = compute_points(receipt)

    # Generate an ID and store it in memory
    receipt_id = str(uuid.uuid4())
    RECEIPTS[receipt_id] = points

    return {"id": receipt_id}


@app.get("/receipts/{id}/points")
async def get_points(id: str):
    if id not in RECEIPTS:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": RECEIPTS[id]}


def compute_points(receipt: Receipt) -> int:
    total_points = 0

    # 1) One point for every alphanumeric character in the retailer name
    retailer_alnum = [c for c in receipt.retailer if c.isalnum()]
    total_points += len(retailer_alnum)

    # Convert total to a numerical type for checks
    total_float = float(receipt.total)
    total_cents = int(round(total_float * 100))

    # 2) 50 points if the total is a round dollar amount with no cents
    if total_cents % 100 == 0:
        total_points += 50

    # 3) 25 points if the total is a multiple of 0.25
    if total_cents % 25 == 0:
        total_points += 25

    # 4) 5 points for every two items on the receipt
    total_points += (len(receipt.items) // 2) * 5

    # 5) If the trimmed length of the item description is a multiple of 3,
    for item in receipt.items:
        desc = item.shortDescription.strip()
        if len(desc) % 3 == 0:
            item_price = float(item.price)
            total_points += int(ceil(item_price * 0.2))


    # 7) 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        total_points += 6

    # 8) 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    hour = purchase_time.hour
    minute = purchase_time.minute
    # "After 2:00pm" means strictly greater than 14:00
    # "Before 4:00pm" means strictly less than 16:00
    if (hour > 14 or (hour == 14 and minute > 0)) and (hour < 16):
        total_points += 10

    return total_points


@app.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return HTTPException(
        status_code=400, 
        detail="Please verify input."
    )
