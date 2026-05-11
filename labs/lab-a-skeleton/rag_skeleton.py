# Lab A Skeleton — fill in the TODOs to complete the minimum viable lab

# Imports — fill these in:
# from sentence_transformers import SentenceTransformer
# import json
# from pathlib import Path


def load_documents(docs_dir: str) -> list[dict]:
    """Load all .txt files from docs_dir.

    Returns a list of dicts, each with keys:
      - "filename": str  (just the file name, not the full path)
      - "text": str      (full file contents)

    Example return value:
      [{"filename": "doc1.txt", "text": "Security Advisory SA-2026-001 ..."}]
    """
    # TODO: use pathlib.Path to iterate over *.txt files in docs_dir
    # TODO: read each file and append {"filename": ..., "text": ...} to a list
    pass


def chunk_document(doc: dict, chunk_size: int = 200) -> list[str]:
    """Split doc["text"] into overlapping chunks of roughly chunk_size characters.

    Returns a list of strings. Each chunk should preserve whole words where
    possible. A simple sliding window is fine for the minimum viable version.
    """
    # TODO: split doc["text"] into chunks
    pass


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Embed each chunk string into a fixed-length float vector.

    Returns a list of vectors in the same order as the input chunks.
    Use SentenceTransformer("all-MiniLM-L6-v2") or any compatible model.
    """
    # TODO: load a SentenceTransformer model and call model.encode(chunks)
    # TODO: return the embeddings as a plain list of lists (not numpy arrays)
    pass


def retrieve(
    query: str,
    chunks: list[str],
    embeddings: list[list[float]],
    top_k: int = 2,
) -> list[str]:
    """Return the top_k most relevant chunks for the query.

    Args:
        query:      The user question.
        chunks:     The full list of text chunks.
        embeddings: Pre-computed embeddings aligned with chunks.
        top_k:      Number of results to return.

    Returns:
        A list of up to top_k chunk strings, ranked by relevance.
    """
    # TODO: embed the query using the same model used in embed_chunks
    # TODO: compute cosine similarity between query embedding and all chunk embeddings
    # TODO: return the top_k chunks sorted by descending similarity score
    pass


def main():
    docs = load_documents("labs/lab-a-samples")
    # TODO: chunk each document — call chunk_document for every doc in docs
    all_chunks = []

    # TODO: embed all chunks — call embed_chunks(all_chunks)
    all_embeddings = []

    query = "What CVEs are mentioned?"
    results = retrieve(query, all_chunks, all_embeddings, top_k=2)
    for i, r in enumerate(results):
        print(f"[{i+1}] {r}")


if __name__ == "__main__":
    main()


# Expected output (exact text will vary by chunking strategy):
# [1] ...text mentioning CVE-2026-... or a patch advisory...
# [2] ...second most relevant chunk about a vulnerability or advisory...
