# Planventure API

Planventure API is a Flask-based backend for managing users and trips, designed to work seamlessly with a React frontend. It provides secure authentication using JWT, user registration and login, and full CRUD operations for trip planning.

## Features
- User registration with email validation and password hashing (bcrypt)
- JWT-based authentication for login and protected routes
- Trip CRUD (Create, Read, Update, Delete) endpoints
- Default itinerary template generation for trips
- CORS configured for React frontend (localhost:3000)
- SQLite database support (default)

## Endpoints

### Auth
- `POST /auth/register` — Register a new user
  - Request: `{ "email": "user@example.com", "password": "yourpassword" }`
  - Response: `{ "message": "User registered successfully.", "token": "<JWT>" }`

- `POST /auth/login` — Login and receive JWT
  - Request: `{ "email": "user@example.com", "password": "yourpassword" }`
  - Response: `{ "message": "Login successful.", "token": "<JWT>" }`

### Trips (All require Authorization header: `Bearer <JWT>`)
- `POST /trips/` — Create a new trip
  - Request:
    ```json
    {
      "destination": "Tokyo",
      "start_date": "2025-08-01",
      "end_date": "2025-08-10",
      "latitude": 35.6895,
      "longitude": 139.6917,
      "itinerary": "Day 1: Shibuya, Day 2: Akihabara, Day 3: Mt. Fuji"
    }
    ```
  - If `itinerary` is omitted, a default template is generated.

- `GET /trips/` — List all trips for all users (customize to filter by user if needed)
- `GET /trips/<trip_id>` — Get a specific trip
- `PUT /trips/<trip_id>` — Update a trip
  - Request: Any of the trip fields (dates must be `YYYY-MM-DD`)
- `DELETE /trips/<trip_id>` — Delete a trip

### Protected Example
- `GET /protected` — Returns a message and user info if JWT is valid

## Models

### User
- `id`, `email`, `password_hash`, `created_at`, `updated_at`

### Trip
- `id`, `user_id`, `destination`, `start_date`, `end_date`, `latitude`, `longitude`, `itinerary`, `created_at`, `updated_at`

## Setup
1. Clone the repo and navigate to `planventure-api`
2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```
3. Set environment variables in a `.env` file (optional):
   - `SECRET_KEY=your-secret-key`
   - `DATABASE_URL=sqlite:///planventure.db`
4. Run the app:
   ```sh
   flask run
   ```

## CORS
CORS is enabled for `http://localhost:3000` and `http://127.0.0.1:3000` to support React development.

## Security
- Passwords are hashed with bcrypt
- JWT tokens are signed with your `SECRET_KEY`
- All trip routes require authentication

## License
See [LICENSE](LICENSE).

## Support
See [SUPPORT.md](SUPPORT.md).

---
For questions or contributions, open an issue or pull request!
