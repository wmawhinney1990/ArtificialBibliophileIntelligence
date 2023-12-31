import os
import fnmatch
from typing import Union
from pathlib import Path

from xml.etree import ElementTree
from sabi import utils

def get_metadata(opf_path):
    tree = ElementTree.parse(opf_path)
    root = tree.getroot()

    ns = {'dc': 'http://purl.org/dc/elements/1.1/',
          'opf': 'http://www.idpf.org/2007/opf'}

    metadata_dict = {}

    for element in root.find('metadata', ns):
        tag_name = element.tag.split('}')[-1]  # remove namespace part of tag
        if ':' in tag_name:  # handle opf:scheme and similar attributes
            _, attribute_name, scheme_value = element.attrib.values()
            value_key = f'{tag_name}_{attribute_name}'
            metadata_dict[value_key] = (element.text, scheme_value)
        else:
            metadata_dict[tag_name] = element.text

    return metadata_dict

class EbookLibrary:

    def __init__(self, ebooks):
        self.library = ebooks

    @classmethod
    def from_dir(cls, directory: Union[str, Path]):

        for ebook_dir in utils.find_epub_directories(directory):
        pass

class Ebook:

    def __init__(self, directory: Union[str, Path]):
        self._rootpath = directory

