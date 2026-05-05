eBPF Runtime Monitor
=====================

WASMShark's eBPF monitor uses bpftrace to attach kernel-level tracepoints
to a running WASM runtime process, observing its actual behavior at the
operating system level.

.. admonition:: Compatibility

   bpftrace is the recommended if bcc fails.

How It Works
------------

The monitor attaches bpftrace programs to four kernel events:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Probe
     - What It Detects
   * - ``execve()``
     - Child process spawning by the WASM runtime
   * - ``mmap(W+X)``
     - Write+Execute memory mapping (fileless shellcode indicator)
   * - ``mprotect(EXEC)``
     - Memory made executable after writing (W^X violation)
   * - ``connect()``
     - Outbound network connections

It also monitors ``/proc/[pid]/`` for:

- Environment variables (credential exposure)
- Open file descriptors (file access)
- TCP connections via ``/proc/net/tcp``
- Syscall frequency via ``/proc/[pid]/syscall``

Basic Usage
-----------

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

Alert Levels
------------

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Level
     - Category
     - Example
   * - CRITICAL
     - MEMORY
     - W+X mmap() — PROT_WRITE|PROT_EXEC mapping detected
   * - HIGH
     - CREDENTIALS
     - SSH_AUTH_SOCK environment variable exposed
   * - HIGH
     - NETWORK
     - Connection to port 9001 (Tor OR port)
   * - MEDIUM
     - NETWORK
     - Outbound TCP connection established

W+X Memory Detection Demo
--------------------------

.. code-block:: bash

   # Build W+X trigger program
   cat > wx_trigger.c << 'EOF'
   #include <sys/mman.h>
   #include <stdio.h>
   #include <unistd.h>
   int main() {
       while (1) {
           void *p = mmap(0, 4096,
                          PROT_READ|PROT_WRITE|PROT_EXEC,
                          MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
           printf("[wx_trigger] W+X mmap at %p\n", p);
           munmap(p, 4096);
           sleep(2);
       }
   }
   EOF
   gcc wx_trigger.c -o wx_trigger

   # Monitor
   ./wx_trigger & PID=$(pgrep -f wx_trigger) && sleep 1 && \
   sudo env "PATH=$PATH" python3 wasmshark_ebpf.py \
     --pid $PID --bpf --timeout 15

Expected output:

.. code-block:: text

   [CRITICAL] MEMORY  W+X mmap() via bpftrace tracepoint
              PROT_WRITE|PROT_EXEC mapping — fileless shellcode staging
              prot=7

   Verdict        : MALICIOUS
   Threat Score   : 100.0/100
   eBPF Active    : ✓ kprobe/tracepoint

.. code-block:: bash

   # Stop trigger
   pkill -f wx_trigger

Command Line Options
--------------------

.. code-block:: text

   python3 wasmshark_ebpf.py [OPTIONS]

   --pid PID         PID of process to monitor (required)
   --bpf             Enable bpftrace eBPF probes
   --no-bpf          Use /proc polling only (no root required)
   --timeout SECS    Monitoring duration in seconds (default: 60)
   --output FILE     Write JSON report to FILE

Runtime Report Fields
---------------------

.. code-block:: json

   {
     "pid":            12326,
     "verdict":        "MALICIOUS",
     "threat_score":   100.0,
     "bpf_used":       true,
     "duration":       20.04,
     "alerts": [
       {
         "level":       "HIGH",
         "category":    "CREDENTIALS",
         "title":       "Sensitive environment variable: SSH_AUTH_SOCK",
         "description": "WASM runtime has access to credential/secret env var",
         "evidence":    "key=SSH_AUTH_SOCK (value redacted)"
       }
     ],
     "new_connections": 4,
     "rwx_regions":     0
   }

Threat Score Calculation
------------------------

The threat score (0–100) is computed from alert weights:

- CRITICAL alerts: +30 points each
- HIGH alerts: +15 points each
- MEDIUM alerts: +5 points each
- W+X memory region detected: +40 points
- SSH credential exposure: +20 points
