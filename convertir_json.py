"""
Conversor de CSV a JSON con diferentes formatos
Genera multiples estructuras JSON optimizadas para diferentes casos de uso
"""

import pandas as pd
import json
from collections import defaultdict


class ConvertidorJSON:
    def __init__(self, archivo_csv='tipos_cambio_bcv_consolidado.csv'):
        print(f"[*] Cargando CSV: {archivo_csv}")
        self.df = pd.read_csv(archivo_csv, encoding='utf-8-sig')
        print(f"[OK] {len(self.df)} registros cargados\n")

    def generar_json_simple(self, archivo_salida='tipos_cambio_simple.json'):
        """
        JSON simple: Array de objetos (igual estructura que CSV)
        """
        print(f"[1] Generando JSON simple...")

        datos = self.df.to_dict('records')

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        print(f"    -> {archivo_salida} ({len(datos)} registros)")
        return archivo_salida

    def generar_json_por_fecha(self, archivo_salida='tipos_cambio_por_fecha.json'):
        """
        JSON organizado por fecha:
        {
          "2025-03-07": {
            "USD": {"pais": "E.U.A.", "compra_bs": 64.58, "venta_bs": 64.75},
            "EUR": {...}
          }
        }
        """
        print(f"[2] Generando JSON indexado por fecha...")

        datos_por_fecha = {}

        for fecha in self.df['fecha'].unique():
            datos_fecha = self.df[self.df['fecha'] == fecha]

            monedas = {}
            for _, row in datos_fecha.iterrows():
                monedas[row['moneda']] = {
                    'pais': row['pais'],
                    'compra_bs': round(row['compra_bs'], 8),
                    'venta_bs': round(row['venta_bs'], 8),
                    'promedio_bs': round((row['compra_bs'] + row['venta_bs']) / 2, 8)
                }

            datos_por_fecha[fecha] = monedas

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_por_fecha, f, ensure_ascii=False, indent=2)

        print(f"    -> {archivo_salida} ({len(datos_por_fecha)} fechas)")
        return archivo_salida

    def generar_json_por_moneda(self, archivo_salida='tipos_cambio_por_moneda.json'):
        """
        JSON organizado por moneda:
        {
          "USD": {
            "pais": "E.U.A.",
            "historico": [
              {"fecha": "2025-03-07", "compra_bs": 64.58, "venta_bs": 64.75},
              ...
            ]
          }
        }
        """
        print(f"[3] Generando JSON indexado por moneda...")

        datos_por_moneda = {}

        for moneda in self.df['moneda'].unique():
            datos_moneda = self.df[self.df['moneda'] == moneda].sort_values('fecha', ascending=False)

            pais = datos_moneda.iloc[0]['pais']

            historico = []
            for _, row in datos_moneda.iterrows():
                historico.append({
                    'fecha': row['fecha'],
                    'compra_bs': round(row['compra_bs'], 8),
                    'venta_bs': round(row['venta_bs'], 8),
                    'promedio_bs': round((row['compra_bs'] + row['venta_bs']) / 2, 8),
                    'fuente': row['fuente']
                })

            datos_por_moneda[moneda] = {
                'pais': pais,
                'total_registros': len(historico),
                'fecha_inicio': datos_moneda['fecha'].min(),
                'fecha_fin': datos_moneda['fecha'].max(),
                'historico': historico
            }

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_por_moneda, f, ensure_ascii=False, indent=2)

        print(f"    -> {archivo_salida} ({len(datos_por_moneda)} monedas)")
        return archivo_salida

    def generar_json_compacto(self, archivo_salida='tipos_cambio_compacto.json'):
        """
        JSON compacto (sin indentación) para transmisión/almacenamiento eficiente
        """
        print(f"[4] Generando JSON compacto...")

        datos = self.df.to_dict('records')

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))

        print(f"    -> {archivo_salida} (compacto)")
        return archivo_salida

    def generar_json_resumen(self, archivo_salida='tipos_cambio_resumen.json'):
        """
        JSON con metadata y estadísticas:
        {
          "metadata": {...},
          "estadisticas": {...},
          "datos": [...]
        }
        """
        print(f"[5] Generando JSON con resumen y estadisticas...")

        # Calcular estadísticas
        stats_por_moneda = {}
        for moneda in self.df['moneda'].unique():
            datos_moneda = self.df[self.df['moneda'] == moneda]

            stats_por_moneda[moneda] = {
                'pais': datos_moneda.iloc[0]['pais'],
                'registros': len(datos_moneda),
                'compra_min': round(datos_moneda['compra_bs'].min(), 2),
                'compra_max': round(datos_moneda['compra_bs'].max(), 2),
                'compra_promedio': round(datos_moneda['compra_bs'].mean(), 2),
                'venta_min': round(datos_moneda['venta_bs'].min(), 2),
                'venta_max': round(datos_moneda['venta_bs'].max(), 2),
                'venta_promedio': round(datos_moneda['venta_bs'].mean(), 2)
            }

        resumen = {
            'metadata': {
                'version': '1.0',
                'generado': pd.Timestamp.now().isoformat(),
                'total_registros': len(self.df),
                'fecha_inicio': self.df['fecha'].min(),
                'fecha_fin': self.df['fecha'].max(),
                'total_monedas': self.df['moneda'].nunique(),
                'total_dias': self.df['fecha'].nunique(),
                'fuentes': self.df['fuente'].unique().tolist()
            },
            'monedas_disponibles': sorted(self.df['moneda'].unique().tolist()),
            'estadisticas': stats_por_moneda,
            'datos': self.df.to_dict('records')
        }

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, ensure_ascii=False, indent=2)

        print(f"    -> {archivo_salida} (con metadata)")
        return archivo_salida

    def generar_json_ultima_fecha(self, archivo_salida='tipos_cambio_ultima.json'):
        """
        JSON solo con los datos de la fecha más reciente (útil para APIs)
        """
        print(f"[6] Generando JSON con ultima fecha disponible...")

        ultima_fecha = self.df['fecha'].max()
        datos_ultimos = self.df[self.df['fecha'] == ultima_fecha]

        resultado = {
            'fecha': ultima_fecha,
            'fecha_formato': pd.to_datetime(ultima_fecha).strftime('%d de %B de %Y'),
            'total_monedas': len(datos_ultimos),
            'tasas': {}
        }

        for _, row in datos_ultimos.iterrows():
            resultado['tasas'][row['moneda']] = {
                'pais': row['pais'],
                'compra_bs': round(row['compra_bs'], 2),
                'venta_bs': round(row['venta_bs'], 2),
                'promedio_bs': round((row['compra_bs'] + row['venta_bs']) / 2, 2)
            }

        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"    -> {archivo_salida} (fecha: {ultima_fecha})")
        return archivo_salida

    def generar_todos(self):
        """Genera todos los formatos JSON"""
        print("="*70)
        print(" CONVERSION CSV -> JSON ".center(70, "="))
        print("="*70 + "\n")

        archivos = []

        archivos.append(self.generar_json_simple())
        archivos.append(self.generar_json_por_fecha())
        archivos.append(self.generar_json_por_moneda())
        archivos.append(self.generar_json_compacto())
        archivos.append(self.generar_json_resumen())
        archivos.append(self.generar_json_ultima_fecha())

        print("\n" + "="*70)
        print(f"[OK] Conversion completa: {len(archivos)} archivos JSON generados")
        print("="*70)

        # Mostrar tamaños
        print("\n[*] Tamanos de archivos:")
        import os
        for archivo in archivos:
            size_kb = os.path.getsize(archivo) / 1024
            print(f"    {archivo:40} {size_kb:>8.1f} KB")

        return archivos


def main():
    conversor = ConvertidorJSON()
    conversor.generar_todos()

    print("\n[*] Ejemplos de uso de cada archivo:")
    print("    1. tipos_cambio_simple.json          -> Datos completos en formato array")
    print("    2. tipos_cambio_por_fecha.json       -> Busqueda rapida por fecha")
    print("    3. tipos_cambio_por_moneda.json      -> Historico completo por moneda")
    print("    4. tipos_cambio_compacto.json        -> Version compacta (menor tamano)")
    print("    5. tipos_cambio_resumen.json         -> Con metadata y estadisticas")
    print("    6. tipos_cambio_ultima.json          -> Solo ultima fecha (API)")
    print()


if __name__ == "__main__":
    main()
