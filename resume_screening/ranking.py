"""Rank candidates by score, then by name and filename."""


def rank_candidates(candidates):
    candidates.sort(key=lambda item: (
        -item["Score Breakdown"]["total"],
        item.get("Name", "").casefold(),
        item.get("Source Filename", "").casefold(),
    ))
    for rank, candidate in enumerate(candidates, start=1):
        candidate["Ranking"] = rank
        candidate["Match Score"] = candidate["Score Breakdown"]["total"]
    return candidates
