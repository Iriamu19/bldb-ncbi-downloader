# BLDB NCBI Downloader

The **BLDB NCBI Downloader** is a Python script designed to fetch and display FASTA sequences from the [Beta-Lactamase DataBase (BLDB)](https://bldb.eu/) and the NCBI database. It extracts accession numbers from a BLDB page and retrieves the corresponding sequences from NCBI.

## Features

- Extracts NCBI accession numbers and query parameters from BLDB HTML pages.
- Constructs NCBI efetch URLs for retrieving FASTA sequences.
- Fetches and displays FASTA sequences for the extracted accession numbers.

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
python bldb_ncbi_downloader.py <BLDB_URL>
```

Replace `<BLDB_URL>` with the URL of the BLDB page you want to process.

### Example

```bash
python bldb_ncbi_downloader.py "http://www.bldb.eu/BLDB.php?prot=A#AAK"
```

The script will output the FASTA sequences for the accession numbers found on the provided BLDB page.

## How It Works

1. **Fetch HTML Content**: The script fetches the HTML content of the provided BLDB URL.
2. **Extract Accessions**: It parses the HTML to extract NCBI accession numbers and optional query parameters (e.g., `from`, `to`, `strand`).
3. **Build efetch URLs**: For each accession, it constructs an efetch URL to retrieve the corresponding FASTA sequence from NCBI.
4. **Fetch FASTA Sequences**: The script fetches and displays the FASTA sequences for the extracted accession numbers.

## Example Output

```plaintext
>>> FASTA for ABC12345 (100-200, strand=1) <<<
>ABC12345.1 Example sequence
ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC
...
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the script.

## Acknowledgments

- [Beta-Lactamase DataBase (BLDB)](https://bldb.eu/)
- [NCBI](https://www.ncbi.nlm.nih.gov/)
