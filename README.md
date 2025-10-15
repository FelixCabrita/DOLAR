# Sistema de Consulta de Tipos de Cambio BCV

Sistema automatizado completo para extraer, consolidar y consultar tipos de cambio del Banco Central de Venezuela.

## Inicio Rapido

```bash
# 1. Instalar dependencias
pip install pandas xlrd

# 2. Extraer datos de archivos Excel
python extractor_bcv.py

# 3. Generar archivos JSON
python convertir_json.py

# 4. Consultar datos
python consulta_bcv.py "marzo 7 2025"
```

## Dataset Consolidado

- **3,948 registros** de tipos de cambio
- **Periodo**: Enero 3 - Octubre 14, 2025
- **188 dias habiles**
- **21 monedas** internacionales

## Formatos Disponibles

### CSV (293 KB)
`tipos_cambio_bcv_consolidado.csv` - Datos tabulares completos

### JSON (6 archivos, ~3.6 MB)
- **simple.json**: Array completo de datos
- **por_fecha.json**: Indexado por fecha (busqueda rapida)
- **por_moneda.json**: Historico por moneda
- **compacto.json**: Version sin espacios
- **resumen.json**: Con metadata y estadisticas
- **ultima.json**: Solo ultima fecha (2.8 KB)

## Consultas

### Consulta por Fecha
```bash
# Usando CSV
python consulta_bcv.py "marzo 7 2025"

# Usando JSON (mas rapido)
python consulta_json.py fecha "marzo 7 2025"
```

**Salida:**
```
===============================================================================
                        TIPOS DE CAMBIO - 2025-03-07
===============================================================================
Moneda Pais                         Compra (Bs.)     Venta (Bs.)    Promedio
-------------------------------------------------------------------------------
USD    E.U.A.                             64.58           64.75        64.67
EUR    Zona Euro                          70.03           70.21        70.12
CNY    China                               8.91            8.94         8.92
...
```

### Historico de Moneda
```bash
python consulta_json.py moneda USD
```

### Tasas Actuales
```bash
python consulta_json.py ultima
```

### Estadisticas
```bash
python consulta_json.py stats
```

## Archivos del Sistema

### Scripts Python
- **extractor_bcv.py** (11 KB) - Extrae datos de Excel trimestrales
- **convertir_json.py** (8.9 KB) - Convierte CSV a 6 formatos JSON
- **consulta_bcv.py** (9.6 KB) - Consulta CSV con menu interactivo
- **consulta_json.py** (8.9 KB) - Consulta JSON (mas rapida)
- **demo_marzo8.py** (2.3 KB) - Demostracion del sistema

### Datos
- **Data_xls/** - 4 archivos Excel del BCV (trimestrales)
- **tipos_cambio_bcv_consolidado.csv** (293 KB)
- **tipos_cambio_*.json** (6 archivos, 3.6 MB total)

### Documentacion
- **README.md** - Este archivo (inicio rapido)
- **INSTRUCCIONES.md** - Guia detallada completa
- **proyecto_bcv.md** - Especificacion tecnica original

## Monedas Disponibles

ANG (Curazao), ARS (Argentina), BOB (Bolivia), BRL (Brasil), CAD (Canada), CLP (Chile), CNY (China), COP (Colombia), CUC (Cuba), DOP (Rep. Dominicana), EUR (Zona Euro), INR (India), JPY (Japon), MXP (Mexico), NIO (Nicaragua), PEN (Peru), RUB (Rusia), TRY (Turquia), TTD (Trinidad y Tobago), USD (E.U.A.), UYU (Uruguay)

## Casos de Uso

### 1. Consulta de Fecha no Habil (marzo 8, 2025)
```bash
python consulta_json.py fecha "marzo 8 2025"
```
El sistema detecta que es fin de semana y sugiere fechas cercanas automaticamente.

### 2. Analisis de Tendencias
```bash
python consulta_bcv.py
# Opcion [2]: Consultar historico de moneda
# Ingresar: USD
# Rango: enero 1 2025 - octubre 14 2025
```

### 3. API/Dashboard (ultima fecha)
```bash
# Usar tipos_cambio_ultima.json (solo 2.8 KB)
curl http://tu-api.com/tipos_cambio_ultima.json
```

## Caracteristicas

- Extraccion automatica de multiples archivos Excel
- Normalizacion de fechas (sheet_name, fecha_valor, fecha_operacion)
- Multiples formatos de entrada: "marzo 7 2025", "07/03/2025", "2025-03-07"
- Sugerencias automaticas de fechas cercanas
- 6 formatos JSON optimizados para diferentes casos
- Consultas rapidas sin cargar datos completos
- Estadisticas y metadata incluidas

## Requisitos

- Python 3.7+
- pandas
- xlrd

## Documentacion Completa

Ver [INSTRUCCIONES.md](INSTRUCCIONES.md) para guia detallada con ejemplos.

## Licencia

Sistema desarrollado para automatizar la extraccion de tipos de cambio del BCV.
