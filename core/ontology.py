import json
import os
from transformers import pipeline
from core.nlp_utils import extract_keywords, infer_category, infer_severity

# === Loaders for pre-defined control files ===

def load_control_set(framework):
    path = f"controls/{framework}.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Control file not found: {path}")
    if os.path.getsize(path) == 0:
        raise ValueError(f"{framework}.json is empty.")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        if not data:
            raise ValueError(f"{framework}.json contains no valid controls.")
        return data

def build_master_control_ontology():
    master = {}
    for framework in ["nis2", "dora", "iso27001"]:
        controls = load_control_set(framework)
        for ctrl in controls:
            key = ctrl.get("id") or ctrl.get("control_id")
            if not key:
                raise ValueError(f"Missing 'id' in control: {json.dumps(ctrl, indent=2)}")
            master[key] = ctrl
    return master

def print_summary():
    ontology = build_master_control_ontology()
    categories = {}
    for ctrl in ontology.values():
        cat = ctrl.get("category", "uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    print(f"Loaded {len(ontology)} controls across frameworks.")
    print("Breakdown by category:")
    for cat, count in categories.items():
        print(f" - {cat}: {count} controls")

# === Semi-automated control generator from raw text ===

def auto_generate_control_json(text_blob, prefix="GEN"):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    sections = [s.strip() for s in text_blob.split("\n\n") if len(s.strip()) > 40]

    controls = []
    for i, section in enumerate(sections):
        summary = summarizer(section, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
        category = infer_category(section)
        keywords = extract_keywords(section)
        severity = infer_severity(section)

        controls.append({
            "id": f"{prefix}-{i+1:02}",
            "title": summary.split(".")[0].strip(),
            "description": section,
            "category": category,
            "keywords": keywords,
            "related_controls": [],
            "severity": severity
        })

    print(f"Generated {len(controls)} enriched controls from input text.")
    return controls

def save_generated_controls(controls, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(controls, f, indent=2, ensure_ascii=False)
    print(f"Saved controls to {output_path}")
