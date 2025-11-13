from __future__ import annotations

import json
from typing import Dict, List, Tuple, Literal

from .morph_engine import Generator, Lexeme, FeatureBundle


class ParadigmTableFormatter:
    """
    Utility class for formatting paradigm tables from morphology data.

    Handles automatic paradigm inference, label generation, and formatting
    in multiple output formats (pretty Unicode tables and JSON).
    """

    def __init__(self, generator: Generator, lexicon: Dict[str, Lexeme]) -> None:
        """
        Initialize the formatter with a generator and lexicon.

        Args:
            generator: The morphology generator with rules
            lexicon: Dictionary mapping lemma names to Lexeme objects
        """
        self._generator = generator
        self._lexicon = lexicon

    def format_table(
        self,
        feature_combinations: List[Tuple[str, FeatureBundle]],
        lexeme_subset: List[str] | None = None,
        format: Literal["pretty", "json"] = "pretty",
    ) -> str:
        """
        Generate a paradigm table with rules as column headers and lexemes as rows.

        Args:
            feature_combinations: List of (label, features) tuples for each column.
                                 Example: [("singular", {"num": "sg"}), ("plural", {"num": "pl"})]
            lexeme_subset: Optional list of lemma names to include. If None, includes all lexemes.
            format: Output format - "pretty" for human-readable Unicode table,
                   "json" for LLM-readable structured data.

        Returns:
            Formatted table string (pretty) or JSON string (json)
        """
        # Determine which lexemes to include
        if lexeme_subset is None:
            lexemes_to_show = list(self._lexicon.items())
        else:
            lexemes_to_show = [
                (name, lex)
                for name, lex in self._lexicon.items()
                if name in lexeme_subset
            ]

        if not lexemes_to_show or not feature_combinations:
            return (
                ""
                if format == "pretty"
                else json.dumps({"columns": [], "rows": [], "total_rows": 0})
            )

        # Build headers: ["Lemma", "Label1", "Label2", ...]
        headers = ["Lemma"] + [label for label, _ in feature_combinations]

        # Build rows
        rows = []
        for lemma_name, lexeme in lexemes_to_show:
            row = [lemma_name]
            for _, features in feature_combinations:
                try:
                    surface_form = self._generator.generate(lexeme, features)
                    row.append(surface_form)
                except Exception:
                    row.append("—")  # em-dash for error/unavailable
            rows.append(row)

        # Return JSON format if requested
        if format == "json":
            return self._format_as_json(headers, rows)

        # Otherwise return pretty Unicode table
        return self._format_as_pretty_table(headers, rows)

    def _format_as_json(self, headers: List[str], rows: List[List[str]]) -> str:
        """Format table data as JSON for LLM consumption"""
        columns = [
            {"name": header.lower().replace(" ", "_"), "type": "string"}
            for header in headers
        ]

        result = {"columns": columns, "rows": rows, "total_rows": len(rows)}

        return json.dumps(result, indent=2, ensure_ascii=False)

    def _format_as_pretty_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Format table data as pretty Unicode table for human reading"""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Build table with Unicode box-drawing
        lines = []

        # Top border
        lines.append("┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐")

        # Headers
        header_row = (
            "│"
            + "│".join(f" {h:<{col_widths[i]}} " for i, h in enumerate(headers))
            + "│"
        )
        lines.append(header_row)

        # Separator
        lines.append("├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤")

        # Data rows
        for row in rows:
            data_row = (
                "│"
                + "│".join(
                    f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)
                )
                + "│"
            )
            lines.append(data_row)

        # Bottom border
        lines.append("└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘")

        return "\n".join(lines)
