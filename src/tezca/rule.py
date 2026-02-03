"""Defines the Rule class used for AST validation.

This module provides the structure for individual rules that consist of a
condition (predicate) and a consequence (action).
"""

import ast
from collections.abc import Callable


class Rule:
    """Represents a single validation rule to be applied to AST nodes.

    A Rule encapsulates the logic for identifying a specific condition within
    an AST node (the predicate) and the side effect to execute when that
    condition is met (the action).

    Attributes:
        predicate: A function that takes an AST node and returns True if the
            rule should trigger, and False otherwise.
        action: A function that executes a side effect (usually raising a
            RuleError) when the predicate returns True.
    """

    def __init__(
        self, predicate: Callable[[ast.AST], bool], action: Callable[[ast.AST], None]
    ) -> None:
        """Initializes a Rule with a specific condition and action.

        Args:
            predicate: A callable that accepts an ast.AST node and returns
                a boolean indicating if the rule matches.
            action: A callable that accepts the matching ast.AST node and
                performs an action (e.g., logging or raising an error).
        """
        self.predicate = predicate
        self.action = action

    def check_and_trigger(self, node: ast.AST) -> None:
        """Evaluates the rule against a specific node.

        If the predicate function returns True for the given node, the
        action function is immediately executed.

        Args:
            node: The AST node to evaluate.
        """
        if self.predicate(node):
            self.action(node)
