# Artificial Bibliophile Intelligence
# Build to showocase how an AI can think

import os
from pathlib import Path
from pprint import pprint as pp
import datetime
import dotenv

import abi

dotenv.load_dotenv()

VERBOSE = True

ebooks_directory = Path(os.getenv("epub_dir"))
library = abi.ebook.EbookLibrary.from_dir(ebooks_directory, 3)

brain = abi.Brain.from_together(os.getenv("together_key"), verbose=VERBOSE)


def read_book(book):
    print(f"The AI reads {book.title}!")
    st = datetime.datetime.now()
    brain.read_book(book)           # How long does it take an AI to read a book?
    et = datetime.datetime.now()
    # And difference it
    elapsed_seconds = (et - st).total_seconds()
    minutes, seconds = divmod((et - st).total_seconds(), 60)
    print(f"::> Reading '{book.title}' only took this AI {minutes} minute(s) {seconds:.2f} second(s) !!")


if __name__ == "__main__":
    book = brain.book_from_ebook(library[0])
    notes_dir = book.notespath

    ####    FOR TESTING
    # ch1 = book[0]
    # brain.read_chapter(ch1)
    ####

    # Uncomment this line to use the AI to read the book
    #read_book(book)
    book_report = abi.ReportMaker.make_report_from_notes('report', notes_dir)

    print(f"\n\n{book_report} ...", end="\n\n")