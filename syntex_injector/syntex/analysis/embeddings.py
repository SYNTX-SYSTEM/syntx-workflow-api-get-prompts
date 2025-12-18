"""
SYNTX Semantic Embeddings - Sentence Transformers mit Caching
"""

import os
import logging
from typing import Optional, List, Tuple
from functools import lru_cache

import numpy as np

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SYNTX.Embeddings")

# Model wird lazy geladen
_model = None
_model_name = None

def _get_model():
    """Lazy Load des Sentence Transformer Models"""
    global _model, _model_name
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Multilingual für Deutsch!
            _model_name = os.getenv("SYNTX_EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
            logger.info(f"Loading embedding model: {_model_name}")
            _model = SentenceTransformer(_model_name)
            logger.info("✅ Embedding model loaded")
        except ImportError:
            logger.error("❌ sentence-transformers not installed!")
            logger.error("   Run: pip install sentence-transformers")
            _model = None
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            _model = None
    return _model


def get_embedding(text: str) -> Optional[np.ndarray]:
    """Berechnet Embedding für einen Text"""
    model = _get_model()
    if model is None or not text or not text.strip():
        return None
    try:
        return model.encode(text, convert_to_numpy=True)
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        return None

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Berechnet Cosine Similarity zwischen zwei Vektoren"""
    if vec1 is None or vec2 is None:
        return 0.0
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))

def semantic_similarity(text1: str, text2: str) -> float:
    """Berechnet semantische Ähnlichkeit zwischen zwei Texten (0.0 - 1.0)"""
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    if emb1 is None or emb2 is None:
        return 0.0
    sim = cosine_similarity(emb1, emb2)
    return max(0.0, min(1.0, sim))

def batch_similarity(text: str, references: List[str]) -> float:
    """Berechnet durchschnittliche Similarity gegen mehrere Referenzen"""
    if not references:
        return 0.0
    scores = [semantic_similarity(text, ref) for ref in references]
    return sum(scores) / len(scores)

def keyword_coverage(text: str, keywords: List[str]) -> float:
    """Berechnet wie viele Keywords im Text vorkommen (0.0 - 1.0)"""
    if not keywords or not text:
        return 0.0
    text_lower = text.lower()
    found = sum(1 for kw in keywords if kw.lower() in text_lower)
    return found / len(keywords)

if __name__ == "__main__":
    print("=== SYNTX EMBEDDINGS TEST ===")
    t1 = "Der Driftkörper analysiert die fundamentale Struktur des Systems."
    t2 = "Die Analyse der Kernstruktur zeigt tiefe Zusammenhänge."
    t3 = "Ich mag Pizza und Bier."
    sim12 = semantic_similarity(t1, t2)
    sim13 = semantic_similarity(t1, t3)
    print(f"Similarity (related): {sim12:.3f}")
    print(f"Similarity (unrelated): {sim13:.3f}")
    print("✅ Embeddings OK" if sim12 > sim13 else "❌ Test failed")
