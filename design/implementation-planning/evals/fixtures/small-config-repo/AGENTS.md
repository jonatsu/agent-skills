# Fixture Instructions

This repository uses `just check-config` for configuration validation. Keep timeout settings together in
`config/defaults.yaml`, define their accepted values in `config/schema.json`, and document them in the same order in
`docs/configuration.md`.

The requested `request_timeout_seconds` setting is configuration and documentation only. No runtime component consumes
it yet.
