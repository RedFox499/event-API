import pytest
from services.user_store import user_store
from services.event_store import event_store
from services.registration_store import registration_store

@pytest.fixture(autouse=True)
def reset_stores():
    event_store.events.clear()
    event_store.next_event_id = 1

    user_store.users.clear()
    user_store.next_user_id = 1

    registration_store.registrations.clear()
    registration_store.next_registration_id = 1