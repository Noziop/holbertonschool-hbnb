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

def test_basemodel_soft_delete():
    """Test BaseModel soft delete! ⚰️"""
    from app.models.basemodel import BaseModel
    
    model = BaseModel()
    model.save()
    
    assert model.is_active is True
    model.delete()
    assert model.is_active is False