#!/usr/bin/env python3
"""Mide inferencia de un LLM local y escribe un CSV.

Runtimes: Ollama (HTTP) o llama.cpp (subprocess). Completá los TODO:
la grilla de cuantización / batch / contexto y el parseo de tokens/s.

Uso:
  python3 medir_inferencia.py --help
  python3 medir_inferencia.py --runtime ollama --model qwen2:0.5b --out resultados.csv
  python3 medir_inferencia.py --runtime llama --model /ruta/modelo.gguf --out resultados.csv

No inventes tokens/s: solo lo que imprima el runtime o lo que calcule
el reloj de pared junto con el conteo de tokens de salida.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any


def medir_ollama(
    model: str,
    prompt: str,
    options: dict[str, Any],
) -> dict[str, Any]:
    """POST a la API local. Campos de timing: según versión de Ollama."""
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }
    ).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode())
    wall = time.perf_counter() - t0

    # TODO: confirmá en TU versión los nombres eval_count / eval_duration (ns).
    eval_count = data.get("eval_count")
    eval_ns = data.get("eval_duration")
    tps = None
    if eval_count and eval_ns:
        tps = float(eval_count) / (float(eval_ns) / 1e9)
    return {
        "runtime": "ollama",
        "model": model,
        "wall_s": wall,
        "eval_count": eval_count,
        "tokens_per_s": tps,
        "raw_keys": ",".join(sorted(data.keys())),
    }


def medir_llama_cli(
    cli: str,
    model: str,
    prompt: str,
    extra: list[str],
) -> dict[str, Any]:
    """Subprocess. Completá flags con `llama-cli -h` (cambian entre versiones)."""
    cmd = [cli, "-m", model, "-p", prompt, *extra]
    t0 = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    wall = time.perf_counter() - t0
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    return {
        "runtime": "llama",
        "model": model,
        "wall_s": wall,
        "returncode": proc.returncode,
        "tokens_per_s": "",  # TODO: extraer el número de tokens/s de `out`
        "tail": out[-500:].replace("\n", " "),
    }


def main() -> None:
    p = argparse.ArgumentParser(
        description="Medir tokens/s de un LLM local y guardar CSV."
    )
    p.add_argument("--runtime", choices=["ollama", "llama"], default="ollama")
    p.add_argument(
        "--model",
        default="qwen2:0.5b",
        help="tag Ollama o ruta al GGUF",
    )
    p.add_argument("--prompt", default="Explicá Amdahl en dos oraciones.")
    p.add_argument("--out", default="resultados.csv")
    p.add_argument(
        "--cuantizacion",
        default="q4",
        help="etiqueta de esta corrida (q4, q8, …); el modelo ya tiene que ser ese GGUF/tag",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="batch (Ollama: num_batch; llama.cpp: -b). Confirmá el flag en -h.",
    )
    p.add_argument(
        "--ctx",
        type=int,
        default=2048,
        help="tamaño de contexto (Ollama: num_ctx; llama.cpp: -c)",
    )
    args = p.parse_args()

    # TODO: expandí la grilla. El enunciado pide variar (a) cuantización
    # (distintos --model / GGUF Q4 vs Q8) y (b) batch y/o contexto.
    # Una sola fila no alcanza: el informe pide ≥ 3 configuraciones.
    configs: list[dict[str, Any]] = [
        {
            "label": f"{args.cuantizacion}_b{args.batch_size}_c{args.ctx}",
            "cuantizacion": args.cuantizacion,
            "batch_size": args.batch_size,
            "ctx": args.ctx,
            "options": {
                "num_ctx": args.ctx,
                "num_batch": args.batch_size,
            },
            "llama_extra": [
                "-n",
                "64",
                "-c",
                str(args.ctx),
                "-b",
                str(args.batch_size),
            ],
        },
        # {"label": "q8_b1_c2048", "cuantizacion": "q8", ...},
        # {"label": "q4_b1_c4096", ...},
    ]

    rows: list[dict[str, Any]] = []
    for cfg in configs:
        if args.runtime == "ollama":
            row = medir_ollama(args.model, args.prompt, cfg["options"])
        else:
            cli = os.environ.get("LLAMA_CLI", "llama-cli")
            extra = list(cfg.get("llama_extra") or [])
            # TODO: agregá -ngl / --threads según tu build (llama-cli -h).
            row = medir_llama_cli(cli, args.model, args.prompt, extra)
        row["label"] = cfg["label"]
        row["cuantizacion"] = cfg["cuantizacion"]
        row["batch_size"] = cfg["batch_size"]
        row["ctx"] = cfg["ctx"]
        rows.append(row)
        print(row)

    keys = sorted({k for r in rows for k in r})
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print("escribi", args.out)


if __name__ == "__main__":
    main()
