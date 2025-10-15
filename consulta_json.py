"""
Consulta rapida de datos JSON generados
Permite buscar en los archivos JSON sin cargar CSV
"""

import json
import sys
from datetime import datetime


class ConsultaJSON:
    def __init__(self):
        self.json_por_fecha = 'tipos_cambio_por_fecha.json'
        self.json_por_moneda = 'tipos_cambio_por_moneda.json'
        self.json_ultima = 'tipos_cambio_ultima.json'
        self.json_resumen = 'tipos_cambio_resumen.json'

    def consultar_fecha(self, fecha):
        """Busca tasas de cambio por fecha (formato: YYYY-MM-DD o marzo 7 2025)"""
        fecha_iso = self._normalizar_fecha(fecha)

        if not fecha_iso:
            print(f"[X] Formato de fecha invalido: {fecha}")
            return None

        try:
            with open(self.json_por_fecha, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            if fecha_iso not in datos:
                print(f"\n[!] No hay datos para la fecha: {fecha_iso}")
                self._sugerir_fechas(fecha_iso, list(datos.keys()))
                return None

            tasas = datos[fecha_iso]

            print(f"\n{'='*80}")
            print(f" TIPOS DE CAMBIO - {fecha_iso} ".center(80, '='))
            print('='*80)
            print(f"\n{'Moneda':<6} {'Pais':<25} {'Compra (Bs.)':>15} {'Venta (Bs.)':>15} {'Promedio':>15}")
            print('-'*80)

            for moneda, info in sorted(tasas.items()):
                print(f"{moneda:<6} {info['pais']:<25} {info['compra_bs']:>15.2f} "
                      f"{info['venta_bs']:>15.2f} {info['promedio_bs']:>15.2f}")

            print(f"\nTotal: {len(tasas)} monedas\n")
            return tasas

        except FileNotFoundError:
            print(f"[X] Archivo no encontrado: {self.json_por_fecha}")
            print("    Ejecuta 'python convertir_json.py' primero")
            return None

    def consultar_moneda(self, codigo_moneda):
        """Muestra historico de una moneda"""
        try:
            with open(self.json_por_moneda, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            moneda = codigo_moneda.upper()

            if moneda not in datos:
                print(f"[X] Moneda no encontrada: {moneda}")
                print(f"    Monedas disponibles: {', '.join(sorted(datos.keys()))}")
                return None

            info = datos[moneda]

            print(f"\n{'='*80}")
            print(f" HISTORICO {moneda} - {info['pais']} ".center(80, '='))
            print('='*80)
            print(f"\nPeriodo: {info['fecha_inicio']} a {info['fecha_fin']}")
            print(f"Total registros: {info['total_registros']}")

            # Mostrar ultimas 10 fechas
            print(f"\n{'Fecha':<15} {'Compra (Bs.)':>15} {'Venta (Bs.)':>15} {'Promedio':>15}")
            print('-'*80)

            for registro in info['historico'][:10]:
                print(f"{registro['fecha']:<15} {registro['compra_bs']:>15.2f} "
                      f"{registro['venta_bs']:>15.2f} {registro['promedio_bs']:>15.2f}")

            if info['total_registros'] > 10:
                print(f"\n... y {info['total_registros'] - 10} registros mas")

            print()
            return info

        except FileNotFoundError:
            print(f"[X] Archivo no encontrado: {self.json_por_moneda}")
            return None

    def mostrar_ultima_fecha(self):
        """Muestra las tasas de la fecha mas reciente"""
        try:
            with open(self.json_ultima, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            print(f"\n{'='*80}")
            print(f" TASAS ACTUALES - {datos['fecha']} ".center(80, '='))
            print('='*80)
            print(f"\n{'Moneda':<6} {'Pais':<25} {'Compra (Bs.)':>15} {'Venta (Bs.)':>15} {'Promedio':>15}")
            print('-'*80)

            for moneda, info in sorted(datos['tasas'].items()):
                print(f"{moneda:<6} {info['pais']:<25} {info['compra_bs']:>15.2f} "
                      f"{info['venta_bs']:>15.2f} {info['promedio_bs']:>15.2f}")

            print(f"\nTotal: {datos['total_monedas']} monedas\n")
            return datos

        except FileNotFoundError:
            print(f"[X] Archivo no encontrado: {self.json_ultima}")
            return None

    def mostrar_estadisticas(self):
        """Muestra estadisticas del dataset"""
        try:
            with open(self.json_resumen, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            meta = datos['metadata']
            stats = datos['estadisticas']

            print(f"\n{'='*80}")
            print(" ESTADISTICAS DEL DATASET ".center(80, '='))
            print('='*80)

            print(f"\nInformacion General:")
            print(f"  Total de registros:  {meta['total_registros']}")
            print(f"  Periodo:             {meta['fecha_inicio']} a {meta['fecha_fin']}")
            print(f"  Dias habiles:        {meta['total_dias']}")
            print(f"  Monedas:             {meta['total_monedas']}")

            print(f"\nMonedas disponibles:")
            print(f"  {', '.join(datos['monedas_disponibles'])}")

            print(f"\nEstadisticas por Moneda (Top 5 por compra promedio):")
            print(f"\n{'Moneda':<6} {'Pais':<20} {'Min':>10} {'Max':>10} {'Promedio':>12}")
            print('-'*80)

            # Ordenar por compra promedio (descendente)
            monedas_ordenadas = sorted(
                stats.items(),
                key=lambda x: x[1]['compra_promedio'],
                reverse=True
            )

            for moneda, info in monedas_ordenadas[:5]:
                print(f"{moneda:<6} {info['pais']:<20} {info['compra_min']:>10.2f} "
                      f"{info['compra_max']:>10.2f} {info['compra_promedio']:>12.2f}")

            print()
            return datos

        except FileNotFoundError:
            print(f"[X] Archivo no encontrado: {self.json_resumen}")
            return None

    def _normalizar_fecha(self, fecha_str):
        """Convierte diferentes formatos de fecha a ISO (YYYY-MM-DD)"""
        formatos = [
            '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', '%d-%m-%Y'
        ]

        for fmt in formatos:
            try:
                fecha = datetime.strptime(fecha_str.strip(), fmt)
                return fecha.strftime('%Y-%m-%d')
            except:
                continue

        # Parseo de texto: "marzo 8 2025"
        try:
            meses = {
                'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
                'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
                'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
            }
            partes = fecha_str.lower().split()
            if len(partes) == 3:
                mes_texto, dia, anio = partes[0], partes[1], partes[2]
                if mes_texto in meses:
                    mes = meses[mes_texto]
                    fecha = datetime(int(anio), mes, int(dia))
                    return fecha.strftime('%Y-%m-%d')
        except:
            pass

        return None

    def _sugerir_fechas(self, fecha_iso, fechas_disponibles, n=5):
        """Sugiere fechas cercanas"""
        from datetime import datetime, timedelta

        fecha_dt = datetime.strptime(fecha_iso, '%Y-%m-%d')

        fechas_dt = [datetime.strptime(f, '%Y-%m-%d') for f in fechas_disponibles]
        fechas_cercanas = sorted(fechas_dt, key=lambda x: abs((x - fecha_dt).days))[:n]

        print(f"\n[*] Fechas disponibles mas cercanas:")
        for f in fechas_cercanas:
            dias_diff = (f - fecha_dt).days
            if dias_diff > 0:
                diff_str = f"(+{dias_diff} dias)"
            elif dias_diff < 0:
                diff_str = f"({dias_diff} dias)"
            else:
                diff_str = "(mismo dia)"

            print(f"   - {f.strftime('%Y-%m-%d')} {diff_str}")


def main():
    if len(sys.argv) < 2:
        print("\nUso:")
        print("  python consulta_json.py fecha <fecha>        # Buscar por fecha")
        print("  python consulta_json.py moneda <codigo>      # Historico de moneda")
        print("  python consulta_json.py ultima               # Mostrar ultima fecha")
        print("  python consulta_json.py stats                # Mostrar estadisticas")
        print("\nEjemplos:")
        print('  python consulta_json.py fecha "marzo 7 2025"')
        print('  python consulta_json.py moneda USD')
        print('  python consulta_json.py ultima')
        print()
        return

    consulta = ConsultaJSON()
    comando = sys.argv[1].lower()

    if comando == 'fecha' and len(sys.argv) >= 3:
        fecha = ' '.join(sys.argv[2:])
        consulta.consultar_fecha(fecha)

    elif comando == 'moneda' and len(sys.argv) >= 3:
        moneda = sys.argv[2]
        consulta.consultar_moneda(moneda)

    elif comando == 'ultima':
        consulta.mostrar_ultima_fecha()

    elif comando == 'stats':
        consulta.mostrar_estadisticas()

    else:
        print(f"[X] Comando invalido: {comando}")


if __name__ == "__main__":
    main()
