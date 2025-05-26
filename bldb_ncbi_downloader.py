import os
import re
from dataclasses import dataclass
from time import sleep
from typing import List, Optional
from urllib.parse import parse_qs

import click
import requests
from requests.exceptions import ConnectionError


@dataclass
class Accession:
    accession: str
    from_position: Optional[str] = None
    to_position: Optional[str] = None
    strand: Optional[str] = None


def fetch_html_content(url: str, session: requests.Session) -> str:
    """
    Fetch the HTML content of a given URL using a session.

    Args:
        url (str): The URL to fetch.
        session (requests.Session): The session to use for the request.

    Returns:
        str: The HTML content of the response.
    """
    response = session.get(url)
    response.raise_for_status()
    return response.text


def extract_ncbi_accessions(html_content: str) -> List[Accession]:
    """
    Extract NCBI accession numbers and parameters from the HTML content.

    Args:
        html_content (str): The HTML content to parse.

    Returns:
        list: A list of Accession objects containing accession and query parameters.
    """
    accession_pattern = r'http://www.ncbi.nlm.nih.gov/nuccore/([^"]+)'
    matches = re.findall(accession_pattern, html_content)

    accessions = []
    for match in matches:
        if "?" in match:
            accession, query_string = match.split("?", 1)
            query_params = parse_qs(query_string)
            accessions.append(
                Accession(
                    accession=accession,
                    from_position=query_params.get("from", [None])[0],
                    to_position=query_params.get("to", [None])[0],
                    strand=query_params.get("strand", [None])[0],
                )
            )
        else:
            accessions.append(Accession(accession=match))
    return accessions


def build_efetch_url(
    accession: str,
    from_position: Optional[str] = None,
    to_position: Optional[str] = None,
    strand: Optional[str] = None,
) -> str:
    """
    Build the NCBI efetch URL for a given accession and optional parameters.

    Args:
        accession (str): The NCBI accession number.
        from_position (str, optional): Start position of the sequence.
        to_position (str, optional): End position of the sequence.
        strand (str, optional): Strand information.

    Returns:
        str: The constructed efetch URL.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_url = f"{base_url}?db=nuccore&id={accession}&rettype=fasta&retmode=text"

    if from_position and to_position:
        efetch_url += f"&seq_start={from_position}&seq_stop={to_position}"
    if strand:
        efetch_url += f"&strand={strand}"

    return efetch_url


def fetch_fasta_sequence(efetch_url: str, session: requests.Session, retries: int = 3, delay: float = 1.0) -> Optional[str]:
    """
    Fetch the FASTA sequence from the efetch URL using a session with retry logic.

    Args:
        efetch_url (str): The efetch URL to fetch the sequence from.
        session (requests.Session): The session to use for the request.
        retries (int): Number of retry attempts in case of connection errors.
        delay (float): Delay (in seconds) between retries.

    Returns:
        str: The FASTA sequence if successful, None otherwise.
    """
    for attempt in range(retries):
        try:
            response = session.get(efetch_url)
            if response.ok:
                return response.text
        except ConnectionError as e:
            print(f"Connection error on attempt {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                sleep(delay)
            else:
                print("Max retries reached. Unable to fetch FASTA sequence.")
    return None


@click.command()
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, writable=True),
    default=None,
    help="Directory to save FASTA sequences as files.",
)
def main(output_dir: Optional[str]):
    """
    Main function to fetch and display FASTA sequences from BLDB and NCBI.

    Args:
        output_dir (str, optional): Directory to save FASTA sequences as files.
    """

    bldb_url = "http://www.bldb.eu/BLDB.php"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with requests.Session() as session:
        html_content = fetch_html_content(bldb_url, session)
        accessions = extract_ncbi_accessions(html_content)

        for accession_obj in accessions:
            if output_dir:
                file_path = os.path.join(output_dir, f"{accession_obj.accession}.fasta")
                # Skip download if the file already exists
                if os.path.exists(file_path):
                    print(f"FASTA for {accession_obj.accession} already exists at {file_path}. Skipping download.")
                    continue

            efetch_url = build_efetch_url(
                accession_obj.accession,
                accession_obj.from_position,
                accession_obj.to_position,
                accession_obj.strand,
            )
            fasta_sequence = fetch_fasta_sequence(efetch_url, session)

            if fasta_sequence:
                if output_dir:
                    with open(file_path, "w") as fasta_file:
                        fasta_file.write(fasta_sequence)
                    print(f"FASTA for {accession_obj.accession} saved to {file_path}")
                else:
                    print(fasta_sequence)
            else:
                print(f"Failed to fetch FASTA for {accession_obj.accession}")
            sleep(0.5)


if __name__ == "__main__":
    main()
