# Sistema de Consulta de Tipos de Cambio BCV

Sistema automatizado para extraer, consolidar y consultar tipos de cambio del Banco Central de Venezuela (BCV).

## Archivos del Sistema

- **extractor_bcv.py**: Extrae y consolida datos de archivos Excel trimestrales
- **consulta_bcv.py**: Interfaz interactiva para consultas
- **tipos_cambio_bcv_consolidado.csv**: Base de datos generada (3,948 registros)
- **Data_xls/**: Directorio con archivos Excel del BCV

## Instalacion de Dependencias

```bash
pip install pandas xlrd
```

## Uso

### 1. Extraer y Consolidar Datos

Ejecutar una vez para procesar todos los archivos Excel:

```bash
python extractor_bcv.py
```

Esto generara el archivo `tipos_cambio_bcv_consolidado.csv` con todos los datos consolidados.

### 2. Consultar Datos

#### Opcion A: Menu Interactivo

```bash
python consulta_bcv.py
```

Menu con opciones:
- [1] Consultar por fecha
- [2] Consultar historico de una moneda
- [3] Listar monedas disponibles
- [4] Listar fechas disponibles
- [5] Salir

#### Opcion B: Consulta Rapida (Linea de Comandos)

```bash
python consulta_bcv.py marzo 7 2025
python consulta_bcv.py 07/03/2025
python consulta_bcv.py 2025-03-07
```

## Ejemplos de Consulta

### Ejemplo 1: Consultar por fecha

```bash
python consulta_bcv.py "marzo 7 2025"
```

**Salida:**
```
================================================================================
                         TIPOS DE CAMBIO - marzo 7 2025
================================================================================
Moneda                 Pais Compra (Bs.) Venta (Bs.) Promedio (Bs.)
   USD               E.U.A.        64.58       64.75          64.67
   EUR            Zona Euro        70.03       70.21          70.12
   CNY                China         8.91        8.94           8.92
   ...

Total de registros: 21
```

### Ejemplo 2: Historico de USD

Desde el menu interactivo:
1. Seleccionar opcion [2]
2. Ingresar: USD
3. Fecha desde: enero 1 2025
4. Fecha hasta: octubre 14 2025

### Ejemplo 3: Fecha no disponible (marzo 8, 2025)

```bash
python consulta_bcv.py "marzo 8 2025"
```

**Salida:**
```
[!] No hay datos para la fecha: 2025-03-08

[*] Fechas disponibles mas cercanas:
   - 2025-03-07 (-1 dias)
   - 2025-03-10 (+2 dias)
   - 2025-03-06 (-2 dias)
```

## Formatos de Fecha Soportados

- **Texto en espanol**: marzo 8 2025, enero 15 2025
- **ISO 8601**: 2025-03-08
- **Formato DD/MM/YYYY**: 08/03/2025
- **Formato MM/DD/YYYY**: 03/08/2025
- **Formato con guiones**: 08-03-2025

## Estructura de Datos

### Campos en el CSV:

- **fecha**: Fecha ISO (YYYY-MM-DD)
- **moneda**: Codigo de moneda (USD, EUR, CNY, etc.)
- **pais**: Nombre del pais o region
- **compra_bs**: Tasa de compra en Bolivares por Moneda Extranjera
- **venta_bs**: Tasa de venta en Bolivares por Moneda Extranjera
- **fuente**: Archivo Excel de origen
- **origen_fecha**: Como se obtuvo la fecha (sheet_name, fecha_valor, fecha_operacion)

## Estadisticas del Dataset

- **Total de registros**: 3,948
- **Periodo**: 2025-01-03 a 2025-10-14
- **Monedas**: 21 diferentes
- **Dias habiles**: 188

## Monedas Disponibles

ANG, ARS, BOB, BRL, CAD, CLP, CNY, COP, CUC, DOP, EUR, INR, JPY, MXP, NIO, PEN, RUB, TRY, TTD, USD, UYU

## Notas Tecnicas

1. **Dias no habiles**: Fines de semana y feriados no tienen datos
2. **Fecha Valor vs Fecha Operacion**: El sistema prioriza "Fecha Valor" cuando esta disponible
3. **Formato de numeros**: Los valores tienen precision de hasta 8 decimales
4. **Encoding**: Los archivos CSV usan UTF-8 con BOM para compatibilidad con Excel

## Solucion de Problemas

### Error: "No se encontro el archivo tipos_cambio_bcv_consolidado.csv"
**Solucion**: Ejecutar primero `python extractor_bcv.py`

### Error: "ModuleNotFoundError: No module named 'xlrd'"
**Solucion**: Instalar dependencias con `pip install xlrd pandas`

### Fecha no encontrada
**Causa**: La fecha consultada es fin de semana o dia no habil
**Solucion**: El sistema sugiere automáticamente las fechas mas cercanas disponibles

## Archivos JSON Generados

El sistema genera 6 archivos JSON con diferentes estructuras optimizadas:

### 1. tipos_cambio_simple.json (829 KB)
Array de objetos con todos los datos (estructura identica al CSV)

### 2. tipos_cambio_por_fecha.json (565 KB)
Indexado por fecha para busqueda rapida. Ejemplo:
```json
{
  "2025-03-07": {
    "USD": {"pais": "E.U.A.", "compra_bs": 64.58, "venta_bs": 64.75}
  }
}
```

### 3. tipos_cambio_por_moneda.json (747 KB)
Historico completo por moneda con estadisticas

### 4. tipos_cambio_compacto.json (609 KB)
Version sin indentacion (mas eficiente para transmision)

### 5. tipos_cambio_resumen.json (904 KB)
Incluye metadata, estadisticas y todos los datos

### 6. tipos_cambio_ultima.json (2.8 KB)
Solo la fecha mas reciente (ideal para APIs/dashboards)

## Consultas JSON

Para consultar directamente los archivos JSON sin cargar el CSV:

```bash
# Consultar por fecha
python consulta_json.py fecha "marzo 7 2025"

# Historico de una moneda
python consulta_json.py moneda USD

# Mostrar ultima fecha disponible
python consulta_json.py ultima

# Ver estadisticas del dataset
python consulta_json.py stats
```

## Conversion CSV a JSON

Para regenerar los archivos JSON:

```bash
python convertir_json.py
```

Esto genera todos los formatos JSON automaticamente (6 archivos, ~3.6 MB total).

## Autor

Sistema desarrollado para automatizar la extraccion de tipos de cambio del BCV.
