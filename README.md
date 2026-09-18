# Simple URL Shortener

**CodeAlpha Backend Development Internship - Task 1**

A backend service built with Flask that shortens long URLs, stores the mapping in a SQLite database, and redirects short codes back to their original destination. Includes a small web frontend to use it without needing the API directly.

## Features

- POST /api/shorten - submit a long URL and get back a short code
- Optional custom short codes
- GET /<short_code> - redirects to the original URL and tracks clicks
- GET /api/stats/<short_code> - view metadata and click count for a link
- GET /api/urls - list all shortened URLs
- Basic web frontend to shorten and browse links
- URL validation - rejects malformed input
- Duplicate detection - re-shortening the same URL returns the existing code

## Tech Stack

- Python 3 and Flask
- SQLite via the built-in sqlite3 module
- Vanilla HTML, CSS, and JavaScript frontend

## Project Structure

url-shortener/
- app.py - Flask app with routes, database logic, and API endpoints
- requirements.txt - Python dependencies
- templates/index.html - frontend page
- static/style.css - styling
- README.md - this file

## Setup and Run

Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the app:

python app.py

The app will be running at http://127.0.0.1:5000. A file called shortener.db is created automatically the first time you run it.

## API Usage

Shorten a URL:

curl -X POST http://127.0.0.1:5000/api/shorten -H "Content-Type: application/json" -d "{\"url\": \"https://www.example.com/some/long/path\"}"

Response:

{
  "short_code": "aZ3kQ1",
  "short_url": "http://127.0.0.1:5000/aZ3kQ1",
  "original_url": "https://www.example.com/some/long/path"
}

Use a custom code:

curl -X POST http://127.0.0.1:5000/api/shorten -H "Content-Type: application/json" -d "{\"url\": \"https://example.com\", \"custom_code\": \"my-link\"}"

Check stats for a link:

curl http://127.0.0.1:5000/api/stats/aZ3kQ1

List all shortened links:

curl http://127.0.0.1:5000/api/urls

## How It Works

1. A user submits a long URL through the form or the API.
2. The backend validates the URL format.
3. A random 6-character short code is generated (or the user's custom code is used, after checking it isn't taken).
4. The mapping between the short code and the original URL is saved in SQLite.
5. When someone visits the short URL, the app looks up the code, increments its click count, and redirects to the original URL.

## Notes

This project was built to fulfill Task 1 of CodeAlpha's Backend Development track: a Flask server, an API endpoint to shorten URLs, database-backed storage, a redirect route, and an optional frontend.

## Author

Built by Arpita Pradhan as part of the CodeAlpha Backend Development Internship.
