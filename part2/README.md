# 🏚️ Haunted-BnB

## 📚 Table des Matières
1. [Project Overview](#-project-overview)
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

## 👻 Architecture

Our haunted mansion follows a clean, layered architecture that separates concerns like ghostly spirits in different realms! Each layer has its own responsibility, making our code maintainable and scalable.

### 🏰 Layer Overview

                🏰 API Layer (Flask)
                      ⬇️
                🎭 Facade Pattern
                      ⬇️
             🧠 Business Logic Layer
                      ⬇️
            💾 Persistence Layer (Memory)

### 🌟 Detailed Architecture Breakdown

**API Layer (Presentation)**
- Handles all HTTP requests and responses
- Uses Flask-RESTX for automatic Swagger documentation
- Implements input validation and error handling

Example of an API endpoint:
```python
@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    @ns.doc(params= {'username': {'description': 'Filter by username', 'type': 'string'},
        'email': {'description': 'Filter by email', 'type': 'string'},
        'name': {'description': 'Filter by name', 'type': 'string'},
        'city': {'description': 'Filter by city', 'type': 'string'},
        'status': {'description': 'Filter by status', 'type': 'string'}})
    def get(self):
        """List all spirits in our realm! 👻"""
        filters = {k: v for k, v in request.args.items() if v}
        return facade.find_users(**filters)
```

**Facade Pattern (Integration)**
- Acts as a simplified interface between API and Business Logic
- Reduces complexity and coupling between layers
- Handles all cross-cutting concerns

Example of Facade implementation:
```python
    @magic_wand()
    def find_users(self, **criteria) -> List[User]:
        """Search for spirits in our realm! 🔮"""
        return User.get_by_attr(multiple=True, **criteria)
```

**Business Logic Layer (Domain)**
- Contains all business rules and validations
- Implements core entity behaviors
- Manages relationships between entities

Example of business logic:
```python
    @classmethod
    @magic_wand()
    def get_by_attr(cls: type[T], multiple: bool = False, **kwargs: Any) -> Union[Optional[T], List[T]]:
        """
        Search the spirit realm by attributes! 🔮
        
        Args:
            multiple: Summon one spirit or the whole haunted house? 
            **kwargs: The supernatural search criteria
        """
        return cls.repository.get_by_attribute(multiple=multiple, **kwargs)

    @classmethod
    @magic_wand()
    def get_all(cls: type[T]) -> List[T]:
        """Summon ALL the spirits! A supernatural roll call! 👻"""
        return cls.repository.get_all()
```

**Persistence Layer (Data)**
- Currently uses in-memory storage (will be replaced with SQL in Part 3)
- Handles all data operations (CRUD)
- Implements repository pattern for data access

Example of repository pattern:
```python
def get_by_attribute(
        self,
        multiple: bool = False,
        **kwargs: Any
    ) -> Union[Any, List[Any]]:
        """
        Get objects by attributes. Summoning entities from the storage beyond! 👻
        
        Args:
            multiple: Want one ghost or a whole haunted house? 🏚️
            **kwargs: The dark specifications (each more cursed than the last!)

        WHY: 
            Because searching through storage is like necromancy:
            You gotta be specific with your summons! 🧙‍♀️

        THE SPIRITS ARE WATCHING! 🦇
        """
        results = [
            obj for obj in self._storage.values() 
            if all(getattr(obj, attr, None) == value 
                for attr, value in kwargs.items())
        ]
        
        if not results:
            return [] if multiple else None
            
        return results if multiple else results[0]
```

### 🎭 Key Architecture Benefits

**Separation of Concerns**
- Each layer has a single responsibility
- Easy to modify one layer without affecting others
- Simplified testing and maintenance

**Scalability**
- Easy to add new features or modify existing ones
- Simple to replace components (like switching from in-memory to SQL)
- Supports future additions like authentication

**Maintainability**
- Clear structure makes code easy to understand
- Reduced coupling between components
- Simplified debugging and error handling

### 🦇 Design Patterns Used

1. **Facade Pattern**
   - Simplifies complex subsystem interactions
   - Provides a unified interface
   - Reduces coupling between layers

2. **Repository Pattern**
   - Abstracts data persistence details
   - Makes switching storage implementations easier
   - Centralizes data access logic

3. **Model-View Pattern**
   - Separates data representation from business logic
   - Enables independent evolution of UI and backend
   - Facilitates testing and maintenance

## 🕯️ Technical Deep Dive

### API Layer
Our ghostly endpoints serve JSON responses for all your supernatural needs:

```python
    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.response(201, 'Spirit summoned successfully')
    @ns.response(400, 'Failed to summon spirit')
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Summon a new spirit into existence! 👻"""
        try:
            return facade.create_user(ns.payload), 201
        except ValueError as e:
            ns.abort(400, f"Failed to summon spirit: {str(e)}")
```

### Facade Pattern
The Facade acts as our spiritual medium, connecting the API with the business logic:

```python
    def __init__(self):
        """Summon our mystical repositories! 🔮"""
        self.user_repository = User.repository
        self.place_repository = Place.repository
        self.amenity_repository = Amenity.repository
        self.review_repository = Review.repository
        self.placeamenity_repository = PlaceAmenity.repository

    # === USER OPERATIONS === 👻
    @magic_wand(validate_input(UserValidation))
    def create_user(self, user_data: dict) -> User:
        """Summon a new spirit into our realm! 👻"""
        return User.create(**user_data)
```

### Business Logic
Core entities that haunt our application:

**Users** 👤
```python
    @classmethod
    @magic_wand(validate_input(UserValidation))
    def create(cls, **kwargs) -> 'User':
        """
        Summon a new user into existence! 🧙‍♀️
        Like creating a new ghost, but with better documentation!
        """
        username = kwargs.get('username')
        email = kwargs.get('email')
        
        # Check if the spirit name is taken
        if cls.get_by_attr(username=username):
            raise ValueError(
                f"The name '{username}' is already haunting our database! 👻"
            )
        
        # Check if the spectral email exists
        if cls.get_by_attr(email=email):
            raise ValueError(
                f"This email '{email}' already belongs to another spirit! 📧"
            )
        
        return super().create(**kwargs)
```

**Places** 🏚️
```python
    @classmethod
    @magic_wand(validate_input(PlaceValidation),
                validate_entity(('User', 'owner_id')))
    def create(cls, **kwargs) -> 'Place':
        """
        Summon a new haunted place into existence! 🏚️
        
        Args:
            **kwargs: The dark ingredients for our haunted creation! 🧪
        
        Returns:
            A newly possessed Place, ready for haunting! 👻
        
        Raises:
            ValueError: When the spirits reject our offering! 💀
        """
        place = cls(**kwargs)
        cls.repository.add(place)
        return place
```

## 🧪 Testing

Run our test suite to ensure no unwanted spirits are present:

```
# Run all tests
```bash
cd /PATH/TO/REPOSITORY/holbertonschool-hbnb/part2
~/Git/holbertonschool-hbnb/part2 (main*)(main) [modified:2 ]
» coverage run --rcfile=../.coveragerc -m unittest discover -s app/tests -p "test_*.py"                                                                                                                                   1 ↵ fassihbe@FGDBe
Loggers initialized
........................................
----------------------------------------------------------------------
Ran 40 tests in 5.086s

OK
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
~/Git/holbertonschool-hbnb/part2 (main*)(main) [modified:2 ]
» coverage report --rcfile=../.coveragerc                                                                                                                                                                                     fassihbe@FGDBe
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
app/__init__.py                                 17      9    47%
app/api/__init__.py                             12      0   100%
app/api/v1/__init__.py                           0      0   100%
app/api/v1/amenities.py                         61     28    54%
app/api/v1/places.py                            98     52    47%
app/api/v1/reviews.py                           60     27    55%
app/api/v1/users.py                             62     25    60%
app/models/__init__.py                           0      0   100%
app/models/amenity.py                           67      9    87%
app/models/basemodel.py                         68      4    94%
app/models/place.py                            158     17    89%
app/models/placeamenity.py                      57      7    88%
app/models/review.py                            85     19    78%
app/models/user.py                              98     23    77%
app/persistence/__init__.py                      0      0   100%
app/persistence/repository.py                   40      2    95%
app/services/__init__.py                         0      0   100%
app/services/facade.py                         135     10    93%
app/tests/test_facade/__init__.py                0      0   100%
app/tests/test_facade/test_facade.py            99      0   100%
app/tests/test_models/__init__.py                0      0   100%
app/tests/test_models/test_amenity.py           57      0   100%
app/tests/test_models/test_attr.py              39      0   100%
app/tests/test_models/test_basemodel.py         62      4    94%
app/tests/test_models/test_place.py             60      0   100%
app/tests/test_models/test_placeamenity.py      45      0   100%
app/tests/test_models/test_review.py            41      0   100%
app/tests/test_models/test_user.py              35      0   100%
app/utils/__init__.py                            2      0   100%
app/utils/magic_wands.py                       128     14    89%
app/utils/model_validations.py                  11      0   100%
----------------------------------------------------------------
TOTAL                                         1597    250    84%
```
# Test specific endpoint
```
curl -X POST http://localhost:5000/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"email": "ghost@haunted.com", "password": "BOO!"}'
```

## 🎃 Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Noziop/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python3 run.py # Assuming you've summoned python 3.* on your system
```

## 🌙 Extra Features

### Frontend Portal
- A spooky vite.js frontend for browsing haunted locations (coming soon!)
- A very simple vanilla HTML/CSS/JS web page to test all the api endpoints

### Decorators :

I was really annoyed to see damned soul, forced to repeat again and again the very same operations in my code. To escape this developper's malediction, especially on the very eve of halloween, i decided to treat myself with some magic little tricks : Decorators.

The whole idea is to summons these little demons each time a function is call, defined by their priority : 
 - validation of inputs
 - validation of an entity (does that "place_id" exists or is it haunting us ?)
 - error handeling
 - logging

#### 1 - Error Handling
Custom error handlers for those ghostly mishaps, wrapped into a highly reusable decorateur, because magic happens in DRY Codes ! :

```python
def magic_wand(*wrappers):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            module = func.__module__.split('.')[-2]  # name of the module (models, facade, api)
            logger = get_logger(module)
            log_data = _prepare_log_data(func, args, kwargs)
            try:
                for wrap in sorted(wrappers, key=lambda w: getattr(w, 'priority', 0), reverse=True):
                    if callable(wrap):
                        result = wrap(*args, **kwargs)
                        if isinstance(result, dict):
                            kwargs.update(result)
                        elif result is False:
                            logger.debug(json.dumps({**log_data, 'status': 'validation_failed', 'wrapper': wrap.__name__}))
                            return
                result = func(*args, **kwargs)
                logger.info(json.dumps({**log_data, 'status': 'success', 'result': str(result)}))
                return result
            except ValueError as e:
                logger.debug(json.dumps({**log_data, 'status': 'value_error', 'error': str(e)}))
                raise
            except Exception as e:
                logger.error(json.dumps({**log_data, 'status': 'error', 'error': str(e)}))
                raise
        return wrapper
    return decorator
```

#### 2 - Input Validation
Ensuring all our ghostly data is properly formatted, and is what we was expecting while summoning them :
```python
def validate_input(*args, **kwargs):
    validators = {}
    for arg in args:
        if isinstance(arg, dict):
            validators.update(arg)
    validators.update(kwargs)

    def wrapper(*func_args, **func_kwargs):
        validated = {}
        for param, expected_type in validators.items():
            if param in func_kwargs:
                try:
                    value = func_kwargs[param]
                    if isinstance(expected_type, tuple):
                        if not isinstance(value, expected_type):
                            raise ValueError(f"{param} must be one of types {expected_type}")
                    elif not isinstance(value, expected_type):
                        raise ValueError(f"{param} must be of type {expected_type.__name__}")
                    validated[param] = value
                except ValueError as e:
                    raise ValueError(f"Invalid {param}: {str(e)}")
        return validated
    wrapper.priority = 2
    return wrapper
```

### Logging
Is there a better time than Halloween to track those paranormal activities:
```python
# Initialisation des loggers
loggers = setup_logging()
print("Loggers initialized")

def get_logger(module):
    return loggers.get(module, logging.getLogger('hbnb_default'))

def _prepare_log_data(func, args, kwargs):
    return {
        'function': func.__name__,
        'class': args[0].__class__.__name__ if args else '',
        'args': str(args[1:]),
        'kwargs': {k: v for k, v in kwargs.items() if k != 'password'}
    }
```

## 🦉 Contributors
- Fassih Belmokhtar - (Lead Ghost Whisperer)

Happy Haunting! 🎃