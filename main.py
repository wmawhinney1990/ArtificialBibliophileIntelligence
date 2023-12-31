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

image_path = Path(__file__).parent / "test04.png"
print(f" ::> image_path.is_file() -> {image_path.is_file()}")


reader = sabi.ImageReader(image_path, verbose=True)
print(f" ::> reader.invert_flag set -> {reader.invert_flag}")

#text = reader.read_image()
#a = sabi.extra.extra01(str(image_path))
#b = sabi.extra.extra02(str(image_path))

ebooks = Path(os.getenv("epub_dir"))

library = sabi.EbookLibrary.from_dir(ebooks)