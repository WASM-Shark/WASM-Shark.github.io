Dynamic Analysis (Wasabi)
=========================

WASMShark integrates `Wasabi <https://github.com/danleh/wasabi>`_ — an
ASPLOS 2019 Best Paper dynamic instrumentation framework for WebAssembly
— to confirm static analysis predictions with actual runtime evidence.

How It Works
------------

1. **Instrument** — Wasabi inserts low-level hooks into every WASM instruction
2. **Execute** — The instrumented binary runs under Node.js with import stubs
3. **Collect** — WASMShark's analysis hooks record runtime behavior
4. **Correlate** — Runtime observations are compared against static findings

.. code-block:: bash

   python3 wasmshark.py sample_cryptominer.wasm \
     --rules ./rules/ --wasabi -q

Runtime Metrics Collected
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Metric
     - Description
   * - Total instructions
     - Total instruction count executed at runtime
   * - XOR ops
     - XOR operations executed (encryption confirmation)
   * - Rotate ops
     - Rotate operations (hash round confirmation)
   * - NOP ops
     - NOPs executed (NOP sled confirmation)
   * - Memory reads/writes
     - Memory access counts
   * - memory.grow calls
     - Dynamic memory expansion count
   * - Branches taken/not taken
     - Branch coverage ratio
   * - Indirect calls
     - Obfuscated dispatch confirmation
   * - Start function
     - Auto-execution confirmation
   * - Call graph
     - Actual runtime call relationships
   * - Suspicious constants
     - Known crypto constants observed at runtime

Static ↔ Dynamic Correlations
-------------------------------

WASMShark automatically correlates runtime observations with static findings:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Correlation
     - Trigger
   * - ``CONFIRMED_XOR``
     - Static XOR > 20 AND runtime XOR > 50
   * - ``CONFIRMED_AUTORUN``
     - Static predicted start function AND runtime confirms it ran
   * - ``CONFIRMED_INDIRECT_CALLS``
     - Static found call_indirect AND runtime confirms they executed
   * - ``MINING_BEHAVIOR_CONFIRMED``
     - CRYPTOMINER rule + high runtime XOR
   * - ``OBFUSCATION_CONFIRMED``
     - Obfuscation rule + runtime indirect calls
   * - ``RANSOMWARE_MEMORY_CONFIRMED``
     - Ransomware rule + runtime memory.grow calls

Example Output
--------------

.. code-block:: text

   WASABI DYNAMIC ANALYSIS
   ──────────────────────────────────────────────────────
   Total instructions executed :          196
   XOR ops at runtime          :            0
   NOP ops at runtime          :           90
   Start func ran              :            5
   Runtime call graph (1 callers):
     func[5] → ['func[0]']

   STATIC ↔ DYNAMIC CORRELATIONS
   ──────────────────────────────────────────────────────
   ✓ [HIGH] CONFIRMED_AUTORUN
     Static predicted auto-exec func[5] — runtime confirms it ran

State Machine Extraction
------------------------

WASMShark builds a state machine from the runtime call sequence:

- Each executed function is a **state**
- Each function call is a **transition**
- Back edges indicate loops
- Terminal states have no outgoing calls

.. code-block:: text

   State Machine
   States (unique functions)  : 2
   Transitions observed       : 1
   Initial state              : func[0]
   Terminal states            : [0]

Dynamic CFG Reconstruction
--------------------------

WASMShark reconstructs the control flow graph from runtime observations
and compares it against the static CFG:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Finding
     - Description
   * - Dead code confirmed
     - Functions in static CFG that never executed
   * - Hidden call paths
     - Runtime edges not present in static CFG
   * - Unexpected functions
     - Functions executed outside static call graph
   * - Coverage
     - Percentage of static functions that actually ran

.. code-block:: bash

   # Generate and view dynamic CFG
   python3 wasmshark.py sample_cryptominer.wasm --wasabi -q

   dot -Tpng sample_cryptominer_dynamic_cfg.dot \
       -o sample_cryptominer_dynamic_cfg.png
   eog sample_cryptominer_dynamic_cfg.png

CFG Node Colors
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Color
     - Meaning
   * - Red
     - Executed, suspicious (score > 20)
   * - Green
     - Executed, clean
   * - Blue (ellipse)
     - Import that was called
   * - Grey dashed
     - Never executed (dead code)
   * - Orange
     - Executed but not in static CFG (unexpected)

Supported Samples
-----------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Sample
     - Wasabi
     - Notes
   * - ``sample_cryptominer.wasm``
     - ✓ Works
     - 196 instructions, start func[5] confirmed
   * - ``sample_browser_cryptojack.wasm``
     - ✓ Works
     - 191 instructions, start func[8] confirmed
   * - ``sample_ransomware.wasm``
     - ✓ Works
     - 211 instructions, WASI stubs applied
   * - ``sample_obfuscated_loader.wasm``
     - ✗ Fails
     - Uses tail call extension (Wasabi 0.3.0 limitation)

.. admonition:: Note

   The obfuscated loader uses WebAssembly tail call instructions which
   Wasabi 0.3.0 does not support. Static analysis still detects it with
   MALICIOUS 100/100 — demonstrating the value of combining both approaches.
