"""Defines the Rule class used for AST validation.

This module provides the structure for individual rules that consist of a
condition (predicate) and a consequence (action).
"""

import ast

from .types import Action, Predicate


class Rule:
    """Represents a single validation rule to be applied to AST nodes.

    A Rule encapsulates the logic for identifying a specific condition within
    an AST node (the predicate) and the side effect to execute when that
    condition is met (the action).

    Attributes:
        predicate (Predicate): A callable that evaluates an AST node and returns
            True if the rule criteria are met.
        action (Action): A callable that executes a side effect (e.g., raising
            an error) when the rule criteria are met.
        predicates (tuple[Predicate, ...]): A tuple containing the initialized
            predicate (and potentially others if extended).
        actions (tuple[Action, ...]): A tuple containing the initialized action
            (and potentially others if extended).
    """

    def __init__(self, predicate: Predicate, action: Action) -> None:
        """Initializes a Rule with a specific condition and action.

        Args:
            predicate: A callable that accepts an ast.AST node and returns
                a boolean indicating if the rule matches.
            action: A callable that accepts the matching ast.AST node and
                performs an action (e.g., logging or raising an error).
        """
        self.predicate: Predicate = predicate
        self.action: Action = action
        self.predicates: tuple[Predicate, ...] = (predicate,)
        self.actions: tuple[Action, ...] = (action,)

    def check_and_trigger(self, node: ast.AST) -> None:
        """Evaluates the rule against a specific node.

        Checks the node against the primary `predicate`. If it returns True,
        the primary `action` is executed immediately.

        Args:
            node: The AST node to evaluate.
        """
        if self.predicate(node):
            self.action(node)
