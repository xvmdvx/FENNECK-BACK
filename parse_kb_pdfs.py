import os
import re
import json
import subprocess

SECTIONS = [
    "Order Review",
    "Information Listed in the Articles",
    "Professional Service",
    "Most Common Rejections",
    "Special Notes",
    "Instructions",
]

SECTION_RE = re.compile(r"^(%s)$" % "|".join(re.escape(s) for s in SECTIONS), re.IGNORECASE)

def canonical(title: str) -> str:
    for s in SECTIONS:
        if s.lower() == title.lower():
            return s
    return title


def parse_pdf(path: str):
    # use pdftotext for faster extraction
    result = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True)
    text = result.stdout
    lines = [l.strip() for l in text.splitlines()]
    data = {}
    current = None
    for line in lines:
        if not line:
            continue
        m = SECTION_RE.match(line)
        if m:
            current = canonical(m.group(1))
            data[current] = []
            continue
        if current:
            data[current].append(line)
    return data


def parse_state_pdfs(folder: str):
    states = {}
    for fname in os.listdir(folder):
        if not fname.lower().endswith('.pdf'):
            continue
        if fname.lower().startswith('global'):
            continue
        state = fname.split(' - ')[0].strip().title()
        path = os.path.join(folder, fname)
        states[state] = parse_pdf(path)
    return states


def parse_global_issues(path: str):
    result = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True)
    text = result.stdout
    issues = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            issues.append(line)
    # deduplicate while preserving order
    seen = set()
    dedup = []
    for item in issues:
        if item not in seen:
            dedup.append(item)
            seen.add(item)
    return dedup


if __name__ == "__main__":
    states_data = parse_state_pdfs("KB-PDFS")
    os.makedirs("data", exist_ok=True)
    with open("data/state_kb.json", "w") as f:
        json.dump(states_data, f, indent=2)

    global_issues = parse_global_issues("GLOBAL ISSUES - KB.pdf")
    with open("data/global_issues.json", "w") as f:
        json.dump(global_issues, f, indent=2)
