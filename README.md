# Five Blocks

Web3 from first principles, in five linked pages:

0. Hashes and Merkle trees
1. State machine replication
2. Byzantine faults and agreement
3. Ethereum
4. Chainlink and oracles

The site is itself a hash chain. Each page is a block whose hash is `SHA-256(previous hash ‖ source files)`. The source files are this repository's original research notes, kept byte for byte in `site/data/` (and in `docs/`). The home page can recompute the whole chain in your browser. From a terminal, block #0 is:

```bash
( printf '%064d' 0; cat site/data/MerkleTree.yaml ) | sha256sum
```

Each page also has a small lab: a SHA-256 playground, a Merkle tree with inclusion proofs, a Byzantine generals calculator, an EIP-1559 fee calculator and an oracle median demo.

Educational only. Nothing here is investment, legal or tax advice.

## Layout

```
_src/
  blocks.json         # chain order, titles and each block's payload files
  pages/*.html        # one body per page (front matter, then HTML)
  layout.html         # shared masthead and footer
  build.py            # computes the chain and writes site/ (standard-library Python)
site/                 # the deployable static site (committed)
  data/               # block payloads: the original notes, byte for byte
  css/blocks.css
  js/blocks.js        # chain verification and the labs (Web Crypto)
  favicon.svg
docs/                 # the original notes, unchanged
index.html            # redirects to site/
vercel.json           # static deploy config (root and site/)
```

## Editing

```bash
python _src/build.py
```

The build recomputes every hash. It stops on a dead local link, a duplicate id, a broken in-page anchor, or a payload with Windows line endings (`.gitattributes` keeps `site/data/` byte-exact). Commit the rebuilt `site/`.

To add a topic, put its notes in `site/data/`, add a block at the end of `_src/blocks.json`, and write `_src/pages/<slug>.html`. Changing an earlier payload changes every later hash, which is the point.

## Deploying

The repo deploys as a plain static site on Vercel or Shadw with no build step. `vercel.json` serves `site/` whether the root directory is blank or set to `site`. There is no root `package.json` or framework config.

## Contributing and licence

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed; see [LICENSE](LICENSE).
