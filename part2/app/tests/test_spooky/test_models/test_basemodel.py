# app/tests/test_spooky/test_models/test_basemodel.py
"""Test module for our BaseModel! 👻"""
import pytest
from datetime import datetime, timezone
import uuid
from time import sleep

@pytest.fixture
def repository():
    """Create a fresh repository for each test! 🏰"""
    from app.persistence.repository import InMemoryRepository
    repo = InMemoryRepository()
    return repo

def test_basemodel_creation():
    """Test basic BaseModel creation with default values! 🎭"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    
    # Vérification des attributs par défaut
    assert hasattr(model, 'id')
    assert isinstance(model.id, str)
    assert uuid.UUID(model.id)
    
    assert hasattr(model, 'created_at')
    assert isinstance(model.created_at, datetime)
    assert model.created_at.tzinfo == timezone.utc
    
    assert hasattr(model, 'updated_at')
    assert isinstance(model.updated_at, datetime)
    assert model.updated_at.tzinfo == timezone.utc
    
    assert hasattr(model, 'is_active')
    assert model.is_active is True

def test_basemodel_with_custom_attributes():
    """Test BaseModel creation with custom attributes! 🎭"""
    from app.models.basemodel import BaseModel
    
    custom_id = str(uuid.uuid4())
    custom_date = datetime.now(timezone.utc)
    
    model = BaseModel(
        id=custom_id,
        created_at=custom_date.isoformat(),
        updated_at=custom_date.isoformat(),
        name="test"  # Attribut custom
    )
    
    assert model.id == custom_id
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)
    assert model.name == "test"

def test_basemodel_to_dict():
    """Test BaseModel to_dict transformation! 🎭"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    model_dict = model.to_dict()
    
    assert isinstance(model_dict, dict)
    assert 'id' in model_dict
    assert 'created_at' in model_dict
    assert 'updated_at' in model_dict
    assert 'is_active' in model_dict
    
    assert isinstance(model_dict['created_at'], str)
    assert isinstance(model_dict['updated_at'], str)

def test_basemodel_update():
    """Test BaseModel update timestamp! 🎭"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    original_updated_at = model.updated_at
    
    sleep(0.1)
    
    model.update({'name': 'test'})
    
    assert model.updated_at > original_updated_at
    assert hasattr(model, 'name')
    assert model.name == 'test'

def test_basemodel_repository_operations(repository):
    """Test BaseModel repository operations! 📚"""
    from app.models.basemodel import BaseModel
    
    # Configuration du repository
    BaseModel.repository = repository
    
    # Test save
    model = BaseModel()
    saved_model = model.save()
    assert saved_model.id == model.id
    
    # Test get_by_id
    retrieved_model = BaseModel.get_by_id(model.id)
    assert retrieved_model.id == model.id
    
    # Test get_by_attr
    found_model = BaseModel.get_by_attr(id=model.id)
    assert found_model.id == model.id
    
    # Test update via repository
    model.update({'name': 'test'})
    updated_model = BaseModel.get_by_id(model.id)
    assert hasattr(updated_model, 'name')
    assert updated_model.name == 'test'

def test_basemodel_deletion_states():
    """Test BaseModel deletion states! ⚰️"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    model.save()
    
    # Test initial states
    assert model.is_active is True
    assert model.is_deleted is False
    
    # Test setting is_active
    model.update({'is_active': False})
    assert model.is_active is False
    assert model.is_deleted is False
    
    # Test hard delete
    assert model.hard_delete() is True
    
    # Verify model is really gone
    with pytest.raises(ValueError):
        BaseModel.get_by_id(model.id)

def test_basemodel_protected_attributes():
    """Test BaseModel protected attributes! 🔒"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    model.save()
    
    # Test updating protected attributes
    with pytest.raises(ValueError):
        model.update({'id': str(uuid.uuid4())})
    
    with pytest.raises(ValueError):
        model.update({'created_at': datetime.now(timezone.utc)})
    
    with pytest.raises(ValueError):
        model.update({'is_deleted': True})

def test_basemodel_to_dict_with_deletion_state():
    """Test BaseModel to_dict with deletion state! 📚"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    model_dict = model.to_dict()
    
    assert isinstance(model_dict, dict)
    assert 'is_active' in model_dict
    assert 'is_deleted' in model_dict
    assert model_dict['is_active'] is True
    assert model_dict['is_deleted'] is False

def test_basemodel_get_by_single_attr(repository):
    """Test BaseModel get_by_attr with single attribute! 🔍"""
    from app.models.basemodel import BaseModel
    
    BaseModel.repository = repository
    
    # Create and save a model with specific attributes
    model = BaseModel(name="test", tag="special")
    model.save()
    
    # Test get by single attribute
    found = BaseModel.get_by_attr(name="test")
    assert found is not None
    assert found.name == "test"
    assert found.id == model.id

def test_basemodel_get_by_multiple_attrs(repository):
    """Test BaseModel get_by_attr with multiple attributes! 🔍"""
    from app.models.basemodel import BaseModel
    
    BaseModel.repository = repository
    
    # Create and save models with different combinations of attributes
    model1 = BaseModel(name="test1", tag="special", category="A")
    model1.save()
    model2 = BaseModel(name="test2", tag="special", category="B")
    model2.save()
    
    # Test get by multiple attributes
    found = BaseModel.get_by_attr(tag="special", category="A")
    assert found is not None
    assert found.name == "test1"
    assert found.category == "A"

def test_basemodel_get_by_multiple_results(repository):
    """Test BaseModel get_by_attr with multiple results! 🔍"""
    from app.models.basemodel import BaseModel
    
    BaseModel.repository = repository
    
    # Create and save multiple models with same attribute
    model1 = BaseModel(tag="special")
    model1.save()
    model2 = BaseModel(tag="special")
    model2.save()
    
    # Test get multiple results
    found = BaseModel.get_by_attr(multiple=True, tag="special")
    assert isinstance(found, list)
    assert len(found) == 2
    assert all(model.tag == "special" for model in found)

def test_basemodel_get_by_nonexistent_attr(repository):
    """Test BaseModel get_by_attr with nonexistent attributes! 🔍"""
    from app.models.basemodel import BaseModel
    
    BaseModel.repository = repository
    
    # Create and save a model
    model = BaseModel(name="test")
    model.save()
    
    # Test get by nonexistent attribute
    found = BaseModel.get_by_attr(nonexistent="value")
    assert found is None
    
    # Test get multiple with nonexistent attribute
    found_multiple = BaseModel.get_by_attr(multiple=True, nonexistent="value")
    assert isinstance(found_multiple, list)
    assert len(found_multiple) == 0

def test_basemodel_get_by_combined_conditions(repository):
    """Test BaseModel get_by_attr with combined conditions! 🔍"""
    from app.models.basemodel import BaseModel
    
    BaseModel.repository = repository
    
    # Create models with various attributes
    model1 = BaseModel(name="test", status="active", priority=1)
    model1.save()
    model2 = BaseModel(name="test", status="inactive", priority=2)
    model2.save()
    
    # Test complex queries
    found = BaseModel.get_by_attr(name="test", status="active")
    assert found is not None
    assert found.priority == 1
    
    # Test with multiple results
    found_multiple = BaseModel.get_by_attr(multiple=True, name="test")
    assert len(found_multiple) == 2
    assert {model.status for model in found_multiple} == {"active", "inactive"}