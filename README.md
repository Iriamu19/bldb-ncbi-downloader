# BLDB NCBI Downloader

The **BLDB NCBI Downloader** is a Python script designed to fetch and display FASTA sequences from the [Beta-Lactamase DataBase (BLDB)](https://bldb.eu/) and the NCBI database. It extracts accession numbers from a BLDB page and retrieves the corresponding sequences from NCBI.

## Features

- Extracts NCBI accession numbers and query parameters from BLDB HTML pages.
- Constructs NCBI efetch URLs for retrieving FASTA sequences.
- Fetches and displays FASTA sequences for the extracted accession numbers.
- Optionally saves FASTA sequences to files in a specified directory.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/bldb-ncbi-downloader.git
   cd bldb-ncbi-downloader
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install .
   ```

## Usage

Run the script using the following command:

```bash
python bldb_ncbi_downloader.py <BLDB_URL> [--output-dir <OUTPUT_DIR>]
```

- Replace `<BLDB_URL>` with the URL of the BLDB page you want to process.
- Optionally, use the `--output-dir` option to specify a directory where the FASTA sequences will be saved as files.

### Example

1. Display FASTA sequences in the terminal:
   ```bash
   python bldb_ncbi_downloader.py "http://www.bldb.eu/BLDB.php?prot=A#AAK"
   ```

2. Save FASTA sequences to a directory:
   ```bash
   python bldb_ncbi_downloader.py "http://www.bldb.eu/BLDB.php?prot=A#AAK" --output-dir ./fasta_sequences
   ```

The script will output the FASTA sequences for the accession numbers found on the provided BLDB page or save them to the specified directory.

## How It Works

1. **Fetch HTML Content**: The script fetches the HTML content of the provided BLDB URL.
2. **Extract Accessions**: It parses the HTML to extract NCBI accession numbers and optional query parameters (e.g., `from`, `to`, `strand`).
3. **Build efetch URLs**: For each accession, it constructs an efetch URL to retrieve the corresponding FASTA sequence from NCBI.
4. **Fetch FASTA Sequences**: The script fetches and displays the FASTA sequences for the extracted accession numbers or saves them to files if the `--output-dir` option is used.

## Example Output

```plaintext
>>> FASTA for ABC12345 (100-200, strand=1) <<<
>ABC12345.1 Example sequence
ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC
...

# If using --output-dir, the output will indicate the saved file:
FASTA for ABC12345 saved to ./fasta_sequences/ABC12345.fasta
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the script.

## Acknowledgments

- [Beta-Lactamase DataBase (BLDB)](https://bldb.eu/)
- [NCBI](https://www.ncbi.nlm.nih.gov/)
