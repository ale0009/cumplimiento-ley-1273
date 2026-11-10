# ADR-0002: Implementación sin dependencias externas en tiempo de ejecución

- **Estado:** Aceptado
- **Fecha:** 2026-11-09
- **Proyecto:** Ley 1273 de 2009 frente a ISO/IEC 27001:2022

## Contexto

La herramienta debe ser ligera, fácilmente auditable e integrable en cualquier entorno sin riesgo de cadena de suministro.

## Decisión

Desarrollar toda la lógica de modelos, procesamiento CSV y generación de Markdown utilizando exclusivamente la biblioteca estándar de Python.

## Consecuencias

Dependencias de producción vacías (dependencies = []), eliminando vectores de vulnerabilidad de paquetes externos.
