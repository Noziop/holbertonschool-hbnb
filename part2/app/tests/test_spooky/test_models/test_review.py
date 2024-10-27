# app/tests/test_spooky/test_models/test_review.py
"""Test module for our Review model! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture(autouse=True)
def setup_repository():
    """Setup clean repository for each test! 🏰"""
    from app.models.review import Review
    from app.persistence.repository import InMemoryRepository
    
    # Create new repository and clear any existing data
    repo = InMemoryRepository()
    repo._storage.clear()
    
    # Set repository for Review class
    Review.repository = repo
    
    yield repo
    
    # Cleanup after test
    repo._storage.clear()

@pytest.fixture
def test_review():
    """Create a test review! 📝"""
    from app.models.review import Review
    
    review = Review(
        place_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        text="This haunted mansion was absolutely terrifying! Would definitely haunt again!",
        rating=5
    )
    review.save()
    return review

def test_review_creation():
    """Test basic Review creation! 🎭"""
    from app.models.review import Review
    
    review = Review(
        place_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        text="A spooky experience that I'll never forget!",
        rating=4
    )
    
    # Required attributes
    assert isinstance(review.place_id, str)
    assert isinstance(review.user_id, str)
    assert review.text == "A spooky experience that I'll never forget!"
    assert review.rating == 4
    
    # BaseModel attributes
    assert hasattr(review, 'id')
    assert hasattr(review, 'created_at')
    assert hasattr(review, 'updated_at')
    assert review.is_active is True
    assert review.is_deleted is False

def test_review_validation():
    """Test Review validation rules! 🎭"""
    from app.models.review import Review
    
    # Test invalid text (too short)
    with pytest.raises(ValueError):
        Review(
            place_id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            text="Too short",
            rating=4
        )
    
    # Test invalid rating (out of range)
    with pytest.raises(ValueError):
        Review(
            place_id=str(uuid.uuid4()),
            user_id=str(uuid.uuid4()),
            text="This is a valid review text that is long enough",
            rating=6
        )
    
    # Test invalid place_id
    with pytest.raises(ValueError):
        Review(
            place_id="",
            user_id=str(uuid.uuid4()),
            text="This is a valid review text that is long enough",
            rating=4
        )
    
    # Test invalid user_id
    with pytest.raises(ValueError):
        Review(
            place_id=str(uuid.uuid4()),
            user_id="",
            text="This is a valid review text that is long enough",
            rating=4
        )

def test_review_update(test_review):
    """Test Review update functionality! 🔄"""
    # Update text and rating
    test_review.update({
        'text': "Updated review: Even spookier than before!",
        'rating': 3
    })
    
    assert test_review.text == "Updated review: Even spookier than before!"
    assert test_review.rating == 3
    
    # Test invalid updates
    with pytest.raises(ValueError):
        test_review.update({'text': "too short"})
    
    with pytest.raises(ValueError):
        test_review.update({'rating': 0})

def test_review_to_dict(test_review):
    """Test Review to_dict transformation! 📝"""
    review_dict = test_review.to_dict()
    
    assert isinstance(review_dict, dict)
    assert review_dict['place_id'] == test_review.place_id
    assert review_dict['user_id'] == test_review.user_id
    assert review_dict['text'] == test_review.text
    assert review_dict['rating'] == test_review.rating
    assert 'id' in review_dict
    assert 'created_at' in review_dict
    assert 'updated_at' in review_dict
    assert 'is_active' in review_dict
    assert 'is_deleted' in review_dict

def test_review_anonymize(test_review):
    """Test Review anonymization! 🎭"""
    # Remember original user_id
    original_user_id = test_review.user_id
    
    # Anonymize review
    test_review.anonymize()
    
    # Check if user_id is None
    assert test_review.user_id is None
    assert test_review.user_id != original_user_id

def test_review_get_by_place():
    """Test Review retrieval by place! 🏰"""
    from app.models.review import Review
    
    place_id = str(uuid.uuid4())
    
    # Create multiple reviews for same place
    review1 = Review(
        place_id=place_id,
        user_id=str(uuid.uuid4()),
        text="First spooky review of this haunted place!",
        rating=5
    )
    review1.save()
    
    review2 = Review(
        place_id=place_id,
        user_id=str(uuid.uuid4()),
        text="Second ghostly experience at this location!",
        rating=4
    )
    review2.save()
    
    # Test retrieval
    place_reviews = Review.get_by_attr(multiple=True, place_id=place_id)
    assert len(place_reviews) == 2
    assert all(review.place_id == place_id for review in place_reviews)

def test_review_get_by_user():
    """Test Review retrieval by user! 👤"""
    from app.models.review import Review
    
    user_id = str(uuid.uuid4())
    
    # Create multiple reviews by same user
    review1 = Review(
        place_id=str(uuid.uuid4()),
        user_id=user_id,
        text="This ghost hunter has visited many haunted places!",
        rating=5
    )
    review1.save()
    
    review2 = Review(
        place_id=str(uuid.uuid4()),
        user_id=user_id,
        text="Another spooky location reviewed by me!",
        rating=3
    )
    review2.save()
    
    # Test retrieval
    user_reviews = Review.get_by_attr(multiple=True, user_id=user_id)
    assert len(user_reviews) == 2
    assert all(review.user_id == user_id for review in user_reviews)

def test_review_get_by_rating():
    """Test Review retrieval by rating! ⭐"""
    from app.models.review import Review
    
    # Create reviews with different ratings
    review1 = Review(
        place_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        text="Perfect haunted experience! Maximum spookiness!",
        rating=5
    )
    review1.save()
    
    review2 = Review(
        place_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        text="Could have been spookier, but still good!",
        rating=3
    )
    review2.save()
    
    # Test retrieval
    five_star_reviews = Review.get_by_attr(multiple=True, rating=5)
    assert len(five_star_reviews) == 1
    assert all(review.rating == 5 for review in five_star_reviews)