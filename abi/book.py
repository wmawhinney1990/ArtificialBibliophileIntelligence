from typing import Union, List
from dataclasses import dataclass
from pathlib import Path

import pickle
import nltk

from abi.ebook import Ebook
from abi import utils

@dataclass
class Chapter:
    title: str
    index: int
    contents: str
    
    def __repr__(self):
        return f'Chapter(title={self.title!r}, index={self.index!r}, tokens={len(self.tokens)!r})'


    @property
    def tokens(self) -> List[str]:
        return nltk.word_tokenize(self.contents)

    @property
    def len(self):
        return len(self.tokens)
    
    @property
    def paragraphs(self) -> List[str]:
        return self.contents.split('\n')

#Books[0] -> Chapter 1

@dataclass
class Book:
    title: str
    ebook: Ebook
    directory: Path

    _first_chapter: int = None
    _last_chapter: int = None
    verbose: bool = False

    def __getitem__(self, index:int) -> Union[Chapter,None]:
        """
        Method to get chapter based on its index.

        :param index (int): The number of the chapter.

        :return (Union[Chapter,None]): returns Chapter object or None if conditions are not met.
        """

        if self._first_chapter is None or self._last_chapter is None:
            return

        # Check whether first and last chapters' indices are in correct range.
        if 0 <= self._first_chapter < self._last_chapter and self._last_chapter < len(self.contents):
            contents = self.contents[self._first_chapter:self._last_chapter]
            return Chapter(self.title, index, contents[index])

        return 

    @property
    def contents(self):
        """Returns the contents of the ebook."""

        return self.ebook.contents

    @property
    def has_chapters(self):
        if self[0] is not None:
            return True
        return False
    

    @property
    def pickle_filename(self):
        """Returns path for pickle file """

        filename = f"{self.title.lower().replace(' ', '_')}.pickle"
        return self.directory / filename

    def save_book(self) -> None:
      """Save relivent data to a pickle file"""

      data ={
          'title': self.title,
          'directory': str(self.directory),
          'first_chapter': self._first_chapter,
          'last_chapter': self._last_chapter
      }

      with open(self.pickle_filename, 'wb') as f:
          pickle.dump(data, f)

    def update_chapters(self, first_chapter:int, last_chapter:int):
        """
        Method to update the first and last chapters of the book after its initialization.

        :param first_chapter (int): The number of the first chapter.
        :param last_Chapter (int): The number of the last chapter.
        """

        if isinstance(first_chapter, int) and isinstance(last_chapter, int):
            self._first_chapter = first_chapter  
            self._last_chapter = last_chapter
            self.save_book()

    @classmethod
    def from_pickle(cls, pickle_filename: Union[str, Path]) -> dict:
        """Returns a Book object created from a pickle file."""
         
        with open(pickle_filename,'rb') as f:
            book = pickle.load(f)

        return book

    @classmethod
    def from_ebook(cls, ebook: Ebook, first_chapter: int=None,
                   last_chapter: int=None, verbose: bool=False) -> "Book":
        pickles = utils.get_pickle_files(ebook.directory)

        if len(pickles) == 0:
            return cls(title=ebook.title, ebook=ebook, directory=ebook.directory)

        pickle = cls.from_pickle(pickles[0])

        if pickle["title"] == ebook.title:
            first_chapter = pickle.get("first_chapter", None)
            last_chapter = pickle.get("last_chapter", None)
            if verbose:
                print(f" ::> Book.from_ebook({ebook.directory.name}): pickle file found!")
                print(f" ::>  \u2514 first_chaper = {first_chapter}")
                print(f" ::>  \u2514 last_chapter = {last_chapter}")

        return cls(title=ebook.title, ebook=ebook, directory=ebook.directory,
                   _first_chapter=first_chapter, _last_chapter=last_chapter, verbose=verbose)

    @classmethod 
    def from_dir(cls, directory:Union[str,Path], verbose: bool=False)->"Book":  
        """Returns a Book object created from a directory that contains an ebook.""" 

        pickle_filename = utils.get_pickle_files(directory)

        if len(pickle_files) == 0:
            return cls.from_ebook(Ebook.from_dir(directory))

        return cls.from_pickle(pickle_filename=Path(pickle_files[0]))