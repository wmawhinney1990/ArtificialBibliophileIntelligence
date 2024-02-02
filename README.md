# Artificial Bibliophile Intelligence
#### Showcasing how AI can think

ABI (Artificial Bibliophile Intelligence) is intended to read an `.epub` book and retain notes local to the `.epub` file.

Very much in development

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

### Run the AI
python main.py

### In Development

- `main.py` has tools to step through the reading of a book one chapter at a time.


#### Development Path
- [ ] Export `Notes.qa` data to an (x,y) csv file
- [ ] Test on more books
- [ ] Write different Notes classes and prompts for difference genres