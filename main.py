from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from database import engine,Base 
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class Event(BaseModel):
    name: str
    category: str
    description: str

events = [
    {
        "id": 1,
        "name": "Boxing Championship",
        "category": "Sports",
        "description": "Boxing competition"
    },
    {
        "id": 2,
        "name": "AI Workshop",
        "category": "Technology",
        "description": "AI learning workshop"
    },
    {
        "id": 3,
        "name": "Music Concert",
        "category": "Entertainment",
        "description": "College music concert"
    }
]

@app.get("/")
def home():
    return {"message": "Welcome to CampusPulse"}
@app.get('/events')
def get_events():
    return events
@app.get("/events/{event_id}")
def get_event(event_id:int):
    for event in events:
        if event["id"] == event_id:
            return event

    raise HTTPException(
        status_code=404,
        detail='Event not found'
    )

@app.post("/events")
def create_event(event:Event):
    new_event={
        "id":len(events) + 1,
        "name": event.name,
        "category":event.category,
        "description":event.description
    }
    events.append(new_event)
    return new_event

class EventUpdate(BaseModel):
    name:str | None=None
    category:str | None=None
    description: str | None=None

@app.patch("/events/{event_id}")

def update_event(event_id : int,updated_data:EventUpdate):
    for event in events:
        if event['id']==event_id:
            event.update(updated_data.dict(exclude_unset=True))

            return event

    raise HTTPException(
            status_code=404,
            detail='Event not found'
        )


@app.delete("/events/{event_id}")
def delete_event(event_id:int):
    for event in events:
        if event["id"]==event_id:
            events.remove(event)
            return{
                "message":"Event deleted successfully"
            }
        raise HTTPException(
            status_code=404,
            detail="Event not found"

        )