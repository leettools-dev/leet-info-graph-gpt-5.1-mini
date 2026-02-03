from fastapi.testclient import TestClient
from src.leet_apps.api.main import app

client = TestClient(app)

def test_user_and_session_and_infographic_flow():
    # create user
    r = client.post('/api/users', json={'email':'test@example.com','name':'Tester'})
    assert r.status_code == 200
    user = r.json()
    assert 'id' in user

    # create session
    r = client.post('/api/sessions', json={'user_id': user['id'], 'prompt':'Summarize EV market trends'})
    assert r.status_code == 200
    session = r.json()
    assert session['status'] == 'created'

    # add source
    r = client.post(f"/api/sessions/{session['id']}/sources", json={'title':'EV Report','url':'https://example.com/ev','snippet':'Growing sales','confidence':0.9})
    assert r.status_code == 200
    source = r.json()
    assert source['session_id'] == session['id']

    # list sources
    r = client.get(f"/api/sessions/{session['id']}/sources")
    assert r.status_code == 200
    sources = r.json()
    assert len(sources) == 1

    # generate infographic
    r = client.post(f"/api/sessions/{session['id']}/infographic", json={'title':'EV Trends 2026','layout_meta':{}})
    assert r.status_code == 200
    ig = r.json()
    assert 'image_url' in ig

    # get infographic
    r = client.get(f"/api/sessions/{session['id']}/infographic")
    assert r.status_code == 200
    ig2 = r.json()
    assert ig2['id'] == ig['id']
