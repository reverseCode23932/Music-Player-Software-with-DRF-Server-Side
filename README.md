# Music-Player-Software-with-DRF-Backend

CLIENT NOT FINISHED

# Music Player Software with DRF Server Side

A backend music streaming API built using Django REST Framework (DRF), designed to serve audio content to a frontend client.

## Project Overview

This project provides a RESTful API for a music player application. The backend is developed using Django and Django REST Framework, offering endpoints to manage and stream music content. The frontend client is in progress and will interact with this API to deliver a seamless music listening experience.

## Technologies Used

* Backend: Django, Django REST Framework (DRF)
* Database: PostgreSQL
* Authentication: Token-based authentication (SIMPLE JWT)
* Environment Management: `python-dotenv` for environment variables
* Audio Storage: Local file system (MP3 files stored in the server)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/reverseCode23932/Music-Player-Software-with-DRF-Server-Side.git
cd Music-Player-Software-with-DRF-Server-Side
```

### 2. Install PostgreSQL

1. Download PostgreSQL from the official website: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. Run the installer and set a superuser password (usually `postgres`).
3. Add PostgreSQL to your system PATH if not done automatically.
4. Start the PostgreSQL service.

### 3. Create Database and User for Django

Log in to PostgreSQL:

```bash
psql -U postgres
```

Create a database and a user:

```sql
CREATE DATABASE music_player_db;
CREATE USER django_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE music_player_db TO django_user;
```

Exit `psql`:

```sql
\q
```

### 4. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

* Windows:

```bash
.\venv\Scripts\activate
```

* macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Set Up Environment Variables

Create a `.env` file in the project root and add the following:

```
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=music_player_db
DB_USER=django_user
DB_PASSWORD=strong_password
DB_HOST=localhost
DB_PORT=5432
```

### 7. Apply Migrations

```bash
python manage.py migrate
```

### 8. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/`.

## Security Considerations

* Never hardcode credentials in your code. Use environment variables.
* Use a dedicated PostgreSQL user with limited privileges for Django.
* Keep the PostgreSQL server not publicly accessible; allow access only from your app server.
* Rotate passwords regularly and use strong, unique passwords.
* Consider using SSL for database connections in production.

## API Endpoints

* **GET /api/songs/**: List all songs
* **POST /api/songs/**: Upload a new song
* **GET /api/songs/{id}/**: Retrieve a song by ID
* **PUT /api/songs/{id}/**: Update a song by ID
* **PATCH /api/songs/{id}/**: Partial update of a song by ID
* **DELETE /api/songs/{id}/**: Delete a song by ID
* **GET /api/playlists/**: List all playlists
* **POST /api/playlists/**: Create a new playlist
* **GET /api/playlists/{id}/**: Retrieve a playlist by ID
* **PUT /api/playlists/{id}/**: Update a playlist by ID
* **PATCH /api/playlists/{id}/**: Partial update of a playlist by ID
* **DELETE /api/playlists/{id}/**: Delete a playlist by ID
* **GET /api/users/**: List all users (admin only)
* **GET /api/users/{id}/**: Retrieve a user by ID (admin only)

## License

MIT License
