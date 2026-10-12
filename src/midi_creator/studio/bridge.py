"""One bounded request at a time, with a Cubase-side response required."""

from contextlib import contextmanager
from pathlib import Path
import secrets
import threading
import time

import mido

from .config import StudioConfig, StudioError
from .protocol import Assembler, frames

_LOCK = threading.Lock()


@contextmanager
def bridge_lock(workspace: Path):
    with _LOCK:
        path = workspace / ".studio-bridge.lock"
        with path.open("a+b") as stream:
            stream.seek(0, 2)
            if not stream.tell():
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            if __import__("os").name == "nt":
                import msvcrt
                try:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError as exc:
                    raise StudioError("Another process is using the Cubase bridge") from exc
                try:
                    yield
                finally:
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                try:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError as exc:
                    raise StudioError("Another process is using the Cubase bridge") from exc
                try:
                    yield
                finally:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


class CubaseBridge:
    def __init__(self, config: StudioConfig):
        self.config = config

    def request(self, operation: str, **payload) -> dict:
        incoming = self.config.data["midi_response_input"]
        outgoing = self.config.data["midi_request_output"]
        if incoming not in mido.get_input_names() or outgoing not in mido.get_output_names():
            raise StudioError("Configured MIDI ports are unavailable; run midi-studio doctor")
        with bridge_lock(self.config.workspace):
            request_id = secrets.randbelow(16383) + 1
            assembler = Assembler(request_id, 1)
            with mido.open_input(incoming) as source, mido.open_output(outgoing) as target:
                for frame in frames({"operation": operation, **payload}, request_id, 0):
                    target.send(mido.Message("sysex", data=frame))
                    time.sleep(0.01)
                deadline = time.monotonic() + 6
                while time.monotonic() < deadline:
                    for message in source.iter_pending():
                        if message.type != "sysex":
                            continue
                        result = assembler.feed(message.data)
                        if result is None:
                            continue
                        if not result.get("ok"):
                            raise StudioError(result.get("error", "Cubase rejected the request"))
                        return {**result, "cubase_acknowledged": True}
                    time.sleep(0.01)
        raise StudioError("No Cubase response. Activate the MIDI Creator remote surface and its ports. "
                          "The outcome of a mutation is unknown; inspect Cubase before retrying.")

    def status(self) -> dict:
        try:
            result = self.request("ping")
            return {"connected": True, **result}
        except (StudioError, OSError) as exc:
            return {"connected": False, "cubase_acknowledged": False, "error": str(exc)}
