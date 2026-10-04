---
name: verify-pstack-coordinator
description: Verify the coordinator UI, metadata and scoped trial path.
version: 0.1.0
author: Lauren Tan (poteto), adapted for gcloudan
license: MIT
platforms: [linux]
---

# Verify this coordinator

## When to Use

Use for changes to this repository's `coordinator` or Hermes observer adapter.
Commands below are relative to the clone. Keep verification in disposable
fixtures; the observer reads selected metadata, never transcript bodies.

## Launch and doctor

Read `docs/COORDINATOR.md` for the deployed service and SSH tunnel. Check the
existing instance before launching another: `terminal` can request
`http://127.0.0.1:9999/api/state` from the host. Confirm the expected schema,
loopback listener and service identity. If absent, launch
`python3 coordinator/server.py --port 9999`; own only that instance.

## Drive and evidence

Run `python3 coordinator/test_server.py -v` for snapshot bounds, omitted sensitive
columns, unavailable-schema handling and request boundaries. Run
`~/.hermes/hermes-agent/venv/bin/python adapters/hermes/test_observer.py` for
native hook dispatch in an isolated temporary home.

For UI changes, use the available browser tool via the documented SSH tunnel.
Check Overview counts, Pstack trials, Worker coverage, source-filtered Session
records and the empty/populated Native task board. Launch one permitted scoped
trial through its button. Observe running and completed/failed state, inspect
the final evidence, then reconcile it against the fixture and actual events.
A completed process is not a passed verification. If browser access is absent,
record the UI path as untested instead of treating HTTP as a screenshot.

Keep screenshots and local trial receipts under ignored `state` or the calling
task's evidence directory. They survive cleanup. Never include native session
content or host-local credentials in a shared commit.

## Cleanup and maintenance

Do not stop the existing user's service to clean a test. Tear down only temporary
instances you created, by their recorded process or unit identity. Preserve the
trial receipts and screenshots. Update this recipe when routes, controls or
runtime interfaces change; a helper that was never executed remains a draft.
