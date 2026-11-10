from pathlib import Path

import pytest

from cumplimiento_1273.__main__ import main
from cumplimiento_1273.informe import informe, matriz
from cumplimiento_1273.modelo import cargar_chequeo, cargar_controles, cargar_delitos, evaluar

EJEMPLO = Path(__file__).parents[1] / "ejemplos" / "autoevaluacion_empresa_anonima.csv"


def test_matriz_cubre_los_articulos_del_titulo_vii_bis():
    articulos = [d.articulo for d in cargar_delitos()]
    assert articulos == ["269A", "269B", "269C", "269D", "269E", "269F", "269G", "269I", "269J"]


def test_penas_verificadas_contra_el_texto_oficial():
    d = {x.articulo: x for x in cargar_delitos()}
    assert d["269A"].prision == (48, 96) and d["269A"].multa_smmlv == (100, 1000)
    assert d["269C"].prision == (36, 72) and d["269C"].multa_smmlv is None
    assert d["269J"].prision == (48, 120) and d["269J"].multa_smmlv == (200, 1500)
    assert d["269I"].prision is None  # remite al art. 240


def test_todos_los_controles_de_la_matriz_existen_en_el_catalogo():
    controles = cargar_controles()
    faltan = {c for d in cargar_delitos() for c in d.controles} - set(controles)
    assert not faltan


def test_cobertura_completa_y_vacia():
    delitos = cargar_delitos()
    todo = {c: "implementado" for d in delitos for c in d.controles}
    assert all(r.cobertura == 1 and r.riesgo == "bajo" for r in evaluar(delitos, todo))
    assert all(r.cobertura == 0 and r.riesgo == "alto" for r in evaluar(delitos, {}))


def test_parcial_vale_la_mitad_y_no_aplica_se_excluye():
    d = [x for x in cargar_delitos() if x.articulo == "269C"]
    estados = {c: "parcial" for c in d[0].controles} | {"7.12": "no_aplica"}
    (r,) = evaluar(d, estados)
    assert r.cobertura == pytest.approx(0.5)
    assert "7.12" not in r.brechas


def test_estado_invalido_se_rechaza(tmp_path):
    p = tmp_path / "c.csv"
    p.write_text("codigo,estado\n5.15,quizas\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no válido"):
        cargar_chequeo(p)


def test_informe_del_ejemplo(tmp_path):
    salida = tmp_path / "informe.md"
    assert main(["evaluar", str(EJEMPLO), "-o", str(salida)]) == 0
    texto = salida.read_text(encoding="utf-8")
    assert "Empresa anónima" in texto and "Controles prioritarios" in texto
    assert "| 269A |" in texto


def test_matriz_markdown():
    assert "8.15 Registro de eventos" in matriz(cargar_delitos(), cargar_controles())
