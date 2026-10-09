from models.event_model import Event

class EventStore:
    def __init__(self):
        self.events = []
        self.next_event_id = 1

    def get_events(self):
        return self.events

    def add_event(self, title, description, location, capacity, start, end):
        event = Event(id=self.next_event_id, title=title, description=description, location=location, capacity=capacity, start=start, end=end)
        self.events.append(event)
        self.next_event_id += 1
        return event

    def delete_event(self, index):
        return self.events.pop(index)


event_store = EventStore()