import subprocess
import tempfile
import os
from Bio import SeqIO
from Bio import AlignIO

def align_with_muscle(records):
    """Aligns a list of Biopython SeqRecords using MUSCLE."""
    if not records:
        raise ValueError("No records to align.")

    with tempfile.TemporaryDirectory() as temp_dir:
        input_fasta = os.path.join(temp_dir, "unaligned.fasta")
        output_fasta = os.path.join(temp_dir, "aligned.fasta")

        SeqIO.write(records, input_fasta, "fasta")
        cmd = ["muscle", "-align", input_fasta, "-output", output_fasta]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True # Raises CalledProcessError if command fails
            )
            
            alignment = AlignIO.read(output_fasta, "fasta")
            return alignment
        
        except FileNotFoundError:
            raise RuntimeError(
                "Couldn't find the 'muscle' executable."
                "Please install MUSCLE and ensure it's in your PATH."
                "You can install it via conda: conda install -c bioconda muscle"
            )
        except subprocess.CalledProcessError as e:
            if "Unknown option" in e.stderr:
                try:
                    cmd_v3 = ["muscle", "-in", input_fasta, "-out", output_fasta]
                    subprocess.run(
                        cmd_v3,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    return AlignIO.read(output_fasta, "fasta")
                except Exception as fallback_error:
                    raise RuntimeError(f"MUSCLE failed (We tried v3 and v5 syntax): {fallback_error}")
                
            raise RuntimeError(f"MUSCLE alignment failed with error:\n{e.stderr}")

def prepare_alignment(records):
    """Wrapper function as main entry point. May add support for MAFFT or ClustalW."""
    print("Running MUSCLE alignment...")
    return align_with_muscle(records)
