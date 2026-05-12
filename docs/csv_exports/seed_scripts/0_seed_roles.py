"""
Seed Roles from CSV
==================
Seed roles from the cleaned tabRole.csv file into the database.
"""
import csv
import sys
import os
from pathlib import Path

# Backend directory path
BACKEND_DIR = Path('/home/eamadmin/eam-2.0/eam-2.1-fastapi-vue/backend')

# Load .env from backend directory
env_file = BACKEND_DIR / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

# Add the backend directory to the path
sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.framework.models.auth import Role
from app.core.database import init_db, async_session_maker


async def seed_roles():
    """Seed roles from CSV file."""
    
    # Initialize database tables
    print("Initializing database...")
    await init_db()
    print("Database initialized.")
    
    async with async_session_maker() as db:
        # Read the CSV file
        csv_path = Path(__file__).parent.parent / "cleaned_csvs" / "tabRole_cleaned.csv"
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"Found {len(rows)} roles in CSV")
        
        seeded_count = 0
        skipped_count = 0
        
        for row in rows:
            # Check if role already exists by name
            existing = await db.execute(
                select(Role).where(Role.name == row['name'])
            )
            if existing.scalar_one_or_none():
                print(f"Skipping existing role: {row['name']}")
                skipped_count += 1
                continue
            
            # Create role
            try:
                role = Role(
                    name=row['name'],
                    description=row['description'] or None,
                    is_active=row['is_active'] == '1' if row['is_active'] else True,
                )
                
                db.add(role)
                await db.flush()
                print(f"Seeded role: {row['name']}")
                seeded_count += 1
            except Exception as e:
                print(f"Error seeding role {row['name']}: {e}")
                await db.rollback()
                skipped_count += 1
        
        await db.commit()
        print(f"\nSeeding complete:")
        print(f"  - Seeded: {seeded_count} roles")
        print(f"  - Skipped: {skipped_count} existing roles")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_roles())
