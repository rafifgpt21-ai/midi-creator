"""Isolate third-party VST3 code in a bounded worker process."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from .config import StudioConfig, StudioError, plugin_binary


def run_serum(config: StudioConfig, operation: str, **arguments) -> dict:
    plugin = plugin_binary(Path(config.data["serum_plugin"]))
    if not plugin.is_file():
        raise StudioError(f"Serum plugin not found: {plugin}")
    with tempfile.TemporaryDirectory(prefix="midi-studio-serum-") as directory:
        request, response = Path(directory) / "request.json", Path(directory) / "response.json"
        request.write_text(json.dumps({"plugin": str(plugin), "plugin_name": config.data["serum_plugin_name"],
                                       "operation": operation, **arguments}), encoding="utf-8")
        try:
            process = subprocess.run([sys.executable, "-m", "midi_creator.studio.serum_worker",
                                      str(request), str(response)], capture_output=True, text=True,
                                     # Never inherit an MCP client's JSON-RPC input
                                     # pipe. On Windows that can stall child startup.
                                     stdin=subprocess.DEVNULL,
                                     timeout=180, cwd=config.workspace)
        except subprocess.TimeoutExpired as exc:
            raise StudioError("Serum worker timed out after 180 seconds; Cubase was not modified") from exc
        if process.returncode or not response.is_file():
            raise StudioError(f"Serum worker failed ({process.returncode}): {process.stderr[-2000:]}")
        result = json.loads(response.read_text(encoding="utf-8"))
        if not result.get("ok"):
            raise StudioError(result.get("error", "Serum worker failed"))
        return result
