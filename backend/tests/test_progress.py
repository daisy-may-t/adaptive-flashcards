def test_learn_mode_shows_new_cards(client):
    """Test that learn mode shows cards never reviewed"""
    # Setup: Create user, deck, and card
    user_response = client.post(
        "/users/",
        json={"username": "learner", "email": "learner@example.com"}
    )
    user_id = user_response.json()["id"]
    
    deck_response = client.post(
        "/decks/",
        json={"title": "Test Deck", "owner_id": user_id}
    )
    deck_id = deck_response.json()["id"]
    
    client.post(
        f"/decks/{deck_id}/cards",
        json={"question": "What is 2+2?", "answer": "4"}
    )
    
    # Test: New cards should appear in learn mode
    response = client.get(f"/users/{user_id}/cards?mode=learn&deck_id={deck_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["card"]["question"] == "What is 2+2?"
    assert data[0]["progress"] is None  # No progress yet

def test_recap_mode_shows_confident_cards(client):
    """Test that recap mode shows cards with high confidence"""
    # Setup: Create user, deck, and card
    user_response = client.post(
        "/users/",
        json={"username": "learner", "email": "learner@example.com"}
    )
    user_id = user_response.json()["id"]
    
    deck_response = client.post(
        "/decks/",
        json={"title": "Test Deck", "owner_id": user_id}
    )
    deck_id = deck_response.json()["id"]
    
    card_response = client.post(
        f"/decks/{deck_id}/cards",
        json={"question": "What is 2+2?", "answer": "4"}
    )
    card_id = card_response.json()["id"]
    
    # Record high confidence review
    client.post(
        "/reviews",
        json={"user_id": user_id, "card_id": card_id, "confidence": 0.9}
    )
    
    # Test: High confidence cards should appear in recap mode
    response = client.get(f"/users/{user_id}/cards?mode=recap&deck_id={deck_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["card"]["question"] == "What is 2+2?"
    assert data[0]["progress"]["confidence_score"] == 0.9

def test_low_confidence_cards_stay_in_learn_mode(client):
    """Test that low confidence cards don't appear in recap mode"""
    # Setup
    user_response = client.post(
        "/users/",
        json={"username": "learner", "email": "learner@example.com"}
    )
    user_id = user_response.json()["id"]
    
    deck_response = client.post(
        "/decks/",
        json={"title": "Test Deck", "owner_id": user_id}
    )
    deck_id = deck_response.json()["id"]
    
    card_response = client.post(
        f"/decks/{deck_id}/cards",
        json={"question": "What is 2+2?", "answer": "4"}
    )
    card_id = card_response.json()["id"]
    
    # Record low confidence review
    client.post(
        "/reviews",
        json={"user_id": user_id, "card_id": card_id, "confidence": 0.3}
    )
    
    # Test: Should be in learn mode
    learn_response = client.get(f"/users/{user_id}/cards?mode=learn&deck_id={deck_id}")
    assert len(learn_response.json()) == 1
    
    # Test: Should NOT be in recap mode
    recap_response = client.get(f"/users/{user_id}/cards?mode=recap&deck_id={deck_id}")
    assert len(recap_response.json()) == 0

def test_record_review_updates_confidence(client):
    """Test that recording reviews updates confidence scores"""
    # Setup
    user_response = client.post(
        "/users/",
        json={"username": "learner", "email": "learner@example.com"}
    )
    user_id = user_response.json()["id"]
    
    deck_response = client.post(
        "/decks/",
        json={"title": "Test Deck", "owner_id": user_id}
    )
    deck_id = deck_response.json()["id"]
    
    card_response = client.post(
        f"/decks/{deck_id}/cards",
        json={"question": "What is 2+2?", "answer": "4"}
    )
    card_id = card_response.json()["id"]
    
    # First review
    response1 = client.post(
        "/reviews",
        json={"user_id": user_id, "card_id": card_id, "confidence": 0.5}
    )
    assert response1.status_code == 201
    assert response1.json()["confidence_score"] == 0.5
    assert response1.json()["review_count"] == 1
    
    # Second review (should be weighted average)
    response2 = client.post(
        "/reviews",
        json={"user_id": user_id, "card_id": card_id, "confidence": 1.0}
    )
    assert response2.status_code == 201
    # 0.7 * 0.5 + 0.3 * 1.0 = 0.65 (need to account for floating point error)
    assert abs(response2.json()["confidence_score"] - 0.65) < 0.0001
    assert response2.json()["review_count"] == 2
    