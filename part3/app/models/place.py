"""Place model module: Where haunted houses come to life! 👻."""

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy.orm import relationship

from app import db
from app.models.basemodel import BaseModel
from app.utils import log_me

if TYPE_CHECKING:  # noqa: F401
    from app.models.amenity import Amenity  # noqa: F401


class PlaceStatus(str, Enum):
    """The different states a haunted place can be in! 👻."""

    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    BLOCKED = "blocked"


class PropertyType(str, Enum):
    """The different types of haunted properties! 🏰."""

    HOUSE = "house"
    APARTMENT = "apartment"
    VILLA = "villa"


class Place(BaseModel):
    """Place: A haunted location in our supernatural realm! 🏰."""

    # SQLAlchemy columns
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner_id = db.Column(
        db.String(36), db.ForeignKey("user.id"), nullable=False
    )
    price_by_night = db.Column(db.Float, nullable=False)
    number_rooms = db.Column(db.Integer, default=1)
    number_bathrooms = db.Column(db.Integer, default=1)
    max_guest = db.Column(db.Integer, default=2)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    status = db.Column(
        db.Enum(PlaceStatus), default=PlaceStatus.ACTIVE, nullable=False
    )
    property_type = db.Column(
        db.Enum(PropertyType), default=PropertyType.APARTMENT, nullable=False
    )
    minimum_stay = db.Column(db.Integer, default=1)

    # Relationships
    owner = relationship("User", back_populates="places")
    place_amenities = relationship("PlaceAmenity", back_populates="place")
    reviews = relationship(
        "Review", back_populates="place", cascade="all, delete-orphan"
    )
    amenities = relationship(
        "Amenity", secondary="placeamenity", back_populates="places"
    )

    def __init__(
        self,
        name: str,
        description: str,
        owner_id: str,
        price_by_night: float,
        number_rooms: int = 1,
        number_bathrooms: int = 1,
        max_guest: int = 2,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        city: Optional[str] = "",
        country: Optional[str] = "",
        status: str = PlaceStatus.ACTIVE.value,
        property_type: str = PropertyType.APARTMENT.value,
        minimum_stay: int = 1,
        **kwargs,
    ):
        """Initialize a new haunted place! ✨."""
        super().__init__(**kwargs)

        # Required attributes
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        self.owner_id = self._validate_owner_id(owner_id)
        self.price_by_night = self._validate_price(price_by_night)

        # Optional attributes with defaults
        self.number_rooms = self._validate_positive_integer(
            number_rooms, "number_rooms"
        )
        self.number_bathrooms = self._validate_positive_integer(
            number_bathrooms, "number_bathrooms"
        )
        self.max_guest = self._validate_positive_integer(
            max_guest, "max_guest"
        )
        self.latitude = self._validate_latitude(latitude) if latitude else None
        self.longitude = (
            self._validate_longitude(longitude) if longitude else None
        )
        self.city = city
        self.country = country
        self.status = self._validate_status(status)
        self.property_type = self._validate_property_type(property_type)
        self.minimum_stay = self._validate_positive_integer(
            minimum_stay, "minimum_stay"
        )

    @log_me(component="business")
    def _validate_name(self, name: str) -> str:
        """Validate place name! 🏰."""
        if not isinstance(name, str) or len(name.strip()) < 3:
            error_msg = "Name must be at least 3 characters!"
            raise ValueError(error_msg)
        return name.strip()

    @log_me(component="business")
    def _validate_description(self, description: str) -> str:
        """Validate place description! 📝."""
        if not isinstance(description, str) or len(description.strip()) < 10:
            error_msg = "Description must be at least 10 characters!"
            raise ValueError(error_msg)
        return description.strip()

    @log_me(component="business")
    def _validate_owner_id(self, owner_id: str) -> str:
        """Validate owner ID! 👤."""
        try:
            from app.models.user import User  # noqa: F811

            if not User.get_by_id(owner_id):
                error_msg = "Invalid owner_id"
                raise ValueError(error_msg)
        except ImportError:
            raise ValueError("User model not implemented yet")
        except ValueError:
            error_msg = "Invalid owner_id"
            raise ValueError(error_msg)
        return owner_id

    @log_me(component="business")
    def _validate_price(self, price: float) -> float:
        """Validate price! 💰."""
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = "Price must be a positive number!"
            raise ValueError(error_msg)
        return price

    @log_me(component="business")
    def _validate_positive_integer(self, value: int, field: str) -> int:
        """Validate positive integer! 🔢."""
        try:
            value = int(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = f"{field} must be a positive integer!"
            raise ValueError(error_msg)
        return value

    @log_me(component="business")
    def _validate_latitude(self, latitude: float) -> float:
        """Validate latitude! 🌍."""
        try:
            latitude = float(latitude)
            if not -90 <= latitude <= 90:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = "Latitude must be between -90 and 90!"
            raise ValueError(error_msg)
        return latitude

    @log_me(component="business")
    def _validate_longitude(self, longitude: float) -> float:
        """Validate longitude! 🌍."""
        try:
            longitude = float(longitude)
            if not -180 <= longitude <= 180:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = "Longitude must be between -180 and 180!"
            raise ValueError(error_msg)
        return longitude

    @log_me(component="business")
    def _validate_status(self, status: str) -> str:
        """Validate place status! 📊."""
        try:
            return PlaceStatus(status)
        except ValueError:
            error_msg = f"Status must be one of: \
                {', '.join(s.value for s in PlaceStatus)}"
            raise ValueError(error_msg)

    @log_me(component="business")
    def _validate_property_type(self, property_type: str) -> str:
        """Validate property type! 🏠."""
        try:
            return PropertyType(property_type)
        except ValueError:
            error_msg = f"Property type must be one of: \
                {', '.join(s.value for s in PropertyType)}"
            raise ValueError(error_msg)

    @log_me(component="business")
    @classmethod
    def filter_by_price(
        cls, min_price: float, max_price: float
    ) -> List["Place"]:
        """Filter places by price range! 💰."""
        return cls.query.filter(
            cls.price_by_night >= min_price,
            cls.price_by_night <= max_price,
            cls.is_deleted == False,  # noqa: E712
            cls.status != PlaceStatus.BLOCKED.value,
        ).all()

    @log_me(component="business")
    @classmethod
    def filter_by_capacity(cls, min_guests: int) -> List["Place"]:
        """Filter places by guest capacity! 👻."""
        return cls.query.filter(
            cls.max_guest >= min_guests,
            cls.is_deleted == False,  # noqa: E712
            cls.status != PlaceStatus.BLOCKED.value,
        ).all()

    @log_me(component="business")
    @classmethod
    def get_by_location(
        cls, lat: float, lon: float, radius: float
    ) -> List["Place"]:
        """Find places within a radius! 🗺️."""
        from math import cos, radians  # Import lazy

        # Pour SQLite, on utilise une approche simplifiée avec un carré
        lat_range = radius / 111.0  # approximation: 1 degré = 111km

        return cls.query.filter(
            cls.latitude.between(lat - lat_range, lat + lat_range),
            cls.longitude.between(
                lon - (radius / (111.0 * cos(radians(lat)))),
                lon + (radius / (111.0 * cos(radians(lat)))),
            ),
            cls.is_deleted == False,  # noqa: E712
            cls.status != PlaceStatus.BLOCKED.value,
        ).all()

    @log_me(component="business")
    def add_amenity(self, amenity: "Amenity") -> None:
        """Add an amenity to this haunted place! ✨."""
        try:
            from app.models.placeamenity import PlaceAmenity  # noqa: F811

            link = PlaceAmenity(place_id=self.id, amenity_id=amenity.id)
            link.save()
        except Exception as e:
            raise ValueError(f"Failed to add amenity: {str(e)}")

    @log_me(component="business")
    def remove_amenity(self, amenity: "Amenity") -> None:
        """Remove an amenity from this haunted place! 🗑️."""
        try:
            from app.models.placeamenity import PlaceAmenity  # noqa: F811

            links = PlaceAmenity.get_by_attr(
                multiple=True, place_id=self.id, amenity_id=amenity.id
            )
            if not links:
                error_msg = f"No link found between place \
                            {self.id} and amenity {amenity.id}"
                raise ValueError(error_msg)

            for link in links:
                link.hard_delete()
        except Exception as e:
            raise ValueError(f"Failed to remove amenity: {str(e)}")

    @log_me(component="business")
    def get_amenities(self) -> List["Amenity"]:
        """Get all amenities of this haunted place! 🎭."""
        try:
            from app.models.amenity import Amenity  # noqa: F811
            from app.models.placeamenity import PlaceAmenity  # noqa: F811

            links = PlaceAmenity.get_by_attr(multiple=True, place_id=self.id)
            amenities = [Amenity.get_by_id(link.amenity_id) for link in links]
            return amenities
        except Exception as e:
            raise ValueError(f"Failed to get amenities: {str(e)}")

    @log_me(component="business")
    def update(self, data: dict) -> "Place":
        """Update place attributes! 🏰."""
        try:
            # Validate new values before update
            if "name" in data:
                data["name"] = self._validate_name(data["name"])
            if "description" in data:
                data["description"] = self._validate_description(
                    data["description"]
                )
            if "price_by_night" in data:
                data["price_by_night"] = self._validate_price(
                    data["price_by_night"]
                )
            if "status" in data:
                data["status"] = self._validate_status(data["status"])
            if "property_type" in data:
                data["property_type"] = self._validate_property_type(
                    data["property_type"]
                )

            return super().update(data)
        except Exception as e:
            raise ValueError(f"Failed to update Place: {str(e)}")

    @log_me(component="business")
    def delete(self) -> bool:
        """Soft delete this haunted place! 🌙."""
        try:
            return self.update({"status": PlaceStatus.BLOCKED})
        except Exception as error:
            raise ValueError(f"Failed to soft delete Place: {str(error)}")

    @log_me(component="business")
    def hard_delete(self) -> bool:
        """Permanently delete place and all related entities! ⚰️."""
        try:
            # Delete related reviews
            try:
                from app.models.review import Review  # noqa: F811

                reviews = Review.get_by_attr(multiple=True, place_id=self.id)
                for review in reviews:
                    review.hard_delete()
            except ImportError:
                pass  # Review model not implemented yet

            # Delete related place-amenity links
            try:
                from app.models.placeamenity import PlaceAmenity  # noqa: F811

                links = PlaceAmenity.get_by_attr(
                    multiple=True, place_id=self.id
                )
                for link in links:
                    link.hard_delete()
            except ImportError:
                pass  # PlaceAmenity model not implemented yet

            # Delete the place itself
            return super().hard_delete()
        except Exception as e:
            raise ValueError(f"Failed to delete Place: {str(e)}")

    @log_me(component="business")
    def to_dict(self) -> Dict[str, Any]:
        """Transform place into dictionary! 📚."""
        base_dict = super().to_dict()
        place_dict = {
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "price_by_night": self.price_by_night,
            "number_rooms": self.number_rooms,
            "number_bathrooms": self.number_bathrooms,
            "max_guest": self.max_guest,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city": self.city,
            "country": self.country,
            "status": self.status.value if self.status else None,
            "property_type": (
                self.property_type.value if self.property_type else None
            ),
            "minimum_stay": self.minimum_stay,
            "owner": self.owner.to_dict(),
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.to_dict() for amenity in self.amenities],
        }
        return {**base_dict, **place_dict}
