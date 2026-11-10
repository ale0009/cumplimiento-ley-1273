# ADR-0003: Empaquetado de datasets normativos con force-include en Hatchling

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Ley 1273 de 2009 frente a ISO/IEC 27001:2022

## Contexto

Los archivos CSV de delitos y controles ISO 27001 son indispensables para el funcionamiento del módulo.

## Decisión

Declarar force-include en pyproject.toml para incrustar datos/delitos.csv y datos/controles_iso27001.csv dentro de la distribución wheel.

## Consecuencias

Permite que el paquete se instale y ejecute de manera autocontenida sin depender de rutas relativas de trabajo.
