from typing import Optional, Union, cast

import click
from pulp_glue.common.context import EntityDefinition, PluginRequirement, PulpEntityContext
from pulp_glue.common.i18n import get_translation
from pulp_glue.internal.context import PulpInternalDistributionContext, PulpInternalRepositoryContext
from pulpcore.cli.common.generic import (
    PulpCLIContext,
    base_path_contains_option,
    base_path_option,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_entity_context,
    pass_pulp_context,
    resource_option,
    show_command,
)

translation = get_translation(__package__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="internal",
    default_type="internal",
    context_table={"internal:internal": PulpInternalRepositoryContext},
)


@click.group()
@click.option(
    "-t",
    "--type",
    "distribution_type",
    type=click.Choice(["internal"], case_sensitive=False),
    default="internal",
)
@pass_pulp_context
@click.pass_context
def distribution(ctx: click.Context, pulp_ctx: PulpCLIContext, distribution_type: str) -> None:
    """Manage distributions of internal content."""
    if distribution_type == "internal":
        ctx.obj = PulpInternalDistributionContext(pulp_ctx)
    else:
        raise NotImplementedError()


filter_options = [label_select_option, base_path_option, base_path_contains_option]
lookup_options = [href_option, name_option]
create_options = [
    click.option("--name", required=True),
    click.option("--base-path", required=True),
    repository_option,
    click.option(
        "--version", type=int, help=_("a repository version number, leave blank for latest")
    ),
]

distribution.add_command(list_command(decorators=filter_options))
distribution.add_command(show_command(decorators=lookup_options))
distribution.add_command(create_command(decorators=create_options))
distribution.add_command(destroy_command(decorators=lookup_options))
distribution.add_command(label_command())


@distribution.command()
@href_option
@name_option
@click.option("--base-path")
@repository_option
@click.option("--version", type=int, help=_("a repository version number, leave blank for latest"))
@pass_entity_context
@pass_pulp_context
def update(
    pulp_ctx: PulpCLIContext,
    distribution_ctx: PulpEntityContext,
    base_path: Optional[str],
    repository: Optional[Union[str, PulpEntityContext]],
    version: Optional[int],
) -> None:
    """Update an existing distribution."""
    body: EntityDefinition = {}

    if base_path is not None:
        body["base_path"] = base_path

    if repository is not None:
        if isinstance(repository, str):
            body["repository"] = repository
        else:
            body["repository"] = repository.pulp_href

    if version is not None:
        body["version"] = version

    distribution_ctx.update(body=body)