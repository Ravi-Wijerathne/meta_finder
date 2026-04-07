# MetaFinder

Extract metadata from common file types and export results to a `.txt` file.

## Setup

### Windows (Portable)

1. Download [MetaFinder Portable](https://github.com/Ravi-Wijerathne/meta_finder/releases/latest/download/MetaFinder-Portable-v1.0.0.zip)
2. Extract and run `MetaFinder.exe`
3. No installation or Python required

### From Source

```bash
git clone https://github.com/Ravi-Wijerathne/meta_finder.git
cd meta_finder
python scripts/run_metafinder.py
```

`scripts/run_metafinder.py` is the recommended launcher.
It automatically creates (or repairs) the `venv` virtual environment and installs missing dependencies before launching MetaFinder.

## Usage

1. Click **Browse** to select a file
2. Click **Extract Metadata**
3. Click **Save to Text** to export results

## License

MIT License - see [LICENSE](LICENSE).
