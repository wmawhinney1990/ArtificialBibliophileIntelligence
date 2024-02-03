# Artificial Bibliophile Intelligence

import together
import colorama

import os
import glob
from pathlib import Path
from pprint import pprint as pp

from abi import AI, Chapter, utils, prompting, Book
from abi.ebook import Ebook

class Brain:

    def __init__(self, ai: AI, verbose: bool=False):
        self._ai = ai
        if verbose: colorama.init()
        self.verbose = verbose
        self.sumt = {}

    @property
    def ai(self):
        return self._ai

    def extract_start_end_indices(self, book_contents: list) -> tuple:
        """Returns a tuple of the first_chapter and the last_chapter"""
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

    def purge_notes(self, notes_path):
        notes_path = Path(notes_path)

        # check if dir exists before running logic
        # else, create the directory

        if not notes_path.exists():
            raise ValueError(f"The provided path '{str(notes_path)!r}' does not exist.")
        if not notes_path.is_dir():
            raise ValueError(f"The provided path '{str(notes_path)!r}' is not a directory.")

        file_types = ['*.pdf', '*.pkl']
    
        for file_type in ['*.pdf', '*.pkl']:
            files = glob.glob(str(notes_path / file_type))
            
            for f in files:
                try:
                    os.remove(f)
                    if self.verbose:
                        print(f"File {f} has been removed successfully")
                    
                except OSError as e:
                    print("Error:", e.strerror)

    def read_chapter(self, chapter: Chapter) -> None:

        prev_summary = None if chapter.chapter == 1 else chapter.prev_chapter.summary
        summary_so_far = [] if prev_summary is None else [prev_summary]

        prompt_temptlate = prompting.Template(chapter.notes.prompt_template)
        prompt_temptlate(title=chapter.title)

        used_tokens = len(utils.tokenize(str(prompt_temptlate)))
        max_context = (self.ai.context_window - used_tokens) / 2

        sections = chapter.sectionize(max_context, overlap=3)
        for i, section in enumerate(sections):

            if self.verbose:
                print(f" ::> Reading section {i+1} of {len(sections)} ...")

            summary = self.ai.summarize(*summary_so_far)
            
            prompt_temptlate(summary=summary, section=section)
            results = self.ai.run_prompt(prompt_temptlate.prompt)

            if self.verbose:
                print(colorama.Fore.LIGHTYELLOW_EX)
                print(f"\n{results!r}\n")
                print(colorama.Fore.RESET)
            
            chapter.notes.take_notes(results)
            summary_so_far.append(chapter.notes.summary)

        if "update_summary" in dir(chapter.notes):
            summary = ai.summarize(*summary_so_far)
            chapter.notes.update_summary(summary)

        chapter.save_notes()

        if self.verbose:
            print(colorama.Fore.LIGHTRED_EX)
            print(f"Chapter {chapter.chapter} done. Notes saved -> {chapter.notes.savepath!r}")
            print(colorama.Fore.RESET)

    def read_book(self, book: Book) -> None:

        for chapter in book:

            if chapter.chapter == 1:
                self.purge_notes(chapter.notes.savepath.parent)

            if self.verbose:
                print(colorama.Fore.MAGENTA)
                print(f" ::> READING CHAPTER {chapter.chapter}")
                

            self.read_chapter(chapter)

        print(colorama.Fore.RESET)

    @classmethod
    def from_together(cls, api_key: str, **kwargs) -> "Brain":
        return cls(AI.together_backend(api_key, **kwargs), **kwargs)

    @classmethod
    def from_openai(cls, api_key: str, **kwargs) -> "Brain":
        pass