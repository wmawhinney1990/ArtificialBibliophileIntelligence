# Artificial Bibliophile Intelligence

import together
import colorama
from pprint import pprint as pp

from abi import AI, Chapter, utils, prompts, Book, Notes
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
        if self.verbose: print(colorama.Fore.LIGHTCYAN_EX)
        book = Book.from_ebook(ebook, verbose=self.verbose)
        if self.verbose: print(colorama.Fore.RESET)
        if book.has_chapters:
            if self.verbose:
                print(" ::> Book chapters loaded from file!")
        else:
            chapter_indices = self.extract_start_end_indices(book.contents)
            book.update_chapters(*chapter_indices)
        return book

    def read_chapter(self, chapter: Chapter, window: int=17, pace: int=15) -> Notes:
        blank_formating = utils.blank_formating(prompts.read_section) # I feel like prompts.read_section should not be here
        context_window = self.ai.context_window                       # Or query the ai.prompt_mistral directly
        used_tokens = len(utils.tokenize(blank_formating))
        window = context_window - used_tokens
        maths = window / chapter.len

        notes = Notes()
        if maths > 1:
            results = self.ai.read_section(chapter.title, notes.notes, chapter.contents)
            if self.verbose:
                print(colorama.Fore.RED)
                print(f"CHAPTER {chapter.index + 1}")
                print(colorama.Fore.LIGHTRED_EX)
                print(f"{results}\n")
                print(colorama.Fore.RESET)

            chapter.notes = results
            return results
        else:
            # This is a way here.
            # Imagine the context window as 100 and the tokens as 160
            # the result would be two windows because 100 / 160 = 0.625
            # Imagine knowing how many section to cut it into
            # Then grabbing chapter.paragraphs
            # section slowly absorbs one paragraph at a time, knowing what context not to go beyond
            # In this way, the chapter can be reasonably split up into sections and ran thru the prompt
            return

    def read_chapter_old(self, chapter: str, window: int=17, pace=15) -> None:
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