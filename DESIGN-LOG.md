# Design log: Web3 → Five Blocks (DADA-lite, Adaptive)

The previous version is kept on the branch `legacy-2026-10-30`: six loose research notes in JSON and YAML at the repo root.

## Brief
A full redesign of the same standard as the Coding Roadmap transit map, but not the same idea, and "more web3-y". The original notes are kept.

## Anchors
- **The block explorer.** Heights, hashes, previous-hash links and payload sizes, set in monospace.
- **Content addressing (Git, IPFS).** A thing's name is its hash, so the content is its own proof.
- **Ethereum blockies.** A per-identity pixel identicon drawn from a hash.
- **Neo-brutalist UI.** Hard 2 px borders, offset shadows and one acid accent, used only as a fill.

## Concept
The site *is* a hash chain.
- **Blocks:** each topic page is a block. Its hash is SHA-256 of the previous hash plus the exact bytes of the original notes it was written from (`site/data/`). Block #0 chains from 64 zeros.
- **Identicons:** each block carries an identicon drawn from its own hash.
- **Verification:** the home page recomputes the whole chain with Web Crypto, and the About page gives the one-line terminal command.
- **Order:** the five blocks form a learning path: integrity → replication → Byzantine agreement → Ethereum → oracles. Each block links back to the ideas it uses.

## Labs, one per idea
- SHA-256 playground.
- Merkle tree with RFC 6962 leaf and node prefixes and a highlighted proof path.
- Byzantine generals n ≥ 3f + 1.
- EIP-1559 fee calculator (ethereum.org's worked example).
- Oracle median versus mean with one lying node.

## Premortem (inline)
1. **The crypto-hype look.** No coins, rockets, gradients or prices; an "educational only" footer; and the identicons are the only imagery.
2. **Verification breaking on deploy because Git rewrote line endings.** `.gitattributes` marks `site/data/**` as `-text`, the payloads were restored byte-exact from the original blobs (`git hash-object` matches), and the build refuses a CR byte.
3. **Too dense for newcomers.** One idea per block, a "Why this order" path on the home page, and a lab on every page.

## BREAK move
The subject is also the structure: a reader can verify the chain they are reading, and tampering shows up (tested).

## Panel R1 (Debord, Shklovsky, Krug, Tufte, a distributed-systems and cryptography reviewer, Bringhurst)
Debord said "ship"; the other five said "ship with fixes". The full text is in `panel/R1/panel.md`.

| Must-fix | Resolution |
|---|---|
| Chain cards and the order steps were misaligned (grid rows stretching) | `align-content: start` and fixed row tracks |
| The oracle lab's mean line struck through the "median" label | The labels now sit on opposite sides of their lines |
| The Merkle lab didn't read as a tree; at 390 px the leaves wrapped under the wrong parents | Bracket edges are drawn between levels, leaves stay 4-up at every width, and the record inputs are 4-up (2-up under 860 px) |
| The Verify result was a run-on line that broke a hash | A heading line ("Chain intact · 5 of 5"), then one row per block with unbroken hashes; a failure names the block |
| PoS finality was described per block | Rewritten to describe checkpoints: justified at two-thirds of the stake, finalised when the next checkpoint is justified, usually about 13 minutes |
| A Byzantine page sentence pointed at the wrong block | It now links state machine replication (#1) and names Ethereum as the next block |

The panel also suggested changing the energy figure to "about 99.95%". **Not applied:** the live ethereum.org page cites CCRI's "more than 99.988%". The text keeps "more than 99.98%" and now names CCRI.

"Should" items that were done:
- The EIP-1559 tip cap is noted.
- The identicons are explained.
- The verify note explains the empty circles.
- The Merkle radios no longer orphan "D" on phones.

Open:
- The masthead's horizontal scroll strip on phones (with an edge fade) hides later items until you scroll; this is the same pattern as the other sites.
- Card summaries are narrow at 1440 px with five cards in a row.

## Measured after the last edit
- **Pages:** 8 pages × 2 widths × 2 colour schemes.
- **Horizontal overflow:** none.
- **AA contrast failures:** none.
- **Targets under 24 px:** only inline links inside sentences.
- **Behaviour in Chrome:**
  - The chain verifies 5 of 5, and block #0 equals `( printf '%064d' 0; cat site/data/MerkleTree.yaml ) | sha256sum`.
  - A tampered payload is flagged at the right block.
  - The Merkle root matches an independent Python RFC 6962 computation.
  - Generals, gas and oracle outputs are correct, with no script errors.
- **Chain tip:** `15238c3606d08555fbd6b2e8aeff68258d3db0da1f16381f33af3b93faddc754`.
