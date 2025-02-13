import argparse
import exiftool
import piexif
import mutagen
import pypdf
import os
from PIL import Image

def reveal_metadata(file_path):
    """Extract metadata from any file type."""
    with exiftool.ExifTool("C:\\Users\\Lucas Frink\\Documents\\Exiftool\\exiftool.exe") as et:
        metadata_bytes = et.execute(b"-X",file_path.encode())
        #metadata = metadata_bytes.decode("utf-8")
    return metadata_bytes

def edit_metadata(file_path, field, value):
    """Modify metadata for supported formats."""
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
        img = Image.open(file_path)
        exif_dict = piexif.load(img.info.get("exif", b""))
        exif_dict["0th"][piexif.ImageIFD.Artist] = value.encode("utf-8")
        exif_bytes = piexif.dump(exif_dict)
        img.save("updated_" + os.path.basename(file_path), exif=exif_bytes)
        print(f"Metadata updated: {field} = {value}")

def scrub_metadata(file_path):
    """Remove metadata from an image or PDF."""
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
        img = Image.open(file_path)
        img.save("scrubbed_" + os.path.basename(file_path))  # Saves without metadata
        print(f"Metadata removed: {file_path}")
    elif file_path.lower().endswith(".pdf"):
        reader = pypdf.PdfReader(file_path)
        writer = pypdf.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({})  # Clears metadata
        with open("scrubbed_" + os.path.basename(file_path), "wb") as f:
            writer.write(f)
        print(f"Metadata removed from {file_path}")

# CLI Argument Parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metadata Tool")
    parser.add_argument("--reveal", help="Reveal metadata of a file")
    parser.add_argument("--edit", help="Edit metadata of a file")
    parser.add_argument("--field", help="Metadata field to edit")
    parser.add_argument("--value", help="New value for the metadata field")
    parser.add_argument("--scrub", help="Remove metadata from a file")

    args = parser.parse_args()
    
    if args.reveal:
        metadata = reveal_metadata(args.reveal)
        print(metadata)
    elif args.edit and args.field and args.value:
        edit_metadata(args.edit, args.field, args.value)
    elif args.scrub:
        scrub_metadata(args.scrub)
