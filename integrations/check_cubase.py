"""Read the selected Serum instance; optionally change and restore its volume."""

import argparse
from datetime import datetime, timezone
import json

from midi_creator.studio.bridge import CubaseBridge
from midi_creator.studio.config import load_config, save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-write", action="store_true")
    args = parser.parse_args()
    config = load_config()
    bridge = CubaseBridge(config)
    status = bridge.status()
    if not status.get("connected"):
        raise RuntimeError(status.get("error", "Cubase is not connected"))
    if args.test_write and (status["playing"] or status["recording"]):
        raise RuntimeError("Stop playback and recording before the reversible write test")
    discovery = bridge.request("objects")
    plugin = next(obj for obj in discovery["objects"]
                  if obj["title"] == config.data["serum_plugin_name"] and obj["parameter_count"] > 100)
    identity = {"object_id": plugin["object_id"], "token": discovery["token"]}

    def volume():
        values = bridge.request("parameters", **identity, query="Main Vol", offset=0, limit=10)
        return next(value for value in values["parameters"] if value["title"] == "Main Vol")

    before = volume()
    result = {"status": status, "plugin": plugin, "before": before,
              "parameter_write_tested": args.test_write, "native_project_created": False}
    if args.test_write:
        original = before["raw"]
        target = original - 0.01 if original >= 0.01 else original + 0.01
        result["test_target"] = target
        try:
            result["write"] = bridge.request("set_parameters", **identity,
                                             values=[{"tag": before["tag"], "raw": target}])
            result["after_change"] = volume()
            result["change_verified"] = abs(result["after_change"]["raw"] - target) < 1e-5
        finally:
            result["restore"] = bridge.request("set_parameters", **identity,
                                               values=[{"tag": before["tag"], "raw": original}])
            result["after_restore"] = volume()
            result["restore_verified"] = abs(result["after_restore"]["raw"] - original) < 1e-5
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    receipt = config.artifact(f"integrations/cubase-live-{stamp}.json")
    if receipt.exists():
        raise RuntimeError("Receipt already exists; preserve the earlier check")
    save_json(receipt, result)
    print(json.dumps(result, indent=2))
    print(f"Receipt: {receipt}")
    if args.test_write and not (result["change_verified"] and result["restore_verified"]):
        raise RuntimeError("Cubase write/readback check failed; see receipt")


if __name__ == "__main__":
    main()
