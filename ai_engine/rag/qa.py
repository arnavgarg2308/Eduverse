from ai_engine.core.model import EduMorphModel
from ai_engine.rag.retriever import EduMorphRetriever


class EduMorphRAG:
    """
    Retrieval-Augmented Educational Generation.

    FAISS retrieves relevant document content.
    FLAN-T5 converts the retrieved content into
    a student-friendly explanation.
    """

    def __init__(self, model: EduMorphModel):
        self.model = model
        self.retriever = EduMorphRetriever()

    def add_document(self, chunks):
        self.retriever.build_index(chunks)

    def answer(
        self,
        query: str,
        education_level: str = "Grade 9",
        top_k: int = 3
    ) -> dict:

        retrieved = self.retriever.retrieve(
            query,
            top_k=top_k
        )

        context = "\n\n".join(
            item["chunk"]
            for item in retrieved
        )

        prompt = f"""
Answer the student's question using ONLY the retrieved educational content.

Education level:
{education_level}

Retrieved educational content:
{context}

Student question:
{query}

Give a clear and simple answer.
Do not invent information that is not present in the retrieved content.

Answer:
"""

        answer = self.model.generate(
            prompt,
            max_new_tokens=150
        )

        return {
            "question": query,
            "answer": answer,
            "sources": retrieved
        }