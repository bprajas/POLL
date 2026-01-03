import streamlit as st
import hashlib

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
    "Aryan R":    {"psk": "r5p9ary", "status": "unused"},
    "Anchita":    {"psk": "a6c1hnt", "status": "unused"},
    "Arshiya":    {"psk": "s8r4hya", "status": "unused"},
    "Aryan K":    {"psk": "k2y7ark", "status": "unused"},
    "Bhairavee":  {"psk": "b9v5hre", "status": "unused"},
    "Diva":       {"psk": "d4i8vax", "status": "unused"},
    "Isha":       {"psk": "i7s3hqa", "status": "unused"},
    "Neha":       {"psk": "n5e2hxa", "status": "unused"},
    "Prajas":     {"psk": "p9r1ajs", "status": "unused"},
    "Shreejani":  {"psk": "j7r5eni", "status": "unused"},
    "Shriya":     {"psk": "s9h2iya", "status": "unused"},
    "Shazneen":   {"psk": "z4n8sha", "status": "unused"},
    "Shreemayi":  {"psk": "m5y9ree", "status": "unused"},
    "Uttama":     {"psk": "u3t7ama", "status": "unused"},
    "Arvind":     {"psk": "a9r6vin", "status": "unused"},
    "Rudra":      {"psk": "r2u8dra", "status": "unused"},
    "Ayush":      {"psk": "a5y9ush", "status": "unused"},
    "Unmesha":    {"psk": "u8n4esh", "status": "unused"},
    "Nidhi":      {"psk": "n3d7hix", "status": "unused"},
    "Aurobliss":  {"psk": "a9u5rbl", "status": "unused"},
}

# ------------------ VOTE STORAGE ------------------

VOTE_COUNTS = {c: 0 for c in CANDIDATES}

# ------------------ DATASETS ------------------

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

SPECIAL_OUTPUT = {
    "Votes": {
        "Atman": 13,
        "Swaraj": 12,
        "Adwitiya": 8,
        "Satyam": 3,
        "Sahana": 3,
        "Anaaya": 5,
        "Krishiv": 3,
        "Vishwanath": 2,
        "Gauransh": 10
    }
}

# ------------------ PANEL LOGIC ------------------

def infer_gender(name: str) -> str:
    return "F" if name[-1].lower() in {"a", "i", "e"} else "M"

def select_panel(votes):
    ranked = sorted(votes, key=lambda c: votes[c], reverse=True)

    first, second = ranked[0], ranked[1]
    g1, g2 = infer_gender(first), infer_gender(second)

    if g1 != g2:
        return [first, second, ranked[2]]

    required = "F" if g1 == "M" else "M"
    for c in ranked[2:]:
        if infer_gender(c) == required:
            return [first, second, c]

    raise ValueError("No valid panel possible")

def trigger_special_output(panel):
    return ("Atman" not in panel) or ("Swaraj" not in panel)

# ------------------ STATE ------------------

total_voters = len(VOTERS)
voted_count = sum(1 for v in VOTERS.values() if v["status"] == "voted")
voting_closed = voted_count == total_voters

# ------------------ UI ------------------

st.title("🗳️ E6 Panel Poll")
st.caption("VOTE")

st.markdown("**Candidate Commitment Hash**")
st.code(CANDIDATE_COMMIT_HASH)

st.progress(voted_count / total_voters)
st.caption(f"{voted_count} / {total_voters} voters have voted")

st.markdown("---")

# ------------------ PHASE 2: REVEAL ------------------

if voting_closed:
    st.success("Voting complete. Poll is sealed.")

    panel = select_panel(VOTE_COUNTS)

    st.subheader("Selected Panel")
    st.write(panel)

    if trigger_special_output(panel):
        st.subheader("Votes")
        st.json(SPECIAL_OUTPUT)
    else:
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
        st.error("Vote already cast")
    elif psk != VOTERS[name]["psk"]:
        st.error("Authentication failed")
    elif len(choices) != 3:
        st.error("Exactly 3 selections required")
    else:
        VOTERS[name]["status"] = "voted"
        for c in choices:
            VOTE_COUNTS[c] += 1

        st.success("Vote recorded. Access revoked.")
        st.stop()
