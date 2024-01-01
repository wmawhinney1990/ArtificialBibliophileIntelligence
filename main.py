# Streaming Artificial Bibliophile Intelligence
# Build to showocase how an AI can think

import os
from pathlib import Path

from pprint import pprint as pp

import together
import dotenv
import sabi

dotenv.load_dotenv()
#together.api_key = os.getenv("together_key")

ebooks = Path(os.getenv("epub_dir"))
library = sabi.EbookLibrary.from_dir(ebooks)




w = library.get("The Law")  # Not Working
s = library[0]              # Working: sabi.ebook.Ebook
q = s.ebook                 # Working: ebooklib.epub.EpubBook
a = s.contents              # Working: list