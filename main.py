# Artificial Bibliophile Intelligence
# Build to showocase how an AI can think

import os
from pathlib import Path

from pprint import pprint as pp

import dotenv
import abi

dotenv.load_dotenv()
#together.api_key = os.getenv("together_key")

VERBOSE = True

ebooks_directory = Path(os.getenv("epub_dir"))
library = abi.ebook.EbookLibrary.from_dir(ebooks_directory, 3)

brain = abi.Brain.from_together(os.getenv("together_key"), verbose=VERBOSE)

book = brain.book_from_ebook(library[0])

ch1 = book[0]
ch2 = book[1]

notes = brain.read_chapter(ch1)

q = notes