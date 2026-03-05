import os
import sys
import argparse
import warnings
from Bio.PDB import MMCIFParser, PDBIO


def convert_cif_to_pdb(cif_path: str, pdb_path: str):
    parser = MMCIFParser(QUIET=True)

    structure_id = os.path.splitext(os.path.basename(cif_path))[0]

    print(f"Parsing: {cif_path}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        structure = parser.get_structure(structure_id, cif_path)

    io = PDBIO()
    io.set_structure(structure)
    io.save(pdb_path)

    print(f"Written: {pdb_path}")


def main(args: argparse.Namespace):
    if not os.path.isfile(args.input):
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    if args.output:
        pdb_path = args.output
    else:
        pdb_path = os.path.splitext(args.input)[0] + ".pdb"

    os.makedirs(os.path.dirname(os.path.abspath(pdb_path)), exist_ok=True)

    convert_cif_to_pdb(args.input, pdb_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a .cif (mmCIF) file to .pdb format.",
        epilog="""
Examples:
  python cif_to_pdb.py structure.cif
  python cif_to_pdb.py structure.cif --output my_structure.pdb
  python cif_to_pdb.py structure.cif --output ./pdbs/my_structure.pdb
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        help="Path to input .cif file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path for output .pdb file (default: same name/location as input with .pdb extension)",
    )
    args = parser.parse_args()
    main(args)
