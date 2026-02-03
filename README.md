# Tezca - The Serpent's Venerable Enemy

<a href="https://commons.wikimedia.org/wiki/File:Codex_F%C3%A9jervary-Mayer_Lamina_01.svg">
  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2e/Codex_F%C3%A9jervary-Mayer_Lamina_01.svg" width="512" alt="Plate 01 from Féjervary-Mayer">
</a>

## Overview

Tezca is a library designed to selectively disable certain features of the python programming
language. The module provides objects that can be used to compose `Ruleset`s, that can then be
invoked to restrict or change the behaviour of the interpreter. This can be useful for:

- Disabling dangerous language features
- Hard enforcement of a specific code style
- Code auditing
- Educational exercises

## How Does it Work?

The various components of the module are used to construct a composite object called a `Ruleset`.
`Ruleset`s are composites that contain a `List[Ruleset|Rule]`, forming a recursive tree of `Rule`s.
Invoking the `RuleEngine` with a `Rule` or `Ruleset` causes the engine to scan the AST for rule
violations and trigger their associated action if any are found. The package also provides hooks
that can ne injected into the interpreter as an audit hook (see
[PEP 578](https://peps.python.org/pep-0578/)). Once the hook has been injected with a ruleset by
calling `monitor_repl`, it will check any new AST nodes compiled and trigger the action associated
with those rules if any are found to be violated. `Rule` actions are simple functions passed to
the `Rule` constructor, that will be executed if a node that violates thr `Rule`s predicate
function is found.

## Example

```python
import ast
from tezca import Rule, RuleError monitor_repl
from tezca.errors import RuleError

def is_import_os(node):
    return isinstance(node, ast.Import) \
           and "os" in (name.name for name in node.names)

def alert(node):
    raise RuleError("User attempting to load `os` module")

monitor_repl([Rule(is_import_os, alert)])

import os # triggers a `RuleError`
```

## Why "Tezca"?

Tezca is named after Tezcatlipoca, the Aztec god of the night and rulership. In Aztec mythology, he
is the main rival of Quetzalcoatl, the great Feathered Serpent. Most of the more obvious names
were already taken in PyPI, and naming this module after a deity most famous for fighting with a
powerful, giant snake seemed fitting given what this module does.
