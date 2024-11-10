# 🏚️ Haunted-BnB

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

[Code Quality](./badges/flake8-badge.svg)
![Test Coverage](./badges/coverage-badge.svg)

*Where every stay is a spooktacular experience!* 🏚️

## 📚 Table des Matières
1. [Project Overview](#-project-overview)
2. [Quick Start](#-quick-start)
3. [H24 Reboot Story](#-h24-reboot-story)
   - [Why This Reboot ?](#why-the-reboot-)
   - [Key DRY Achievements](#key-dry-achievements-)
   - [TDD Approch](#tdd-approach-)
2. [Architecture](#-architecture)
   - [Layer Overview](#-layer-overview)
   - [Detailed Architecture Breakdown](#-detailed-architecture-breakdown)
   - [Key Architecture Benefits](#-key-architecture-benefits)
   - [Design Patterns Used](#-design-patterns-used)
3. [Technical Deep Dive](#-technical-deep-dive)
   - [API Layer](#api-layer)
   - [Facade Pattern](#facade-pattern)
   - [Business Logic](#business-logic)
4. [Testing](#-testing)
5. [Installation & Setup](#-installation--setup)
6. [Extra Features](#-extra-features)
   - [Frontend Portal](#frontend-portal)
   - [Decorators](#decorators)
7. [Contributors](#-contributors)

## 🦇 Project Overview

Haunted-BnB is a spooky twist on the classic Airbnb concept - a RESTful API that lets users rent haunted properties! Built with Flask and following a clean architecture pattern, this project demonstrates advanced Python development practices with a slightly supernatural touch.

## 🔄 H24 Reboot Story

This project underwent a complete reboot during H24 to create a cleaner, more maintainable codebase with a focus on simplicity and reliability.

### Why the Reboot? 🤔

While the original implementation was fully functional, I wasn't satisfied with:
- Too many decorators making the code harder to follow
- Repetitive error handling patterns
- Complex validation approaches

I wanted something:
- Simpler yet powerful
- DRYer than a desert
- Easier to maintain and test

### Key DRY Achievements ✨

1. **Type Hints Everywhere**
```python
    @classmethod
    def filter_by_capacity(cls, min_guests: int) -> List['Place']:
        """Filter places by guest capacity! 👻"""
        cls.logger.debug(f"Filtering places by minimum capacity: {min_guests}")

        # Récupérer toutes les places
        places = cls.get_all_by_type()

        # Filtrer par capacité
        filtered = [
            place for place in places
            if place.max_guest >= min_guests
        ]

        cls.logger.info(f"Found {len(filtered)} places with capacity >= {min_guests}")
        return filtered
```

2. **Universal CRUD in Facade**
```python
def create(self, model_class: Type[T], data: dict) -> T:
    """Create any entity type with a single method!"""
    return model_class.create(**data)

def find(self, model_class: Type[T], **criteria) -> List[T]:
    """Find any entity type with a single method!"""
    return model_class.get_by_attr(multiple=True, **criteria)
```

3. **Single Error Handler**
```python
@log_me  # Our one and only decorator!
def post(self):
    try:
        return facade.create(Place, ns.payload), 201
    except ValueError as e:
        ns.abort(400, str(e))
```

### TDD Approach 🧪

While not strictly TDD (I admit it! 😅), we maintained a strong focus on testing:
- Tests written alongside code
- High coverage (94%)
- Test-first mindset for new features

## 🎭 Architecture Overview

### Super DRY Facade Pattern
One class to rule them all! Our facade handles all CRUD operations for any entity type:
- create(model_class, data)
- find(model_class, **criteria)
- get(model_class, id)
- update(model_class, id, data)
- delete(model_class, id, hard=False)

### Type Safety First!
Type hints everywhere for better:
- Code completion
- Error catching
- Documentation
- Maintainability

### API Layer
```python
# API user endpoint to list users, parameters query friendly
@log_me
    @ns.doc('list_users',
            responses={
                200: 'Success',
                400: 'Invalid parameters',
                404: 'No users found'
            })
    @ns.marshal_list_with(output_user_model)
    @ns.param('username', 'Ghost name', type=str, required=False)
    @ns.param('email', 'Spirit contact', type=str, required=False)
    @ns.param('first_name', 'First haunting name', type=str, required=False)
    @ns.param('last_name', 'Last haunting name', type=str, required=False)
    def get(self):
        """Lilith's List of Lost Souls"""
        try:
            criteria = {}
            for field in ['username', 'email', 'first_name', 'last_name']:
                if field in request.args and request.args[field]:
                    criteria[field] = request.args[field]
            return facade.find(User, **criteria)
        except Exception as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")
```

### Business Logic
```python
# Basemodel Method to search object(s)
# Returns all attributes if no criterias given
# Returns matching attributes to the given attiributs :

@classmethod
    def get_by_attr(cls: type[T], multiple: bool = False, **kwargs: Any) -> Union[Optional[T], List[T]]:
        """Search instances by attributes! 🔮"""
        cls.logger.debug(f"Searching {cls.__name__} with attributes: {kwargs}")
        result = cls.repository.get_by_attribute(multiple=multiple, **kwargs)
        if result:
            cls.logger.info(f"Found {len(result) if multiple else 1} {cls.__name__}(s)")
        else:
            cls.logger.info(f"No {cls.__name__} found matching criteria")
        return result

# Facade Methode using **Type Hint** to create a user/ a place / a review / an amenity
def create(self, model_class: Type[T], data: dict) -> T:
        """Create a new haunted entity! ✨"""
        try:
            self.logger.debug(f"Creating {model_class.__name__} with data: {data}")
            instance = model_class(**data)
            instance.save()
            self.logger.info(f"Created {model_class.__name__} with ID: {instance.id}")
            return instance
        except Exception as e:
            self.logger.error(f"Failed to create {model_class.__name__}: {str(e)}")
            raise
```

### Repository Pattern
```python
def get_by_attribute(self, multiple: bool = False, **kwargs: Any):
    """Find entities by their attributes"""
    results = [
        obj for obj in self._storage.values()
        if all(getattr(obj, attr) == value
            for attr, value in kwargs.items())
    ]
    return results if multiple else results[0] if results else None
```

## 🌟 Features

### Core Components
- **Models**: Clean, validated entities
- **Repository**: Simple data storage
- **Facade**: Streamlined operations
- **API**: RESTful endpoints with swagger

### Logging System
- Request tracking
- Response monitoring
- Error logging
- Debug information

## 🧪 Testing

### Coverage Report
Current coverage: 84% across all modules
- Models: 90%+ coverage
- API Layer: 75%+ coverage
- Repository: 95% coverage

### Running Tests

# Run tests with coverage
```bash
» coverage run --rcfile=../.coveragerc -m pytest app/tests/test_spooky                                                                                                                                                        fassihbe@FGDBe
============================================================================================================ test session starts ============================================================================================================
platform linux -- Python 3.10.12, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/fassihbe/Git/holbertonschool-hbnb/part2
plugins: Faker-30.3.0, cov-5.0.0
collected 160 items

app/tests/test_spooky/test_api/test_amenities_api.py ....................                                                                                                                                                             [12%]
app/tests/test_spooky/test_api/test_places_api.py .........................                                                                                                                                                           [28%]
app/tests/test_spooky/test_api/test_reviews_api.py ........                                                                                                                                                                           [33%]
app/tests/test_spooky/test_api/test_users_api.py ............                                                                                                                                                                         [40%]
app/tests/test_spooky/test_models/test_amenity.py .....                                                                                                                                                                               [43%]
app/tests/test_spooky/test_models/test_basemodel.py .......................                                                                                                                                                           [58%]
app/tests/test_spooky/test_models/test_place.py ..............                                                                                                                                                                        [66%]
app/tests/test_spooky/test_models/test_placeamenity.py .........                                                                                                                                                                      [72%]
app/tests/test_spooky/test_models/test_review.py ........                                                                                                                                                                             [77%]
app/tests/test_spooky/test_models/test_user.py ......................                                                                                                                                                                 [91%]
app/tests/test_spooky/test_services/test_facade.py .........                                                                                                                                                                          [96%]
app/tests/test_spooky/test_utils/test_logging.py .....                                                                                                                                                                                [100%]

===================================================================================================== 160 passed in 54.28s ======================================================================================================
```
# Get coverage report
```bash
» coverage report --rcfile=../.coveragerc                                                                                                                                                                                     fassihbe@FGDBe
Name                                                     Stmts   Miss  Cover
----------------------------------------------------------------------------
app/__init__.py                                             13      0   100%
app/api/__init__.py                                         14      0   100%
app/api/utils.py                                            19      0   100%
app/api/v1/__init__.py                                       0      0   100%
app/api/v1/amenities.py                                     77      6    92%
app/api/v1/places.py                                       135     13    90%
app/api/v1/reviews.py                                       80     18    78%
app/api/v1/users.py                                         65      4    94%
app/models/__init__.py                                       0      0   100%
app/models/amenity.py                                       93     18    81%
app/models/basemodel.py                                    101      0   100%
app/models/place.py                                        235     27    89%
app/models/placeamenity.py                                  44      8    82%
app/models/review.py                                        92      9    90%
app/models/user.py                                         120     19    84%
app/persistence/repository.py                               48      4    92%
app/services/__init__.py                                     0      0   100%
app/services/facade.py                                      74      3    96%
app/tests/__init__.py                                        0      0   100%
app/tests/conftest.py                                       25      1    96%
app/tests/test_spooky/__init__.py                            0      0   100%
app/tests/test_spooky/test_api/__init__.py                   0      0   100%
app/tests/test_spooky/test_api/test_amenities_api.py       122      7    94%
app/tests/test_spooky/test_api/test_places_api.py          161      0   100%
app/tests/test_spooky/test_api/test_reviews_api.py          64      0   100%
app/tests/test_spooky/test_api/test_users_api.py            75      0   100%
app/tests/test_spooky/test_models/__init__.py                0      0   100%
app/tests/test_spooky/test_models/test_amenity.py           57      0   100%
app/tests/test_spooky/test_models/test_basemodel.py        270      2    99%
app/tests/test_spooky/test_models/test_place.py            200     23    88%
app/tests/test_spooky/test_models/test_placeamenity.py     156     25    84%
app/tests/test_spooky/test_models/test_review.py           111      0   100%
app/tests/test_spooky/test_models/test_user.py             221      0   100%
app/tests/test_spooky/test_services/__init__.py              0      0   100%
app/tests/test_spooky/test_services/test_facade.py          94      0   100%
app/tests/test_spooky/test_utils/__init__.py                 0      0   100%
app/tests/test_spooky/test_utils/test_logging.py            83      0   100%
app/utils/__init__.py                                        3      0   100%
app/utils/haunted_logger.py                                 27      0   100%
----------------------------------------------------------------------------
TOTAL                                                     2879    187    94%
```

## 🎃 Installation

1. Clone and checkout
```bash
git clone https://github.com/Noziop/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
git checkout crazy_H-24_startover
```

2. Setup environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run server
```bash
python3 run.py
```

## 👻 Contributors
- Fassih Belmokhtar (Ghost Whisperer Extraordinaire)

Happy Haunting! 🎃
