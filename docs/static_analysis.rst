Static Analysis
===============

WASMShark's static analysis engine parses and analyzes WebAssembly binaries
without executing them, extracting structural, behavioral, and cryptographic
indicators of malicious behavior.

Binary Parser
-------------

The parser handles all 13 WASM section types defined in the WebAssembly
specification:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Section
     - ID
     - Description
   * - Type
     - 1
     - Function type signatures
   * - Import
     - 2
     - Imported functions, memories, tables, globals
   * - Function
     - 3
     - Function index to type mapping
   * - Table
     - 4
     - Indirect call tables
   * - Memory
     - 5
     - Linear memory declarations
   * - Global
     - 6
     - Global variable declarations
   * - Export
     - 7
     - Exported functions and memories
   * - Start
     - 8
     - Auto-executing function (malware indicator)
   * - Element
     - 9
     - Table initialization
   * - Code
     - 10
     - Function bytecode
   * - Data
     - 11
     - Memory initialization data
   * - Custom
     - 0
     - Non-standard sections (hidden payloads)

Disassembler
------------

WASMShark disassembles function bytecode into readable instruction sequences
supporting 80+ WASM opcodes including:

- Integer and floating-point arithmetic
- Memory load/store with alignment and offset
- Control flow: ``block``, ``loop``, ``if``, ``br``, ``br_if``, ``br_table``
- Function calls: ``call``, ``call_indirect``
- Local and global variable access

Per-Function Metrics
^^^^^^^^^^^^^^^^^^^^

For each function, WASMShark computes:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Metric
     - Description
   * - ``size``
     - Byte size of function body
   * - ``xor_ops``
     - Count of XOR instructions (encryption indicator)
   * - ``rot_ops``
     - Count of rotate instructions (hash round indicator)
   * - ``nop_max_run``
     - Longest consecutive NOP sled
   * - ``indirect_calls``
     - Count of ``call_indirect`` (obfuscated dispatch)
   * - ``cyclomatic``
     - Cyclomatic complexity
   * - ``suspicious_score``
     - Weighted suspicion score 0–100

CFG Builder
-----------

The control flow graph builder correctly resolves WASM's structured control
flow using a scope stack that tracks ``block``, ``loop``, and ``if`` scopes.
This enables accurate:

- Cyclomatic complexity computation
- Back-edge detection
- Unreachable block identification
- Loop nesting depth calculation

.. admonition:: Key fix

   WASM uses structured control flow — ``br depth N`` branches to the Nth
   enclosing scope. WASMShark's CFG builder correctly resolves these targets
   using a scope stack, unlike naive CFG builders that report cyclomatic=1
   for all functions.

Taint Analysis
--------------

WASMShark performs intra-procedural taint analysis, tracking data flow from
suspicious sources (imports, memory loads) through operations to dangerous
sinks (network sends, file writes).

Taint sources include:

- External function calls that return data
- Memory loads from data segments
- Function parameters

Taint is propagated through:

- Arithmetic and logical operations
- Memory stores and loads
- Local variable assignments

Entropy Analysis
----------------

Shannon entropy and chi-square statistics are computed for:

- The entire binary
- Each section independently

High entropy sections (>7.0) indicate encrypted or compressed payloads.

.. code-block:: text

   DATA  off=0x063e  sz=519  ent=7.588  χ²=267 ⚠ HIGH-ENT

Crypto Constant Detection
--------------------------

WASMShark scans bytecode for 25 known cryptographic constants:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Constant
     - Value
     - Algorithm
   * - SHA-256 H0
     - ``0x6a09e667``
     - SHA-256 initialization vector
   * - ChaCha20 'expa'
     - ``0x61707865``
     - ChaCha20 sigma constant
   * - AES GF multiplier
     - ``0x01010101``
     - AES Galois Field
   * - CRC32 polynomial
     - ``0xEDB88320``
     - CRC32
   * - XTEA delta
     - ``0x9E3779B9``
     - XTEA block cipher
   * - Leet constant
     - ``0x13371337``
     - Common malware marker

Scoring Engine
--------------

WASMShark computes three independent scores:

**Malice Score (0–100)**
   Weighted sum of all findings. CRITICAL findings contribute 30 points,
   HIGH 15, MEDIUM 8, LOW 3.

**Obfuscation Score (0–100)**
   Based on NOP sleds, XOR density, indirect call ratio, entropy, and
   custom section presence.

**Complexity Score (0–100)**
   Based on cyclomatic complexity, Halstead volume, and fan-in/fan-out.

Import Fingerprinting (Imphash)
--------------------------------

WASMShark computes an MD5 hash of the sorted import list for each binary.
Samples with the same imphash have identical import profiles — useful for
clustering related malware families.

.. code-block:: text

   Imphash: 93673bcbdb40d03a171ff7f0fd3fbe74
