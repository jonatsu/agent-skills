# exporter

Backend service module that creates CSV exports of an account's report data.

## Usage

```python
from exporter.service import ExportService

service = ExportService(log)
service.request_export(account, now)
```

`log` is an `ExportLog` and `now` is a timezone-aware `datetime`. Each call records one export request and returns the
export's identifier.
