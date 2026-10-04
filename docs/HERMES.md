# Pstack on headless Hermes

Hermes executes the work on its own machine. Your laptop can remain the viewer
and SSH client. A graphical desktop on Hermes is unnecessary for these methods.

The initial side experiment installed three native skills under the existing
`software-development` category: `pstack-how`, `pstack-swarm` and `pstack-adopt`.
The original planning, debugging, TDD and other skills remain. The native catalog
provides discovery; the Cursor router and named Cursor investigator are not
installed. Delegation uses Hermes's actual `delegate_task` interface.

## Use it

Start a fresh Hermes conversation and ask:

> Load pstack-how. Explain how this subsystem works, with source evidence.
> Use pstack-swarm only if distinct investigations improve coverage.

Or:

> Load pstack-adopt. Compare upstream blast-radius in the pstack clone with my
> existing change-planning workflow. Add only useful missing behavior.

These requests make selection explicit for the first trial. Normal catalog
discovery is available, but installation does not prove automatic selection.
Existing conversations can retain cached catalogs. No running service or chat
was restarted during this installation.

## Installation and checks

The source adapters live in `adapters/hermes/skills`. With the inspected runtime
layout, run from the clone:

```sh
~/.hermes/hermes-agent/venv/bin/python adapters/hermes/install.py
python3 scripts/build_board.py
```

The installer uses native `skill_manage`, preserves differing installed skills,
and respects staged/blocked approval results. It is idempotent for exact copies.
It validates catalog retention and `skill_view` loading, then records an ignored
host-local receipt. It assumes the inspected runtime at `~/.hermes/hermes-agent`;
another layout needs that path adapted before use.

The actual first install grew the catalog from 89 to 92 names and retained every
existing name. All three skills passed native creation and load checks. Metadata
warnings were corrected through native edits, and an unchanged rerun passed.
Those initial checks were installation and loading only. Live walkthrough,
two-child delegation and impact trials have now been exercised; see
[the coordinator record](COORDINATOR.md) for current evidence and limits.

## View the board from your laptop

The generated `board/index.html` is a searchable, read-only view of all 77
source features, the main adaptation state, installed Hermes methods and the
latest local receipt. It does not show live sessions, worker activity or model
usage. Regenerate it after changing the ledger or receipt.

On Hermes, serve only the generated board directory:

```sh
cd ~/repos/pstack
python3 -m http.server 8765 --bind 127.0.0.1 --directory board
```

Keep that terminal running, or use your usual process manager. For the initial
experiment, a background server was started, bound only to Hermes's loopback.
Its PID and log are ignored files in `adapters/hermes`. It has no boot auto-start.

In a laptop terminal, open an SSH tunnel:

```sh
ssh -N -L 127.0.0.1:18765:127.0.0.1:8765 hermes@192.168.8.174
```

Use your normal authenticated SSH configuration. On the current Windows computer,
the dedicated key can be selected with:

```powershell
ssh -i "$HOME/.ssh/pstack_hermes_ed25519" -o IdentitiesOnly=yes -N -L 127.0.0.1:18765:127.0.0.1:8765 hermes@192.168.8.174
```

Then open [the board](http://127.0.0.1:18765) in your laptop browser. The tunnel
must remain running; Ctrl+C closes it. If port 18765 is already occupied, choose
another local port. Nothing needs to listen on Hermes's public/LAN address.

HTTP 200 and the loopback-only listener were checked. The board was opened
through the tunnel, and its Hermes filter and search were exercised in a browser.
This is the first visibility layer. A live activity UI would require a separate
integration with Hermes's actual event/session interface; this board does not
pretend to provide that.
