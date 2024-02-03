# Artificial Bibliophile Intelligence
#### Showcasing how AI can think

ABI (Artificial Bibliophile Intelligence) is intended to read an `.epub` book and retain notes local to the `.epub` file.

### Installation
1. Clone this repository
2. Navigate into the repository
3. Install the dependencies (preferred in an virtual environment)
4. Update the `.env` file

```bash
git clone https://github.com/wmawhinney1990/ArtificialBibliophileIntelligence ABI
cd ABI
pip install -r requirements.txt
cp .env-example .env
nano .env    # Update your api_key and epub library drirectory
```

### Getting Started

#### Overview
Books were downloaded from [Project Gutenburg](https://www.gutenberg.org/).
`.epub` books were downloaded and added to a [Calibre](https://calibre-ebook.com/download) Library
the directory of this Calibre is requred in the `.env` file

#### Running it
1. Make sure `.env` is updated
2. Run either `python main.py` or `python -i main.py`

#### Examples
See `/examples` for PDF examples of books reports
 

### Development Path
- [ ] Export `Notes.qa` data to an (x,y) csv file
- [ ] Test on more books
- [ ] Write different Notes classes and prompts for difference genres
- [ ] Bug fixes outlined in comments throughout the code
