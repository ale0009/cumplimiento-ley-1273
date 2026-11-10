# Ley 1273 de 2009 frente a ISO/IEC 27001:2022

Herramienta de apoyo para auditoría de seguridad: relaciona cada delito informático del Código Penal colombiano (Título VII bis, creado por la Ley 1273 de 2009) con los controles del Anexo A de ISO/IEC 27001:2022 que reducen el riesgo de que ocurra en una organización, y genera un informe de brechas a partir de una lista de chequeo.

## Problema
Una empresa puede ser víctima de estos delitos y, a la vez, responder por no haber protegido datos de terceros. La pregunta de auditoría no es solo "¿nos pueden atacar?", sino "¿podemos demostrar que controlamos el acceso, registramos los eventos y protegemos los datos?". La ley dice qué conductas se castigan; ISO 27001 dice qué controles las previenen o las detectan. Este repositorio une las dos cosas.

## Qué contiene
- `datos/delitos.csv`: los artículos 269A a 269J (excepto 269H, que son agravantes), con la conducta resumida, la pena de prisión y la multa en SMMLV, verificadas contra el texto publicado por la [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=34492).
- `datos/controles_iso27001.csv`: los 31 controles del Anexo A que usa la matriz.
- `src/cumplimiento_1273/`: carga de datos, evaluación de cobertura y generación del informe en Markdown.

## Cómo ejecutarlo
Requiere Python 3.11 y [uv](https://docs.astral.sh/uv/).
```bash
uv run python -m cumplimiento_1273 matriz                       # matriz delito → controles
uv run python -m cumplimiento_1273 plantilla mi_chequeo.csv     # lista de chequeo vacía
uv run python -m cumplimiento_1273 evaluar ejemplos/autoevaluacion_empresa_anonima.csv -o informe.md
uv run pytest -q
```
En la lista de chequeo, cada control tiene un estado: `implementado`, `parcial`, `no_implementado` o `no_aplica`.

## Cómo se calcula el riesgo
Para cada delito, la cobertura es (controles implementados + 0,5 × parciales) / controles aplicables. Los marcados `no_aplica` no cuentan, y un control ausente de la lista se toma como no implementado. Riesgo **alto** si la cobertura es menor que 50 %, **medio** si es menor que 80 % y **bajo** en otro caso. El informe ordena los controles pendientes según cuántos delitos dejan expuestos, para priorizar.

## Ejemplo
`ejemplos/autoevaluacion_empresa_anonima.csv` es una autoevaluación ficticia de una empresa mediana. Su informe (`evaluar`) marca 4 delitos con riesgo alto (269B, 269E, 269G y 269J), 3 con riesgo medio y 2 con riesgo bajo. Las brechas que más delitos dejan expuestos son el registro de eventos (8.15) y el monitoreo (8.16), con 4 cada una, y la autenticación segura (8.5), con 3.

## Limitaciones
- La relación delito → control es un criterio técnico de auditoría, no una interpretación jurídica. **No es asesoría legal.**
- No incluye la Ley 1581 de 2012 (protección de datos personales) ni la Ley 1266 de 2008 (habeas data); son candidatas para una versión futura.
- La cobertura mide si un control existe, no qué tan eficaz es; una auditoría real necesita evidencia de cada control.

## Origen
Basado en trabajos académicos de la Universidad ECCI sobre responsabilidad legal en TIC y prevención de delitos informáticos; este último lo hice con mi compañero [**David Alexander Rincón Corredor (Kuronoma)**](https://www.linkedin.com/in/davidalexanderrinconcorredorkuronoma/). Esta es una reimplementación individual y abierta.
