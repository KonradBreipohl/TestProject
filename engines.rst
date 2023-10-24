.. _engines:

Planning engines
==================

LPG
---
**Support Features:**

- classical and numeric state variables.
- durative actions.


Fast-Downward
-------------
**Support Features:**

- Classical planning support with full information, non-numeric, deterministic instantaneous actions.

**Advantages:**

- Integration within the unified_planning library facilitated by the AIPlan4EU project, making it accessible for broader use.
- Recognized as one of the most successful systems for classical planning.

**Disadvantages:**

- Specificity to classical planning scenarios may limit its applicability to other types of planning problems.

EnhSP
-----

**Support Features:**

- Boolean and numeric state variables, actions, processes, and events (PDDL+ language).

**Advantages:**

- Handles disjunctive preconditions and conditional effects without expensive compilations.

**Disadvantages:**

- Optimality only assured for specific PDDL+ fragments (simple numeric planning problems)​

symk 
----

**Support Features:**

- State-of-the-art classical optimal and top-k planner based on symbolic search extending Fast Downward. It can find a single optimal plan or a set of k different best plans with the lowest cost for a given planning task.

tamer
------

Tamer is a temporal planner that supports temporal action-based problems.


pyperplan
---------

**Support Features:**

- Classical planning based on different search heuristics.
- Action-based problems with hierarchical typing.
- Supports the STRIPS PDDL fragment without action costs.

**Advantages:**

- Lightweight and written in Python.

**Disadvantages:**

- Does not support action costs in the STRIPS PDDL fragment, which could limit its usefulness in certain planning scenarios.
- The default planning algorithm is a blind breadth-first search, which does not scale well, although other heuristic search algorithms are available.
- Limited to specific PDDL fragments, which may not cater to more complex or varied planning needs.

fmap
----

**Support Features:**

- Distributed heuristic search.
- Forward partial-order planning scheme allowing parallel action planning among agents.
- State-based estimates utilizing frontier state.

**Advantages:**

- Enhanced solution plan quality due to parallel action planning.
- Accurate state-based estimates for improved planning.