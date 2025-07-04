import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

CATEGORY_KEYWORDS = {
    "access_control": ["authentication", "authorization", "privilege", "identity", "mfa", "user access"],
    "incident_response": ["incident", "detection", "response", "report", "csirt", "notification"],
    "risk_management": ["risk", "assessment", "treatment", "mitigation", "register", "governance"],
    "business_continuity": ["continuity", "disaster recovery", "rto", "rpo", "resilience"],
    "third_party_risk": ["vendor", "supply chain", "outsourcing", "third-party"],
    "encryption": ["encryption", "crypto", "tls", "pki", "aes", "key management"],
    "governance": ["roles", "responsibility", "policy", "framework", "board"]
}

def extract_keywords(text):
    doc = nlp(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks]
    keywords += [ent.text.lower() for ent in doc.ents]
    return list(set([kw.strip() for kw in keywords if len(kw) > 2]))

def infer_category(text):
    text_lower = text.lower()
    scores = {}
    for category, words in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for word in words if word in text_lower)
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else "other"

def infer_severity(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["must", "required", "critical", "mandatory"]):
        return "high"
    elif any(w in text_lower for w in ["should", "recommended", "appropriate"]):
        return "medium"
    else:
        return "low"
