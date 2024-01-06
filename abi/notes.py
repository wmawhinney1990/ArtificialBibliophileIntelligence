from dataclasses import dataclass
from typing import Union, List
from pathlib import Path

@dataclass
class Notes:
    notes: Union[List[str], str] = None