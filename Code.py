import streamlit as st
import hashlib
import secrets
import time

# ===============================
# CONFIGURATION
# ===============================

CANDIDATES = {
    "Adwitiya": "Adwitiya",
    "Atman": "Atman",
    "Anaaya": "Anaaya",
    "Sahana": "Sahana",
    "Gauransh": "Gauransh",
    "Swaraj": "Swaraj",
}

def hash_str(s):
    return hashlib.sha256(s.encode()).hexdigest()

CANDIDATE_COMMIT_HASH = hash_str(str(sorted(CANDIDATES.items())))

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
# SESSION STATE INIT
# ===============================

for key in ["challenge", "name", "authenticated"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "authenticated" else False

# ===============================
# UI
# ===============================

st.title("E6 Program Panel Poll")

st.markdown("**Candidate commitment hash:**")
st.code(CANDIDATE_COMMIT_HASH)

name = st.selectbox("Select your name", [""] + list(VOTERS.keys()))

if name:
    if VOTERS[name]["status"] == "voted":
        st.error("You have already voted. Access revoked.")
        st.stop()

    if st.button("Request challenge"):
        st.session_state.challenge = secrets.token_hex(16)
        st.session_state.name = name
        st.session_state.authenticated = False

# ----------------
# Challenge
# ----------------
if st.session_state.challenge:
    st.markdown("**Challenge issued:**")
    st.code(st.session_state.challenge)
    
    response = st.text_input("Enter SHA256(challenge + PSK)")
    
    if st.button("Authenticate"):
        expected = hash_str(st.session_state.challenge + VOTERS[name]["psk"])
        if response == expected:
            st.session_state.authenticated = True
            st.success("Authenticated")
        else:
            st.error("Authentication failed")

# ----------------
# Voting (Pick 3)
# ----------------
if st.session_state.authenticated:
    selected = st.multiselect(
        "Select exactly 3 candidates",
        list(CANDIDATES.keys()),
        format_func=lambda x: CANDIDATES[x]
    )

    if st.button("Cast vote"):
        if len(selected) != 3:
            st.warning("You must select exactly 3 candidates")
        else:
            VOTERS[name]["status"] = "voted"

            entry = {
                "voter_hash": hash_str(name),
                "candidates": selected,
                "candidate_commitment": CANDIDATE_COMMIT_HASH,
                "timestamp": time.time(),
                "prev_hash": LEDGER[-1]["hash"] if LEDGER else GENESIS_HASH
            }
            entry["hash"] = hash_str(str(entry))
            LEDGER.append(entry)

            st.success("Vote recorded. Session terminated.")
            st.session_state.clear()
            st.stop()

# ----------------
# Ledger (audit)
# ----------------
st.markdown("---")
if st.checkbox("Show ledger (audit)"):
    st.json(LEDGER)
