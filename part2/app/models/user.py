from werkzeug.security import generate_password_hash, check_password_hash
from .basemodel import BaseModel

class User(BaseModel):
    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)
        self.is_active = True  # Pour gérer l'état du compte

    @classmethod
    def create(cls, username, email, password):
        existing_user = cls.get_by_username(username) or cls.get_by_email(email)
        if existing_user:
            raise Conflict("A user Already exists with these credentials (Username or Email or both).")

        # Vérifier que tous les champs requis sont renseignés
        if not all([username, email, password]):
            raise BadRequest("All fields (username, email, password) are required.")

        # Créer le nouvel utilisateur
        new_user = cls(username, email, password)

        # Sauvegarder dans la couche de persistance
        try:
            # Ici, on appellerait la méthode de sauvegarde de la couche de persistance
            # Par exemple : persistence.save(new_user)
            pass
        except Exception as e:
            # Gérer les erreurs de sauvegarde
            raise BadRequest(f"Error while saving user : {str(e)}")

        return new_user

    @classmethod
    def get_by_username(cls, username):
        for user in cls.users:
            if user.username == username:
                return user
        return None

    @classmethod
    def get_by_email(cls, email):
        # Cette méthode serait implémentée dans la couche de persistance
        pass

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # Ne pas oublier de mettre à jour dans la persistance

    def delete(self):
        self.is_active = False
        # Logique pour "soft delete" l'utilisateur

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active
        })
        return user_dict

    # Méthodes liées à l'authentification
    def authenticate(self, password):
        return self.check_password(password) and self.is_active