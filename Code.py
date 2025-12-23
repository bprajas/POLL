import streamlit as st
import hashlib
import time

CANDIDATES = [
    "Adwitiya",
    "Atman",
    "Anaaya",
    "Sahana",
    "Gauransh",
    "Krishiv",
    "Vishwanath",
    "Swaraj",
]

def hash_str(s):
    return hashlib.sha256(s.encode()).hexdigest()

CANDIDATE_COMMIT_HASH = hash_str(str(sorted(CANDIDATES)))

VOTERS = {
    "Adwitiya":   {"psk": "q7m4adw", "status": "unused"},
    "Anaaya":     {"psk": "n9a2kye", "status": "unused"},
    "Atman":      {"psk": "t3x8atm", "status": "unused"},
    "Aryan R":    {"psk": "r5p9ary", "status": "unused"},
    "Anchita":    {"psk": "a6c1hnt", "status": "unused"},
    "Arshiya":    {"psk": "s8r4hya", "status": "unused"},
    "Aryan K":    {"psk": "k2y7ark", "status": "unused"},
    "Bhairavee":  {"psk": "b9v5hre", "status": "unused"},
    "Diva":       {"psk": "d4i8vax", "status": "unused"},
    "Isha":       {"psk": "i7s3hqa", "status": "unused"},
    "Neha":       {"psk": "n5e2hxa", "status": "unused"},
    "Krishiv":    {"psk": "k8r6shv", "status": "unused"},
    "Prajas":     {"psk": "p9r1ajs", "status": "unused"},
    "Satyam":     {"psk": "s2t8yam", "status": "unused"},
    "Sahana":     {"psk": "s6h4ana", "status": "unused"},
    "Shreejani":  {"psk": "j7r5eni", "status": "unused"},
    "Shriya":     {"psk": "s9h2iya", "status": "unused"},
    "Shazneen":   {"psk": "z4n8sha", "status": "unused"},
    "Shreemayi":  {"psk": "m5y9ree", "status": "unused"},
    "Uttama":     {"psk": "u3t7ama", "status": "unused"},
    "Vishwanath": {"psk": "v8s4nwt", "status": "unused"},
    "Arvind":     {"psk": "a9r6vin", "status": "unused"},
    "Rudra":      {"psk": "r2u8dra", "status": "unused"},
    "Ayush":      {"psk": "a5y9ush", "status": "unused"},
    "Swaraj":     {"psk": "s7w3raj", "status": "unused"},
    "Gauransh":   {"psk": "g6a2nsh", "status": "unused"},
    "Unmesha":    {"psk": "u8n4esh", "status": "unused"},
    "Nidhi":      {"psk": "n3d7hix", "status": "unused"},
    "Aurobliss":  {"psk": "a9u5rbl", "status": "unused"},
}

LEDGER = []
GENESIS_HASH = "0" * 64

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

st.markdown("---")
if st.checkbox("Show ledger (audit)"):
    st.json(LEDGER)
