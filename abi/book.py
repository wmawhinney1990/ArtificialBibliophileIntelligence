from typing import Union, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path

import pickle

from abi.ebook import Ebook
from abi import utils
from abi.notes import BasicNotes as Notes

@dataclass
class Chapter:
    title: str
    chapter: int
    index: int
    contents: str
    _notes: Union[Path, Notes]

    _prev_chapter: Optional['Callable[[], Chapter]'] = None  # pointer to function that returns previous/next chapter (or None)
    _next_chapter: Optional['Callable[[], Chapter]'] = None  #   see Book.__getitem__; I barely unstand this code

    _num = 0
    
    def __repr__(self):
        return f'Chapter(title={self.title!r}, chapter={self.chapter!r}, index={self.index!r}, tokens={self.length!r})'

    @property
    def prev_chapter(self) -> "Chapter":
        """Returns previous Chapter."""
        if isinstance(self._prev_chapter, Callable):
            self._prev_chapter = self._prev_chapter()
        return self._prev_chapter
    @property
    def next_chapter(self) -> "Chapter":
        """Returns Nnext Chapter."""
        if isinstance(self._next_chapter, Callable):
            self._next_chapter = self._next_chapter()
        return self._next_chapter

    @property
    def tokens(self) -> List[str]:
        """Returns the tokens for the contents of the chapter."""
        return utils.tokenize(self.contents)

    @property
    def length(self) -> int:
        """Returns the number of tokens for the content of the chapter."""
        return len(self.tokens)
    
    @property
    def paragraphs(self) -> List[str]:
        """Returns a list of paragrphs for the chapter."""
        return self.contents.split('\n')

    @property
    def summary(self):
        return self.notes.summary

    @property
    def notes(self) -> Notes:
        self._num =+ 1
        if isinstance(self._notes, Path):
            if self._notes.is_file():
                self.load_notes(self._notes)
            else:
                self._notes = Notes(savepath=self._notes)

        return self._notes

    def sectionize_paragraphs(self, paragraphs: List[str], token_limit: int, overlap: int=1) -> List[str]:
        section = '\n'.join(paragraphs)
        if len(utils.tokenize(section)) <= token_limit:
            return [section]
        mid = len(paragraphs) // 2

        first_half = self.sectionize_paragraphs(paragraphs[:mid + overlap], token_limit)
        second_half = self.sectionize_paragraphs(paragraphs[mid - overlap:], token_limit)

        return first_half + second_half

    def sectionize(self,token_limit: int, overlap: int=2) -> List[str]:
        sections = self.sectionize_paragraphs(self.paragraphs, token_limit, overlap)
        return sections

    def save_notes(self) -> None:
        if not self.notes.is_full:
            print("  ::> Cannot save notes! Missing items!")
            return

        self.notes.savepath.parent.mkdir(parents=True, exist_ok=True)

        with open(str(self.notes.savepath), 'wb') as f:
            pickle.dump(self.notes, f)
                       
    def load_notes(self, notespath: Path) -> None :
        if not notespath.is_file():
            raise ValueError(f"File {str(notespath)} does not exist.")
            
        with open(str(notespath), 'rb') as f:
            self._notes = pickle.load(f)

#Books[0] -> Chapter 1

@dataclass
class Book:
    title: str
    ebook: Ebook
    directory: Path

    _first_chapter: int = field(default=None) 
    _last_chapter: int = field(default=None) 
    verbose: bool = False

    _chapters_cache : dict[int,'Chapter'] = field(default_factory=dict)

    def __getitem__(self, index: int) -> Union[Chapter,None]:
        """
        Method to get chapter based on its index.
        Chapters are cached through _chapter_cache dictionary.

        :param index (int): The number of the chapter.

        :return (Union[Chapter,None]): returns Chapter object or None if conditions are not met.
        """

        if self._first_chapter is None or self._last_chapter is None:
            print(f" --> Get fucked! Class members setting first and last chapters, one or both is None!")
            return

        chapter = index + 1
        cached_chapter = self._chapters_cache.get(index)
        if cached_chapter != None:
            if self.verbose: print(f"  ::> Returning cached Chapter at index {index}; Chapter {chapter}") 
            return cached_chapter

        chapter_count = self._last_chapter-self._first_chapter

        # Implement code for indes = -1

        if 0 <= index <= chapter_count:
            contents = self.contents[self._first_chapter:self._last_chapter]

            prev_chapter = None if index == 0 else lambda: self[index-1]
            next_chapter = None if index == chapter_count else lambda: self[index+1]
            if self.verbose: print(f"  ::> Book[{index}]: prev = {index-1}, next = {index+1}")

            notes = self.directory / Notes.__name__.lower() / f"chapter{chapter:03}.pkl"

            chapter = Chapter(self.title, chapter, index+self._first_chapter, contents[index], notes, prev_chapter, next_chapter)

            # Chapter caching happens through Book._chapters_cache and managed through this method, Book.__getitem__
            self._chapters_cache[index] = chapter
            if self.verbose: print(f"  ::> Book[{index}]: Caching Chapter {chapter.chapter}")

            return chapter
        else:
            print(f"Failure: {index}")

        return

    def __iter__(self):

        if self.valid_chapters:

            for i in range(self._last_chapter - self._first_chapter):
                yield self[i]

    @property    
    def notespath(self):
        notespath = self[0].notes.savepath.parent
        self._chapters_cache = {}
        return notespath

    @property
    def valid_chapters(self) -> bool:
        if not self.has_chapters:
            print(f" !:> Book chapters are None! Book.valid_chapters returns False")
            return False

        if 0 < self._first_chapter < self._last_chapter:
            return True

        return False
    

    @property
    def contents(self):
        """Returns the contents of the ebook."""

        return self.ebook.contents

    @property
    def has_chapters(self):
        """Returns True or False if chapters are identified."""
        if self._first_chapter is None or self._last_chapter is None:
            return False
        return True

    @property
    def pickle_filename(self):
        """Returns path for pickle file """

        filename = f"{self.title.lower().replace(' ', '_')}.pkl"
        return self.directory / filename



    def get_chapter(self, chapter: int):
        """Returns chapter based on chapter number."""
        return self[chapter-1]

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