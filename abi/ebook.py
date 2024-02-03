from xml.etree import ElementTree
from typing import List, Union
from pathlib import Path
from dataclasses import dataclass

from ebooklib import epub

from abi import utils

@dataclass
class EbookMetadata:
    """
    A Data Class used to represent metadata of an EBook.
    
    Attributes:
        uuid (str)
            The unique identifier for the book.
        version (float)
            The version of the book.
        title (str)
            The title of the book.
        creator (str)
            The author or creator of the book. 
        subjects (List[str])
            List containing subjects related to this eBook.  
        title_sort(str, optional)
            Sorted title if available else None. Default is None.
        cover(str, optional)
            Link to cover image if available else None.Default is None.

    Methods:
        from_file(file_path: Union[Path, str]) -> "EbookMetadata"
            Class method that takes a file path and returns an instance 
            of EbookMetadata populated from metadata in given file.
    """
    uuid: str
    version: float
    title: str
    creator: str
    subjects: List[str]
    title_sort: str = None
    cover: str = None

    def __repr__(self):
        prefix = f"{self.__module__}.{type(self).__name__}"
        return f"<{prefix} title='{self.title}' author='{self.creator}' version={self.version}>"

    @classmethod
    def from_file(cls, file_path: Union[Path, str]) -> "EbookMetadata":
        tree = ElementTree.parse(str(file_path))
        root = tree.getroot()
        version = root.attrib['version']

        namespace = {'dc': 'http://purl.org/dc/elements/1.1/', 'opf': 'http://www.idpf.org/2007/opf'}

        uuid = root.find('.//dc:identifier[@id="uuid_id"]', namespaces=namespace).text
        title = root.find('.//dc:title', namespaces=namespace).text
        author = root.find('.//dc:creator[@opf:role="aut"]', namespaces=namespace).text
        subjects = [ elem.text for elem in root.findall('.//dc:subject', namespaces=namespace) ]

        title_sort_elem = root.find('.//*[@name="calibre:title_sort"]', namespaces=namespace)
        title_sort = title_sort_elem.attrib['content'] if title_sort_elem is not None else None 

        cover_elem = root.find('./guide/reference[@type="cover"]', namespaces=namespace)
        cover = cover_elem.get('href') if cover_elem is not None else None

        return cls(uuid=uuid, version=float(version), title=title, creator=author,
                   subjects=subjects, title_sort=title_sort, cover=cover)
@dataclass
class Ebook:
    directory: Path
    ebook: epub.EpubBook
    title: str
    metadata: EbookMetadata
    _contents: list = None

    def __repr__(self):
        prefix = f"{self.__module__}.{type(self).__name__}"
        epub = self.ebook.title
        metadata = self.metadata
        version = self.ebook.version
        return f"<{prefix} epub='{epub}' metadata={metadata} version={version}>"

    @property
    def contents(self):
        if self._contents is None:
            self._contents = utils.extract_ebook_contents(self.ebook)
        return self._contents

    @property
    def min(self):
        #return self
        prefix = f"{self.__module__}.{type(self).__name__}"
        epub = self.ebook.title
        version = self.ebook.version
        return f"<{prefix} epub='{epub}' version={version}>"

    @classmethod
    def from_dir(cls, directory: Union[str, Path]) -> "Ebook":
        directory = Path(directory)
        ebook = epub.read_epub( list(directory.glob('**/*.epub'))[0] )
        metadata = EbookMetadata.from_file( list(directory.glob('**/metadata.opf'))[0] )
        return cls(directory, ebook, ebook.title, metadata)
    
# Depricated
class EbookLibrary:

    def __init__(self, ebooks: list):
        self.library = ebooks

    def __getitem__(self, index: int):
        return self.library[index]

    @property
    def min(self):
        return [ item.min for item in self.library ]

    def get(self, name: str):
        """ Not Implemented. Return if match on ebook.title """
        print(f" -: EbookLibrary.get({name})")
        return None

    @classmethod
    def from_dir(cls, directory: Union[str, Path], index: Union[None, int]=None) -> "EbookLibrary":
        ebooks = [ Ebook.from_dir(ebook_dir) for ebook_dir in utils.find_epub_directories(directory, index) ]
        return cls(ebooks)