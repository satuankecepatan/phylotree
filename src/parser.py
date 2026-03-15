from Bio import SeqIO
from Bio.Align import MultipleSeqAlignment
import io

def load_fasta(file_obj):
    """Reads a FASTA file and returns a list of sequence records."""
    try:
        # For if it's a string from a web upload
        if isinstance(file_obj, str) and not file_obj.endswith(('.fasta', '.fas', '.fa')):
            file_obj = io.StringIO(file_obj)
        
        records = list(SeqIO.parse(file_obj, "fasta"))

        if not records:
            raise ValueError("No sequences found, ensure the file is in valid FASTA format.")
        
        return records
    except Exception as e:
        raise ValueError(f"Error reading FASTA file: {e}")

def validate_alignment(records):
    """Checks if a list of sequence records are all the same length.
    This is a hard requirement for distance-based phylogenetic trees."""
    if not records:
        raise ValueError("No records to validate.")
    
    first_seq_len = len(records[0].seq)

    for i, record in enumerate(records):
        if len(record.seq) != first_seq_len:
            raise ValueError(
                f"Alignment error."
                f"Sequence '{record.id}' has length {len(record.seq)},"
                f"The program expected {first_seq_len}."
                f"Distance matrices require all sequences to be aligned (same length)."
            )
    return True, first_seq_len

def get_alignment(file_obj):
    """Reads a FASTA file, validates it, then returns a MultipleSeqAlignment object ready for tree building."""
    records = load_fasta(file_obj)
    is_aligned, seq_length = validate_alignment(records)

    if is_aligned:
        alignment = MultipleSeqAlignment(records)
        return alignment
