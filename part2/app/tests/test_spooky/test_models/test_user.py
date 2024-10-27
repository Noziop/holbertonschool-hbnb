# app/tests/test_spooky/test_models/test_user.py
"""Test module for our UserModel! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture
def repository():
    """Create a fresh repository for each test! 🏰"""
    from app.persistence.repository import InMemoryRepository
    return InMemoryRepository()

def test_user_creation():
    """Test basic User creation with default values! 🎭"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly"
    )
    
    # Vérification des attributs requis
    assert hasattr(user, 'id')
    assert isinstance(user.id, str)
    assert uuid.UUID(user.id)
    
    assert hasattr(user, 'username')
    assert user.username == "friendly_ghost"
    
    assert hasattr(user, 'email')
    assert user.email == "ghost@haunted.com"
    
    assert hasattr(user, 'password_hash')  # On vérifie le hash, pas le password
    
    assert hasattr(user, 'first_name')
    assert user.first_name == "Casper"
    
    assert hasattr(user, 'last_name')
    assert user.last_name == "Friendly"
    
    # Vérification des attributs par défaut
    assert hasattr(user, 'is_active')
    assert user.is_active is True
    
    assert hasattr(user, 'is_admin')
    assert user.is_admin is False

def test_user_with_optional_attributes():
    """Test User creation with optional attributes! 🎭"""
    from app.models.user import User
    
    user = User(
        username="spooky_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly",
        address="13 Haunted Street",
        postal_code="13666",
        city="Ghostville",
        phone="+1-666-GHOST"
    )
    
    assert user.username == "spooky_ghost"
    assert user.address == "13 Haunted Street"
    assert user.postal_code == "13666"
    assert user.city == "Ghostville"
    assert user.phone == "+1-666-GHOST"

def test_user_update():
    """Test User update! 🎭"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly"
    )
    
    original_updated_at = user.updated_at
    
    # Update required fields
    user.update({
        'username': 'super_ghost',
        'first_name': 'Super',
        'last_name': 'Ghost'
    })
    
    assert user.username == 'super_ghost'
    assert user.first_name == 'Super'
    assert user.last_name == 'Ghost'
    assert user.updated_at > original_updated_at
    
    # Update optional fields
    user.update({
        'address': '666 Spooky Lane',
        'phone': '+1-666-BOO'
    })
    
    assert user.address == '666 Spooky Lane'
    assert user.phone == '+1-666-BOO'

def test_user_to_dict():
    """Test User to_dict transformation! 🎭"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly",
        address="13 Haunted Street",
        phone="+1-666-GHOST"
    )
    
    user_dict = user.to_dict()
    
    assert isinstance(user_dict, dict)
    assert 'id' in user_dict
    assert 'username' in user_dict
    assert 'email' in user_dict
    assert 'password' not in user_dict  # Password should not be in dict
    assert 'password_hash' not in user_dict  # Hash should not be in dict
    assert 'first_name' in user_dict
    assert 'last_name' in user_dict
    assert 'address' in user_dict
    assert 'phone' in user_dict
    assert 'created_at' in user_dict
    assert 'updated_at' in user_dict
    assert 'is_active' in user_dict
    assert 'is_admin' in user_dict

def test_user_account_states():
    """Test User account states (pause, reactivate)! 🌙"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Test pause account
    assert user.pause_account() is True
    assert user.is_active is False
    assert user.is_deleted is False
    
    # Test reactivate account
    assert user.reactivate_account() is True
    assert user.is_active is True
    assert user.is_deleted is False

def test_user_delete():
    """Test User deletion with related entities! ⚰️"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Test soft delete
    assert user.delete() is True
    assert user.is_active is False
    assert user.is_deleted is True
    
    # Test cannot reactivate deleted account
    with pytest.raises(ValueError):
        user.reactivate_account()

def test_user_places_visibility():
    """Test User places visibility when account is paused! 🏠"""
    from app.models.user import User
    from app.models.place import Place
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Create a place for the user
    place = Place(
        name="Haunted Mansion",
        owner_id=user.id,
        description="A spooky place",
        price_by_night=100
    )
    place.save()
    
    # Test place visibility when account is paused
    user.pause_account()
    assert place.is_active is False
    
    # Test place visibility when account is reactivated
    user.reactivate_account()
    assert place.is_active is True

def test_user_delete_with_reviews():
    """Test User deletion with reviews! 📝"""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    
    # Create user
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Create place first
    owner = User(
        username="place_owner",
        email="owner@haunted.com",
        password="Owner123!@#",
        first_name="Owner",
        last_name="Ghost"
    )
    owner.save()
    
    place = Place(
        name="Haunted Manor",
        description="A very spooky place!",
        owner_id=owner.id,
        price_by_night=100.0
    )
    place.save()
    
    # Now create review
    review = Review(
        user_id=user.id,
        place_id=place.id,
        text="Spooky place!",
        rating=5
    )
    review.save()
    
    # Test soft delete
    user.delete()
    
    # Check if review is anonymized
    updated_review = Review.get_by_id(review.id)
    assert updated_review.user_id is None

def test_user_get_by_username(repository):
    """Test User retrieval by username! 🔍"""
    from app.models.user import User
    User.repository = repository
    
    # Create test users
    user1 = User(
        username="ghost1",
        email="ghost1@haunted.com",
        password="Ghost123!@#",
        first_name="Casper",
        last_name="First"
    )
    user1.save()
    
    # Test retrieval
    found = User.get_by_attr(username="ghost1")
    assert found is not None
    assert found.username == "ghost1"
    assert found.email == "ghost1@haunted.com"

def test_user_get_by_email(repository):
    """Test User retrieval by email! 📧"""
    from app.models.user import User
    User.repository = repository
    
    # Create test user
    user = User(
        username="ghost2",
        email="ghost2@haunted.com",
        password="Ghost123!@#",
        first_name="Casper",
        last_name="Second"
    )
    user.save()
    
    # Test retrieval
    found = User.get_by_attr(email="ghost2@haunted.com")
    assert found is not None
    assert found.username == "ghost2"

def test_user_get_by_multiple_criteria(repository):
    """Test User retrieval by multiple criteria! 🔍"""
    from app.models.user import User
    User.repository = repository
    
    # Create test users
    user1 = User(
        username="ghost3",
        email="ghost3@haunted.com",
        password="Ghost123!@#",
        first_name="Casper",
        last_name="Third",
        city="Ghostville"
    )
    user1.save()
    
    user2 = User(
        username="ghost4",
        email="ghost4@haunted.com",
        password="Ghost123!@#",
        first_name="Casper",
        last_name="Fourth",
        city="Ghostville"
    )
    user2.save()
    
    # Test retrieval by multiple criteria
    found = User.get_by_attr(city="Ghostville", username="ghost3")
    assert found is not None
    assert found.username == "ghost3"
    
    # Test retrieval of multiple users
    found_multiple = User.get_by_attr(multiple=True, city="Ghostville")
    assert len(found_multiple) == 2
    assert {user.username for user in found_multiple} == {"ghost3", "ghost4"}

def test_user_get_by_admin_status(repository):
    """Test User retrieval by admin status! 👑"""
    from app.models.user import User
    User.repository = repository
    
    # Create admin and non-admin users
    admin = User(
        username="admin_ghost",
        email="admin@haunted.com",
        password="Admin123!@#",
        first_name="Admin",
        last_name="Ghost",
        is_admin=True
    )
    admin.save()
    
    user = User(
        username="normal_ghost",
        email="normal@haunted.com",
        password="Ghost123!@#",
        first_name="Normal",
        last_name="Ghost"
    )
    user.save()
    
    # Test retrieval of admin users
    admins = User.get_by_attr(multiple=True, is_admin=True)
    assert len(admins) == 1
    assert admins[0].username == "admin_ghost"

def test_user_get_by_active_status(repository):
    """Test User retrieval by active status! 🌟"""
    from app.models.user import User
    User.repository = repository
    
    # Create and pause a user
    user = User(
        username="inactive_ghost",
        email="inactive@haunted.com",
        password="Ghost123!@#",
        first_name="Inactive",
        last_name="Ghost"
    )
    user.save()
    user.pause_account()
    
    # Test retrieval by active status
    inactive_users = User.get_by_attr(multiple=True, is_active=False)
    assert len(inactive_users) == 1
    assert inactive_users[0].username == "inactive_ghost"

def test_user_get_nonexistent(repository):
    """Test User retrieval with nonexistent criteria! 👻"""
    from app.models.user import User
    User.repository = repository
    
    # Test retrieval with nonexistent username
    found = User.get_by_attr(username="nonexistent")
    assert found is None
    
    # Test retrieval with nonexistent email
    found = User.get_by_attr(email="nonexistent@haunted.com")
    assert found is None

def test_user_get_by_combined_filters(repository):
    """Test User retrieval with combined filters! 🔍"""
    from app.models.user import User
    User.repository = repository
    
    # Create test users
    user1 = User(
        username="ghost5",
        email="ghost5@haunted.com",
        password="Ghost123!@#",
        first_name="Casper",
        last_name="Fifth",
        city="Ghostville",
        is_admin=True
    )
    user1.save()
    
    user2 = User(
        username="ghost6",
        email="ghost6@haunted.com",
        password="Ghost123!@#",
        first_name="Casper",
        last_name="Sixth",
        city="Ghostville",
        is_admin=True
    )
    user2.save()
    
    # Test complex filters
    found = User.get_by_attr(
        city="Ghostville",
        is_admin=True,
        is_active=True
    )
    assert found is not None
    
    found_multiple = User.get_by_attr(
        multiple=True,
        city="Ghostville",
        is_admin=True
    )
    assert len(found_multiple) == 2

def test_user_soft_delete_with_reviews_and_places():
    """Test complete user soft delete cascade! ⚰️"""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    
    # Create user
    user = User(
        username="ghost_owner",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Owner"
    )
    user.save()
    
    # Create place owned by user
    place = Place(
        name="Haunted Manor",
        description="A very spooky place!",
        owner_id=user.id,
        price_by_night=100.0
    )
    place.save()
    
    # Create another user for the other place
    other_owner = User(
        username="other_owner",
        email="other@haunted.com",
        password="Other123!@#",
        first_name="Other",
        last_name="Ghost"
    )
    other_owner.save()
    
    # Create another place for user to review
    other_place = Place(
        name="Other Manor",
        description="Another spooky place!",
        owner_id=other_owner.id,  # Utiliser l'ID du other_owner créé
        price_by_night=150.0
    )
    other_place.save()
    
    # Create review by user
    review = Review(
        place_id=other_place.id,
        user_id=user.id,
        text="This place was terrifyingly awesome!",
        rating=5
    )
    review.save()
    
    # Soft delete user
    user.delete()
    
    # Check cascade effects
    # 1. User's places should be hard deleted
    with pytest.raises(ValueError):
        Place.get_by_id(place.id)
    
    # 2. User's reviews should be anonymized
    updated_review = Review.get_by_id(review.id)
    assert updated_review.user_id is None
    assert updated_review.text == review.text  # Content preserved
    
    # 3. User should be marked as deleted
    assert user.is_deleted is True
    assert user.is_active is False

def test_user_review_place_constraints():
    """Test user can't review their own place! 🚫"""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    
    # Create user
    user = User(
        username="ghost_owner",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Owner"
    )
    user.save()
    
    # Create place owned by user
    place = Place(
        name="Haunted Manor",
        description="A very spooky place!",
        owner_id=user.id,
        price_by_night=100.0
    )
    place.save()
    
    # Try to review own place
    with pytest.raises(ValueError, match="Cannot review your own place"):
        review = Review(
            place_id=place.id,
            user_id=user.id,
            text="This is my awesome place!",
            rating=5
        )

def test_place_owner_validation():
    """Test place owner relationship validation! 🏰"""
    from app.models.place import Place
    
    # Try to create place with non-existent owner
    with pytest.raises(ValueError, match="Invalid owner_id"):
        place = Place(
            name="Ghost Manor",
            description="A spooky place!",
            owner_id="non-existent-id",
            price_by_night=100.0
        )

def test_review_cascade_on_place_delete():
    """Test reviews are deleted when place is deleted! 🏚️"""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    
    # Create owner first
    owner = User(
        username="place_owner",
        email="owner@haunted.com",
        password="Owner123!@#",
        first_name="Owner",
        last_name="Ghost"
    )
    owner.save()
    
    # Create place
    place = Place(
        name="Doomed Manor",
        description="Soon to be demolished!",
        owner_id=owner.id,  # Utiliser un vrai user_id
        price_by_night=100.0
    )
    place.save()
    
    # Create reviews for the place
    review1 = Review(
        place_id=place.id,
        user_id=str(uuid.uuid4()),
        text="Great place, shame it's being demolished!",
        rating=5
    )
    review1.save()
    
    review2 = Review(
        place_id=place.id,
        user_id=str(uuid.uuid4()),
        text="Will miss this haunted spot!",
        rating=4
    )
    review2.save()
    
    # Hard delete place
    place.hard_delete()
    
    # Check that reviews are gone
    reviews = Review.get_by_attr(multiple=True, place_id=place.id)
    assert len(reviews) == 0

# app/tests/test_spooky/test_models/test_user.py

def test_user_password_validation():
    """Test User password validation edge cases! 🔒"""
    from app.models.user import User
    
    # Test password too short
    with pytest.raises(ValueError):
        User(
            username="test_ghost",
            email="test@ghost.com",
            password="Short1",  # Too short
            first_name="Test",
            last_name="Ghost"
        )
    
    # Test password without uppercase
    with pytest.raises(ValueError):
        User(
            username="test_ghost",
            email="test@ghost.com",
            password="nouppercase123",
            first_name="Test",
            last_name="Ghost"
        )
    
    # Test password without lowercase
    with pytest.raises(ValueError):
        User(
            username="test_ghost",
            email="test@ghost.com",
            password="NOLOWERCASE123",
            first_name="Test",
            last_name="Ghost"
        )
    
    # Test password without number
    with pytest.raises(ValueError):
        User(
            username="test_ghost",
            email="test@ghost.com",
            password="NoNumbersHere!",
            first_name="Test",
            last_name="Ghost"
        )

def test_user_deletion_edge_cases():
    """Test User deletion edge cases! ⚰️"""
    from app.models.user import User
    
    # Test delete with invalid repository
    user = User(
        username="test_ghost",
        email="test@ghost.com",
        password="Test123!@#",
        first_name="Test",
        last_name="Ghost"
    )
    user.save()
    
    # Test delete with None repository
    user.repository = None
    with pytest.raises(ValueError, match="Repository not available"):
        user.delete()
    
    # Test hard_delete with None repository
    with pytest.raises(ValueError, match="Repository not available"):
        user.hard_delete()

def test_user_validation_edge_cases():
    """Test User validation edge cases! 🎭"""
    from app.models.user import User
    
    # Test invalid email formats
    invalid_emails = [
        "not.an.email",
        "@nodomain.com",
        "no@domain",
        "spaces in@email.com",
        ""
    ]
    
    for email in invalid_emails:
        with pytest.raises(ValueError):
            User(
                username="test_ghost",
                email=email,
                password="Test123!@#",
                first_name="Test",
                last_name="Ghost"
            )
    
    # Test invalid usernames
    invalid_usernames = [
        "ab",  # Too short
        "invalid@username",  # Invalid character
        "spaces not allowed",
        ""
    ]
    
    for username in invalid_usernames:
        with pytest.raises(ValueError):
            User(
                username=username,
                email="test@ghost.com",
                password="Test123!@#",
                first_name="Test",
                last_name="Ghost"
            )
    
    # Test invalid names
    invalid_names = [
        "a",  # Too short
        "Invalid123",  # Numbers not allowed
        "Invalid@Name",  # Special chars not allowed
        ""
    ]
    
    for name in invalid_names:
        with pytest.raises(ValueError):
            User(
                username="test_ghost",
                email="test@ghost.com",
                password="Test123!@#",
                first_name=name,
                last_name="Ghost"
            )