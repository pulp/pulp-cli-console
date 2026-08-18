# Changelog

[//]: # (You should *NOT* be adding new change log entries to this file, this)
[//]: # (file is managed by towncrier. You *may* edit previous change logs to)
[//]: # (fix problems like typo corrections or such.)
[//]: # (To add a new change log entry, please see)
[//]: # (https://docs.pulpproject.org/contributing/git.html#changelog-update)

[//]: # (WARNING: Don't drop the towncrier directive!)

[//]: # (towncrier release notes start)

## 0.1.7 (2026-08-18) {: #0.1.7 }


#### Bugfixes {: #0.1.7-bugfix }

- Fixed `pulp console populated-domain create` to call the `api_pulp_create_domain_create` operation instead of the now-removed `api_pulp_create_domain_post`. `pulp-service` added RBAC support to its self-service domain-creation endpoint, which changed the auto-generated OpenAPI operation ID from a `_post` to a `_create` suffix.


### Pulp-console GLUE {: #0.1.7-pulp-console-glue }


No significant changes.


---

## 0.1.6 (2026-08-13) {: #0.1.6 }


#### Misc {: #0.1.6-misc }

- Raised the `pulp-cli` upper version bound to `<0.41` to allow running against `pulp-cli` 0.40.


### Pulp-console GLUE {: #0.1.6-pulp-console-glue }


#### Misc {: #0.1.6-pulp-console-glue-misc }

- Raised the `pulp-glue` upper version bound to `<0.41` to allow running against `pulp-cli` 0.40.


---

## 0.1.0.dev (unreleased)

Initial release.