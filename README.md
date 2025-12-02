# Maykin Media Django Case

This project implements a hotel data importer and a simple frontend to view hotels by city.

## Prerequisites

- Python 3
- Django 5.1.4

## Setup

1.  **Clone the repository** (if not already done).
2.  **Create and Activate Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt 
    ```
4.  **Configure Environment**:
    Create a `.env` file in the root directory, based on the `.env.example` file.
    
5.  **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

## Usage

### Import Data

To import the latest city and hotel data, run:

```bash
python manage.py import_hotel_data
```

This command fetches data from the configured URLs using the credentials provided in the environment.

### Run Server

Start the development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the city selection screen.

## Testing

Run the unit tests to verify the application:

```bash
python manage.py test hotels
```

## Project Structure

-   `hotels/`: Main application containing models, views, and management commands.
    -   `models.py`: `City` and `Hotel` models.
    -   `management/commands/import_hotel_data.py`: Custom command to import data.
    -   `views.py`: Views for city selection and hotel listing.
    -   `urls.py`: URL routing for the hotels app.
    -   `tests.py`: Unit tests.
    -   `templates/hotels/`: HTML templates.
