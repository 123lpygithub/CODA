"""Deterministic lexical-semantic retrieval for retrospective impact checks."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass


_TOKEN_PATTERN = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


@dataclass(frozen=True)
class SemanticMatch:
    document_id: str
    score: float
    shared_terms: tuple[str, ...]


def _tokens(text: str) -> list[str]:
    return [token.casefold() for token in _TOKEN_PATTERN.findall(text) if len(token) > 1]


def rank_semantic_impacts(
    query: str,
    documents: dict[str, str],
    *,
    top_k: int,
    minimum_score: float,
) -> list[SemanticMatch]:
    """Rank historical records by IDF-weighted lexical overlap.

    This baseline is local, reproducible, and provider independent. An embedding
    retriever can later implement the same return contract.
    """

    if top_k <= 0 or not documents:
        return []
    query_counts = Counter(_tokens(query))
    if not query_counts:
        return []
    document_tokens = {key: _tokens(value) for key, value in documents.items()}
    document_frequency = Counter(
        token for tokens in document_tokens.values() for token in set(tokens)
    )
    document_count = len(document_tokens)
    query_weights = {
        token: count * (math.log((document_count + 1) / (document_frequency[token] + 1)) + 1)
        for token, count in query_counts.items()
    }
    query_norm = math.sqrt(sum(weight * weight for weight in query_weights.values()))
    matches: list[SemanticMatch] = []
    for document_id, tokens in document_tokens.items():
        counts = Counter(tokens)
        shared = set(query_weights).intersection(counts)
        if not shared:
            continue
        document_weights = {
            token: count * (math.log((document_count + 1) / (document_frequency[token] + 1)) + 1)
            for token, count in counts.items()
        }
        document_norm = math.sqrt(
            sum(weight * weight for weight in document_weights.values())
        )
        numerator = sum(query_weights[token] * document_weights[token] for token in shared)
        score = numerator / max(query_norm * document_norm, 1e-12)
        if score >= minimum_score:
            matches.append(
                SemanticMatch(
                    document_id=document_id,
                    score=score,
                    shared_terms=tuple(sorted(shared)[:12]),
                )
            )
    return sorted(matches, key=lambda match: (-match.score, match.document_id))[:top_k]
