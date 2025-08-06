import os
import json
from glob import glob

def find_manifest_files():
    return (
        glob("modules/**/**/*_manifest.json", recursive=True) +
        glob("modules/**/inceptum_manifest.json", recursive=True)
    )

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    compiled = []
    updated = []
print("Manifest files found:", find_manifest_files())

for manifest_path in find_manifest_files():
        try:
            data = load_json(manifest_path)
            # Πλήρη δεδομένα για compiled
            compiled.append({
                "agent": data.get("agent"),
                "module_name": data.get("module_name"),
                "version": data.get("version"),
                "description_gr": data.get("description_gr"),
                "description_en": data.get("description_en"),
                "core_functions": data.get("core_functions"),
                "ethical_signature": data.get("ethical_signature"),
                "source_file": manifest_path
            })
            # Συνοπτικά για updated
            updated.append({
                "agent": data.get("agent"),
                "title_gr": data.get("module_name") or "",
                "title_en": data.get("module_name") or "",
                "description_gr": data.get("description_gr"),
                "description_en": data.get("description_en")
            })
        except Exception as e:
            print(f"Error in {manifest_path}: {e}")

    # Γράφει τα json
    with open("codex_agents_compiled.json", "w", encoding="utf-8") as f:
        json.dump(compiled, f, ensure_ascii=False, indent=2)
    with open("codex_agents_updated.json", "w", encoding="utf-8") as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
