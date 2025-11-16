from typing import List, Optional
from src.domain.entities.event import Event
from src.domain.interfaces.event_repository import EventRepository
from src.infrastructure.cache.cache_client import cache_client


class EventService:
    """Service containing business logic for events"""
    
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository
    
    def create_event(self, event: Event) -> Event:
        """Create a new event with validation"""
        # Validate event date is in the future
        if not event.is_future_event():
            raise ValueError("Event date must be in the future")
        
        # Create event
        created_event = self.event_repository.create(event)
        
        # Invalidate cache for events list
        cache_client.delete("events:all")
        
        return created_event
    
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID with caching"""
        # Try to get from cache first
        cache_key = f"event:{event_id}"
        cached_data = cache_client.get(cache_key)
        
        if cached_data:
            # Reconstruct Event from cached data
            return Event(
                event_id=cached_data["id"],
                name=cached_data["name"],
                description=cached_data["description"],
                date=cached_data["date"],
                location=cached_data["location"],
                capacity=cached_data["capacity"]
            )
        
        # If not in cache, get from database
        event = self.event_repository.get_by_id(event_id)
        
        if event:
            # Store in cache for 5 minutes
            cache_data = {
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location,
                "capacity": event.capacity
            }
            cache_client.set(cache_key, cache_data, expiration=300)
        
        return event
    
    def get_all_events(self) -> List[Event]:
        """Get all events with caching"""
        # Try cache first
        cache_key = "events:all"
        cached_data = cache_client.get(cache_key)
        
        if cached_data:
            return [
                Event(
                    event_id=e["id"],
                    name=e["name"],
                    description=e["description"],
                    date=e["date"],
                    location=e["location"],
                    capacity=e["capacity"]
                )
                for e in cached_data
            ]
        
        # Get from database
        events = self.event_repository.get_all()
        
        # Cache the results
        if events:
            cache_data = [
                {
                    "id": e.id,
                    "name": e.name,
                    "description": e.description,
                    "date": e.date.isoformat(),
                    "location": e.location,
                    "capacity": e.capacity
                }
                for e in events
            ]
            cache_client.set(cache_key, cache_data, expiration=300)
        
        return events
    
    def update_event(self, event: Event) -> Event:
        """Update an event with validation"""
        # Validate event exists
        existing_event = self.event_repository.get_by_id(event.id)
        if not existing_event:
            raise ValueError(f"Event with id {event.id} not found")
        
        # Update event
        updated_event = self.event_repository.update(event)
        
        # Invalidate cache
        cache_client.delete(f"event:{event.id}")
        cache_client.delete("events:all")
        cache_client.delete(f"event:stats:{event.id}")
        
        return updated_event
    
    def delete_event(self, event_id: int) -> bool:
        """Delete an event"""
        result = self.event_repository.delete(event_id)
        
        if result:
            # Invalidate cache
            cache_client.delete(f"event:{event_id}")
            cache_client.delete("events:all")
            cache_client.delete(f"event:stats:{event_id}")
        
        return result
    
    def get_event_statistics(self, event_id: int) -> dict:
        """Get event statistics with caching"""
        # Try cache first
        cache_key = f"event:stats:{event_id}"
        cached_stats = cache_client.get(cache_key)
        
        if cached_stats:
            return cached_stats
        
        # Get event and calculate statistics
        event = self.event_repository.get_by_id(event_id)
        if not event:
            raise ValueError(f"Event with id {event_id} not found")
        
        attendee_count = self.event_repository.get_attendee_count(event_id)
        available_spots = event.capacity - attendee_count
        occupancy_percentage = (attendee_count / event.capacity) * 100 if event.capacity > 0 else 0
        
        stats = {
            "event_id": event.id,
            "event_name": event.name,
            "total_capacity": event.capacity,
            "registered_attendees": attendee_count,
            "available_spots": available_spots,
            "occupancy_percentage": round(occupancy_percentage, 2)
        }
        
        # Cache for 2 minutes (stats change frequently)
        cache_client.set(cache_key, stats, expiration=120)
        
        return stats