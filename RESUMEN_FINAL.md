# Resumen Final - Sistema BCV

Sistema completo de extraccion, consulta y exportacion de tipos de cambio del BCV.

## Archivos Disponibles

### Scripts Python (6)
1. **extractor_bcv.py** - Extrae datos de Excel trimestrales
2. **convertir_json.py** - Convierte CSV a 6 formatos JSON
3. **consulta_bcv.py** - Consulta CSV (menu interactivo)
4. **consulta_json.py** - Consulta JSON (rapida)
5. **exportar_usd.py** - Exporta solo USD
6. **consulta_usd.py** - Consulta USD especializada
7. **demo_marzo8.py** - Demostracion del sistema

### Datos - Todas las Monedas (7 archivos)
1. **tipos_cambio_bcv_consolidado.csv** (293 KB) - CSV original
2. **tipos_cambio_simple.json** (829 KB) - Array completo
3. **tipos_cambio_por_fecha.json** (565 KB) - Indexado por fecha
4. **tipos_cambio_por_moneda.json** (747 KB) - Historico por moneda
5. **tipos_cambio_compacto.json** (609 KB) - Sin espacios
6. **tipos_cambio_resumen.json** (904 KB) - Con metadata
7. **tipos_cambio_ultima.json** (2.8 KB) - Solo ultima fecha

### Datos - Solo USD (3 archivos)
1. **tipos_cambio_usd.json** (26 KB) - USD limpio
2. **tipos_cambio_usd_detallado.json** (32 KB) - USD con fuente
3. **tipos_cambio_usd_compacto.json** (19 KB) - USD sin espacios

### Documentacion (4)
1. **README.md** - Inicio rapido
2. **INSTRUCCIONES.md** - Guia completa
3. **RESUMEN_FINAL.md** - Este archivo
4. **proyecto_bcv.md** - Especificacion original

## Flujo de Trabajo

```
1. Extraer datos Excel -> CSV
   python extractor_bcv.py

2. Convertir CSV -> JSON (todas las monedas)
   python convertir_json.py

3. Exportar solo USD
   python exportar_usd.py
```

## Consultas

### Todas las Monedas

```bash
# CSV (menu interactivo)
python consulta_bcv.py

# JSON (rapida)
python consulta_json.py fecha "marzo 7 2025"
python consulta_json.py moneda USD
python consulta_json.py ultima
python consulta_json.py stats
```

### Solo USD

```bash
# Fecha especifica
python consulta_usd.py "marzo 7 2025"

# Rango de fechas
python consulta_usd.py "enero 1 2025" "marzo 31 2025"

# Ultimas N fechas
python consulta_usd.py ultimas 10

# Estadisticas
python consulta_usd.py stats
```

## Datos del Sistema

### Dataset Completo
- **3,948 registros** totales
- **21 monedas** diferentes
- **188 dias habiles**
- **Periodo**: 2025-01-03 a 2025-10-14

### Dataset USD
- **188 registros** (uno por dia habil)
- **Tasa inicial**: Bs. 52.51 (2025-01-03)
- **Tasa final**: Bs. 197.00 (2025-10-14)
- **Variacion**: +275.19%
- **Promedio general**: Bs. 102.44

## Monedas Disponibles (21)

ANG (Curazao), ARS (Argentina), BOB (Bolivia), BRL (Brasil), CAD (Canada),
CLP (Chile), CNY (China), COP (Colombia), CUC (Cuba), DOP (Rep. Dominicana),
EUR (Zona Euro), INR (India), JPY (Japon), MXP (Mexico), NIO (Nicaragua),
PEN (Peru), RUB (Rusia), TRY (Turquia), TTD (Trinidad y Tobago), USD (E.U.A.),
UYU (Uruguay)

## Ejemplos de Salida

### Consulta USD por Fecha
```
======================================================================
====================== DOLAR (USD) - 2025-03-07 ======================
======================================================================

  Pais:             E.U.A.
  Compra (Bs.):     64.58
  Venta (Bs.):      64.75
  Promedio (Bs.):   64.67
```

### Estadisticas USD
```
Informacion General:
  Total de fechas:       188
  Fecha inicial:         2025-01-03
  Fecha final:           2025-10-14

Tasa Promedio (Bs.):
  Minima:                52.51
  Maxima:                197.00
  General:               102.44

Variacion Total:
  2025-01-03: Bs. 52.51
  2025-10-14: Bs. 197.00
  Cambio: +275.19%
```

## Tamanos de Archivos

### Total por Categoria
- **Scripts Python**: ~52 KB (7 archivos)
- **Datos completos**: ~3.6 MB (7 archivos JSON + 1 CSV)
- **Datos USD**: ~77 KB (3 archivos JSON)
- **Documentacion**: ~15 KB (4 archivos MD)

### Comparacion de Tamaños
- CSV original: 293 KB
- JSON todas las monedas: 565 KB - 904 KB
- JSON solo USD: 19 KB - 32 KB
- **Reduccion**: 91-94% usando USD vs datos completos

## Ventajas del Sistema

1. **Multiples formatos**: CSV, JSON (6 variantes), JSON-USD (3 variantes)
2. **Consultas rapidas**: Indexacion por fecha y por moneda
3. **Datos especializados**: USD en archivos separados (19-32 KB)
4. **API-ready**: Archivo ultima.json de solo 2.8 KB
5. **Estadisticas incluidas**: Metadata y calculos automaticos
6. **Formatos flexibles**: "marzo 7 2025", "07/03/2025", "2025-03-07"

## Casos de Uso

### 1. Dashboard Web
Usar `tipos_cambio_ultima.json` (2.8 KB) para mostrar tasas actuales

### 2. Aplicacion Movil
Usar `tipos_cambio_usd_compacto.json` (19 KB) para consultas offline

### 3. API REST
Servir los JSON pre-generados directamente (sin procesamiento)

### 4. Analisis Historico
Usar `tipos_cambio_por_moneda.json` para graficos y tendencias

### 5. Busqueda Rapida
Usar `tipos_cambio_por_fecha.json` para consultas O(1) por fecha

## Instalacion Rapida

```bash
# Clonar/descargar el proyecto
cd DOLAR

# Instalar dependencias
pip install pandas xlrd

# Generar todos los datos
python extractor_bcv.py
python convertir_json.py
python exportar_usd.py

# Listo para consultar
python consulta_usd.py "hoy"
```

## Comandos Mas Usados

```bash
# Ver tasas de hoy
python consulta_usd.py ultimas 1

# Ver mes actual
python consulta_usd.py "octubre 1 2025" "octubre 14 2025"

# Ver todas las estadisticas
python consulta_usd.py stats

# Buscar fecha especifica
python consulta_usd.py "marzo 7 2025"
```

## Actualizaciones Futuras

- [ ] Descarga automatica desde portal BCV
- [ ] Actualizacion incremental (solo nuevas fechas)
- [ ] API REST con Flask/FastAPI
- [ ] Dashboard web con graficos
- [ ] Notificaciones de cambios significativos
- [ ] Exportacion a Excel con formato
- [ ] Comparacion entre monedas
- [ ] Calculo de devaluacion automatico

---

**Sistema desarrollado para automatizar la extraccion de tipos de cambio del BCV.**
