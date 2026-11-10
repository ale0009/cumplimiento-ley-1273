"""Carga de la matriz y evaluación de una lista de chequeo de controles."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

PESOS = {"implementado": 1.0, "parcial": 0.5, "no_implementado": 0.0}
ESTADOS = set(PESOS) | {"no_aplica"}


@dataclass(frozen=True)
class Delito:
    articulo: str
    nombre: str
    conducta: str
    prision: tuple[int, int] | None
    multa_smmlv: tuple[int, int] | None
    controles: tuple[str, ...]


@dataclass(frozen=True)
class Resultado:
    delito: Delito
    cobertura: float | None  # 0..1; None si ningún control aplica
    brechas: tuple[str, ...]  # controles no implementados o parciales

    @property
    def riesgo(self) -> str:
        if self.cobertura is None:
            return "no evaluado"
        if self.cobertura < 0.5:
            return "alto"
        if self.cobertura < 0.8:
            return "medio"
        return "bajo"


def _rango(minimo: str, maximo: str) -> tuple[int, int] | None:
    return (int(minimo), int(maximo)) if minimo and maximo else None


def _datos(nombre: str) -> Path:
    local = Path(__file__).resolve().parents[2] / "datos" / nombre
    return local if local.exists() else Path(str(resources.files("cumplimiento_1273") / nombre))


def cargar_delitos(ruta: Path | None = None) -> list[Delito]:
    with open(ruta or _datos("delitos.csv"), encoding="utf-8", newline="") as f:
        return [
            Delito(
                articulo=fila["articulo"],
                nombre=fila["nombre"],
                conducta=fila["conducta"],
                prision=_rango(fila["prision_min_meses"], fila["prision_max_meses"]),
                multa_smmlv=_rango(fila["multa_min_smmlv"], fila["multa_max_smmlv"]),
                controles=tuple(c.strip() for c in fila["controles"].split(";") if c.strip()),
            )
            for fila in csv.DictReader(f)
        ]


def cargar_controles(ruta: Path | None = None) -> dict[str, str]:
    with open(ruta or _datos("controles_iso27001.csv"), encoding="utf-8", newline="") as f:
        return {fila["codigo"]: fila["nombre"] for fila in csv.DictReader(f)}


def cargar_chequeo(ruta: Path) -> dict[str, str]:
    """Lee un CSV `codigo,estado`. Un control ausente cuenta como no implementado."""
    estados: dict[str, str] = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        for n, fila in enumerate(csv.DictReader(f), start=2):
            estado = fila["estado"].strip().lower()
            if estado not in ESTADOS:
                raise ValueError(f"Línea {n}: estado '{estado}' no válido; usa {sorted(ESTADOS)}")
            estados[fila["codigo"].strip()] = estado
    return estados


def evaluar(delitos: list[Delito], estados: dict[str, str]) -> list[Resultado]:
    resultados = []
    for d in delitos:
        aplicables = [c for c in d.controles if estados.get(c, "no_implementado") != "no_aplica"]
        if not aplicables:
            resultados.append(Resultado(d, None, ()))
            continue
        puntos = sum(PESOS[estados.get(c, "no_implementado")] for c in aplicables)
        brechas = tuple(c for c in aplicables if estados.get(c, "no_implementado") != "implementado")
        resultados.append(Resultado(d, puntos / len(aplicables), brechas))
    return resultados
