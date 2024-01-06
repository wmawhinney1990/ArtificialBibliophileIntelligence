# Artificial Bibliophile Intelligence

import together
import colorama

from abi import AI, Chapter, utils, prompts, Book
from abi.ebook import Ebook

class Brain:

    def __init__(self, ai: AI, verbose: bool=False):
        self._ai = ai
        if verbose: colorama.init()
        self.verbose = verbose

    @property
    def ai(self):
        return self._ai

    def extract_start_end_indices(self, book_contents: list) -> tuple:
        if self.verbose: print(colorama.Fore.LIGHTGREEN_EX)
        first_chapter_index = self.ai.find_chapter(book_contents)
        last_chapter_index = len(book_contents) - self.ai.find_chapter(book_contents[::-1])
        if self.verbose: print(colorama.Fore.RESET)
        return first_chapter_index, last_chapter_index

    def book_from_ebook(self, ebook: Ebook):
        book = Book.from_ebook(ebook, verbose=self.verbose)
        if book.has_chapters:
            if self.verbose:
                print(" ::> Book chapters loaded from file!")
        else:
            chapter_indices = self.extract_start_end_indices(book.contents)
            book.update_chapters(*chapter_indices)
        return book

    def read_chapter(self, chapter: str, window: int=17, pace=15) -> None:
        paragraphs = chapter.split("\n")
        chapter = Chapter(chapter, paragraphs)
        for chunk in utils.get_slices(paragraphs, window, window-pace):
            print(chunk)

    def read_book(self, book: Book, callbacks) -> None:
        for chapter in book.chapters:
            result = read_chapter(chapter)

    @classmethod
    def from_together(cls, api_key: str, **kwargs) -> "Brain":
        return cls(AI.together_backend(api_key, **kwargs), **kwargs)

    @classmethod
    def from_openai(cls, api_key: str, **kwargs) -> "Brain":
        pass