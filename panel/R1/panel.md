# R1 critic panel: Five Blocks

Inputs: `EVIDENCE.md`, 12 screenshots in `panel/shots/`, `site/css/blocks.css`, and the five topic sources in `_src/pages/`. One round, six seats. Each critic judges only what the evidence shows.

---

## Guy Debord (spectacle)

**Verdict: ship.**

There is no spectacle here: no coins, no rockets, no prices, no promise of wealth. The commodity form of crypto, the token as a lottery ticket, is named only to be refused ("It is not advice to buy, sell or hold any token"). The hash and the identicon are signs that do work: press Verify and they are recomputed in front of you. The site uses the vocabulary of Web3 (blockies, hex, chartreuse) to take apart the mystique, not to sell it. The one risk is that the blockie identicons and the acid-green accent are MetaMask's visual dialect. They are kept honest only because they are derived and checkable.

- *could:* on the home page, put one line next to the identicons saying they are derived from the block hash (for example in `.verify-out` before verification). Otherwise they read as decoration borrowed from wallet UIs.

## Viktor Shklovsky (estrangement)

**Verdict: ship with fixes.**

The device is alive. The reader expects a site *about* blockchains and finds a site that *is* one. Its own hashes are laid bare, and the reader can make it fail (the evidence shows block #1 flagged after tampering). This is estrangement in the proper sense: the familiar "page" becomes a datum with a fingerprint. Where it goes slack is the moment of recognition. After Verify, the result is a grey run-on sentence of truncated hashes (`home-verified-1440-light.png`: "…#4 15238c3606…" breaks onto a new line as "ddc754 ✓"). The climax of the device is set as small print.

- *should:* turn `.verify-out` into a per-block result (one row per block: `#n · hash · ✓/×`), and give the success state a clear heading line ("Chain intact: 5/5"). Stop hashes breaking mid-token (`overflow-wrap: anywhere` → keep `white-space: nowrap` per hash item).

## Steve Krug (usability)

**Verdict: ship with fixes.**

The home page passes the trunk test. Name, five numbered blocks, one obvious green button. The block pages have a "you are here" (underlined nav item, "BLOCK #0 OF 5", the ToC). Three things make me think:

1. *should:* before you verify, each card shows an empty grey circle (`.state`) with no label. That looks like an unchecked checkbox I am supposed to click. Give it an accessible and visible meaning: a `title`/`aria-label` of "not yet verified", or a dashed border with a "?" glyph.
2. *should:* at 390 px the nav (`.bnav`) scrolls sideways and is cut off at "Byzantin…" (`index-390-light.png`, `ethereum-390-dark.png`). Ethereum, Oracles and About are invisible, and only a fade hints at more. Either wrap the nav onto two rows at ≤720 px, or drop the `#n` prefixes and the long labels there (for example "Merkle · SMR · BFT · ETH · Oracles · About").
3. *could:* the "Prove record" radio D wraps alone onto its own line at 390 px (`lab-merkle-390-dark.png`). Put the legend on its own line above the four radios.

## Edward Tufte (labs and diagrams)

**Verdict: ship with fixes.**

The labs are honest. They compute real values, and the generals' dot row is a clean small multiple of honest and traitor. Two graphics fail at the level of the mark:

1. *must:* **Oracle lab, label collision.** In `lab-oracle-1440-light.png` the dashed red mean line runs through the word "median" (the median label sits at `left: 6px` and extends right into the mean line, 14 °C away). When the two statistics are close (the most important case), their labels overwrite each other. Fix: in `.or-nodes .mark:not(.mean) span`, anchor the median label to the *left* of its line (`left: auto; right: 6px`), and keep the mean label to the right. Or let JS flip a label to the left whenever the two marks are less than about 70 px apart.
2. *must:* **Merkle lab, the tree is not a tree.** There are no edges between levels, so "Proof" and "Path" are encoded only by fill and border, and at 390 px `.mk-row.l2` collapses to two columns (`@media (max-width:560px)`). Leaves C and D then sit under Leaf A and Leaf B (`lab-merkle-390-dark.png`), which visually asserts the wrong parentage. Fix: keep `.mk-row.l2` at 4 columns at every width (shrink `.hv` to about 6 characters plus the ellipsis), and draw parent–child connectors, for example a `::before` vertical tick on each node and a horizontal bracket under each `l1` and `l0` pair. Draw the path edges in `--ink` and the rest in `--rule`.
3. *could:* the record inputs (`.mk-leaves`, `auto-fit minmax(200px)`) give 3 + 1 at 1440 px, which orphans Record D. Use `repeat(4, minmax(0,1fr))` above 860 px and `repeat(2, …)` below, so the inputs line up with the four leaves beneath them.

## Distributed systems and cryptography reviewer

**Verdict: ship with fixes.** The core material is correct, and I checked it:

- the n ≥ 3f + 1 oral-messages bound, and that signed messages tolerate any number of traitors;
- the 2005 Dijkstra Prize going to the 1980 PSL paper;
- FLP in 1985;
- the quorum intersection 2(2f+1) − (3f+1) = f + 1;
- f + 1 matching replies;
- 20 sibling hashes × 32 B = 640 B for 2^20 ≥ 10^6 leaves;
- the RFC 6962 0x00/0x01 prefixes and the second-preimage explanation;
- the proof for A = {Leaf B, Hash CD};
- the EIP-1559 burn, 21,000 gas, and the ethereum.org worked example of 252,000 gwei;
- the Merge on 15 Sep 2022, London in Aug 2021, and launch on 30 Jul 2015;
- the 2017 Chainlink white paper authors, OCR in 2021, the DECO and Town Crier acquisitions, and LINK on ERC-677 with a supply of 1 billion;
- the median bound when fewer than half of the reports are faulty.

Wrong or imprecise sentences:

1. *must:* `byzantine-faults.html`: **"Blocks are finalised once validators holding two-thirds of the stake have voted for them"**. `ethereum.html`: **"A block is final once validators with two-thirds of the stake have voted for it: the Byzantine threshold from block #2."**
   Gasper (Casper FFG) finalises *epoch checkpoints*, not individual blocks by a single vote. Correction: "Every epoch (32 slots) has a checkpoint block. A checkpoint is *justified* when validators holding two-thirds of the staked ether vote for it. It becomes *final* when the next checkpoint is justified on top of it, usually after about two epochs (around 13 minutes). Every block before a final checkpoint is final too. Two-thirds is the 3f + 1 threshold again, measured in stake."
2. *must:* `byzantine-faults.html`, last paragraph: **"In both cases, the chain is state machine replication run by mutually distrusting replicas, which is the subject of the next block."**
   State machine replication is block #1, the *previous* block, and the next block is #3 (Ethereum). Correction: "In both cases, the chain is state machine replication (block #1) run by mutually distrusting replicas. The next block, Ethereum, is one such chain."
3. *should:* `ethereum.html`: **"Ethereum's electricity use fell by more than 99.98%, according to the estimate cited on ethereum.org."**
   ethereum.org's own pages state "~99.95%". The 99.988% figure is CCRI's. Either write "by about 99.95%, according to ethereum.org", or keep 99.98% and cite CCRI (2022) as the source. Do not attribute it to ethereum.org.

(*could, not must:* `fee = gas used × (base fee + priority fee)` omits the cap. The tip actually paid is min(max priority fee, max fee − base fee). One clause in the `.tip`/list under the formula would close this.)

## Robert Bringhurst (typography)

**Verdict: ship with fixes.**

The pairing works: a grotesque with a single-storey "y" for text, and a monospace for hashes, kickers and labels, letterspaced in small caps. The hero is set tight and confident. The measure in `.prose` (72ch) is right. The faults:

1. *must:* **The cards are not aligned.** In `index-1440-light.png`, card #3 "Ethereum" (a one-line title) sits about 4 px lower than its neighbours, and its HASH/PREV lines rise above theirs. "#3 The platform" in *Why this order* drops in the same way. The cause is `.blk a { display:grid; height:100% }` and `.path-list li { display:grid }`, whose implicit rows stretch to share the leftover height. Fix: `.blk a { align-content: start; grid-template-rows: auto auto 1fr auto auto; }` (so the summary absorbs the slack and the meta rows sit on a common bottom line), and `.path-list li { align-content: start; }`.
2. *should:* at 1440 px the five card summaries run to about 22 characters per line (`.blk-sum` inside a 5-column grid). That is a ragged, hyphen-hungry measure. Either cut each summary to two short lines' worth, or set `.blk-sum { font-size: .92rem; hyphens: auto; }` and `text-wrap: pretty`.
3. *could:* in `.verify-out`, monospace prose with ✓ glyphs and "·" separators is setting a table as a paragraph (see Shklovsky). Set it as a table or a list.

---

## Consensus

### Must-fix (deduplicated, at most 6)

1. **Card and step alignment (CSS).** Add `.blk a { align-content: start; grid-template-rows: auto auto 1fr auto auto; }` so titles align and the HASH/PREV rows share a bottom line. Add `.path-list li { align-content: start; }` so "#3 The platform" no longer drops.
2. **Oracle lab label collision (CSS/JS).** Anchor the median label to the left of its line (`.or-nodes .mark:not(.mean) span { left: auto; right: 6px; }`). Or flip a label in `blocks.js` when the median and mean marks are less than about 70 px apart. The word "median" must never be crossed by the mean line.
3. **Merkle lab keeps its tree shape (CSS/JS).** Remove the `@media (max-width:560px) .mk-row.l2 {2 columns}` rule so the leaves stay in 4 columns, and shorten `.hv` at narrow widths. Add parent–child connectors between `l2→l1→l0`, with path edges in `--ink`. Set `.mk-leaves` to 4 columns (2 below 860 px) so Record D is not orphaned.
4. **Verify result as a structured readout (JS + CSS).** Render `.verify-out` as a heading line ("Chain intact · 5/5 blocks", or the first failing block) plus one row per block (`#n  hash  ✓/×`). No hash may break mid-token.
5. **PoS finality wording (page HTML).** In `byzantine-faults.html` and `ethereum.html`, replace "blocks are finalised once two-thirds … voted" with the checkpoint-justification/finalisation sentence given by the technical reviewer.
6. **Two factual fixes (page HTML).** In `byzantine-faults.html`, change "…which is the subject of the next block" to "…state machine replication (block #1) run by mutually distrusting replicas. The next block, Ethereum, is one such chain." In `ethereum.html`, change "more than 99.98%, according to … ethereum.org" to "about 99.95%, according to ethereum.org" (or cite CCRI for 99.988%).

### Should, deferred (open items, not blocking)

- Mobile `.bnav`: wrap it or shorten the labels so all six destinations are visible at 390 px.
- Pre-verify `.state` circle: give it a label or glyph meaning "not yet verified".
- `.blk-sum` measure at 1440 px: shorten the summaries or add `hyphens: auto; text-wrap: pretty`.
- EIP-1559 tip cap: add one clause.
- Explain the identicon on the home page; put the D radio on its own line at 390 px.

### Convergence

The panel converged in one round. All six critics agree the concept and content are sound, and no one asked for a rework. Every must-fix is a concrete local defect visible in the evidence. A second round would only re-check these six fixes against fresh screenshots, so it would confirm rather than add anything. **Ship after the six fixes. No R2 is needed beyond a screenshot recheck.**
