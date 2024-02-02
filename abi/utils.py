import os
import re
import nltk
import fnmatch
from typing import List, Union
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

str_to_bool = lambda s: {"true": True, "false": False}.get(s.lower())

def find_epub_directories(root_dir: str, index=None) -> list:
    epubs = []

    for dirpath, _, files in os.walk(root_dir):
        for filename in fnmatch.filter(files, '*.epub'):
            epubs.append(Path(dirpath))

    if index: return epubs[:index]
    return epubs

def sanitize_content(content: str) -> str:
    text = re.sub('\n+', '\n', content)
    clean_text = text.strip()
    return clean_text

def extract_ebook_contents(epub_book: epub.EpubBook) -> list:
    chapters = []
    for item in epub_book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            chapters.append(sanitize_content(soup.text))
    return chapters

def parse_output(text: str) -> str:
    text = sanitize_content(text)
    return text.split('\n')

def inline_print(text: str, end: str='') -> None:
    print(f'\r{text}', end=end, flush=True)

def get_slices(stuff: list, window: int=17, overlap: int=2):
    step = window - overlap
    return (stuff[i : i + window] for i in range(0, len(stuff) - overlap , step))

def get_pickle_files(directory: Union[str, Path]) -> List[Path]:
    """
    Utility function to return all .pkl files from the given directory.

    :param directory (Union[str, Path]): The path of the directory.

    :return (List[Path]): A list of paths for each .pkl file in the directory.
    """

    # Convert string path to Path object if necessary
    if isinstance(directory, str):
        directory = Path(directory)

    # Get all .pickle files in the specified directory 
    pickle_files = [file for file in directory.glob('*.pkl')]

    return pickle_files

def blank_formating(string: str) -> str:
    return re.sub(r'{.*?}', '', string)

def tokenize(text: str) -> int:
    return nltk.word_tokenize(text)