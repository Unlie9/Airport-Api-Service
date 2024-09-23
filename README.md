# Airport Service API
Airport API service for management flights

# Features
* JWT authenticated
* Documentation is located at api/doc/swagger/
* Managing orders, flights, airplanes, routes, crew, airports as admin
* Searching flights as authenticated user and create orders 
* Filtering and validation of tickets data
* CRUD operations for airplane types, airplanes, airports, crew, routes, flights, and orders

# Installing using GitHub
Install PostgresSQL and create database
> git clone https://github.com/Unlie9/Airport-Api-Service.git
> 
> cd airport_service
> 
> python -m venv venv
> 
> source venv/bin/activate
> 
> pip install -r requirements.txt
> 
> Create and fill .evn file using .env.template
> 
> python manage.py migrate
> 
> python manage.py runserver

# Run with Docker
Docker should be installed
> docker-compose build
> 
> docker-compose up
> 
The API will be available at `http://localhost:8003`.

#### User Management
- `POST api/user/register/` - Register a new user
- `POST api/user/token/` - Obtain JWT token
- `POST api/user/token/refresh/` - Refresh JWT token
- `POST api/user/token/verify/` - Verify JWT token
- `GET api/user/me/` - Retrieve or update the authenticated user

#### AirLink API (prefix: `/api/`)
- `/airplane-types/` - List and create airplane types as admin
- `/airplanes/` - List and create airplanes as admin
- `/airports/` - List and create airports as admin
- `/crew/` - List and create crew members as admin
- `/routes/` - List and create routes as admin
- `/flights/` - List as user and create flights as admin
- `/orders/` - List and create orders as user

## Admin Interface

The Django admin interface is available at `api/admin/`. You can use it to manage the database entries directly.
