import click
from pulp_glue.common.context import PulpContext
from pulp_glue.console.context import AdminTaskContext

from pulpcore.cli.common.generic import (
    PulpCLIContext,
    pass_pulp_context,
)

def attach_tasks_commands(console_group: click.Group) -> None:
    @console_group.group()
    @pass_pulp_context
    @click.pass_context
    def tasks(ctx: click.Context, pulp_ctx: PulpContext, /) -> None:
        """Manage admin tasks."""
        ctx.obj = AdminTaskContext(pulp_ctx)

    @tasks.command()
    @click.option("--limit", type=int, help="Limit the number of tasks shown")
    @click.option("--offset", type=int, help="Skip a number of tasks")
    @click.pass_context
    @pass_pulp_context
    def list(
        pulp_ctx: PulpCLIContext, 
        ctx: click.Context, 
        /, 
        limit: int = None, 
        offset: int = None
    ) -> None:
        """List all admin tasks."""
        task_ctx = ctx.obj
        result = task_ctx.list(limit=limit, offset=offset)
        pulp_ctx.output_result(result)
