from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_registration_pass():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    user1_id = create_user.json()["id"]

    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 3,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    assert register_user.status_code == 200
    assert register_user.json()["event_id"] == event_id
    assert register_user.json()["user_id"] == user1_id

def test_create_registration_duplicate_fail():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    user1_id = create_user.json()["id"]

    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 3,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    assert register_user.status_code == 200
    assert register_user.json()["event_id"] == event_id
    assert register_user.json()["user_id"] == user1_id

    register_user_duplicate = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    assert register_user_duplicate.status_code == 409

def test_create_registration_404_fail():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    user1_id = create_user.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": 9999,
            "user_id": user1_id
        }
    )
    assert register_user.status_code == 404

def test_create_registration_user_404_fail():
    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 3,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": 99999
        }
    )
    assert register_user.status_code == 404

def test_create_registration_capacity_fail():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    create_user2 = client.post(
        "/users",
        json={"name": "test",
              "email": "test2@example.com"}
    )
    assert create_user2.status_code == 200
    assert create_user2.json()["email"] == "test2@example.com"

    create_user3 = client.post(
        "/users",
        json={"name": "test",
              "email": "test3@example.com"}
    )
    assert create_user3.status_code == 200
    assert create_user3.json()["email"] == "test3@example.com"

    user1_id = create_user.json()["id"]
    user2_id = create_user2.json()["id"]
    user3_id = create_user3.json()["id"]

    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 2,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    register_user2 = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user2_id
        }
    )
    register_user3 = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user3_id
        }
    )
    assert register_user3.status_code == 409

def test_delete_registration_pass():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    user1_id = create_user.json()["id"]

    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 3,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    assert register_user.status_code == 200
    registration_id = register_user.json()["id"]
    delete_registration = client.delete(f"/registrations/{registration_id}")

    assert delete_registration.status_code == 200

    get_registration_deleted = client.get(f"/registrations/{registration_id}")
    assert get_registration_deleted.status_code == 404

def test_delete_registration_fail():
    delete_registration = client.delete(f"/registrations/{9999}")
    assert delete_registration.status_code == 404

def test_get_registration_details():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    create_user2 = client.post(
        "/users",
        json={"name": "test",
              "email": "test2@example.com"}
    )
    assert create_user2.status_code == 200
    assert create_user2.json()["email"] == "test2@example.com"

    create_user3 = client.post(
        "/users",
        json={"name": "test",
              "email": "test3@example.com"}
    )
    assert create_user3.status_code == 200
    assert create_user3.json()["email"] == "test3@example.com"

    user1_id = create_user.json()["id"]
    user2_id = create_user2.json()["id"]
    user3_id = create_user3.json()["id"]

    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 3,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    register_user2 = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user2_id
        }
    )
    register_user3 = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user3_id
        }
    )

    details = client.get(f"/events/{event_id}/registrations")
    assert details.status_code == 200
    assert len(details.json()) == 3

    for registration in details.json():
        assert registration["event_id"] == event_id

def test_get_user_registrations():
    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    assert create_user.json()["email"] == "test@example.com"

    create_user2 = client.post(
        "/users",
        json={"name": "test",
              "email": "test2@example.com"}
    )
    assert create_user2.status_code == 200
    assert create_user2.json()["email"] == "test2@example.com"

    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 3,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    user1_id = create_user.json()["id"]
    user2_id = create_user2.json()["id"]

    register_user = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user1_id
        }
    )
    register_user2 = client.post(
        "/registrations",
        json={
            "event_id": event_id,
            "user_id": user2_id
        }
    )
    get_user_registrations = client.get(f"/users/{user1_id}/registrations")
    assert get_user_registrations.status_code == 200
    assert len(get_user_registrations.json()) == 1
    for registration in get_user_registrations.json():
        assert registration["user_id"] == user1_id