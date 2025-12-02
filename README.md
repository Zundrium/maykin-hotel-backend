# Maykin Media Django Case

This project implements a hotel data importer and a simple frontend to view hotels by city.

## Prerequisites

- Python 3
- Django 5.1.4

## Quick Start

Run the automated setup script on linux:

```bash
./setup.sh
```

or on windows:

```bash
./setup.bat
```

This script will:
- Create a virtual environment
- Install dependencies
- Apply migrations
- Import hotel data (if .env is configured)

Then start the server:
```bash
source .venv/bin/activate
python manage.py runserver
```

## Manual Setup

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

### Automated Daily Imports (Cronjob)

To set up automated daily imports at 3 AM, add the following cronjob:

```bash
0 3 * * * cd /path/to/project && /path/to/venv/bin/python /path/to/project/manage.py import_hotel_data >> /var/log/import_hotel_data.log 2>&1
```

Example with actual paths:
```bash
0 3 * * * cd /home/user/maykin_csv_model_sync && /home/user/maykin_csv_model_sync/.venv/bin/python /home/user/maykin_csv_model_sync/manage.py import_hotel_data >> /var/log/import_hotel_data.log 2>&1
```

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
