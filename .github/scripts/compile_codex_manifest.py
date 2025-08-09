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
    print("Manifest files found:", 
find_manifest_files())
    for manifest_path in find_manifest_files():
        try:
            data = load_json(manifest_path)
            # Πλήρη δεδομένα για compiled
            compiled.append({
                "agent": data.get("agent"),
                "module_name": data.get("module_name"),
                "version": data.get("version"),
                "description": data.get("description"),
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
import os, json

COMPILED_PATH = "codex_agents_compiled.json"

# Φόρτωσε το compiled από το σωστό αρχείο
with open(COMPILED_PATH, "r", encoding="utf-8") as f:
    compiled_data = json.load(f)

# Υποστήριξη και για list και για dict σχήμα
if isinstance(compiled_data, list):
    agents = compiled_data
elif isinstance(compiled_data, dict):
    agents = compiled_data.get("agents", [])
else:
    agents = []

def g(v, d=""):
    return v if v is not None else d

# ============= 1) magna_index_pointer.md =================
pointer = ["# Magna Index Pointer", "", "## Agents / Πράκτορες", ""]
for a in sorted(agents, key=lambda x: g(x.get("full_name") or x.get("agent") or "", "").lower()):
    full_name = g(a.get("full_name") or a.get("agent") or "Unknown Agent")
    version   = g(a.get("version") or "")
    desc      = g(a.get("description") or "")
    # Προσπάθησε να βρεις φάκελο· αν δεν υπάρχει, άστο κενό
    folder = a.get("agent") or a.get("agent_folder") or ""
    pointer.append(f"- **{full_name}** (v{version}) — {desc}".rstrip())
    if folder:
        pointer.append(f"  Path: `modules/{folder}`")
    pointer.append("")  # κενή γραμμή ανά item

with open("magna_index_pointer.md", "w", encoding="utf-8") as f:
    f.write("\n".join(pointer))
print("✅ magna_index_pointer.md updated.")

# ============= 2) README.md (root) =======================
readme = [
    "# Culture Key — Agents Overview / Επισκόπηση Πρακτόρων",
    "",
    "## Active Agents / Ενεργοί Πράκτορες",
    ""
]
for a in sorted(agents, key=lambda x: g(x.get("full_name") or x.get("agent") or "", "").lower()):
    full_name = g(a.get("full_name") or a.get("agent") or "Unknown Agent")
    version   = g(a.get("version") or "")
    desc      = g(a.get("description") or "")
    readme.append(f"- **{full_name}** (v{version}) — {desc}".rstrip())

readme += ["", "---", "© Culture Key — Non-Commercial, Ethical AI"]
with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(readme))
print("✅ README.md updated.")
