Quick Start
===========

Basic Scan
----------

.. code-block:: bash

   python3 wasmshark.py sample_cryptominer.wasm

Full Analysis
-------------

.. code-block:: bash

   python3 wasmshark.py sample_cryptominer.wasm \
     --rules ./rules/ \
     --plugins ./plugins/ \
     --html --json --sarif

Open the HTML report:

.. code-block:: bash

   xdg-open sample_cryptominer_wasmshark.html

Static + Dynamic Analysis
--------------------------

.. code-block:: bash

   python3 wasmshark.py sample_cryptominer.wasm \
     --rules ./rules/ --wasabi -q

View Dynamic CFG
----------------

.. code-block:: bash

   dot -Tpng sample_cryptominer_dynamic_cfg.dot \
       -o sample_cryptominer_dynamic_cfg.png
   eog sample_cryptominer_dynamic_cfg.png

Or paste the ``.dot`` file at https://dreampuf.github.io/GraphvizOnline/

Directory Scan with CSV
-----------------------

.. code-block:: bash

   python3 wasmshark.py -d ./samples/ \
     --rules ./rules/ --csv results.csv

.. code-block:: text

   CSV batch scan: 6 files → results.csv

     → sample_cryptominer.wasm      MALICIOUS  malice=100
     → sample_ransomware.wasm       MALICIOUS  malice=100
     → sample_clean.wasm            CLEAN      malice=0

   SUMMARY
     MALICIOUS : 5
     CLEAN     : 1

Diff Two Samples
----------------

.. code-block:: bash

   python3 wasmshark.py sample_cryptominer.wasm \
     --diff sample_ransomware.wasm \
     --rules ./rules/

.. code-block:: text

   WASM DIFF: sample_cryptominer.wasm  vs  sample_ransomware.wasm

   IMPORTS
   + wasi_snapshot_preview1.fd_write  (new)
   + wasi_snapshot_preview1.random_get  (new)
   - env.sha256_block  (removed)

   IMPORT FINGERPRINT
   A: 93673bcbdb40d03a171ff7f0fd3fbe74
   B: 8e5e267e6022a78562ac203a0be3571a
   Match: NO — different import profile

   RULE CHANGES
   + WASI_RANSOM_TRIAD  (newly triggered)
   - CRYPTOMINER_WASM  (no longer triggered)

eBPF Runtime Monitor
--------------------

.. code-block:: bash

   # Start WASM process
   wasmtime run \
     --preload env=loop.wasm \
     --preload memory=loop.wasm \
     cryptominer_live.wasm &
   PID=$!
   sleep 1

   # Monitor with eBPF
   sudo env "PATH=$PATH" python3 wasmshark_ebpf.py \
     --pid $PID --bpf --timeout 20 --output runtime.json

.. code-block:: text

   [+] eBPF probes attached via bpftrace
       Watching: execve(), mmap(W+X), mprotect(EXEC), connect()

   [HIGH] Sensitive environment variable: SSH_AUTH_SOCK
   [MEDIUM] New TCP connection: 18.97.36.19:443

   eBPF Active    : ✓ kprobe/tracepoint
   Verdict        : MALICIOUS
   Threat Score   : 100.0/100

W+X Memory Detection
--------------------

.. code-block:: bash

   gcc wx_trigger.c -o wx_trigger

   ./wx_trigger & PID=$(pgrep -f wx_trigger) && sleep 1 && \
   sudo env "PATH=$PATH" python3 wasmshark_ebpf.py \
     --pid $PID --bpf --timeout 15

   pkill -f wx_trigger

.. code-block:: text

   [CRITICAL] W+X mmap() via bpftrace tracepoint
              PROT_WRITE|PROT_EXEC mapping — fileless shellcode staging
              prot=7

   Threat Score : 100.0/100

Watch Mode
----------

.. code-block:: bash

   python3 wasmshark_watch.py . \
     --rules ./rules/ --interval 2

Automatically rescans any ``.wasm`` file in the directory when it changes.
Useful for CI/CD pipelines.
