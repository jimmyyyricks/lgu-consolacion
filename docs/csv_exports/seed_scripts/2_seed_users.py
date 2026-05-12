"""
Seed Users from CSV
==================
Seed users from the cleaned tabUser.csv file into the database.
"""
import csv
import sys
import os
import bcrypt
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
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert
from app.core.framework.models.auth import User, Role, user_roles
from app.core.database import init_db, engine, async_session_maker


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def load_user_role_mappings():
    """Load user-role mappings from cleaned tabHas Role.csv."""
    csv_path = Path(__file__).parent.parent / "cleaned_csvs" / "tabHasRole_cleaned.csv"
    user_roles_mapping = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_email = row['user_email']
            role_name = row['role_name']
            
            if user_email not in user_roles_mapping:
                user_roles_mapping[user_email] = []
            user_roles_mapping[user_email].append(role_name)
    
    return user_roles_mapping


async def seed_users():
    """Seed users from CSV file."""
    
    # Initialize database tables
    print("Initializing database...")
    await init_db()
    print("Database initialized.")
    
    # Load user-role mappings
    print("Loading user-role mappings...")
    user_role_mappings = load_user_role_mappings()
    print(f"Loaded {len(user_role_mappings)} user-role mappings")
    
    async with async_session_maker() as db:
        # Read the CSV file
        csv_path = Path(__file__).parent.parent / "cleaned_csvs" / "tabUser_cleaned.csv"
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"Found {len(rows)} users in CSV")
        
        # Default password for all users
        default_password = "METpower123!"
        hashed_default = hash_password(default_password)
        
        seeded_count = 0
        skipped_count = 0
        
        for row in rows:
            # Check if user already exists by email
            existing_by_email = await db.execute(
                select(User).where(User.email == row['email'])
            )
            user = existing_by_email.scalar_one_or_none()
            
            if user:
                print(f"Updating existing user: {row['username']} ({row['email']})")
                # Assign roles to existing user
                user_roles_list = user_role_mappings.get(row['email'], [])
                if user_roles_list:
                    for role_name in user_roles_list:
                        # Get role from database
                        role_result = await db.execute(
                            select(Role).where(Role.name == role_name)
                        )
                        role = role_result.scalar_one_or_none()
                        
                        if role:
                            # Check if user already has this role
                            existing_user_role = await db.execute(
                                select(user_roles).where(
                                    user_roles.c.user_id == user.id,
                                    user_roles.c.role_id == role.id
                                )
                            )
                            if not existing_user_role.scalar_one_or_none():
                                # Assign role to user using association table
                                await db.execute(
                                    insert(user_roles).values(
                                        user_id=user.id,
                                        role_id=role.id
                                    )
                                )
                                print(f"  - Assigned role: {role_name}")
                            else:
                                print(f"  - Role already assigned: {role_name}")
                        else:
                            print(f"  - Role not found: {role_name}")
                    await db.flush()
                skipped_count += 1
                continue
            
            # Check if user exists by username
            existing_by_username = await db.execute(
                select(User).where(User.username == row['username'])
            )
            if existing_by_username.scalar_one_or_none():
                print(f"Skipping existing user by username: {row['username']}")
                skipped_count += 1
                continue
            
            # Create user
            try:
                user = User(
                    username=row['username'],
                    email=row['email'],
                    full_name=row['full_name'],
                    first_name=row['first_name'] or None,
                    last_name=row['last_name'] or None,
                    contact_number=row['contact_number'] or None,
                    department=row['department'] or None,
                    site=row['site'] or None,
                    employee_id=row['employee_id'] or None,
                    hashed_password=hashed_default,
                    is_active=row['is_active'] == '1' if row['is_active'] else True,
                    is_superuser=row['is_superuser'] == '1' if row['is_superuser'] else False,
                )
                
                db.add(user)
                await db.flush()
                print(f"Seeded user: {row['username']} ({row['email']})")
                seeded_count += 1
                
                # Assign roles to user
                user_roles_list = user_role_mappings.get(row['email'], [])
                if user_roles_list:
                    for role_name in user_roles_list:
                        # Get role from database
                        role_result = await db.execute(
                            select(Role).where(Role.name == role_name)
                        )
                        role = role_result.scalar_one_or_none()
                        
                        if role:
                            # Assign role to user using association table
                            await db.execute(
                                insert(user_roles).values(
                                    user_id=user.id,
                                    role_id=role.id
                                )
                            )
                            print(f"  - Assigned role: {role_name}")
                        else:
                            print(f"  - Role not found: {role_name}")
                    await db.flush()
                
            except Exception as e:
                print(f"Error seeding user {row['username']}: {e}")
                await db.rollback()
                skipped_count += 1
        
        await db.commit()
        print(f"\nSeeding complete:")
        print(f"  - Seeded: {seeded_count} users")
        print(f"  - Skipped: {skipped_count} existing users")
        print(f"  - Default password: {default_password}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_users())
