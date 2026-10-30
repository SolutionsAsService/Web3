# R1 evidence: Web3 → "Five Blocks: Web3 from first principles"

Site: `H:/UBM/_web3/site` (8 pages: index, merkle-trees, state-machine-replication, byzantine-faults, ethereum, chainlink, about, 404).
Source: `_src/build.py`, `_src/blocks.json`, `_src/pages/*.html`; CSS `site/css/blocks.css`; JS `site/js/blocks.js`.
Screenshots: `H:/UBM/_web3/panel/shots/<page>-<1440|390>-<light|dark>.png`, plus lab close-ups: `lab-merkle-*`, `lab-oracle-*`, `lab-generals-*` and `home-verified-*` (after pressing Verify).

Brief from the user: a DADA redesign as good as the Coding Roadmap site (a transit-map visualisation), but not the same, and "more web3-y". The repo held five research notes (JSON and YAML), and these must be kept.

Concept: the site is a real hash chain.
- **Blocks:** each topic page is a block whose hash is SHA-256(previous hash ‖ exact bytes of its original notes); block #0's previous hash is 64 zeros.
- **Identicons:** each block shows a blockie-style identicon derived from its own hash.
- **Verify:** the home page "Verify" button refetches the payloads and recomputes the chain with Web Crypto.
- **Order:** the learning path is integrity → replication → Byzantine agreement → Ethereum → oracles.

Labs: SHA-256 playground, Merkle tree with RFC 6962 domain separation and proof path, Byzantine generals n ≥ 3f+1, EIP-1559 fee calculator, and an oracle median-versus-mean demo.

Measured after the last edit (32 runs, 8 pages × 2 widths × 2 schemes):
- No horizontal overflow and no AA contrast failures.
- Small targets: inline links in sentences only, plus the header-card previous-hash link, which was then padded to 28 px.

Behaviour test in Chrome:
- Chain verification passes. The block #0 hash equals the CLI `( printf '%064d' 0; cat site/data/MerkleTree.yaml ) | sha256sum`.
- With one payload tampered, block #1 is flagged.
- The Merkle root equals an independent Python RFC 6962 computation.
- Generals (n=4, f=2) correctly fails, and gas 65,000 × (12.5 + 1.5) = 910,000 gwei.
- Oracle: median 21.4 versus mean 39.8 with one liar at 150.
- No script errors.

Content: rewritten and sourced to primary papers (Lamport/Shostak/Pease, Schneider, Castro and Liskov, RFC 6962, ethereum.org and EIPs, Chainlink white papers). About lists the corrections to the notes. The site gives no investment advice and shows no prices.

Inline premortem:
1. Crypto-hype aesthetic (neon gradients, coins, rockets): no imagery; the only "graphics" are hashes, identicons and lab diagrams.
2. Verification that breaks on deploy because of line endings: `.gitattributes -text` plus a build assertion against CR.
3. Too dense for newcomers: one idea per block, with each block linking back to the earlier ones.

BREAK move: the site's own structure is the subject. You can verify the chain you are reading.
