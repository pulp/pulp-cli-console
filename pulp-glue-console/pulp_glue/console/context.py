import typing as t
from gettext import gettext as _

from pulp_glue.common.context import PulpContext
from pulp_glue.common.context import PulpEntityContext


class PulpVulnerabilityReportContext(PulpEntityContext):
    """Context for working with vulnerability reports."""

    ENTITY = _("vulnerability report")
    ENTITIES = _("vulnerability reports")
    ID_PREFIX = "vuln_report"
    HREF = "service_vulnerability_report_href"

    def upload(self, file: t.IO[bytes], chunk_size: int = 1000000) -> t.Dict[str, t.Any]:
        """Upload a vulnerability report from a JSON file.

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
        
    def list(self, limit=None, offset=None, parameters=None):
        """List all admin tasks."""
        if parameters is None:
            parameters = {}
        if limit:
            parameters["limit"] = limit
        if offset:
            parameters["offset"] = offset
        
        # Use the correct attribute _api_root instead of api_root
        url = f"{self.pulp_ctx._api_root}api/pulp/admin/tasks/"
        return self.pulp_ctx.call("tasks_list", url, parameters=parameters)