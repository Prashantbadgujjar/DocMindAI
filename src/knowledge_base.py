
from dataclasses import dataclass

import faiss
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    text: str
    source: str
    location: str
    score: float = 0.0


class KnowledgeBase:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.chunks = []
        self.index = None

    def build(self, blocks):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200
        )

        texts = []

        for block in blocks:

            split_chunks = splitter.split_text(block.text)

            for chunk_text in split_chunks:

                if len(chunk_text.strip()) < 20:
                    continue

                chunk = Chunk(
                    text=chunk_text,
                    source=block.source,
                    location=block.location
                )

                self.chunks.append(chunk)

                texts.append(chunk_text)

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)

        self.index.add(
            embeddings.astype("float32")
        )

        return {
            "chunks": len(self.chunks)
        }

    def search(self, query, top_k=2):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k
        )

        results = []

        for dist, idx in zip(distances[0], indices[0]):

            chunk = self.chunks[idx]
            chunk.score = float(1 / (1 + dist))

            results.append(chunk)

        return results
