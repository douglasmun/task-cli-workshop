"""
Lab A — Minimum Viable RAG Pipeline

Goal: build a retrieval pipeline over the cybersecurity documents in
lab-a-samples/. When complete, querying "What CVEs are mentioned?"
should return chunks from the advisory documents, not the runbooks.

Dependencies (install before starting):
    pip install sentence-transformers numpy

Run from the repo root:
    python labs/lab-a-skeleton/rag_skeleton.py

Expected output (exact text varies by chunking strategy):
    Query: What CVEs are mentioned?
    [1] ...chunk containing CVE-2025-38471 or CVE-2026-1847...
    [2] ...second CVE-related chunk...

    Query: How should analysts respond to a ransomware alert?
    [1] ...chunk from the SOC ransomware runbook...
    [2] ...second relevant runbook chunk...
"""

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Step 1 — Load documents
# ---------------------------------------------------------------------------

def load_documents(docs_dir: str) -> list[dict[str, str]]:
    """Read every .txt file in docs_dir and return a list of document dicts.

    Args:
        docs_dir: Path to the directory containing .txt sample files.
                  Relative to the current working directory, e.g.
                  "labs/lab-a-samples".

    Returns:
        A list of dicts, one per file, each with exactly two keys:
          - "filename": the bare filename, e.g. "doc01_cve_django_auth_bypass.txt"
          - "text":     the full UTF-8 contents of the file

    Example:
        >>> docs = load_documents("labs/lab-a-samples")
        >>> len(docs)
        10
        >>> docs[0].keys()
        dict_keys(['filename', 'text'])
        >>> "CVE-2025-38471" in docs[0]["text"]
        True

    Implementation hint:
        Use pathlib.Path(docs_dir).glob("*.txt") to iterate. Read each
        file with Path.read_text(encoding="utf-8").
    """
    # TODO: iterate over *.txt files in docs_dir
    # TODO: for each file, append {"filename": file.name, "text": file.read_text(...)}
    # TODO: return the list
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 2 — Chunk documents
# ---------------------------------------------------------------------------

def chunk_document(doc: dict[str, str], chunk_size: int = 300) -> list[str]:
    """Split doc["text"] into overlapping word-boundary chunks.

    A retrieval system works better when chunks are small enough to be
    topically focused (not the whole document) but large enough to provide
    context for a language model. 200–400 characters is a practical range
    for these short advisory documents.

    Args:
        doc:        A dict with at least a "text" key (output of load_documents).
        chunk_size: Target character length per chunk. Chunks should not split
                    in the middle of a word. A 20% overlap between consecutive
                    chunks helps avoid cutting relevant content at boundaries.

    Returns:
        A list of non-empty chunk strings. For a 300-character chunk_size
        on a 900-character document you should get roughly 4–5 chunks
        (depending on overlap).

    Example:
        >>> doc = {"filename": "test.txt", "text": "word " * 200}
        >>> chunks = chunk_document(doc, chunk_size=100)
        >>> all(len(c) <= 130 for c in chunks)   # allow some overshoot for word boundaries
        True
        >>> len(chunks) > 3
        True

    Implementation hint:
        Split on whitespace to get words. Walk forward by chunk_size characters
        worth of words. For overlap, back up by ~20% before starting the next
        chunk. Filter out any empty strings before returning.
    """
    # TODO: split doc["text"] into word tokens
    # TODO: accumulate tokens until chunk_size characters are reached
    # TODO: step forward by (chunk_size * 0.8) characters for the next chunk start
    # TODO: return the list of chunk strings
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 3 — Embed chunks
# ---------------------------------------------------------------------------

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Convert a list of text chunks into a list of embedding vectors.

    Uses the SentenceTransformer "all-MiniLM-L6-v2" model, which produces
    384-dimensional vectors and runs on CPU in reasonable time.

    Args:
        chunks: A list of text strings (output of chunk_document calls).

    Returns:
        A list of float vectors in the same order as the input. Each vector
        has 384 elements. The return type is a plain Python list of lists —
        not a numpy array — so it can be stored and compared without numpy
        as a hard dependency in later steps.

    Example:
        >>> vecs = embed_chunks(["ransomware encrypts files"])
        >>> len(vecs)
        1
        >>> len(vecs[0])
        384
        >>> isinstance(vecs[0][0], float)
        True

    Implementation hint:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        raw = model.encode(chunks)          # returns a numpy array
        return raw.tolist()                 # convert to plain Python list
    """
    # TODO: load SentenceTransformer("all-MiniLM-L6-v2")
    # TODO: call model.encode(chunks) — this batches all chunks in one pass
    # TODO: convert the numpy result to a Python list of lists with .tolist()
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Step 4 — Retrieve relevant chunks
# ---------------------------------------------------------------------------

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Return the cosine similarity between two equal-length float vectors.

    Cosine similarity = dot(a, b) / (|a| * |b|). Returns a value in [-1, 1]
    where 1 means identical direction and 0 means orthogonal.

    Args:
        vec_a: A float vector.
        vec_b: A float vector of the same length as vec_a.

    Returns:
        A float in the range [-1.0, 1.0].

    Example:
        >>> v = [1.0, 0.0, 0.0]
        >>> cosine_similarity(v, v)
        1.0
        >>> cosine_similarity([1.0, 0.0], [0.0, 1.0])
        0.0

    Implementation hint:
        dot  = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = sum(x ** 2 for x in vec_a) ** 0.5
        norm_b = sum(x ** 2 for x in vec_b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    Note: you may also use numpy if you prefer — import is already available
    from embed_chunks. Both approaches are acceptable.
    """
    # TODO: compute dot product
    # TODO: compute L2 norms of each vector
    # TODO: return dot / (norm_a * norm_b), guarding against zero division
    raise NotImplementedError


def retrieve(
    query: str,
    chunks: list[str],
    embeddings: list[list[float]],
    top_k: int = 3,
) -> list[tuple[float, str]]:
    """Return the top_k most semantically relevant chunks for a query.

    Args:
        query:      The natural-language question to answer.
        chunks:     The full list of text chunks (parallel to embeddings).
        embeddings: Pre-computed embeddings, one per chunk (output of embed_chunks).
        top_k:      How many results to return.

    Returns:
        A list of (score, chunk_text) tuples sorted by descending score,
        length min(top_k, len(chunks)).

    Example:
        >>> # With real embeddings, a CVE query should rank CVE docs highest
        >>> results = retrieve("What CVEs are mentioned?", chunks, embeddings, top_k=2)
        >>> len(results)
        2
        >>> all(isinstance(score, float) for score, _ in results)
        True
        >>> results[0][0] >= results[1][0]   # sorted descending
        True

    Implementation hint:
        1. Embed the query: embed_chunks([query])[0]
        2. Score each chunk: cosine_similarity(query_vec, chunk_emb)
        3. Zip scores with chunks, sort by score descending, slice to top_k
    """
    # TODO: embed the query using embed_chunks (reuse the same model call pattern)
    # TODO: compute cosine_similarity between the query vector and each stored embedding
    # TODO: pair each score with its chunk string
    # TODO: sort descending by score and return the top_k pairs
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Main — run two sample queries
# ---------------------------------------------------------------------------

def main() -> None:
    docs_dir = "labs/lab-a-samples"

    print("Loading documents...")
    docs = load_documents(docs_dir)
    print(f"  Loaded {len(docs)} documents")

    print("Chunking...")
    all_chunks: list[str] = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))
    print(f"  {len(all_chunks)} chunks total")

    print("Embedding (this may take 30–60 s on first run)...")
    all_embeddings = embed_chunks(all_chunks)
    print(f"  Embedding shape: {len(all_embeddings)} x {len(all_embeddings[0])}")

    queries = [
        "What CVEs are mentioned and what are their CVSS scores?",
        "How should analysts respond to a ransomware alert?",
        "Which threat actors targeted financial institutions in Southeast Asia?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        results = retrieve(query, all_chunks, all_embeddings, top_k=2)
        for rank, (score, chunk) in enumerate(results, 1):
            preview = chunk[:120].replace("\n", " ")
            print(f"  [{rank}] score={score:.3f}  {preview}...")


if __name__ == "__main__":
    main()
