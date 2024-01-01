# Streaming Artificial Bibliophile Intelligence
# Build to showocase how an AI can think

import os
from pathlib import Path

from pprint import pprint as pp

import dotenv
import sabi

dotenv.load_dotenv()
#together.api_key = os.getenv("together_key")

CONTENT_CAPTURE_WINDOW = 500

ebooks = Path(os.getenv("epub_dir"))
library = sabi.EbookLibrary.from_dir(ebooks)

ai = sabi.ABI.use_together_api(os.getenv("together_key"))


contents = library[0].contents

q = []

for i, content in enumerate(contents[2:]):

    print(f"Working on {i}/{len(contents)}")

    sanitized_content = sabi.utils.sanitize_content(content)

    if len(sanitized_content) > CONTENT_CAPTURE_WINDOW:
        sanitized_content = sanitized_content[:CONTENT_CAPTURE_WINDOW]

    q.append(ai.npl_is_chapter(sanitized_content))