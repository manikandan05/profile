# Manikandan M profile site

Static landing page for a software architect focused on data security and compliance. No build step is needed to host it.

## Deploy to GitHub Pages

1. Create a public repository named `manikandan05.github.io` under your GitHub account.
2. Copy the contents of this folder into the repository root (`about_me.html`, `styles.css`, `script.js`, `assets/`, and the other pages).
3. Push to `main`, then open Settings, Pages, and choose "Deploy from a branch", `main`, `/ (root)`.

Your existing timeline stays at `/profile` if it lives in its own repository named `profile`.

## Editing content

Copy lives in `tools/build.py`. After editing, run `python3 tools/build.py` to regenerate `about_me.html`, `404.html`, `privacy.html` and `terms.html`. `tools/og.html` is the source for `assets/og.png`.

## Licenses

Geist fonts (SIL OFL) and Phosphor icons (MIT) are bundled locally. License files are in `assets/fonts/`.
