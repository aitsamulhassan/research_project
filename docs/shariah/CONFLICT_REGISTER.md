# Conflict register

Machine-readable register: `docs/shariah/conflicts.json`.

## Unresolved

**AAOIFI SS (8) vs SBP IBD Circular 01 of 2012.** SS (8) is the named Murabahah standard, but official clauses were not retrieved. The 2012 circular is an IBI invoice/payment instruction. They are not treated as the same rule. Murabahah identifications therefore cannot receive overall PASS.

## Resolved by scope

**SECP SGR 2023 vs SBP SGF 2025.** SGR excludes SBP-regulated banking companies. SGF applies to IBIs. The engine selects by `institution_class`.

## Partial later circular

**IBD 2008 Essentials vs IBD 2012 invoice circular.** 2012 amends 2008 Appendix-A Murabaha subclause vi. The 2008 annex PDF was not retrieved. Only 2012 paragraphs 1, 2, and 4 are implemented.

Unresolved conflicts that match a case force REVIEW unless a NOT_STRUCTURABLE_WITHOUT_REDESIGN outcome already applies.
