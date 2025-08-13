import sys
import zipfile
import json
import glob
import os

def main(input_zip_path, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(input_zip_path, 'r') as z:
        with z.open('library.json') as f:
            data = json.load(f)
            docs = data.get("docs", [])
            for doc in docs:
                doc_data = doc.get("data", {})
                doc_title = doc_data.get("doc_title", "untitled")
                safe_title = "".join(c for c in doc_title if c.isalnum() or c in " _-").rstrip()
                output_txt_path = os.path.join(output_dir, f"{safe_title}.txt")

                lines = [
                    f"Title: {doc_data.get('doc_title', '')}",
                    f"File Name: {doc_data.get('doc_file_name_title', '')}",
                    f"Authors: {doc_data.get('doc_authors', '')}",
                    f"Annotation: {doc_data.get('doc_annotation', '')}",
                    "",
                    "Citations:"
                ]
                os.makedirs(output_dir, exist_ok=True)
                output_txt_path = os.path.join(output_dir, f"{safe_title}.txt")
                print(output_txt_path)
                citations = doc.get("citations", [])
                for idx, citation in enumerate(citations, 1):
                    note_body = citation.get("note_body", "")
                    note_page = citation.get("note_page", "")
                    lines.append(f"{idx}. Page: {note_page}\n   Note: {note_body}")

                with open(output_txt_path, 'w', encoding='utf-8') as out_f:
                    out_f.write("\n".join(lines))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path/to/files/*.bak>")
        sys.exit(1)
    files = glob.glob(sys.argv[1])
    if not files:
        print("No files matched the pattern.")
        sys.exit(1)
    for file_path in files:
        output_path = "output"
        os.makedirs(output_path, exist_ok=True)
        main(file_path, output_path)
        print(f"Processed {file_path} -> {output_path}")
