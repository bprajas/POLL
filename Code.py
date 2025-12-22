import streamlit as st
import hashlib
import time

# ===============================
# CONFIGURATION
# ===============================

# ---- FIXED CANDIDATES ----
CANDIDATES = [
    "Adwitiya",
    "Atman",
    "Anaaya",
    "Sahana",
    "Gauransh",
    "Swaraj",
]

def hash_str(s):
    return hashlib.sha256(s.encode()).hexdigest()

CANDIDATE_COMMIT_HASH = hash_str(str(sorted(CANDIDATES)))

# ---- FIXED VOTERS (29) ----
VOTERS = {
    "Adwitiya":   {"psk": "adwitiya", "status": "unused"},
    "Anaaya":     {"psk": "anaaya", "status": "unused"},
    "Atman":      {"psk": "atman", "status": "unused"},
    "Aryan R":    {"psk": "aryanr", "status": "unused"},
    "Anchita":    {"psk": "anchita", "status": "unused"},
    "Arshiya":    {"psk": "arshiya", "status": "unused"},
    "Aryan K":    {"psk": "aryank", "status": "unused"},
    "Bhairavee":  {"psk": "bhairavee", "status": "unused"},
    "Diva":       {"psk": "diva", "status": "unused"},
    "Isha":       {"psk": "isha", "status": "unused"},
    "Neha":       {"psk": "neha", "status": "unused"},
    "Krishiv":    {"psk": "krishiv", "status": "unused"},
    "Prajas":     {"psk": "prajas", "status": "unused"},
    "Satyam":     {"psk": "satyam", "status": "unused"},
    "Sahana":     {"psk": "sahana", "status": "unused"},
    "Shreejani":  {"psk": "shreejani", "status": "unused"},
    "Shriya":     {"psk": "shriya", "status": "unused"},
    "Shazneen":   {"psk": "shazneen", "status": "unused"},
    "Shreemayi":  {"psk": "shreemayi", "status": "unused"},
    "Uttama":     {"psk": "uttama", "status": "unused"},
    "Vishwanath": {"psk": "vishwanath", "status": "unused"},
    "Arvind":     {"psk": "arvind", "status": "unused"},
    "Rudra":      {"psk": "rudra", "status": "unused"},
    "Ayush":      {"psk": "ayush", "status": "unused"},
    "Swaraj":     {"psk": "swaraj", "status": "unused"},
    "Gauransh":   {"psk": "gauransh", "status": "unused"},
    "Unmesha":    {"psk": "unmesha", "status": "unused"},
    "Nidhi":      {"psk": "nidhi", "status": "unused"},
    "Aurobliss":  {"psk": "aurobliss", "status": "unused"},
}

LEDGER = []
GENESIS_HASH = "0" * 64

# ===============================
# UI
# ===============================

st.title("E6 Panel Poll")

st.markdown("**Candidate commitment hash:**")
st.code(CANDIDATE_COMMIT_HASH)

name = st.selectbox("Select your name", [""] + list(VOTERS.keys()))
psk = st.text_input("Enter your secret", type="password")

choice = st.radio("Select ONE candidate", CANDIDATES)

if st.button("Cast Vote"):
    if name == "" or name not in VOTERS:
        st.error("Invalid voter")
    elif VOTERS[name]["status"] == "voted":
        st.error("You have already voted. Access permanently revoked.")
    elif psk != VOTERS[name]["psk"]:
        st.error("Authentication failed")
    else:
        # ---- LOCK VOTER ----
        VOTERS[name]["status"] = "voted"

        prev_hash = LEDGER[-1]["hash"] if LEDGER else GENESIS_HASH
        entry = {
            "voter_hash": hash_str(name),
            "choice": choice,
            "candidate_commitment": CANDIDATE_COMMIT_HASH,
            "timestamp": time.time(),
            "prev_hash": prev_hash
        }
        entry["hash"] = hash_str(str(entry))
        LEDGER.append(entry)

        st.success("Vote recorded. Voting access permanently closed.")
        st.stop()

# ===============================
# AUDIT
# ===============================

st.markdown("---")
if st.checkbox("Show ledger (audit)"):
    st.json(LEDGER)
