from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path
import json
import re

from abi.prompting import basic_notes

@dataclass
class BaseNotes:
    savepath: Union[str, Path] = field(default_factory=Path)

    @property
    def is_full(self):
        excluded = {'is_full', 'savepath', 'take_notes'}
        members = [x for x in dir(self) if not (x.startswith('__') and x.endswith('__')) and x not in excluded]
        return all(members)

    @abstractmethod 
    def prompt_template(self) -> str:
        pass

    @abstractmethod 
    def take_notes(self, notes: str) -> None:
        pass

@dataclass
class BasicNotes(BaseNotes):
    summary: str = None
    points: list = field(default_factory=list)
    qa: dict = field(default_factory=dict)

    @property
    def prompt_template(self) -> str:
        return basic_notes

    def take_notes(self, notes: str) -> None:
        
        sections = [ section.strip() for section in notes.split('####') if section ]

        for section in sections:
            title, *content_lines = map(str.strip, section.split('\n'))

            if "Summary" in title:
                self.summary = ' '.join(content_lines)

            elif "Notes" in title:
                self.points.extend([ point.lstrip("- ") for point in content_lines ])

            elif "JSON" in title:
                json_str = ''.join(content_lines)
                match = re.search(r'\{.*?\}', json_str)

                if match:
                    self.qa.update(json.loads(match.group()))

__all__ = ['BasicNotes']