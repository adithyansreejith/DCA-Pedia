import os
import json
from datetime import datetime

# Configuration
PDF_ROOT = "static/pdfs"
DATA_FILE = "data/pdfs.js"

programs_config = {
    "msc-ai-ds": {
        "title": "MSc AI/DS Resources",
        "description": "Master of Science in Artificial Intelligence & Data Science",
        "folder": "Msc AI-DS"
    },
    "mca": {
        "title": "MCA Resources",
        "description": "Master of Computer Applications",
        "folder": "MCA"
    },
    "integrated-mca": {
        "title": "Integrated MCA Resources",
        "description": "Integrated Master of Computer Applications",
        "folder": "Integrated MCA"
    }
}

def get_file_size(path):
    size_bytes = os.path.getsize(path)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def generate_manifest():
    manifest = {}
    
    for key, config in programs_config.items():
        folder_path = os.path.join(PDF_ROOT, config["folder"])
        files = []
        
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.pdf'):
                    full_path = os.path.join(folder_path, filename)
                    stats = os.stat(full_path)
                    files.append({
                        "name": filename,
                        "size": get_file_size(full_path),
                        "date": datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')
                    })
        
        manifest[key] = {
            "title": config["title"],
            "description": config["description"],
            "folder": config["folder"],
            "files": files
        }

    # Write as JS file
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write("const pdfData = ")
        f.write(json.dumps(manifest, indent=4))
        f.write(";")
    
    print(f"Successfully updated {DATA_FILE}")

if __name__ == "__main__":
    generate_manifest()
