from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
import re
from app.utils import *

class Amenity(BaseModel):
    repository = InMemoryRepository()


    @magic_wand(validate_input(AmenityValidation))
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = self._validate_name(name)

    @staticmethod
    @magic_wand()
    def _validate_name(name):
        if not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not re.match(r'^[\w\s-]+$', name):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        return name.strip()

    @classmethod
    @magic_wand(validate_input(AmenityValidation))
    def create(cls, **kwargs):
        try:
            amenity_to_create = cls.get_by_name(kwargs['name'])
            if amenity_to_create:
                raise ValueError(f"Amenity with name '{kwargs['name']}' already exists")
            else:
                amenity = cls(**kwargs)
                cls.repository.add(amenity)
                return amenity
        except KeyError:
            raise ValueError("Missing required attribute: name")
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Failed to create amenity: {str(e)}")

    @classmethod
    @magic_wand(validate_input(AmenityValidation))
    def get_by_name(cls, name):
        """Get amenity by name"""
        return cls.repository.get_by_attribute('name', name)

    @classmethod
    @magic_wand(validate_input({'keyword': str}))
    def search(cls, keyword):
        return [amenity for amenity in cls.get_all() if keyword.lower() in amenity.name.lower()]


    @magic_wand(validate_input({'data': dict}))
    def update(self, data):
        if getattr(self, '_is_updating', False):
            return self
        
        self._is_updating = True
        try:
            print(f"DEBUG Model - Starting update with data: {data}")
            if 'name' in data:
                new_name = data['name']
                print(f"DEBUG Model - Checking name: {new_name}")
                existing_amenity = Amenity.get_by_name(new_name)
                print(f"DEBUG Model - Existing amenity check: {existing_amenity}")  # Ajout de ce debug
                
                if existing_amenity:
                    print(f"DEBUG Model - Comparing IDs: self={self.id}, existing={existing_amenity.id}")  # Et celui-ci
                    if existing_amenity.id != self.id:
                        print("DEBUG Model - Name already exists, raising error")  # Et celui-là
                        raise ValueError(f"Amenity with name '{new_name}' already exists")
                
                self.name = self._validate_name(new_name)
                print(f"DEBUG Model - Name updated to: {self.name}")
            
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(self, key, value)
            
            return self
        except ValueError as e:
            print(f"DEBUG Model - ValueError caught: {str(e)}")  # Et celui-ci
            raise  # Relance l'erreur telle quelle
        except Exception as e:
            print(f"DEBUG Model - Unexpected error: {str(e)}")  # Et celui-ci
            raise
        finally:
            self._is_updating = False
    
    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict