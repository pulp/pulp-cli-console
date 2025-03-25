from gettext import gettext as _
from typing import Any, ClassVar, Dict, Optional

from pulp_glue.common.context import (
    EntityDefinition,
    PluginRequirement,
    PulpContentContext,
    PulpEntityContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)


class PulpInternalContentContext(PulpContentContext):
    """Context for Internal Content."""
    
    PLUGIN = "internal"
    RESOURCE_TYPE = "content"
    ENTITY = _("internal content")
    ENTITIES = _("internal content")
    HREF = "internal_internal_content_href"
    ID_PREFIX = "content_internal_content"
    NEEDS_PLUGINS = [PluginRequirement("internal", specifier=">=1.0.0")]


class PulpInternalDistributionContext(PulpEntityContext):
    """Context for Internal Distribution."""
    
    PLUGIN = "internal"
    RESOURCE_TYPE = "internal"
    ENTITY = _("internal distribution")
    ENTITIES = _("internal distributions")
    HREF = "internal_internal_distribution_href"
    ID_PREFIX = "distributions_internal_internal"
    NEEDS_PLUGINS = [PluginRequirement("internal", specifier=">=1.0.0")]

    def preprocess_entity(self, body: EntityDefinition, partial: bool = False) -> EntityDefinition:
        body = super().preprocess_entity(body, partial)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpInternalRemoteContext(PulpRemoteContext):
    """Context for Internal Remote."""
    
    PLUGIN = "internal"
    RESOURCE_TYPE = "internal"
    ENTITY = _("internal remote")
    ENTITIES = _("internal remotes")
    HREF = "internal_internal_remote_href"
    ID_PREFIX = "remotes_internal_internal"
    NEEDS_PLUGINS = [PluginRequirement("internal", specifier=">=1.0.0")]


class PulpInternalRepositoryVersionContext(PulpRepositoryVersionContext):
    """Context for Internal Repository Version."""
    
    PLUGIN = "internal"
    RESOURCE_TYPE = "internal"
    HREF = "internal_internal_repository_version_href"
    ID_PREFIX = "repositories_internal_internal_versions"
    NEEDS_PLUGINS = [PluginRequirement("internal", specifier=">=1.0.0")]


class PulpInternalRepositoryContext(PulpRepositoryContext):
    """Context for Internal Repository."""
    
    PLUGIN = "internal"
    RESOURCE_TYPE = "internal"
    HREF = "internal_internal_repository_href"
    ID_PREFIX = "repositories_internal_internal"
    VERSION_CONTEXT = PulpInternalRepositoryVersionContext
    NEEDS_PLUGINS = [PluginRequirement("internal", specifier=">=1.0.0")]
    CAPABILITIES = {
        "sync": [PluginRequirement("internal", specifier=">=1.0.0")],
    }
    
    # Add custom methods for your repository operations here
    # For example:
    # def import_content(self, href: str, artifact: str, ...) -> Any:
    #     body = {...}
    #     return self.pulp_ctx.call("your_import_method_id", parameters={self.HREF: href}, body=body)