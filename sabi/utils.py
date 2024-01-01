import os
import re
import fnmatch
from pathlib import Path

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def find_epub_directories(root_dir: str) -> list:
    epubs = []

    for dirpath, _, files in os.walk(root_dir):
        for filename in fnmatch.filter(files, '*.epub'):
            epubs.append(Path(dirpath))

    return epubs

def extract_ebook_contents(epub_book: epub.EpubBook) -> list:
    chapters = []
    for item in epub_book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            chapters.append(soup.text)
    return chapters

def sanitize_content(content):
    text = re.sub('\n+', '\n', content)
    clean_text = text.strip()
    return clean_text

def parse_output(text):
    text = sanitize_content(text)
    return text.split('\n')