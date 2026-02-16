# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pulp-cli-console is a CLI plugin for [Pulp](https://pulpproject.org/) that adds console administrative commands (task management, vulnerability reports, domain management). It extends pulp-cli via the entry points plugin system.

## Build & Development Commands

```bash
make build          # Build both packages (CLI + glue)
make format         # Auto-format with isort + black
make lint           # Run all linting (shellcheck, isort, black, flake8, mypy)
make test           # Run all tests (requires Pulp server; copies tests/cli.toml.example if needed)
make livetest       # Run only integration tests (marker: live)
make unittest       # Run only unit tests (marker: not live)
make unittest_glue  # Run only glue unit tests
```

Run a single test:
```bash
python3 -m pytest -v tests/test_file.py::test_function_name
python3 -m pytest -v -m pulp_console  # by marker
```

Mypy for the CLI package requires: `MYPYPATH=pulp-glue-console mypy`

## Dual-Package Architecture

The repo contains **two separate Python packages** that are versioned and released together:

1. **pulp-cli-console** (root `pyproject.toml`) — Click-based CLI commands under `pulpcore/cli/console/`
2. **pulp-glue-console** (`pulp-glue-console/pyproject.toml`) — API client layer under `pulp-glue-console/pulp_glue/console/`

Both use PEP 420 namespace packages (`pulpcore.cli.*` and `pulp_glue.*`). Versions must stay synchronized — bump-my-version handles this across all files.

### CLI Layer (`pulpcore/cli/console/`)

- `__init__.py` — Plugin `mount()` entry point. Patches OpenAPI to handle HTTP 202 responses. Creates the `pulp console` command group and attaches subcommands.
- `task.py` — `pulp console task list` with extensive filtering
- `vulnerability.py` — `pulp console vulnerability {list,show,npm,rpm}`
- `populated_domain.py` — `pulp console populated-domain create`

Commands follow the pattern: define an `attach_*_commands(group)` function that adds Click commands to the console group.

### Glue Layer (`pulp-glue-console/pulp_glue/console/`)

- `context.py` — `PulpVulnerabilityReportContext` (entity-based, extends `PulpEntityContext`) and `AdminTaskContext` (direct API calls). Contexts encapsulate all Pulp REST API interaction.

## Code Style

- Line length: 100 (black, isort, flake8 all configured consistently)
- isort: black profile
- mypy: strict mode
- Fully typed codebase with `py.typed` markers

## Changelog & Commits

- Changelog entries go in `CHANGES/` as `{issue_number}.{feature,bugfix,removal,devel,misc}` files (towncrier)
- Commits must reference issues (`fixes #123` or `closes #123`)
- No `[noissue]`, `WIP`, `DRAFT`, or `DO NOT MERGE` in commit messages

## Plugin Registration

Registered via entry point in `pyproject.toml`:
```toml
[project.entry-points."pulp_cli.plugins"]
console = "pulpcore.cli.console"
```

pulp-cli discovers this and calls the `mount(main, **kwargs)` function in `__init__.py`.
