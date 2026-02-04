"""Defines the RuleSet composite class for AST validation.

This module provides the RuleSet class, which aggregates multiple Rule instances
into a single entity. It allows for the collective management and execution of
distinct validation rules while maintaining a unified interface.
"""

import ast
import itertools

from .rule import Rule
from .types import Action, Predicate


class RuleSet(Rule):
    """A composite Rule that encapsulates and manages multiple individual rules.

    This class aggregates a collection of Rule objects. While it appears as a
    single Rule to the outside world, it maintains the distinct logic of each
    internal rule.

    Attributes:
        predicate (Predicate): The combined predicate (inherited from Rule).
            Returns True if ANY of the internal rules match.
        action (Action): The combined action (inherited from Rule).
            Executes ALL internal actions sequentially if triggered directly.
        predicates (tuple[Predicate, ...]): A flattened tuple of all predicates
            from the contained rules.
        actions (tuple[Action, ...]): A flattened tuple of all actions from the
            contained rules.
    """

    __last_rule_state: tuple[tuple[Predicate, ...], tuple[Action, ...]] = (tuple(), tuple())
    __handlers: dict[Predicate, Action] = dict()

    def __init__(self, rules: list[Rule]) -> None:
        """Initializes a RuleSet by flattening specific logic from a list of Rules.

        This sets up the parent Rule class with a "combined" behavior (any predicate
        triggers, all actions run) for interface compatibility, while storing the
        individual components for granular execution in `check_and_trigger`.

        Args:
            rules: A list of Rule instances to include in this set.
        """
        predicates: tuple[Predicate, ...] = tuple(
            itertools.chain.from_iterable(r.predicates for r in rules)
        )
        actions: tuple[Action, ...] = tuple(itertools.chain.from_iterable(r.actions for r in rules))
        predicate: Predicate = self._create_combined_predicate(predicates)
        action: Action = self._create_combined_action(actions)
        super().__init__(predicate, action)
        self.predicates = predicates
        self.actions = actions

    @staticmethod
    def _create_combined_predicate(predicates: tuple[Predicate, ...]) -> Predicate:
        """Creates a single predicate that returns True if ANY internal predicate matches.

        Args:
            predicates: A tuple of predicate functions.

        Returns:
            A new predicate function acting as a logical OR across the input tuple.
        """

        def predicate(node: ast.AST) -> bool:
            return any(p(node) for p in predicates)

        return predicate

    @staticmethod
    def _create_combined_action(actions: tuple[Action, ...]) -> Action:
        """Creates a single action that executes ALL internal actions sequentially.

        Args:
            actions: A tuple of action functions.

        Returns:
            A new action function that iterates through and runs every action.
        """

        def action(node: ast.AST) -> None:
            [f(node) for f in actions]

        return action

    @property
    def handlers(self) -> dict[Predicate, Action]:
        """Returns a memoized dictionary mapping actions to predicates."""
        cur_state = (self.predicates, self.actions)
        if cur_state != self.__last_rule_state:
            self.__last_rule_state = cur_state
            self.__handlers = dict(zip(self.predicates, self.actions, strict=True))
        return self.__handlers

    def check_and_trigger(self, node: ast.AST) -> None:
        """Evaluates each internal rule individually against the node.

        Unlike the standard Rule execution (which might trigger one action based on
        one predicate), this iterates through all internal predicate/action pairs.
        For every predicate that returns True, the specific corresponding action
        is executed.

        Args:
            node: The AST node to evaluate.
        """
        handlers = self.handlers
        for predicate in handlers:
            if predicate(node):
                handlers[predicate](node)
