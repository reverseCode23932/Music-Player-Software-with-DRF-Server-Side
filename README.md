# Music-Player-Software-with-DRF-Backend


currently no client folder (working on it).

# Music Player Software with DRF Server Side

A backend music streaming API built using Django REST Framework (DRF), designed to serve audio content to a frontend client.

## Project Overview

This project provides a RESTful API for a music player application. The backend is developed using Django and Django REST Framework, offering endpoints to manage and stream music content. The frontend client is in progress and will interact with this API to deliver a seamless music listening experience.

## Technologies Used

* Backend: Django, Django REST Framework (DRF)
* Database: PostgreSQL
* Authentication: Token-based authentication (DRF's default)
* Environment Management: `python-dotenv` for environment variables
* Audio Storage: Local file system (MP3 files stored in the server)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/reverseCode23932/Music-Player-Software-with-DRF-Server-Side.git
cd Music-Player-Software-with-DRF-Server-Side
```

### 2. Create a Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add the following:

```
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=music_player_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/`.

## API Endpoints

* **GET /api/songs/**: List all songs
* **POST /api/songs/**: Upload a new song
* **GET /api/songs/{id}/**: Retrieve a song
* **PUT /api/songs/{id}/**: Update a song
* **DELETE /api/songs/{id}/**: Delete a song

## License

MIT License
