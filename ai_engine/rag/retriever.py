import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class EduMorphRetriever:
    """
    Lightweight local RAG retriever.

    Sentence Transformer -> embeddings
    FAISS -> similarity search
    """

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def build_index(self, chunks):
        if not chunks:
            raise ValueError("No chunks provided.")

        self.chunks = chunks

        embeddings = self.embedding_model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def retrieve(self, query, top_k=3):
        if self.index is None:
            raise RuntimeError(
                "Index has not been built yet."
            )

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.chunks))
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            results.append({
                "chunk": self.chunks[index],
                "score": float(score)
            })

        return results