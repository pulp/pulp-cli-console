from typing import Any

import click
from pulp_glue.common.i18n import get_translation
from pulpcore.cli.common.generic import pulp_group

from pulpcore.cli.internal.distribution import distribution
from pulpcore.cli.internal.remote import remote
from pulpcore.cli.internal.repository import repository

translation = get_translation(__package__)
_ = translation.gettext

__version__ = "0.1.0.dev"


@pulp_group("internal")
def internal_group() -> None:
    """Manage Internal plugin."""
    pass


def mount(main: click.Group, **kwargs: Any) -> None:
    """Mount the internal commands to the CLI."""
    internal_group.add_command(distribution)
    internal_group.add_command(remote)
    internal_group.add_command(repository)
    main.add_command(internal_group)