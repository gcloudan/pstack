# Hermes browser interfaces and coordinator

This side experiment improves Hermes's harness and makes its work visible from
a laptop. It is separate from installing the Cursor kit on a work computer.

## What is live

The coordinator reads selected metadata from Hermes's default profile:

- Recent session records, with source, parent relationship, timing and counters.
  An open record does not establish an active model turn.
- Native Kanban tasks, attempt states and prerequisite links, without dispatching
  or changing those boards. Both the default and named boards are inspected.
  The default board is empty; the active named `life-ops` board contains existing tasks.
- Metadata-only start/stop receipts from an additive worker observer.
- Coordinator-owned disposable trials, including running/process-completed
  states, observed tool names and final evidence.
- A searchable source adoption map, separating Hermes from the Cursor layer.

The view refreshes every five seconds. It does not read transcript bodies,
credential configuration or arbitrary log files. Titles and task bodies are
excluded. The worker observer drops goals, summaries and tool arguments.
Other Hermes profiles are not automatically monitored by this default-profile
view. Events from earlier sessions cannot be reconstructed as live telemetry.

## Open it

On the home network, open [Sites & access](http://192.168.8.174:9999/#access).
It lists the live coordinator, native Hermes dashboard, browser editor and
original adoption view. Phones and other computers on that network use the same
IP links; `localhost` always refers to the device opening it.

The deployed coordinator binds `0.0.0.0:9999` and accepts the explicitly declared
LAN Host `192.168.8.174:9999`. Network viewers cannot obtain a trial-launch token
or launch model calls. Launch requires a loopback peer, loopback Host, matching
Origin and the process token. The standalone server still defaults to loopback.
Do not forward these LAN ports to the public internet.

The native dashboard runs separately on port 9119 through Hermes's own password
auth provider. Its unauthenticated config API returns 401. The username is
`hermes`; the generated login is stored only on Hermes at
`~/.hermes/runtime/pstack-dashboard-login.txt` (0600), never in this repository.
The service's hash/signing secret are private in `pstack-dashboard.env`.
The existing browser editor is already available on port 8080.

For the localhost control view, open this tunnel on your laptop and keep it running:

```sh
ssh -N -L 127.0.0.1:9999:127.0.0.1:9999 hermes@192.168.8.174
```

Then visit [the coordinator](http://127.0.0.1:9999). On the current Windows
computer, select the dedicated identity if it is not in your SSH configuration:

```powershell
ssh -i "$HOME/.ssh/pstack_hermes_ed25519" -o IdentitiesOnly=yes -N -L 127.0.0.1:9999:127.0.0.1:9999 hermes@192.168.8.174
```

The tunnel is currently open for this computer. Closing it disconnects the
viewer. The backend is an enabled user service; no graphical desktop is needed.
Its availability after reboot follows the host's user-manager/login policy.

```sh
systemctl --user status pstack-coordinator.service
systemctl --user restart pstack-coordinator.service
journalctl --user -u pstack-coordinator.service -n 40
```

Do not restart it during a trial: the service owns those child processes.
Unresolved prior ownership blocks another fixture trial after a restart.
Process identity uses Linux start ticks to distinguish reused PIDs.

## Use the stack in Hermes

Four native methods are installed: `pstack-how`, `pstack-swarm`, `pstack-impact`
and `pstack-adopt`. The existing planning, debugging, TDD and review skills stay.
The alias `/pstack-investigate` loads the walkthrough and delegation methods.
The project-local `verify-pstack-coordinator` recipe is available in trusted
sessions started in this clone.

Give the outcome and scope. Let workers choose their own searches. A small
task stays in the parent; independent slices get scoped briefs. The parent
checks evidence rather than treating agreement as proof. `pstack-impact` traces
downstream effects and tests the facts on which a safety conclusion depends.

The trial buttons on the localhost control connection make real model calls using your configured Hermes provider.
They accept only predefined prompts against the disposable reminder fixture.
One trial owns that shared fixture at a time. Native command approvals remain
active. No yolo mode or built-in tool override permission is granted.
Fixture fingerprints are captured for new runs and compared at completion.
Process success, unchanged files and substantive verification are separate facts.

## Evidence so far

The walkthrough traced the current 30-minute boundary, paused suppression,
unreachable 60-minute legacy implementation and absence of desktop delivery.
The two-child coverage trial used actual `delegate_task`, completed both slices,
and returned a parent-checked synthesis. The observer recorded two starts and
two completed stops. The three existing fixture tests were independently rerun.

The impact trial assessed changing the default from 30 to 60 without applying
the change. It identified the affected rendering/entry point and boundary test,
and distinguished the unaffected explicit override and paused path. Its current
suite passed; it did not claim to have run mutated hypothetical code.

Some extra inline probes were blocked by native command approval. Reports kept
those conclusions as source deductions. No approval controls were bypassed.
The fixture and test scope remain small; these trials do not prove general
productivity gains or correctness on production projects.

Seven coordinator checks cover metadata bounds/omissions, unavailable schemas,
request protections, restart ownership, chronological history and mixed native
millisecond/ISO timestamps. The observer's native hook registry test ran in an
isolated temporary Hermes home and confirmed that private payload sentinels were
excluded. Both metadata and HTTP paths were exercised on the real host.

## Installation and maintenance

The source is in `coordinator` and `adapters/hermes/observer`. Install or update
the native methods through `adapters/hermes/install.py`; it preserves customized
files and native approval results. Install the observer in the user plugin
directory, then enable it through the supported CLI:

```sh
~/.local/bin/hermes plugins enable pstack-coordinator --no-allow-tool-override
```

For the inspected layout, install the user service from the clone:

```sh
python3 scripts/install-coordinator-service.py
```

The helper verifies its candidate unit before changing the owned server, refuses
to interrupt running trials and preserves an unrelated differing unit. The
native plugin enable command reported a gateway hook reload; fresh CLI processes
also loaded it. Hermes's core source and existing chats were not replaced.

Run checks after changes:

```sh
python3 coordinator/test_server.py -v
~/.hermes/hermes-agent/venv/bin/python adapters/hermes/test_observer.py
python3 scripts/validate.py
```

Host receipts, trial outputs and observer logs stay local and out of shared
commits. Worker start records with lazy/unassigned session IDs may not join their
stop records; the view labels that missing correlation rather than inventing it.
The observer rotates its metadata log at 8 MiB. Evidence remains after a trial.


## Network setup and limits

`scripts/enable-hermes-network.py` is a deployment helper for this specific
Hermes host, not a generic work-Cursor installer. It adds the LAN viewer and
`pstack-hermes-dashboard.service`, leaving the existing gateway and editor
processes in place. Both authored user services are enabled. Its access directory
is private deployment state under `state/coordinator/access.local.json`.

The native dashboard includes `/chat`, `/sessions`, `/skills`, `/models`,
`/plugins`, `/profiles`, `/cron` and its existing `/kanban` plugin. The native
Kanban supports dispatch/assignment actions; this experiment has not nudged its
dispatcher or changed existing tasks. Its chat shows workers belonging to that
chat session; the custom observer supplies lifecycle receipts from fresh
plugin-enabled sessions across the default profile.

A localhost tunnel and a LAN link do not grant access from arbitrary networks.
Away-from-home access still needs a private VPN such as Tailscale and owner
sign-in. No VPN account, public tunnel, router port forward or publicly reachable
admin endpoint has been created. Hindsight on localhost:8888 is an internal API,
not an additional coordinator website.

Eight behavioral tests cover read-only snapshots, named-board discovery,
private-column omission, stale ownership, ordering, and network Host/origin/
launch-token boundaries. Login and the actual network pages were checked in
this computer's browser. Individual phone routing has not been tested.
