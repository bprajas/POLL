import streamlit as st
import hashlib
import secrets
import time

# ===============================
# STATIC CONFIG
# ===============================

CANDIDATES = {
    "A": "Candidate Alpha",
    "B": "Candidate Beta",
    "C": "Candidate Gamma"
}

def hash_str(s):
    return hashlib.sha256(s.encode()).hexdigest()

CANDIDATE_COMMIT_HASH = hash_str(str(sorted(CANDIDATES.items())))

VOTERS = {
    "Alice": {"psk": "alpha123", "status": "unused"},
    "Bob":   {"psk": "bravo456", "status": "unused"},
    "Carol": {"psk": "charlie789", "status": "unused"},
}

LEDGER = []
GENESIS_HASH = "0" * 64

# ===============================
# SESSION STATE INIT
# ===============================

if "challenge" not in st.session_state:
    st.session_state.challenge = None
if "name" not in st.session_state:
    st.session_state.name = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ===============================
# UI
# ===============================

st.title("Local Voting Prototype")

st.markdown("**Candidate commitment:**")
st.code(CANDIDATE_COMMIT_HASH)

# ---- Identity ----
name = st.selectbox("Select your name", [""] + list(VOTERS.keys()))

if name:
    if VOTERS[name]["status"] == "voted":
        st.error("You have already voted. Access revoked.")
        st.stop()

    if st.button("Request challenge"):
        st.session_state.challenge = secrets.token_hex(16)
        st.session_state.name = name
        st.session_state.authenticated = False

# ---- Challenge ----
if st.session_state.challenge:
    st.markdown("**Challenge issued**")
    st.code(st.session_state.challenge)

    response = st.text_input("Enter SHA256(challenge + PSK)")

    if st.button("Authenticate"):
        expected = hash_str(
            st.session_state.challenge + VOTERS[name]["psk"]
        )
        if response == expected:
            st.session_state.authenticated = True
            st.success("Authenticated")
        else:
            st.error("Authentication failed")

# ---- Voting ----
if st.session_state.authenticated:
    choice = st.radio(
        "Select candidate",
        list(CANDIDATES.keys()),
        format_func=lambda x: CANDIDATES[x]
    )

    if st.button("Cast vote"):
        VOTERS[name]["status"] = "voted"

        entry = {
            "voter_hash": hash_str(name),
            "candidate": choice,
            "candidate_commitment": CANDIDATE_COMMIT_HASH,
            "timestamp": time.time(),
            "prev_hash": LEDGER[-1]["hash"] if LEDGER else GENESIS_HASH,
        }
        entry["hash"] = hash_str(str(entry))
        LEDGER.append(entry)

        st.success("Vote recorded. Session terminated.")
        st.session_state.clear()
        st.stop()

# ---- Audit ----
st.markdown("---")
if st.checkbox("Show ledger (audit)"):
    st.json(LEDGER)
