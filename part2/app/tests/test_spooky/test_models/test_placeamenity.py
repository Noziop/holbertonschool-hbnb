# app/tests/test_spooky/test_models/test_placeamenity.py
"""Test module for our PlaceAmenity model! 👻"""
import uuid
from datetime import datetime, timezone

import pytest


@pytest.fixture(autouse=True)
def setup_repository():
    """Setup clean repository for each test! 🏰"""
    from app.models.amenity import Amenity
    from app.models.place import Place
    from app.models.placeamenity import PlaceAmenity
    from app.models.user import User
    from app.persistence.repository import InMemoryRepository

    # Create new repository and clear any existing data
    repo = InMemoryRepository()
    repo._storage.clear()

    # Set repository for all classes
    PlaceAmenity.repository = repo
    Place.repository = repo
    Amenity.repository = repo
    User.repository = repo

    yield repo

    # Cleanup after test
    repo._storage.clear()


@pytest.fixture
def test_owner():
    """Create a test owner! 👻"""
    from app.models.user import User

    owner = User(
        username="ghost_owner",
        email="owner@haunted.com",
        password="Ghost123!@#",
        first_name="Ghost",
        last_name="Owner",
    )
    owner.save()
    return owner


@pytest.fixture
def test_place(test_owner):
    """Create a test place! 🏰"""
    from app.models.place import Place

    place = Place(
        name="Haunted Manor",
        description="A very spooky place!",
        owner_id=test_owner.id,
        price_by_night=100.0,
    )
    place.save()
    return place


@pytest.fixture
def test_amenity():
    """Create a test amenity! 🎭"""
    from app.models.amenity import Amenity

    amenity = Amenity(
        name="Ghost Detector", description="Detects supernatural activity!"
    )
    amenity.save()
    return amenity


def test_placeamenity_creation(test_place, test_amenity):
    """Test basic PlaceAmenity creation! 🎭"""
    from app.models.placeamenity import PlaceAmenity

    link = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)

    assert link.place_id == test_place.id
    assert link.amenity_id == test_amenity.id
    assert hasattr(link, "id")
    assert hasattr(link, "created_at")
    assert hasattr(link, "updated_at")
    assert link.is_active is True
    assert link.is_deleted is False


def test_placeamenity_validation():
    """Test PlaceAmenity validation rules! 🎭"""
    from app.models.placeamenity import PlaceAmenity

    # Test invalid place_id
    with pytest.raises(ValueError):
        PlaceAmenity(place_id="invalid-id", amenity_id=str(uuid.uuid4()))

    # Test invalid amenity_id
    with pytest.raises(ValueError):
        PlaceAmenity(place_id=str(uuid.uuid4()), amenity_id="invalid-id")


def test_placeamenity_to_dict(test_place, test_amenity):
    """Test PlaceAmenity to_dict transformation! 📝"""
    from app.models.placeamenity import PlaceAmenity

    link = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)
    link.save()

    link_dict = link.to_dict()

    assert isinstance(link_dict, dict)
    assert link_dict["place_id"] == test_place.id
    assert link_dict["amenity_id"] == test_amenity.id
    assert "id" in link_dict
    assert "created_at" in link_dict
    assert "updated_at" in link_dict
    assert "is_active" in link_dict
    assert "is_deleted" in link_dict


# app/tests/test_spooky/test_models/test_placeamenity.py


def test_placeamenity_validation_edge_cases(test_place, test_amenity):
    """Test PlaceAmenity validation edge cases! 🔍"""
    from app.models.placeamenity import PlaceAmenity

    # Test avec place_id invalide
    with pytest.raises(ValueError):
        PlaceAmenity(place_id="", amenity_id=test_amenity.id)

    # Test avec amenity_id invalide
    with pytest.raises(ValueError):
        PlaceAmenity(place_id=test_place.id, amenity_id="")

    # Test avec repository None
    link = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)
    link.repository = None

    with pytest.raises(ValueError):
        link.save()

    with pytest.raises(ValueError):
        link.hard_delete()


def test_placeamenity_duplicate_link(test_place, test_amenity):
    """Test PlaceAmenity duplicate prevention! 🎭"""
    from app.models.placeamenity import PlaceAmenity

    # Create first link
    link1 = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)
    link1.save()

    # Try to create duplicate link
    with pytest.raises(ValueError):
        link2 = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)
        link2.save()


def test_placeamenity_get_methods(test_place, test_amenity):
    """Test PlaceAmenity get methods! 🔍"""
    from app.models.placeamenity import PlaceAmenity

    # Create link
    link = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)
    link.save()

    # Test get_by_id
    found = PlaceAmenity.get_by_id(link.id)
    assert found.id == link.id

    # Test get_by_attr with multiple=True
    found_multiple = PlaceAmenity.get_by_attr(multiple=True, place_id=test_place.id)
    assert len(found_multiple) == 1
    assert all(l.place_id == test_place.id for l in found_multiple)

    # Test get_by_attr with non-existent attributes
    not_found = PlaceAmenity.get_by_attr(nonexistent="value")
    assert not_found is None


def test_placeamenity_cascade_on_place_delete():
    """Test PlaceAmenity links are deleted when place is deleted! 🏰"""
    from app.models.amenity import Amenity
    from app.models.place import Place
    from app.models.placeamenity import PlaceAmenity
    from app.models.user import User

    # Create owner
    owner = User(
        username="test_owner",
        email="owner@test.com",
        password="Test123!@#",
        first_name="Test",
        last_name="Owner",
    )
    owner.save()

    # Create place
    place = Place(
        name="Test Place",
        description="Test Description",
        owner_id=owner.id,
        price_by_night=100.0,
    )
    place.save()

    # Create amenity
    amenity = Amenity(name="Test Amenity", description="Test Description")
    amenity.save()

    # Create link
    link = PlaceAmenity(place_id=place.id, amenity_id=amenity.id)
    link.save()

    # Get link ID for later check
    link_id = link.id
    amenity_id = amenity.id

    # Delete place
    place.hard_delete()

    # Verify:
    # 1. Link is deleted
    with pytest.raises(ValueError):
        PlaceAmenity.get_by_id(link_id)

    # 2. Amenity still exists
    amenity = Amenity.get_by_id(amenity_id)
    assert amenity is not None


def test_placeamenity_validation_complete(test_owner):
    """Test PlaceAmenity validation completely! 🔗"""
    from app.models.amenity import Amenity
    from app.models.place import Place
    from app.models.placeamenity import PlaceAmenity

    # Create valid place and amenity
    place = Place(
        name="Test Manor",
        description="Test Description",
        owner_id=test_owner.id,
        price_by_night=100.0,
    )
    place.save()

    amenity = Amenity(name="Test Amenity", description="Test Description")
    amenity.save()

    # Test normal creation
    link = PlaceAmenity(place_id=place.id, amenity_id=amenity.id)
    link.save()

    # Test invalid place_id format
    with pytest.raises(ValueError):
        PlaceAmenity(place_id="", amenity_id=amenity.id)  # Invalid empty ID

    # Test invalid amenity_id format
    with pytest.raises(ValueError):
        PlaceAmenity(place_id=place.id, amenity_id="")  # Invalid empty ID

    # Test non-existent place_id
    with pytest.raises(ValueError):
        PlaceAmenity(
            place_id=str(uuid.uuid4()),  # Valid format but doesn't exist
            amenity_id=amenity.id,
        )

    # Test non-existent amenity_id
    with pytest.raises(ValueError):
        PlaceAmenity(
            place_id=place.id,
            amenity_id=str(uuid.uuid4()),  # Valid format but doesn't exist
        )


def test_placeamenity_import_errors():
    """Test PlaceAmenity import error handling! 🎭"""
    import sys

    from app.models.placeamenity import PlaceAmenity

    # Sauvegarder les modules existants
    old_modules = dict(sys.modules)

    # Simuler l'absence des modules
    sys.modules["app.models.place"] = None
    sys.modules["app.models.amenity"] = None

    # Test création avec modules manquants
    link = PlaceAmenity(place_id="some-id", amenity_id="other-id")

    # Restaurer les modules
    sys.modules.update(old_modules)


def test_placeamenity_validation_complete(test_place, test_amenity):
    """Test PlaceAmenity validation completely! 🔗"""
    from app.models.placeamenity import PlaceAmenity

    # Test création normale
    link = PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)
    link.save()

    # Test ID vide
    with pytest.raises(ValueError):
        PlaceAmenity(place_id="", amenity_id=test_amenity.id)

    # Test ID invalide
    with pytest.raises(ValueError):
        PlaceAmenity(place_id="invalid-id", amenity_id=test_amenity.id)

    # Test lien dupliqué
    with pytest.raises(ValueError, match="Link already exists"):
        PlaceAmenity(place_id=test_place.id, amenity_id=test_amenity.id)


def test_placeamenity_import_errors(monkeypatch):
    """Test PlaceAmenity import error handling! 🎭"""
    from app.models.placeamenity import PlaceAmenity

    # Simuler l'erreur d'import pour Place
    def mock_import_error(*args):
        raise ImportError("Place not found")

    monkeypatch.setattr("builtins.__import__", mock_import_error)

    # Test validation avec Place manquant
    link = PlaceAmenity(place_id="test-id", amenity_id="test-id")

    # Test validation avec Amenity manquant
    link = PlaceAmenity(place_id="test-id", amenity_id="test-id")
