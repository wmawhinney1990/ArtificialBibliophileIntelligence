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

#ch1 = book[0]
#brain.read_chapter(ch1)

start_time = datetime.datetime.now()

# Time this shit. How long does it take an AI to read a book?
brain.read_book(book)

end_time = datetime.datetime.now()

# And difference it
elapsed_seconds = (end_time - start_time).total_seconds()
es = elapsed_seconds

#t = abi.prompting.Template(abi.prompting.read_section)
