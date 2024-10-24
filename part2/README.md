# 🏚️ Haunted-BnB 

## 🦇 Project Overview

Haunted-BnB is a spooky twist on the classic Airbnb concept - a RESTful API that lets users rent haunted properties! Built with Flask and following a clean architecture pattern, this project demonstrates advanced Python development practices with a slightly supernatural touch.

## 👻 Architecture

Our haunted mansion is built on four solid (but creaky) floors:

                🏰 API Layer (Flask)
                      ⬇️
                🎭 Facade Pattern
                      ⬇️
             🧠 Business Logic Layer
                      ⬇️
            💾 Persistence Layer (Memory)

## 🕯️ Technical Deep Dive

### API Layer
Our ghostly endpoints serve JSON responses for all your supernatural needs:

BOC
@api.route('/api/v1/users')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return facade.list_users()
EOC

### Facade Pattern
The Facade acts as our spiritual medium, connecting the API with the business logic:

BOC
class Facade:
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        
    def create_user(self, user_data):
        return self.user_repository.create(user_data)
EOC

### Business Logic
Core entities that haunt our application:

**Users** 👤
BOC
class User(BaseModel):
    def __init__(self, email, password, first_name=None, last_name=None):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
EOC

**Places** 🏚️
BOC
class Place(BaseModel):
    def __init__(self, name, description, price_per_night, owner_id):
        super().__init__()
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.owner_id = owner_id
EOC

## 🧪 Testing

Run our test suite to ensure no unwanted spirits are present:

BOC
# Run all tests
python -m pytest tests/

# Test specific endpoint
curl -X POST http://localhost:5000/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"email": "ghost@haunted.com", "password": "BOO!"}'
EOC

## 🎃 Installation & Setup

1. Clone the repository:
BOC
git clone https://github.com/Noziop/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
EOC

2. Create and activate virtual environment:
BOC
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
EOC

3. Install dependencies:
BOC
pip install -r requirements.txt
EOC

4. Run the application:
BOC
python run.py
EOC

## 🌙 Extra Features

### Frontend Portal
A spooky React frontend for browsing haunted locations (coming soon!)

### Error Handling
Custom error handlers for those ghostly mishaps:
BOC
@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return {'message': str(error)}, 400
EOC

### Input Validation
Ensuring all our ghostly data is properly formatted:
BOC
class PlaceValidator:
    @staticmethod
    def validate_price(price):
        if price <= 0:
            raise ValidationError("Price must be positive")
EOC

### Logging
Track those paranormal activities:
BOC
logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
EOC

## 🦉 Contributors
- Suzie (Lead Ghost Whisperer)

Happy Haunting! 🎃