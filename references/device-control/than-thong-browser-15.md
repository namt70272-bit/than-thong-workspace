# Browser/device control patterns
> Nguon: G:AiBrowser-Dung
> Ngay: 2026-05-13

Browser-Use is an async python >= 3.11 library that implements AI browser driver abilities using LLMs + playwright. We want our library APIs to be ergonomic, intuitive, and hard to get wrong.  ## Code Style  - Use async python - Use tabs for indentation in all python code, not spaces - Use the modern python >3.12 typing style, e.g. use `str | None` instead of `Optional[str]`, and `list[str]` instead of `List[str]` - Try to keep all console logging logic in separate methods all prefixed with `_log_...`, e.g. `def _log_pretty_path(path: Path) -> str` so as not to clutter up the main logic. - Use pydantic v2 models to represent internal data, and any user-facing API parameter that might otherwise be a dict
