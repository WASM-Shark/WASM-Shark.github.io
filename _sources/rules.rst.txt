Detection Rules
===============

WASMShark uses a custom rule language (``.wsr`` files) for signature-based
detection. Rules are evaluated against the analysis report and contribute
to the final malice score.

Rule Format
-----------

.. code-block:: text

   rule RULE_NAME {
       meta:
           description = "Human readable description"
           author      = "WASMShark"
           severity    = CRITICAL
           tags        = mining, crypto, autorun
       condition:
           imports contains "sha256"
           has_start_func
           malice_score > 50
   }

Severity Levels
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Severity
     - Score
     - Meaning
   * - CRITICAL
     - 30
     - High-confidence malicious behavior
   * - HIGH
     - 15
     - Strong malicious indicator
   * - MEDIUM
     - 8
     - Suspicious behavior
   * - LOW
     - 3
     - Weak indicator

Available Conditions
---------------------

**Import conditions**

.. code-block:: text

   imports contains "sha256"        # Import name matches pattern
   import_count > 5                 # Total import count
   is_wasi                          # Has WASI imports

**String/IoC conditions**

.. code-block:: text

   strings contains "stratum"       # String in data sections
   ioc contains ".onion"            # IoC pattern match

**Crypto conditions**

.. code-block:: text

   crypto_constant "SHA-256 H0"     # Specific constant present

**Score conditions**

.. code-block:: text

   malice_score > 60
   obfusc_score > 40
   entropy > 7.0

**Structural conditions**

.. code-block:: text

   has_start_func                   # Auto-executing start section
   has_taint                        # Taint flow detected
   has_indirect_calls               # call_indirect present
   has_custom_sections              # Non-standard sections
   function_count > 20
   xor_ops > 30

Rule Files
----------

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - File
     - Rules
     - Coverage
   * - ``rules3.wsr``
     - Core: cryptominer, ransomware, C2, dropper
   * - ``advanced.wsr``
     - Supply chain, browser, Stratum, WASI combos
   * - ``extended.wsr``
     - Extended coverage: 9 threat categories
   * - ``structural.wsr``
     - Behavioral patterns, no keyword matching

**Total: 168 simple detection rules now (More Will be added in future)**

Notable Rules
-------------

**CRYPTOMINER_WASM**

.. code-block:: text

   condition:
       imports contains "sha256"
       imports contains "randomx"
       ioc contains "http"

**WASI_RANSOM_TRIAD**

.. code-block:: text

   condition:
       is_wasi
       imports contains "path_rename"
       imports contains "random_get"
       imports contains "fd_write"

**CONFIRMED_CRYPTOMINER** (composite)

.. code-block:: text

   condition:
       crypto_constant "SHA-256 H0"
       imports contains "sha256"
       ioc contains "http"

**EVASIVE_MALICIOUS** (score-based)

.. code-block:: text

   condition:
       malice_score > 60
       obfusc_score > 60

Writing Custom Rules
--------------------

Add your own ``.wsr`` file to the ``rules/`` directory:

.. code-block:: bash

   cat > rules/my_rules.wsr << 'EOF'
   rule MY_CUSTOM_RULE {
       meta:
           description = "My custom detection rule"
           severity    = HIGH
           tags        = custom
       condition:
           imports contains "my_suspicious_import"
           malice_score > 30
   }
   EOF

   python3 wasmshark.py sample.wasm --rules ./rules/

All ``.wsr`` files in the rules directory are automatically loaded.
