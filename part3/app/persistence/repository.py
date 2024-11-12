"""Repository pattern for our haunted database! 👻"""
from app import db
from app.utils import log_me


class SQLAlchemyRepository:
    """SQLAlchemy implementation of our haunted repository! 👻"""

    def __init__(self, model):
        """Initialize with a specific model class! 🎭"""
        self.model = model

    @log_me(component="persistence")
    def add(self, obj):
        """Summon a new spirit into our database! ✨"""
        db.session.add(obj)
        db.session.commit()

    @log_me(component="persistence")
    def get(self, obj_id):
        """Channel a specific spirit from the beyond! 🔮"""
        return self.model.query.get(obj_id)

    @log_me(component="persistence")
    def get_all(self):
        """Summon ALL the spirits! 👻"""
        return self.model.query.all()

    @log_me(component="persistence")
    def get_by_email(self, email):
        """Find a spirit by their spectral email! 📧"""
        return self.model.query.filter_by(email=email).first()

    @log_me(component="persistence")
    def update(self, obj_id, data):
        """Transform a spirit's essence! 🌟"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    @log_me(component="persistence")
    def delete(self, obj_id):
        """Banish a spirit back to the void! ⚡"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    @log_me(component="persistence")
    def get_by_attribute(self, multiple: bool = False, **kwargs):
        """Find spirits by their spectral signatures! 🔍

        Args:
            multiple: Want one ghost or a whole haunted house? 🏚️
            **kwargs: The dark specifications for our search
        """
        query = self.model.query.filter_by(**kwargs)
        print(f"REPO - kwargs: {kwargs}")
        print(f"REPO - query: {query}")
        return query.all() if multiple else query.first()

    @log_me(component="persistence")
    def save(self, obj):
        """Save or update a spirit in our realm! 💾"""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to save: {str(e)}")

    @log_me(component="persistence")
    def update(self, obj):
        """Transform a spirit's essence! 🌟"""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to update: {str(e)}")

    @log_me(component="persistence")
    def delete(self, obj):
        """Soft delete a spirit! 👻"""
        try:
            obj.is_deleted = True
            db.session.add(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to delete: {str(e)}")

    @log_me(component="persistence")
    def hard_delete(self, obj):
        """Permanently banish a spirit! ⚰️"""
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to hard delete: {str(e)}")
