"""Helpers for normalizing uploaded text CSV files."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


TEXT_COLUMN_ALIASES = {
    "text",
    "tweet text",
    "tweet_text",
    "review",
    "review text",
    "review_text",
    "feedback",
    "comment",
    "content",
    "body",
}


@dataclass(frozen=True)
class TextSchema:
    text_column: str
    total_rows: int
    dropped_rows: int


def _normalize_column_name(column: object) -> str:
    return str(column).strip().lower().replace("_", " ")


def _find_text_column(columns: pd.Index) -> str | None:
    for column in columns:
        if _normalize_column_name(column) in TEXT_COLUMN_ALIASES:
            return str(column)
    return None


def _clean_text_series(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip()


def normalize_text_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, TextSchema]:
    """Return a dataframe with a canonical non-empty text column."""

    text_column = _find_text_column(df.columns)
    if text_column is None:
        raise ValueError(
            "CSV must include a text, review, feedback, comment, or Xquik Tweet Text column."
        )

    cleaned = _clean_text_series(df[text_column])
    normalized = pd.DataFrame({"text": cleaned})
    normalized = normalized[normalized["text"] != ""].reset_index(drop=True)
    if normalized.empty:
        raise ValueError("CSV text rows are empty. Add at least 1 non-empty row.")

    return normalized, TextSchema(
        text_column=text_column,
        total_rows=len(df),
        dropped_rows=len(df) - len(normalized),
    )


def split_manual_text(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]
