import typing as t
from gettext import gettext as _

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
