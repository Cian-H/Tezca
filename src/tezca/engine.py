"""A module for enforcing rules on Abstract Syntax Trees (AST).

This module provides the RuleEngine class, which extends the standard
ast.NodeVisitor to apply a set of validation or transformation rules
during the traversal of an AST.
"""

import ast

from .rule import Rule


class RuleEngine(ast.NodeVisitor):
    """Orchestrates the application of rules during AST traversal.

    This class visits nodes in an Abstract Syntax Tree and applies a provided
    list of rules to each node. It ensures that every rule has the opportunity
    to inspect every visited node.

    Attributes:
        rules: A list of Rule objects that will be applied to the AST nodes.
    """

    def __init__(self, rules: list[Rule]) -> None:
        """Initializes the RuleEngine with a specific set of rules.

        Args:
            rules: A list of Rule instances to be checked against nodes
                during the traversal.
        """
        self.rules = rules

    def visit(self, node: ast.AST) -> None:
        """Visits a node and applies all registered rules.

        This method iterates through all stored rules, triggering their
        check logic on the current node. After checking the rules, it
        continues the traversal to the node's children via generic_visit.

        Args:
            node: The AST node currently being visited.
        """
        for rule in self.rules:
            rule.check_and_trigger(node)
        self.generic_visit(node)
