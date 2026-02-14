def test_create_user(client):
    """Test creating a new user"""
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data

def test_create_duplicate_user(client):
    """Test that duplicate usernames are rejected"""
    # Create first user
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    
    # Try to create duplicate
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "other@example.com"}
    )
    assert response.status_code == 400

def test_get_user(client):
    """Test retrieving a user by ID"""
    # Create user
    create_response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    user_id = create_response.json()["id"]
    
    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"

def test_get_nonexistent_user(client):
    """Test that getting a nonexistent user returns 404"""
    response = client.get("/users/999")
    assert response.status_code == 404
    