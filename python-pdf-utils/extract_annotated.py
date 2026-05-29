# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pypdf2",
# ]
# ///
import argparse
from posix import kill

from PyPDF2 import PdfReader, PdfWriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A utility that extract PDF pages with annotations from <inputs> and writes only those pages to <output>.",
    )
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("-o", required=True)
    parser.add_argument(
        "--ignore-annots",
        help="Comma-separated list of annotations to remove.",
        default="/Link",
    )

    args = parser.parse_args()

    to_ignore = [
        a.strip()  #
        for a in args.ignore_annots.split(",")
    ]

    readers = [
        PdfReader(open(i, "rb"))  #
        for i in args.inputs
    ]

    all_keys = set()
    with open(args.o, "wb") as f:
        writer = PdfWriter()
        for reader in readers:
            for page in reader.pages:
                if "/Annots" not in page:
                    continue
                annots = [
                    a  #
                    for a in page["/Annots"]
                    if a.get_object()["/Subtype"] not in to_ignore
                ]
                if annots:
                    page.annotations.clear()
                    page.annotations.extend(annots)
                    writer.add_page(page)
                all_keys.update(page.keys())
        print(f"Writing out {len(writer.pages)} pages.")
        if len(writer.pages) == 0:
            writer.add_blank_page()
        writer.write(f)
        writer.close()
