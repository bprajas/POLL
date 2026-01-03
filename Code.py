import streamlit as st
import hashlib
import time

# ------------------ CONFIG ------------------

st.set_page_config(
    page_title="E6 Panel Poll",
    page_icon="🗳️",
    layout="centered"
)

# ------------------ CORE DATA ------------------

CANDIDATES = [
    "Adwitiya", "Atman", "Anaaya",
    "Sahana", "Gauransh", "Krishiv",
    "Vishwanath", "Swaraj", "Satyam"
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

GENESIS_HASH = "0" * 64

# ------------------ FINAL DATASET ------------------

FINAL_DATASET = {
    "dataset_name": "E6 Independent Dataset",
    "released_after": "All voters submitted ballots",
    "values": [
        {"t": 0, "value": 12},
        {"t": 1, "value": 19},
        {"t": 2, "value": 7},
        {"t": 3, "value": 25},
    ]
}

# ------------------ STATE CHECK ------------------

total_voters = len(VOTERS)
voted_count = sum(1 for v in VOTERS.values() if v["status"] == "voted")
voting_closed = voted_count == total_voters

# ------------------ HEADER ------------------

st.title("🗳️ E6 Panel Poll")
st.caption("Commitment-based voting • No result disclosure")

st.markdown("**Candidate Commitment Hash**")
st.code(CANDIDATE_COMMIT_HASH)

st.progress(voted_count / total_voters)
st.caption(f"{voted_count} / {total_voters} voters have voted")

st.markdown("---")

# ------------------ PHASE 2: DATASET REVEAL ------------------

if voting_closed:
    st.success("Voting complete. Poll is permanently sealed.")
    st.subheader("Released Dataset")
    st.json(FINAL_DATASET)
    st.stop()

# ------------------ PHASE 1: VOTING ------------------

left, right = st.columns(2)

with left:
    st.subheader("Voter Authentication")
    name = st.selectbox("Your name", [""] + list(VOTERS.keys()))
    psk = st.text_input("Secret key", type="password")

with right:
    st.subheader("Ballot")
    st.caption("Select exactly **3** candidates")
    choices = st.multiselect(
        "Candidates",
        CANDIDATES,
        max_selections=3
    )

st.markdown("---")

if st.button("Submit Ballot", use_container_width=True):
    if name == "" or name not in VOTERS:
        st.error("Invalid voter identity")
    elif VOTERS[name]["status"] == "voted":
        st.error("Vote already cast. Access revoked.")
    elif psk != VOTERS[name]["psk"]:
        st.error("Authentication failed")
    elif len(choices) != 3:
        st.error("Exactly 3 selections are required.")
    else:
        VOTERS[name]["status"] = "voted"

        prev_hash = LEDGER[-1]["hash"] if LEDGER else GENESIS_HASH
        entry = {
            "voter_hash": hash_str(name),
            "choices": sorted(choices),
            "candidate_commitment": CANDIDATE_COMMIT_HASH,
            "timestamp": time.time(),
            "prev_hash": prev_hash
        }
        entry["hash"] = hash_str(str(entry))

        st.success("Vote recorded. Voting rights permanently closed.")
        st.stop()

# ------------------ AUDIT ------------------

with st.expander("Audit Ledger"):
    st.json(LEDGER)
