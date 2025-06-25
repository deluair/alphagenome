"""
Data management module for AlphaGenome Analytics.
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class DataManager:
    """
    Data management class for storing and retrieving analysis results.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("./data")
        self.storage_path.mkdir(exist_ok=True)
        
    def save_data(self, data: Any, filename: str) -> None:
        """Save data to storage."""
        import pickle
        filepath = self.storage_path / filename
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
            
    def load_data(self, filename: str) -> Any:
        """Load data from storage."""
        import pickle
        filepath = self.storage_path / filename
        with open(filepath, 'rb') as f:
            return pickle.load(f)
            
    def list_files(self) -> List[str]:
        """List all files in storage."""
        return [f.name for f in self.storage_path.iterdir() if f.is_file()] 