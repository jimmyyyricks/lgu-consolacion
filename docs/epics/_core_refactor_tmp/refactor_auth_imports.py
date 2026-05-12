#!/usr/bin/env python3
"""
Automated Refactoring Script - Story 3: Auth Entity Migration
=============================================================
Updates import statements to use new core framework location.
"""

import ast
import os
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthImportRefactorer:
    """Refactors auth imports from old location to new core framework location."""
    
    def __init__(self, backend_root: Path):
        self.backend_root = backend_root
        self.files_changed = 0
        self.errors = []
    
    def find_files_to_update(self) -> List[Path]:
        """Find all Python files that import from app.models.auth."""
        files_to_update = []
        
        for py_file in self.backend_root.rglob("*.py"):
            # Skip the new core framework files and __pycache__
            if "core/framework" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "from app.core.framework.models.auth import" in content:
                        files_to_update.append(py_file)
            except Exception as e:
                self.errors.append(f"Error reading {py_file}: {e}")
        
        return files_to_update
    
    def refactor_imports(self, file_path: Path) -> bool:
        """Refactor imports in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Track if we made changes
            changed = False
            new_content = content
            
            # Replace old imports with new ones
            old_imports = [
                "from app.core.framework.models.auth import",
                "from app.core.framework.models import User, Role, EntityPermission",
                "from app.core.framework.models import User",
                "from app.core.framework.models import Role", 
                "from app.core.framework.models import EntityPermission"
            ]
            
            new_imports = [
                "from app.core.framework.models.auth import",
                "from app.core.framework.models import User, Role, EntityPermission",
                "from app.core.framework.models import User",
                "from app.core.framework.models import Role",
                "from app.core.framework.models import EntityPermission"
            ]
            
            for old, new in zip(old_imports, new_imports):
                if old in new_content:
                    new_content = new_content.replace(old, new)
                    changed = True
                    logger.info(f"Updated import in {file_path}: {old} -> {new}")
            
            # Write back if changed
            if changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.files_changed += 1
                return True
            
            return False
            
        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")
            return False
    
    def add_deprecation_warnings(self, file_path: Path) -> bool:
        """Add deprecation warnings to old models/auth.py file."""
        if file_path.name != "auth.py" or file_path.parent.name != "models":
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if deprecation warning already exists
            if "DeprecationWarning" in content:
                return False
            
            # Add deprecation warning at the top
            deprecation_warning = '''"""
DEPRECATED: This module has been moved to app.core.framework.models.auth
Please update your imports to use the new location.

This file will be removed in a future version.
"""
import warnings

warnings.warn(
    "app.models.auth is deprecated. Use app.core.framework.models.auth instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location for backward compatibility
from app.core.framework.models.auth import *

'''
            
            new_content = deprecation_warning + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            logger.info(f"Added deprecation warning to {file_path}")
            return True
            
        except Exception as e:
            self.errors.append(f"Error adding deprecation warning to {file_path}: {e}")
            return False
    
    def run_refactoring(self) -> Tuple[int, List[str]]:
        """Run the complete refactoring process."""
        logger.info("Starting auth import refactoring...")
        
        # Find files to update
        files_to_update = self.find_files_to_update()
        logger.info(f"Found {len(files_to_update)} files to update")
        
        # Update imports in each file
        for file_path in files_to_update:
            self.refactor_imports(file_path)
        
        # Add deprecation warning to old auth.py
        old_auth_path = self.backend_root / "app" / "models" / "auth.py"
        if old_auth_path.exists():
            self.add_deprecation_warnings(old_auth_path)
        
        # Update models/__init__.py
        models_init_path = self.backend_root / "app" / "models" / "__init__.py"
        if models_init_path.exists():
            self.update_models_init(models_init_path)
        
        return self.files_changed, self.errors
    
    def update_models_init(self, file_path: Path) -> bool:
        """Update models/__init__.py to use new imports."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace old imports with new ones
            old_line = "from app.core.framework.models.auth import User, Role, EntityPermission"
            new_line = "from app.core.framework.models.auth import User, Role, EntityPermission"
            
            if old_line in content:
                new_content = content.replace(old_line, new_line)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                logger.info(f"Updated models/__init__.py imports")
                self.files_changed += 1
                return True
            
            return False
            
        except Exception as e:
            self.errors.append(f"Error updating models/__init__.py: {e}")
            return False


def main():
    """Main refactoring function."""
    # Get backend root directory
    script_dir = Path(__file__).parent
    backend_root = script_dir.parent.parent
    
    # Run refactoring
    refactorer = AuthImportRefactorer(backend_root)
    files_changed, errors = refactorer.run_refactoring()
    
    # Report results
    logger.info(f"Refactoring complete!")
    logger.info(f"Files changed: {files_changed}")
    
    if errors:
        logger.error(f"Errors encountered: {len(errors)}")
        for error in errors:
            logger.error(f"  - {error}")
        return 1
    else:
        logger.info("No errors encountered!")
        return 0


if __name__ == "__main__":
    exit(main())
