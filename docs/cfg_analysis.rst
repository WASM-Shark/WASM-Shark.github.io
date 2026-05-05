CFG Analysis
============

WASMShark implements advanced control flow graph analysis algorithms from
compiler theory to detect structural anomalies that indicate obfuscation.

Algorithms
----------

Lengauer-Tarjan Dominance Tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Computes immediate dominators for every basic block using the Cooper et al.
iterative algorithm. Enables:

- Accurate natural loop detection
- Loop nesting depth measurement
- Dominator tree depth analysis (deep trees = complex nested control flow)

Tarjan's SCC Algorithm
^^^^^^^^^^^^^^^^^^^^^^

Identifies strongly connected components — groups of blocks where every
block can reach every other block. Non-trivial SCCs indicate cyclic control
flow (loops). Large SCCs with multiple entry points indicate **irreducible
control flow** — a strong obfuscation indicator.

Natural Loop Detection
^^^^^^^^^^^^^^^^^^^^^^

A natural loop exists for every back edge (an edge from a node to one of
its dominators). WASMShark identifies:

- Loop header (entry point)
- Loop body (all nodes in the loop)
- Back edge source
- Loop nesting depth

Irreducible CFG Detection
^^^^^^^^^^^^^^^^^^^^^^^^^^

A CFG is **irreducible** when a non-trivial SCC has multiple entry points
from outside the SCC. This cannot occur in normal structured code and is
a strong indicator of obfuscated control flow.

.. code-block:: text

   [HIGH] IRREDUCIBLE_CFG
   3 nodes in irreducible CFG regions — non-structured control flow,
   strong obfuscation indicator

Path Count Estimation
^^^^^^^^^^^^^^^^^^^^^

WASMShark estimates the number of distinct execution paths through a
function using dynamic programming on the DAG (ignoring back edges).

Exponential path counts (>1,000,000) indicate path-explosion obfuscation:

.. code-block:: text

   [HIGH] PATH_EXPLOSION
   Estimated 1.2e+08 execution paths — exponential path complexity

CFG Fingerprinting
^^^^^^^^^^^^^^^^^^

Each function's CFG topology is hashed to a 12-character fingerprint.
Functions sharing the same fingerprint have identical control flow structure
— useful for detecting clone-padding obfuscation.

.. code-block:: text

   CFG clone group detected: func[0] and func[3] identical topology
   fingerprint=6b9337ea99af

Running CFG Analysis
--------------------

.. code-block:: bash

   # Run with CFG advanced plugin
   python3 wasmshark.py sample_obfuscated_loader.wasm \
     --plugins ./plugins/ -v

   # Export CFG anomaly DOT files
   python3 wasmshark.py sample_obfuscated_loader.wasm \
     --plugins ./plugins/ \
     --cfg-anomaly \
     --cfg-overview ./cfgs/

   # Render SVG
   dot -Tsvg cfgs/module_overview.dot -o cfgs/overview.svg
   xdg-open cfgs/overview.svg

Anomaly Detection
-----------------

The ``plugin_cfg_anomaly.py`` plugin detects:

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Anomaly
     - Severity
     - Description
   * - IRREDUCIBLE_CFG
     - HIGH
     - Non-structured control flow — obfuscation
   * - DEEP_LOOP_NESTING
     - HIGH
     - Loop nesting depth ≥ 4
   * - PATH_EXPLOSION
     - HIGH
     - >1,000,000 estimated execution paths
   * - LARGE_SCC
     - HIGH
     - SCC with >5 nodes
   * - DISPATCHER_BLOCK
     - HIGH
     - Block with >4 successors (flattening)
   * - UNREACHABLE_BLOCKS
     - MEDIUM
     - Dead code — never reachable from entry
   * - HIGH_CYCLOMATIC
     - HIGH
     - Cyclomatic complexity > 50
   * - CFG_CLONE_CLUSTER
     - MEDIUM
     - Many functions with identical CFG shape

Module Overview Export
----------------------

The module overview DOT file shows all functions as nodes:

- Node size reflects function size in bytes
- Red nodes have anomaly findings
- Yellow nodes are moderately suspicious
- Green nodes are clean
- Edge direction shows call relationships

.. code-block:: bash

   dot -Tsvg cfgs/module_overview.dot -o cfgs/overview.svg
   firefox cfgs/overview.svg
