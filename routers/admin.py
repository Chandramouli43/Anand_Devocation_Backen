# app/routers/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from core.database import get_db
from core.dependencies import require_admin
from core.security import hash_password

from models.location import Location
from models.user import User
from models.enums import UserRole
from models.trip import Trip, TripStatus
from models.advertisement import Advertisement

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],  # 🔒 ADMIN ONLY
)

# =====================================================
# LOCATION MANAGEMENT
# =====================================================

@router.post("/locations")
def create_location(
    name: str,
    db: Session = Depends(get_db),
):
    if db.query(Location).filter(Location.name == name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location already exists",
        )

    loc = Location(name=name)
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc


@router.delete("/locations/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    loc = db.get(Location, location_id)
    if not loc:
        raise HTTPException(404, "Location not found")

    db.delete(loc)
    db.commit()
    return {"message": "Location deleted"}

# =====================================================
# AGENT MANAGEMENT
# =====================================================

@router.post("/agents")
def create_agent(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    agent = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=UserRole.AGENT,   # 🔒 forced
        is_active=True,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "message": "Agent created successfully",
        "agent_id": str(agent.id),
        "email": agent.email,
    }


@router.delete("/agents/{agent_id}")
def deactivate_agent(
    agent_id: str,
    db: Session = Depends(get_db),
):
    agent = db.get(User, agent_id)

    if not agent or agent.role != UserRole.AGENT:
        raise HTTPException(404, "Agent not found")

    agent.is_active = False
    db.commit()

    return {
        "message": "Agent deactivated successfully",
        "agent_id": agent_id,
    }

# =====================================================
# TRIP MANAGEMENT (ADMIN FULL CRUD)
# =====================================================

@router.post("/trips")
def create_trip(
    title: str,
    description: str,
    location_id: int,
    start_date: date,
    end_date: date,
    price: int,
    capacity: int,
    db: Session = Depends(get_db),
):
    trip = Trip(
        title=title,
        description=description,
        location_id=location_id,
        start_date=start_date,
        end_date=end_date,
        price=price,
        capacity=capacity,
        status=TripStatus.DRAFT,
        is_active=True,
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.put("/trips/{trip_id}")
def update_trip(
    trip_id: str,
    title: str | None = None,
    description: str | None = None,
    price: int | None = None,
    capacity: int | None = None,
    status: TripStatus | None = None,
    db: Session = Depends(get_db),
):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")

    if title is not None:
        trip.title = title
    if description is not None:
        trip.description = description
    if price is not None:
        trip.price = price
    if capacity is not None:
        trip.capacity = capacity
    if status is not None:
        trip.status = status

    db.commit()
    return trip


@router.delete("/trips/{trip_id}")
def deactivate_trip(
    trip_id: str,
    db: Session = Depends(get_db),
):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")

    trip.is_active = False
    db.commit()
    return {"message": "Trip deactivated"}


@router.get("/trips")
def list_all_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()

# =====================================================
# ADVERTISEMENT MANAGEMENT
# =====================================================

@router.post("/advertisements")
def create_advertisement(
    title: str,
    image_url: str,
    trip_id: str,
    db: Session = Depends(get_db),
):
    if not db.get(Trip, trip_id):
        raise HTTPException(404, "Trip not found")

    ad = Advertisement(
        title=title,
        image_url=image_url,
        trip_id=trip_id,
        is_active=True,
    )

    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


@router.delete("/advertisements/{ad_id}")
def deactivate_advertisement(
    ad_id: str,
    db: Session = Depends(get_db),
):
    ad = db.get(Advertisement, ad_id)
    if not ad:
        raise HTTPException(404, "Advertisement not found")

    ad.is_active = False
    db.commit()
    return {"message": "Advertisement deactivated"}


@router.get("/advertisements")
def list_advertisements(db: Session = Depends(get_db)):
    return db.query(Advertisement).all()
