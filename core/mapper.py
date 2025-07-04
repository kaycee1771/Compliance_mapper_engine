import yaml
import re
from sentence_transformers import SentenceTransformer, util
from core.ontology import build_master_control_ontology

model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_input_text(input_item):
    if isinstance(input_item, tuple):
        text = input_item[0]
    else:
        text = input_item
    return re.sub(r"[^a-zA-Z0-9\s\.\-]", "", text).strip().lower()

def flatten_input_artifacts(parsed_inputs):
    flat_texts = []

    for entry in parsed_inputs:
        typ, src, content = entry
        
        # Debugging: Print the content to ensure it's a string
        print(f"Processing: {content}")

        if isinstance(content, tuple):
            # If content is a tuple, extract the actual text (3rd item in the tuple)
            text = content[2] if len(content) > 2 else ''
            flat_texts.append((typ, src, str(text)))  # Enforce string here
        elif isinstance(content, str):
            flat_texts.append((typ, src, content))  # Already a string, append it
        elif isinstance(content, list):  # Handle list content (e.g., Git commits)
            # If it's a list, ensure we only get strings by joining them
            combined_text = " ".join([str(line) for line in content if isinstance(line, str)])
            flat_texts.append((typ, src, combined_text))  # Join list items into a single string

    return flat_texts

def compute_semantic_matches(input_texts, controls, threshold=0.42):
    results = []
    control_ids = list(controls.keys())
    control_texts = [controls[ctrl]["description"] for ctrl in control_ids]
    control_embeddings = model.encode(control_texts, convert_to_tensor=True)

    for typ, src, input_text in input_texts:
        print(f"Cleaning input: {input_text}")  # Debugging the input text
        cleaned = clean_input_text(str(input_text))  # Ensure string input
        input_embedding = model.encode(cleaned, convert_to_tensor=True)
        similarities = util.cos_sim(input_embedding, control_embeddings)[0]

        for i, score in enumerate(similarities):
            if score.item() >= threshold:
                results.append({
                    "input_type": typ,
                    "source": src,
                    "text": input_text,
                    "matched_control": control_ids[i],
                    "similarity": round(score.item(), 3)
                })
            elif score.item() >= 0.3:
                print(f"[~] Low match: {input_text[:60]} → {control_ids[i]} ({round(score.item(), 3)})")

    return results

def run_phase3_mapper():
    with open("data/parsed/phase1_outputs.yaml", "r", encoding="utf-8") as f:
        parsed_inputs = yaml.load(f, Loader=yaml.FullLoader)

    input_texts = flatten_input_artifacts(parsed_inputs)
    ontology = build_master_control_ontology()

    matches = compute_semantic_matches(input_texts, ontology)

    with open("data/parsed/phase3_matches.yaml", "w", encoding="utf-8") as f:
        yaml.dump(matches, f, allow_unicode=True)

    print(f"Found {len(matches)} control matches from input data. Output saved to phase3_matches.yaml")
