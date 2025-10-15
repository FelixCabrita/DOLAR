# 📊 Proyecto: Extracción Automática de Tipos de Cambio del BCV

## 🧩 Descripción General
El **Banco Central de Venezuela (BCV)** publica diariamente una tabla de **tipos de cambio de referencia** para distintas monedas extranjeras.  
Los datos se organizan en archivos Excel trimestrales, donde **cada hoja representa una fecha** y contiene la tabla con las cotizaciones correspondientes.

El objetivo del proyecto es **automatizar la lectura y consolidación de esos valores**, **almacenando explícitamente el día para cada registro**, para facilitar análisis históricos y comparaciones entre fechas.

---

## 🧾 Estructura del Archivo Original
Cada archivo (p. ej. `2_1_2d25_smc.xls`) representa un **trimestre** y contiene:

- **Una hoja por día hábil** (ejemplo: `02012025`, `03012025`, `04012025`, etc.).
- En cada hoja:
  - **Fecha de Operación** y **Fecha Valor**.
  - Tabla de cotizaciones con columnas principales:
    - `Moneda / País`
    - `Compra (BID)` y `Venta (ASK)` en **M.E./US$** y en **Bs./M.E.**
  - Notas aclaratorias sobre el tipo de cambio de referencia.

Ejemplo visual simplificado:

| Moneda | País        | Compra Bs./M.E. | Venta Bs./M.E. |
|--------|-------------|------------------|-----------------|
| USD    | E.U.A.      | 52.44            | 52.57           |
| EUR    | Zona Euro   | 54.03            | 54.16           |
| CNY    | China       | 7.18             | 7.22            |

---

## 🎯 Problema Identificado
- Los datos diarios están **distribuidos entre múltiples hojas**, dificultando la comparación histórica.
- No existe una **hoja resumen**; y la **fecha** debe inferirse por hoja o encabezado.
- Extraer y comparar valores entre días manualmente es **ineficiente**.

---

## 🚀 Solución Propuesta
Desarrollar una herramienta que:
1. **Lea automáticamente todas las hojas** de un archivo trimestral.
2. **Obtenga la fecha de cada hoja** desde uno de estos orígenes, priorizados:
   - **Nombre de la hoja** (formato `DDMMYYYY`, p. ej. `02012025`).
   - O bien los campos del encabezado: **Fecha Valor** (preferida) o **Fecha Operación**.
3. **Identifique la fila de la moneda de interés** (p. ej. USD, EUR, etc.).
4. **Extraiga los valores** de **Compra** y **Venta** en **Bs./M.E.**.
5. **Consolide los registros** en una estructura uniforme, **guardando el día de cada valor**.
6. Permita **unir varios trimestres** en un histórico continuo y exportarlo a **CSV/Excel/BD**.

---

## 🧱 Modelo de Datos (Salida Estandarizada)
Cada fila del dataset consolidado debe respetar esta estructura:

- `fecha` (string, **ISO 8601 `YYYY-MM-DD`**).  
- `moneda` (string, código o nombre corto, p. ej. `USD`, `EUR`).  
- `pais` (string opcional, p. ej. `E.U.A.`, `Zona Euro`).  
- `compra_bs` (number, **Bs./M.E.** — columna *Compra (BID)*).  
- `venta_bs` (number, **Bs./M.E.** — columna *Venta (ASK)*).  
- `fuente` (string opcional; p. ej. nombre de archivo o trimestre).  
- `origen_fecha` (string opcional; `sheet_name` | `fecha_valor` | `fecha_operacion`).

**Ejemplo de una fila:**  
```
fecha: "2025-01-02"
moneda: "USD"
pais: "E.U.A."
compra_bs: 52.44086925
venta_bs: 52.57230000
fuente: "2_1_2d25_smc.xls"
origen_fecha: "sheet_name"
```

> **Regla clave:** siempre transformar la fecha detectada al formato **`YYYY-MM-DD`** antes de guardar.

---

## 📈 Beneficios
- **Histórico confiable**: cada valor queda asociado al día exacto.
- **Automatización total**: no se requiere abrir hojas manualmente.
- **Formato consistente**: listo para análisis, gráficos y comparaciones.
- **Portabilidad**: exportable a CSV/Excel o integrable a una BD relacional.

---

## 📅 Flujo de Trabajo
1. Seleccionar archivo(s) trimestrales de origen.
2. Procesar todas las hojas; **normalizar la fecha** por hoja.
3. Extraer la moneda(s) objetivo con sus valores de compra/venta en **Bs./M.E.**.
4. Validar y **consolidar** el dataset.
5. Exportar y documentar.

---

## ✅ Validaciones y Reglas
- Si una hoja **no contiene** la moneda objetivo, **omitirla** y registrar el evento en un log.
- Si faltan columnas esperadas, marcar el registro como **inválido** y continuar.
- Priorizar **Fecha Valor** sobre **Fecha Operación** si ambas están disponibles.
- En caso de disparidades numéricas, registrar la hoja afectada para revisión manual.

---

## 🧠 Extensiones Futuras
- Descarga directa y programada desde el portal del BCV.
- Endpoints de consulta (API REST) por fecha y moneda.
- Panel de visualización con tendencias y alertas de variación diaria.
- Soporte multi-moneda en una sola ejecución.

---

**Objetivo:** Centralizar y estandarizar los tipos de cambio del BCV, **siempre almacenando el día de cada valor** en formato ISO.
