import inspect
import os
import sys

# Ajoute le répertoire parent au chemin de recherche de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity
from app.models.basemodel import BaseModel

def create_validation_dict(cls):
    attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    validation_dict = {}
    for attr, value in attributes:
        if not attr.startswith('__'):  # Ignore les attributs spéciaux
            if isinstance(value, property):
                # Si c'est une propriété, on prend le type de retour si possible
                return_type = inspect.signature(value.fget).return_annotation
                validation_dict[attr] = return_type if return_type != inspect.Signature.empty else object
            else:
                validation_dict[attr] = type(value)
    return validation_dict

# Crée automatiquement les dictionnaires de validation
UserValidation = create_validation_dict(User)
PlaceValidation = create_validation_dict(Place)
AmenityValidation = create_validation_dict(Amenity)
ReviewValidation = create_validation_dict(Review)
PlaceAmenityValidation = create_validation_dict(PlaceAmenity)
BaseModelValidation = create_validation_dict(BaseModel)

# Chemin du fichier de sortie
output_file = os.path.join(os.path.dirname(__file__), 'model_validations.py')

# Écris les dictionnaires dans un fichier
with open(output_file, 'w') as f:
    f.write("# Ce fichier est généré automatiquement. Ne pas modifier manuellement.\n\n")
    for model_name in ['User', 'Place', 'Amenity', 'Review', 'PlaceAmenity']:
        validation_dict = globals()[f"{model_name}Validation"]
        f.write(f"{model_name}Validation = {{\n")
        for attr, attr_type in validation_dict.items():
            f.write(f"    '{attr}': {attr_type.__name__},\n")
        f.write("}\n\n")

print(f"Fichier de validation généré : {output_file}")