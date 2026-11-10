"""Generación de la matriz y del informe de brechas en Markdown."""
from __future__ import annotations

from collections import Counter

from .modelo import Delito, Resultado


def _pena(d: Delito) -> str:
    if d.prision is None:
        return "Penas del art. 240 (hurto calificado)"
    texto = f"{d.prision[0]}–{d.prision[1]} meses"
    if d.multa_smmlv:
        texto += f" y multa de {d.multa_smmlv[0]:,}–{d.multa_smmlv[1]:,} SMMLV".replace(",", ".")
    return texto


def matriz(delitos: list[Delito], controles: dict[str, str]) -> str:
    filas = ["| Artículo | Delito | Pena | Controles ISO/IEC 27001:2022 |", "|---|---|---|---|"]
    for d in delitos:
        ctrl = "; ".join(f"{c} {controles.get(c, '¿?')}" for c in d.controles)
        filas.append(f"| {d.articulo} | {d.nombre} | {_pena(d)} | {ctrl} |")
    return "\n".join(filas)


def informe(resultados: list[Resultado], controles: dict[str, str], organizacion: str) -> str:
    lineas = [f"# Informe de brechas frente a la Ley 1273 de 2009 — {organizacion}", ""]
    conteo = Counter(r.riesgo for r in resultados)
    lineas.append(
        f"Resumen: {conteo['alto']} delitos con riesgo alto, {conteo['medio']} medio y {conteo['bajo']} bajo "
        "(cobertura = controles implementados + la mitad de los parciales, sobre los que aplican)."
    )
    lineas += ["", "| Artículo | Delito | Cobertura | Riesgo |", "|---|---|---:|---|"]
    orden = {"alto": 0, "medio": 1, "bajo": 2, "no evaluado": 3}
    for r in sorted(resultados, key=lambda r: (orden[r.riesgo], r.delito.articulo)):
        cob = "—" if r.cobertura is None else f"{r.cobertura:.0%}"
        lineas.append(f"| {r.delito.articulo} | {r.delito.nombre} | {cob} | {r.riesgo} |")
    brechas = Counter(c for r in resultados for c in r.brechas)
    if brechas:
        lineas += ["", "## Controles prioritarios", "", "Ordenados por cuántos delitos dejan expuestos:", ""]
        for c, n in brechas.most_common():
            lineas.append(f"- **{c} {controles.get(c, '¿?')}**: afecta {n} delito(s).")
    lineas += ["", "> Herramienta de apoyo para auditoría y divulgación. No es asesoría legal."]
    return "\n".join(lineas) + "\n"
