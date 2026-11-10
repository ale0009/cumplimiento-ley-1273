"""CLI: `matriz`, `plantilla` y `evaluar`."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .informe import informe, matriz
from .modelo import cargar_chequeo, cargar_controles, cargar_delitos, evaluar


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cumplimiento_1273", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("matriz", help="Imprime la matriz delito → controles")
    pl = sub.add_parser("plantilla", help="Crea una lista de chequeo vacía (CSV)")
    pl.add_argument("salida", type=Path)
    ev = sub.add_parser("evaluar", help="Evalúa una lista de chequeo y genera el informe")
    ev.add_argument("chequeo", type=Path)
    ev.add_argument("--organizacion", default="Empresa anónima")
    ev.add_argument("-o", "--salida", type=Path)
    a = p.parse_args(argv)

    delitos, controles = cargar_delitos(), cargar_controles()
    if a.cmd == "matriz":
        print(matriz(delitos, controles))
    elif a.cmd == "plantilla":
        usados = sorted({c for d in delitos for c in d.controles}, key=lambda c: [int(x) for x in c.split(".")])
        with open(a.salida, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["codigo", "control", "estado"])
            w.writerows([c, controles.get(c, ""), "no_implementado"] for c in usados)
        print(f"Plantilla con {len(usados)} controles en {a.salida}")
    else:
        texto = informe(evaluar(delitos, cargar_chequeo(a.chequeo)), controles, a.organizacion)
        if a.salida:
            a.salida.write_text(texto, encoding="utf-8")
            print(f"Informe guardado en {a.salida}")
        else:
            sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
