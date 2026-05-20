# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Dict
import os

# --- MODELS ---
class FoodListingCreate(BaseModel):
    item_name: str = Field(..., example="Dal & Rice")
    servings_available: int = Field(..., gt=0)
    pickup_location: str = Field(..., example="Hostel Mess")
    fresh_for_hours: int = Field(..., gt=0, example=4) # NEW: Expiry input

class ClaimRecord(BaseModel):
    name: str
    phone: str
    qty: int

# What the Admin sees (includes claim history)
class AdminListingResponse(BaseModel):
    id: int
    item_name: str
    servings_available: int
    total_servings: int
    pickup_location: str
    created_at: str
    expires_at: str
    claims: List[ClaimRecord]

# What the NGO sees (private, no phone numbers)
class RecipientListingResponse(BaseModel):
    id: int
    item_name: str
    servings_available: int
    pickup_location: str
    created_at: str
    expires_at: str

class ClaimRequest(BaseModel):
    recipient_name: str
    recipient_phone: str 
    servings_needed: int = Field(..., gt=0)

# --- IN-MEMORY DATABASE ---
db: Dict[int, dict] = {}
current_id = 1

# --- APP SETUP ---
app = FastAPI()

# --- API ENDPOINTS ---
@app.post("/api/admin/listings", response_model=AdminListingResponse)
async def create_listing(payload: FoodListingCreate):
    global current_id
    
    now = datetime.now()
    expiry_time = now + timedelta(hours=payload.fresh_for_hours)
    
    new_listing = {
        "id": current_id,
        "item_name": payload.item_name,
        "servings_available": payload.servings_available,
        "total_servings": payload.servings_available, # Track original amount
        "pickup_location": payload.pickup_location,
        "created_at": now.strftime("%I:%M %p"),
        "expires_at": expiry_time.strftime("%I:%M %p"),
        "claims": [] # List to hold claim history
    }
    db[current_id] = new_listing
    current_id += 1
    return new_listing

# NEW: Admin-only route to see history
@app.get("/api/admin/listings", response_model=List[AdminListingResponse])
async def get_admin_listings():
    # Show listings from newest to oldest
    return list(reversed(db.values()))

# Recipient route (only shows available food, hides claims)
@app.get("/api/recipient/listings", response_model=List[RecipientListingResponse])
async def get_recipient_listings():
    return [listing for listing in db.values() if listing["servings_available"] > 0]

@app.post("/api/recipient/listings/{listing_id}/claim")
async def claim_food(listing_id: int, payload: ClaimRequest):
    if listing_id not in db:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    listing = db[listing_id]
    if payload.servings_needed > listing["servings_available"]:
        raise HTTPException(status_code=400, detail=f"Only {listing['servings_available']} servings available.")
    
    # Deduct the servings
    listing["servings_available"] -= payload.servings_needed
    
    # Log the claim with name and phone number
    listing["claims"].append({
        "name": payload.recipient_name,
        "phone": payload.recipient_phone,
        "qty": payload.servings_needed
    })
    
    return {
        "message": "Successfully claimed!",
        "remaining_servings": listing["servings_available"]
    }

# --- SERVE FRONTEND ---
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")