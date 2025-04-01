import typing as t
from gettext import gettext as _

from pulp_glue.common.context import PulpContext, PulpEntityContext


class PulpVulnerabilityReportContext(PulpEntityContext):
    """Context for working with vulnerability reports."""

    ENTITY = _("vulnerability report")
    ENTITIES = _("vulnerability reports")
    ID_PREFIX = "vuln_report"
    HREF = "service_vulnerability_report_href"

    def create(self, file: t.IO[bytes], chunk_size: int = 1000000) -> t.Dict[str, t.Any]:
        """Create a vulnerability report from a JSON file.

        Args:
            file: The file object to upload
            chunk_size: The chunk size for the upload

        Returns:
            The created vulnerability report entity
        """
        # Read the raw file content
        file_content = file.read()
        # Submit the file content to the Pulp API
        response = self.pulp_ctx.call(
            operation_id="vuln_report_create",
            body={"package_json": file_content},
            validate_body=False,
        )
        return t.cast(t.Dict[str, t.Any], response)


class AdminTaskContext:
    """Context for accessing admin tasks directly without using the entity framework."""

    def __init__(self, pulp_ctx: PulpContext) -> None:
        self.pulp_ctx = pulp_ctx

    def list(
        self,
        limit=None,
        offset=None,
        parameters=None,
        name=None,
        name__contains=None,
        logging_cid__contains=None,
        state=None,
        state__in=None,
        task_group=None,
        parent_task=None,
        worker=None,
        created_resources=None,
        started_at__gte=None,
        started_at__lte=None,
        finished_at__gte=None,
        finished_at__lte=None,
    ):
        """List all admin tasks with optional filtering parameters."""
        if parameters is None:
            parameters = {}
        if limit:
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset

        # Add all task filters from generic.py
        if name:
            parameters["name"] = name
        if name__contains:
            parameters["name__contains"] = name__contains
        if logging_cid__contains:
            parameters["logging_cid__contains"] = logging_cid__contains
        if state:
            parameters["state"] = state
        if state__in:
            parameters["state__in"] = state__in
        if task_group:
            parameters["task_group"] = task_group
        if parent_task:
            parameters["parent_task"] = parent_task
        if worker:
            parameters["worker"] = worker
        if created_resources:
            parameters["created_resources"] = created_resources
        if started_at__gte:
            parameters["started_at__gte"] = started_at__gte
        if started_at__lte:
            parameters["started_at__lte"] = started_at__lte
        if finished_at__gte:
            parameters["finished_at__gte"] = finished_at__gte
        if finished_at__lte:
            parameters["finished_at__lte"] = finished_at__lte

        # Use the correct attribute _api_root instead of api_root
        url = f"{self.pulp_ctx._api_root}api/pulp/admin/tasks/"
        return self.pulp_ctx.call("tasks_list", url, parameters=parameters)
