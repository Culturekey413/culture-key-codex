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
import re, json, os
COMPILED_PATH = "codex_agents_compiled.json"
README_PATH   = "README.md"
POINTER_PATH  = "magna_index_pointer.md"

# --- load compiled agents (list or dict) ---
with open(COMPILED_PATH, "r", encoding="utf-8") as f:
    compiled = json.load(f)
agents_raw = compiled if isinstance(compiled, list) else compiled.get("agents", [])

# --- de-duplicate by 'agent' or 'full_name' to μην βγαίνουν διπλές γλώσσες ---
uniq = {}
for a in agents_raw:
    key = (a.get("agent") or a.get("full_name") or "").strip().lower()
    if not key:
        continue
    # κράτα την πρώτη πλήρη εγγραφή
    if key not in uniq:
        uniq[key] = a
agents = list(uniq.values())

def g(a, k, default=""):
    v = a.get(k)
    return v if v is not None else default

# ---------- 1) build Agents section (clean, δίγλωσσο header) ----------
section_lines = []
section_lines.append("")
for a in sorted(agents, key=lambda x: (g(x,"full_name") or g(x,"agent","")).lower()):
    full_name = g(a, "full_name") or g(a, "agent", "Unknown Agent")
    version   = g(a, "version", "")
    desc      = g(a, "description", "")
    line = f"- **{full_name}**" + (f" (v{version})" if version else "") + (f" — {desc}" if desc else "")
    section_lines.append(line)
section_lines.append("")

generated_block = "\n".join(section_lines)

# ---------- 2) replace ONLY the marked region in README ----------
if os.path.exists(README_PATH):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()
    start = r"<!-- AGENTS_SECTION_START -->"
    end   = r"<!-- AGENTS_SECTION_END -->"
    pattern = re.compile(f"{start}.*?{end}", flags=re.DOTALL)
    replacement = f"<!-- AGENTS_SECTION_START -->\n<!-- generated: do not edit by hand -->\n{generated_block}\n<!-- AGENTS_SECTION_END -->"
    if pattern.search(readme):
        readme = pattern.sub(replacement, readme)
    else:
        # αν λείπουν οι markers, μην γράψεις όλο το README· απλώς πρόσθεσέ τους στο τέλος
        readme += f"\n\n## Active Agents / Ενεργοί Πράκτορες\n{replacement}\n"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)
    print("✅ README.md (agents section) updated.")
else:
    print("⚠️ README.md not found; skipped.")

# ---------- 3) regenerate magna_index_pointer.md (ολόκληρο, όχι markers) ----------
pointer = ["# Magna Index Pointer", "", "## Agents / Πράκτορες", ""]
for a in sorted(agents, key=lambda x: (g(x,"full_name") or g(x,"agent","")).lower()):
    full_name = g(a, "full_name") or g(a, "agent", "Unknown Agent")
    version   = g(a, "version", "")
    desc      = g(a, "description", "")
    agent_id  = g(a, "agent", "")
    pointer.append(f"- **{full_name}**" + (f" (v{version})" if version else "") + (f" — {desc}" if desc else ""))
    if agent_id:
        pointer.append(f"  Path: `modules/{agent_id}`")
    pointer.append("")
with open(POINTER_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(pointer))
print("✅ magna_index_pointer.md rebuilt.")
