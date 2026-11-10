# ADR-0001: Fórmula cuantitativa de cobertura ponderada y rangos de riesgo

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Ley 1273 de 2009 frente a ISO/IEC 27001:2022

## Contexto

Se requiere un método sistemático para categorizar el nivel de vulnerabilidad penal frente a controles parciales o implementados.

## Decisión

Calcular cobertura como (implementados + 0.5 * parciales) / aplicables y clasificar riesgo alto (<50%), medio (<80%) y bajo (>=80%).

## Consecuencias

Proporciona una escala reproducible de priorización que valora el avance gradual de la organización sin subjetividades.
