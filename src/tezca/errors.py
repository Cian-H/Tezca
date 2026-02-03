"""Exception classes for the AST rule engine.

This module provides specific exceptions used to report violations found
during AST traversal and rule checking.
"""

import ast


class RuleError(Exception):
    """An exception raised when a rule violation occurs.

    This exception automatically extracts location information (line number
    and column offset) from the provided AST node, if available, and
    prepends it to the error message for better debugging.

    Attributes:
        node: The AST node associated with the violation, if any.
        lineno: The line number where the violation occurred, or None.
        col_offset: The column offset where the violation occurred, or None.
    """

    def __init__(self, message: str, node: ast.AST | None = None) -> None:
        """Initializes the RuleError with a message and optional AST context.

        If a node is provided, the error message is formatted to include the
        line number and column offset (e.g., "Line 10, Col 4: Error message").

        Args:
            message: A human-readable description of the rule violation.
            node: The AST node where the violation was detected. Defaults to None.
        """
        self.node = node
        self.lineno = getattr(node, "lineno", None) if node else None
        self.col_offset = getattr(node, "col_offset", None) if node else None
        formatted_message = message
        if self.lineno is not None:
            location_info = f"Line {self.lineno}"
            if self.col_offset is not None:
                location_info += f", Col {self.col_offset}"
            formatted_message = f"{location_info}: {message}"

        super().__init__(formatted_message)
