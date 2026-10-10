from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_event():
    response = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 1,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert response.status_code == 200
    assert response.json()["capacity"] == 1
    assert response.json()["id"] == 1
    assert response.json()['title'] == "event1"
    assert response.json()['description'] == "description"
    assert response.json()['location'] == "loc"
    assert response.json()['start'] == "2026-11-14T18:00:00"
    assert response.json()['end'] == "2026-11-15T18:00:00"

def test_create_event_capacity_zero():
    response = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 0,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert response.status_code == 422

def test_get_event_by_id_pass():
    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 1,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    get_event = client.get(f'/events/{event_id}')

    assert get_event.status_code == 200
    assert get_event.json()["title"] == "event1"

def test_get_event_by_id_fail():
    get_event = client.get(f'/events/{1337}')
    assert get_event.status_code == 404

def test_delete_event_pass():
    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 1,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200

    event_id = create_event.json()["id"]
    delete_event = client.delete(f'/events/{event_id}')

    assert delete_event.status_code == 200
    assert delete_event.json()["title"] == "event1"

    get_event = client.get(f'/events/{event_id}')
    assert get_event.status_code == 404

def test_delete_event_fail():
    delete_event = client.delete(f'/events/{1333}')
    assert delete_event.status_code == 404

def test_update_event_pass():
    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 1,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    update_event = client.patch(f'/events/{event_id}', json={
        "title": "event_new",
    })
    assert update_event.status_code == 200
    assert update_event.json()["title"] == "event_new"
    assert update_event.json()["description"] == "description"
    assert update_event.json()["location"] == "loc"
    assert update_event.json()["capacity"] == 1
    assert update_event.json()["start"] == "2026-11-14T18:00:00"
    assert update_event.json()["end"] == "2026-11-15T18:00:00"

def test_update_event_fail():
    update_event = client.patch(f'/events/{1335}', json={
        "title": "event_new",
    })
    assert update_event.status_code == 404

def test_update_event_capacity_fail():
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

    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    create_user2 = client.post(
        "/users",
        json={"name": "test",
              "email": "test1@example.com"}
    )
    assert create_user2.status_code == 200
    create_registration1 = client.post(
        "/registrations",
        json={
            "event_id": 1,
            "user_id": create_user.json()["id"],
        }
    )
    assert create_registration1.status_code == 200
    create_registration2 = client.post(
        "/registrations",
        json={
            "event_id": 1,
            "user_id": create_user2.json()["id"],
        }
    )
    assert create_registration2.status_code == 200

    update_event = client.patch(f'/events/{event_id}', json={
        "capacity": 1,
    })
    assert update_event.status_code == 409

def test_update_event_capacity_pass():
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

    create_user = client.post(
        "/users",
        json={"name": "test",
              "email": "test@example.com"}
    )
    assert create_user.status_code == 200
    create_user2 = client.post(
        "/users",
        json={"name": "test",
              "email": "test1@example.com"}
    )
    assert create_user2.status_code == 200
    create_registration1 = client.post(
        "/registrations",
        json={
            "event_id": 1,
            "user_id": create_user.json()["id"],
        }
    )
    assert create_registration1.status_code == 200
    create_registration2 = client.post(
        "/registrations",
        json={
            "event_id": 1,
            "user_id": create_user2.json()["id"],
        }
    )
    assert create_registration2.status_code == 200

    update_event = client.patch(f'/events/{event_id}', json={
        "capacity": 2,
    })
    assert update_event.status_code == 200
    assert update_event.json()["capacity"] == 2

def test_update_event_date_fail():
    create_event = client.post('/events', json={
        "title": "event1",
        "description": "description",
        "location": "loc",
        "capacity": 1,
        "start": "2026-11-14T18:00:00",
        "end": "2026-11-15T18:00:00",
    })
    assert create_event.status_code == 200
    event_id = create_event.json()["id"]

    update_event = client.patch(f'/events/{event_id}', json={
        "end": "2026-11-13T18:00:00",
    })

    assert update_event.status_code == 422
    assert update_event.json()['detail'] == "end time cannot be before start time"