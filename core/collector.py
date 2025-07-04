import os
import pdfplumber
import docx
import yaml
import git
import glob
import chardet
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text_from_txt(file_path):
    with open(file_path, "rb") as f:
        raw = f.read()
        encoding = chardet.detect(raw)['encoding']
        return raw.decode(encoding or 'utf-8', errors='ignore')

def extract_text_from_policy_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return ""

def parse_git_repo(repo_path):
    repo = git.Repo(repo_path)
    commits = repo.iter_commits()
    return [f"{c.author.name} {c.committed_datetime} {c.message}" for c in commits]

def parse_infra_config(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def run_collector():
    all_results = []

    # Policies
    policy_files = glob.glob("data/raw/policies/*")
    for f in policy_files:
        text = extract_text_from_policy_file(f)
        entities = extract_entities(text)
        all_results.append(["policy", f, entities])  # Tuple to list

    # Git repos
    repo_dirs = [d for d in os.listdir("data/raw/git_repos") if os.path.isdir(os.path.join("data/raw/git_repos", d))]
    for repo in repo_dirs:
        repo_path = os.path.join("data/raw/git_repos", repo)
        commits = parse_git_repo(repo_path)
        all_results.append(["git_repo", repo, commits])  # Tuple to list

    # Infra configs
    config_files = glob.glob("data/raw/infra_configs/**/*", recursive=True)
    for f in config_files:
        text = parse_infra_config(f)
        entities = extract_entities(text)
        all_results.append(["infra_config", f, entities])  # Tuple to list

    # Save intermediate output 
    os.makedirs("data/parsed", exist_ok=True)
    with open("data/parsed/phase1_outputs.yaml", "w", encoding="utf-8") as out:
        yaml.dump(all_results, out, allow_unicode=True)

    print("Phase 1 complete. Output saved to data/parsed/phase1_outputs.yaml")

