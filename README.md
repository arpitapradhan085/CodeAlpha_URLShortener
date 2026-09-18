# Simple URL Shortener

CodeAlpha Backend Development Internship - Task 1

A Flask backend that shortens long URLs, stores the mapping in SQLite, and redirects short codes to their original destination. Includes a simple web frontend.

## Features
- POST /api/shorten - shorten a URL, with optional custom code
- GET /<short_code> - redirects to the original URL and tracks clicks
- GET /api/stats/<short_code> - view click count and metadata
- GET /api/urls - list all shortened URLs
- URL validation and duplicate detection

## Setup
pip install -r requirements.txt
python3 app.py

Then open http://127.0.0.1:5000 in your browser.

## Tech Stack
Python, Flask, SQLite, HTML/CSS/JavaScript
