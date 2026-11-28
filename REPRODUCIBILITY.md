# Reproduce the checks

From the repository root, using Python 3.9 or newer with the standard library:

    python3 -I verification/src/replay.py
    python3 -I scripts/verify_repository.py

The replay enumerates each projective point once and compares the ranks of the actual payoff coefficient jets with their exact double-base model. The log records the expected output. These checks diagnose the local algebra in the complex proof.

The repository verifier checks the manifest, SHA-256 ledger, archive member bytes and a text privacy screen. The PDF build and visualization instructions are in their respective directories. The archived paper is the version of record for this packet.

Run `python3 formal/closing/verify.py` with the versions pinned in `formal/closing/` to replay the partial Lean proof. [Declarations and scope](formal/closing/README.md)
