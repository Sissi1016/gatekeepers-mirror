Raw inputs are not committed. Each file is downloaded once by `code/01_download.py`, with a
user-agent that identifies this project, and cached locally; the script records source URL,
license, download date, size and SHA-256 in `data/raw/MANIFEST.json`.

Sources used by the ICLR prototype:
- berenslab/iclr-dataset (`iclr26v1.parquet`, MIT): ICLR 2017–2026 submissions with title, abstract,
  authors, decision, reviewer scores, keywords, label.
- Samarth0710/reviewarena on Hugging Face (CC BY 4.0): reviews, meta-reviews, rebuttals and OCR full text
  for ICLR 2020–2026 (used only where the prototype needs review text).
- OpenAlex API (CC0 metadata): later publication and citation counts for matched titles.
