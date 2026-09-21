from app.rag.ingest import build_index


count = build_index()

print(
    f"Index created. "
    f"Chunks: {count}"
)