"""
Exporta solo USD del archivo tipos_cambio_por_fecha.json
Genera un JSON limpio con solo datos de USD
"""

import json
import pandas as pd


def exportar_solo_usd_desde_json():
    """Extrae USD del JSON por fecha"""
    print("[*] Cargando tipos_cambio_por_fecha.json...")

    with open('tipos_cambio_por_fecha.json', 'r', encoding='utf-8') as f:
        datos_completos = json.load(f)

    # Extraer solo USD de cada fecha
    usd_por_fecha = {}

    for fecha, monedas in datos_completos.items():
        if 'USD' in monedas:
            usd_por_fecha[fecha] = monedas['USD']

    # Guardar archivo
    with open('tipos_cambio_usd.json', 'w', encoding='utf-8') as f:
        json.dump(usd_por_fecha, f, ensure_ascii=False, indent=2)

    print(f"[OK] Exportado: {len(usd_por_fecha)} fechas con datos de USD")
    print(f"    Archivo: tipos_cambio_usd.json")

    # Calcular tamaño
    import os
    size_kb = os.path.getsize('tipos_cambio_usd.json') / 1024
    print(f"    Tamaño: {size_kb:.1f} KB")

    return usd_por_fecha


def exportar_solo_usd_desde_csv():
    """Extrae USD del CSV original (alternativa)"""
    print("\n[*] Cargando CSV y filtrando USD...")

    df = pd.read_csv('tipos_cambio_bcv_consolidado.csv', encoding='utf-8-sig')
    usd_df = df[df['moneda'] == 'USD'].copy()

    # Crear estructura indexada por fecha
    usd_por_fecha = {}

    for _, row in usd_df.iterrows():
        usd_por_fecha[row['fecha']] = {
            'pais': row['pais'],
            'compra_bs': round(row['compra_bs'], 8),
            'venta_bs': round(row['venta_bs'], 8),
            'promedio_bs': round((row['compra_bs'] + row['venta_bs']) / 2, 8),
            'fuente': row['fuente']
        }

    # Guardar archivo con mas detalle
    with open('tipos_cambio_usd_detallado.json', 'w', encoding='utf-8') as f:
        json.dump(usd_por_fecha, f, ensure_ascii=False, indent=2)

    print(f"[OK] Exportado: {len(usd_por_fecha)} fechas con USD detallado")
    print(f"    Archivo: tipos_cambio_usd_detallado.json")

    # Calcular tamaño
    import os
    size_kb = os.path.getsize('tipos_cambio_usd_detallado.json') / 1024
    print(f"    Tamaño: {size_kb:.1f} KB")

    return usd_por_fecha


def exportar_usd_compacto():
    """Versión compacta sin indentación"""
    print("\n[*] Generando version compacta...")

    with open('tipos_cambio_usd.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)

    with open('tipos_cambio_usd_compacto.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))

    import os
    size_kb = os.path.getsize('tipos_cambio_usd_compacto.json') / 1024
    print(f"[OK] Version compacta guardada")
    print(f"    Archivo: tipos_cambio_usd_compacto.json")
    print(f"    Tamaño: {size_kb:.1f} KB")


def mostrar_ejemplo():
    """Muestra un ejemplo del JSON generado"""
    print("\n" + "="*70)
    print(" EJEMPLO DE DATOS USD ".center(70, "="))
    print("="*70)

    with open('tipos_cambio_usd.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)

    # Mostrar primeras 3 fechas
    fechas = sorted(datos.keys(), reverse=True)[:3]

    ejemplo = {fecha: datos[fecha] for fecha in fechas}

    print("\nEstructura (ultimas 3 fechas):")
    print(json.dumps(ejemplo, ensure_ascii=False, indent=2))

    print(f"\nTotal de fechas: {len(datos)}")


def main():
    print("="*70)
    print(" EXPORTACION DE USD ".center(70, "="))
    print("="*70 + "\n")

    # Opción 1: Desde JSON existente (más rápido)
    exportar_solo_usd_desde_json()

    # Opción 2: Desde CSV (incluye campo 'fuente')
    exportar_solo_usd_desde_csv()

    # Opción 3: Versión compacta
    exportar_usd_compacto()

    # Mostrar ejemplo
    mostrar_ejemplo()

    print("\n" + "="*70)
    print("[OK] Exportacion completa: 3 archivos generados")
    print("="*70)

    print("\n[*] Archivos generados:")
    print("    1. tipos_cambio_usd.json            - Solo USD (limpio)")
    print("    2. tipos_cambio_usd_detallado.json  - USD con campo 'fuente'")
    print("    3. tipos_cambio_usd_compacto.json   - Version sin espacios")
    print()


if __name__ == "__main__":
    main()
