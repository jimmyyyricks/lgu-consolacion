"""
Seed Permissions from CSV
===========================
Seed entity permissions from the cleaned permissions.csv file into the database.
Permissions are connected to roles by role_name.
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
from sqlalchemy import select, update
from app.core.framework.models.auth import Role, EntityPermission
from app.core.database import init_db, async_session_maker


async def seed_permissions():
    """Seed permissions from CSV file."""
    
    # Initialize database tables
    print("Initializing database...")
    await init_db()
    print("Database initialized.")
    
    async with async_session_maker() as db:
        # Read the CSV file
        csv_path = Path(__file__).parent.parent / "cleaned_csvs" / "permissions.csv"
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"Found {len(rows)} permission mappings in CSV")
        
        seeded_count = 0
        updated_count = 0
        skipped_count = 0
        
        for row in rows:
            # Get role by name
            role_result = await db.execute(
                select(Role).where(Role.name == row['role_name'])
            )
            role = role_result.scalar_one_or_none()
            
            if not role:
                print(f"Skipping permission for unknown role: {row['role_name']}")
                skipped_count += 1
                continue
            
            # Check if permission already exists for this role and entity
            existing = await db.execute(
                select(EntityPermission).where(
                    EntityPermission.role_id == role.id,
                    EntityPermission.entity_name == row['entity_name']
                )
            )
            existing_permission = existing.scalar_one_or_none()
            
            # Create or update permission
            try:
                if existing_permission:
                    # Update existing permission
                    await db.execute(
                        update(EntityPermission).where(
                            EntityPermission.id == existing_permission.id
                        ).values(
                            can_read=row['can_read'].lower() == 'true' if row['can_read'] else False,
                            can_create=row['can_create'].lower() == 'true' if row['can_create'] else False,
                            can_update=row['can_update'].lower() == 'true' if row['can_update'] else False,
                            can_delete=row['can_delete'].lower() == 'true' if row['can_delete'] else False,
                            in_sidebar=row['in_sidebar'].lower() == 'true' if row['in_sidebar'] else False,
                        )
                    )
                    updated_count += 1
                else:
                    # Create new permission
                    permission = EntityPermission(
                        role_id=role.id,
                        entity_name=row['entity_name'],
                        can_read=row['can_read'].lower() == 'true' if row['can_read'] else False,
                        can_create=row['can_create'].lower() == 'true' if row['can_create'] else False,
                        can_update=row['can_update'].lower() == 'true' if row['can_update'] else False,
                        can_delete=row['can_delete'].lower() == 'true' if row['can_delete'] else False,
                        can_select=False,  # Default
                        can_export=False,  # Default
                        can_import=False,  # Default
                        in_sidebar=row['in_sidebar'].lower() == 'true' if row['in_sidebar'] else False,
                    )
                    
                    db.add(permission)
                    seeded_count += 1
                
                # Commit in batches to avoid memory issues
                if (seeded_count + updated_count) % 100 == 0:
                    await db.commit()
                    print(f"  Progress: {seeded_count} seeded, {updated_count} updated...")
                    
            except Exception as e:
                print(f"Error seeding permission for role {row['role_name']}, entity {row['entity_name']}: {e}")
                await db.rollback()
                skipped_count += 1
        
        # Final commit
        await db.commit()
        print(f"\nSeeding complete:")
        print(f"  - Seeded: {seeded_count} permissions")
        print(f"  - Updated: {updated_count} permissions")
        print(f"  - Skipped: {skipped_count} permissions")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_permissions())
