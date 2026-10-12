"""Exercise the real local stdio server and save a concise connection receipt."""

import argparse
import asyncio
from datetime import timedelta
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from midi_creator.studio.config import load_config, save_json


async def check(config, bundle, live):
    params = StdioServerParameters(command=sys.executable,
             args=["-m", "midi_creator.studio.mcp_server", "--config", str(config.path)],
             cwd=str(config.workspace))
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=240)) as client:
            initialized = await client.initialize()
            available = await client.list_tools()

            async def call(name, arguments):
                result = await client.call_tool(name, arguments)
                if result.isError:
                    raise RuntimeError(f"{name}: {result.content}")
                return result.structuredContent or json.loads(result.content[0].text)

            status = await call("studio_status", {"check_cubase": live})
            serum = await call("serum_parameters", {"query": "main_vol", "limit": 1})
            verification = await call("verify_cubase_session", {"folder": bundle}) if bundle else None
            return {"ok": status["ok"] and serum["ok"] and (verification is None or verification["ok"]),
                    "server": initialized.serverInfo.model_dump(),
                    "tools": sorted(tool.name for tool in available.tools),
                    "studio": status, "serum_worker": serum, "bundle": verification,
                    "live_control_verified": bool(status["cubase"].get("connected"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--bundle")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    config = load_config(args.config)
    output = config.artifact(args.out) if args.out else None
    if output and output.exists():
        parser.error("Receipt already exists; use a new path")
    result = asyncio.run(check(config, args.bundle, args.live))
    if output:
        save_json(output, result)
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
