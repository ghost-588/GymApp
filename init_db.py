#!/usr/bin/env python3
"""
Database initialization script.
Run this script to create the SQLite database and tables.
"""

from app.database import create_tables

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")
    print("SQLite database file: gymapp.db")
