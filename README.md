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
Invoking `Ruleset.invoke` causes the `Ruleset` to be injected into the interpreter as an audit hook
(see [PEP 578](https://peps.python.org/pep-0578/)). Once the `Ruleset` hook has been injected, it
checks the nodes of the AST to ensure that the imposed rules haven't been violated. If any `Rule`
is triggered, it will then respone by running specified code (e.g: raising an error).

## Why "Tezca"?

Tezca is named after Tezcatlipoca, the Aztec god of the night and rulership. In Aztec mythology, he
is the main rival of Quetzalcoatl, the great Feathered Serpent. Most of the more obvious names
were already taken in PyPI, and naming this module after a deity most famous for fighting with a
powerful, giant snake seemed fitting given what this module does.
