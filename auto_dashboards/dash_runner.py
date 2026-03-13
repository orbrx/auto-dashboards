"""Internal runner for launching Dash apps behind Jupyter proxy.

The runner loads a user script without executing its ``__main__`` block,
resolves a Dash app object from ``create_app`` or ``app``, and starts it with
managed runtime settings.
"""

import argparse
import inspect
import runpy
from pathlib import Path
from typing import Callable, Dict, Optional, Sequence


def _normalize_proxy_path(proxy_path: str) -> str:
    """Ensure proxy path uses a trailing slash."""
    return proxy_path if proxy_path.endswith("/") else f"{proxy_path}/"


def _filter_callable_kwargs(
    callable_obj: Callable[..., object],
    candidates: Dict[str, object]
) -> Dict[str, object]:
    """Return keyword arguments accepted by a callable signature."""
    signature = inspect.signature(callable_obj)
    accepted: Dict[str, object] = {}
    for name, parameter in signature.parameters.items():
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY
        ) and name in candidates:
            accepted[name] = candidates[name]
    return accepted


def _create_app_from_namespace(namespace: Dict[str, object], proxy_path: str) -> Optional[object]:
    """Build an app from optional ``create_app`` factory."""
    create_app_obj = namespace.get("create_app")
    if not callable(create_app_obj):
        return None

    kwargs = _filter_callable_kwargs(
        create_app_obj,
        {
            "proxy_path": proxy_path,
            "requests_pathname_prefix": proxy_path,
            "routes_pathname_prefix": "/",
        }
    )
    return create_app_obj(**kwargs)


def _resolve_dash_app(namespace: Dict[str, object], proxy_path: str) -> object:
    """Resolve user app from ``create_app`` or top-level ``app`` symbol."""
    app_obj = _create_app_from_namespace(namespace, proxy_path)
    if app_obj is None:
        app_obj = namespace.get("app")
    if app_obj is None:
        raise RuntimeError(
            "Dash script must expose either a top-level 'app' or a callable 'create_app'."
        )
    return app_obj


class ManagedDashConstructor:
    """Temporarily inject proxy-safe defaults at Dash construction time."""

    def __init__(self, proxy_path: str):
        self.proxy_path = proxy_path
        self._dash_module: Optional[object] = None
        self._original_dash_cls: Optional[type] = None

    def __enter__(self) -> "ManagedDashConstructor":
        import dash as dash_module

        self._dash_module = dash_module
        self._original_dash_cls = dash_module.Dash
        proxy_path = self.proxy_path
        original_dash_cls = self._original_dash_cls

        class ManagedDash(original_dash_cls):  # type: ignore[misc, valid-type]
            def __init__(self, *args: object, **kwargs: object):
                # Dash requires these prefixes to be constructor-time values.
                requests_prefix = kwargs.get("requests_pathname_prefix")
                if requests_prefix in (None, "/"):
                    kwargs["requests_pathname_prefix"] = proxy_path
                if kwargs.get("routes_pathname_prefix") is None:
                    kwargs["routes_pathname_prefix"] = "/"
                super().__init__(*args, **kwargs)

        dash_module.Dash = ManagedDash
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._dash_module is not None and self._original_dash_cls is not None:
            self._dash_module.Dash = self._original_dash_cls


def _start_dash_app(app_obj: object, port: int) -> None:
    """Start a resolved Dash app with managed runtime settings."""
    run_method = getattr(app_obj, "run", None)
    if callable(run_method):
        run_method(host="127.0.0.1", port=port, debug=False)
        return

    run_server_method = getattr(app_obj, "run_server", None)
    if callable(run_server_method):
        run_server_method(host="127.0.0.1", port=port, debug=False)
        return

    raise RuntimeError("Resolved Dash app does not expose run() or run_server().")


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch a Dash script with Auto Dashboards managed defaults."
    )
    parser.add_argument("--script-path", required=True, help="Path to the user Dash script.")
    parser.add_argument("--port", required=True, type=int, help="Port to bind the Dash app.")
    parser.add_argument("--proxy-path", required=True, help="Jupyter proxy path prefix.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the target Dash script with managed defaults."""
    args = _parse_args(argv)
    script_path = Path(args.script_path).resolve()
    if not script_path.exists():
        raise FileNotFoundError(f"Dash script does not exist: {script_path}")

    proxy_path = _normalize_proxy_path(args.proxy_path)
    with ManagedDashConstructor(proxy_path=proxy_path):
        namespace = runpy.run_path(str(script_path), run_name="auto_dashboards_loader")
    app_obj = _resolve_dash_app(namespace=namespace, proxy_path=proxy_path)
    _start_dash_app(app_obj=app_obj, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
