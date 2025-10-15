"""
Consulta rapida de USD
Script especializado para consultar tasas del dolar
"""

import json
import sys
from datetime import datetime


class ConsultaUSD:
    def __init__(self, archivo='tipos_cambio_usd.json'):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                self.datos = json.load(f)
            print(f"[OK] Base de datos USD cargada: {len(self.datos)} fechas disponibles")
            print(f"     Periodo: {min(self.datos.keys())} a {max(self.datos.keys())}\n")
        except FileNotFoundError:
            print(f"[X] Archivo no encontrado: {archivo}")
            print("    Ejecuta 'python exportar_usd.py' primero")
            sys.exit(1)

    def consultar_fecha(self, fecha):
        """Consulta tasa USD por fecha"""
        fecha_iso = self._normalizar_fecha(fecha)

        if not fecha_iso:
            print(f"[X] Formato de fecha invalido: {fecha}")
            return None

        if fecha_iso not in self.datos:
            print(f"\n[!] No hay datos de USD para la fecha: {fecha_iso}")
            self._sugerir_fechas(fecha_iso)
            return None

        tasa = self.datos[fecha_iso]

        print(f"\n{'='*70}")
        print(f" DOLAR (USD) - {fecha_iso} ".center(70, '='))
        print('='*70)
        print(f"\n  Pais:             {tasa['pais']}")
        print(f"  Compra (Bs.):     {tasa['compra_bs']:,.2f}")
        print(f"  Venta (Bs.):      {tasa['venta_bs']:,.2f}")
        print(f"  Promedio (Bs.):   {tasa['promedio_bs']:,.2f}")
        print()

        return tasa

    def consultar_rango(self, fecha_desde, fecha_hasta):
        """Consulta rango de fechas"""
        fecha_desde_iso = self._normalizar_fecha(fecha_desde)
        fecha_hasta_iso = self._normalizar_fecha(fecha_hasta)

        if not fecha_desde_iso or not fecha_hasta_iso:
            print("[X] Formato de fecha invalido")
            return None

        # Filtrar fechas en el rango
        fechas_rango = [f for f in sorted(self.datos.keys())
                        if fecha_desde_iso <= f <= fecha_hasta_iso]

        if not fechas_rango:
            print(f"[!] No hay datos en el rango {fecha_desde_iso} - {fecha_hasta_iso}")
            return None

        print(f"\n{'='*70}")
        print(f" USD: {fecha_desde_iso} a {fecha_hasta_iso} ".center(70, '='))
        print('='*70)
        print(f"\n{'Fecha':<15} {'Compra (Bs.)':>15} {'Venta (Bs.)':>15} {'Promedio':>15}")
        print('-'*70)

        tasas = []
        for fecha in reversed(fechas_rango):  # Más recientes primero
            tasa = self.datos[fecha]
            print(f"{fecha:<15} {tasa['compra_bs']:>15.2f} {tasa['venta_bs']:>15.2f} {tasa['promedio_bs']:>15.2f}")
            tasas.append(tasa['promedio_bs'])

        # Estadísticas
        print('-'*70)
        print(f"{'ESTADISTICAS':<15} {'Min':>15} {'Max':>15} {'Promedio':>15}")
        print(f"{'':15} {min(tasas):>15.2f} {max(tasas):>15.2f} {sum(tasas)/len(tasas):>15.2f}")
        print(f"\nTotal de registros: {len(fechas_rango)}")
        print()

        return fechas_rango

    def mostrar_ultimas(self, n=10):
        """Muestra las últimas N fechas"""
        fechas = sorted(self.datos.keys(), reverse=True)[:n]

        print(f"\n{'='*70}")
        print(f" ULTIMAS {n} TASAS USD ".center(70, '='))
        print('='*70)
        print(f"\n{'Fecha':<15} {'Compra (Bs.)':>15} {'Venta (Bs.)':>15} {'Promedio':>15}")
        print('-'*70)

        for fecha in fechas:
            tasa = self.datos[fecha]
            print(f"{fecha:<15} {tasa['compra_bs']:>15.2f} {tasa['venta_bs']:>15.2f} {tasa['promedio_bs']:>15.2f}")

        print()

    def mostrar_estadisticas(self):
        """Muestra estadísticas generales"""
        promedios = [tasa['promedio_bs'] for tasa in self.datos.values()]
        compras = [tasa['compra_bs'] for tasa in self.datos.values()]
        ventas = [tasa['venta_bs'] for tasa in self.datos.values()]

        print(f"\n{'='*70}")
        print(" ESTADISTICAS USD ".center(70, '='))
        print('='*70)

        print(f"\nInformacion General:")
        print(f"  Total de fechas:       {len(self.datos)}")
        print(f"  Fecha inicial:         {min(self.datos.keys())}")
        print(f"  Fecha final:           {max(self.datos.keys())}")

        print(f"\nTasa de Compra (Bs.):")
        print(f"  Minima:                {min(compras):,.2f}")
        print(f"  Maxima:                {max(compras):,.2f}")
        print(f"  Promedio:              {sum(compras)/len(compras):,.2f}")

        print(f"\nTasa de Venta (Bs.):")
        print(f"  Minima:                {min(ventas):,.2f}")
        print(f"  Maxima:                {max(ventas):,.2f}")
        print(f"  Promedio:              {sum(ventas)/len(ventas):,.2f}")

        print(f"\nTasa Promedio (Bs.):")
        print(f"  Minima:                {min(promedios):,.2f}")
        print(f"  Maxima:                {max(promedios):,.2f}")
        print(f"  General:               {sum(promedios)/len(promedios):,.2f}")

        # Calcular variación
        primera_fecha = min(self.datos.keys())
        ultima_fecha = max(self.datos.keys())
        primera_tasa = self.datos[primera_fecha]['promedio_bs']
        ultima_tasa = self.datos[ultima_fecha]['promedio_bs']
        variacion = ((ultima_tasa - primera_tasa) / primera_tasa) * 100

        print(f"\nVariacion Total:")
        print(f"  {primera_fecha}: Bs. {primera_tasa:,.2f}")
        print(f"  {ultima_fecha}: Bs. {ultima_tasa:,.2f}")
        print(f"  Cambio: {variacion:+.2f}%")
        print()

    def _normalizar_fecha(self, fecha_str):
        """Convierte diferentes formatos de fecha a ISO"""
        formatos = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', '%d-%m-%Y']

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

    def _sugerir_fechas(self, fecha_iso, n=5):
        """Sugiere fechas cercanas"""
        fecha_dt = datetime.strptime(fecha_iso, '%Y-%m-%d')
        fechas_dt = [(f, datetime.strptime(f, '%Y-%m-%d')) for f in self.datos.keys()]
        fechas_cercanas = sorted(fechas_dt, key=lambda x: abs((x[1] - fecha_dt).days))[:n]

        print(f"\n[*] Fechas disponibles mas cercanas:")
        for fecha_str, fecha_dt_c in fechas_cercanas:
            dias_diff = (fecha_dt_c - fecha_dt).days
            if dias_diff > 0:
                diff_str = f"(+{dias_diff} dias)"
            elif dias_diff < 0:
                diff_str = f"({dias_diff} dias)"
            else:
                diff_str = "(mismo dia)"
            print(f"   - {fecha_str} {diff_str}")


def main():
    if len(sys.argv) < 2:
        print("\nUso:")
        print("  python consulta_usd.py <fecha>                  # Consultar fecha especifica")
        print("  python consulta_usd.py <desde> <hasta>          # Consultar rango")
        print("  python consulta_usd.py ultimas [N]              # Ultimas N fechas")
        print("  python consulta_usd.py stats                    # Estadisticas")
        print("\nEjemplos:")
        print('  python consulta_usd.py "marzo 7 2025"')
        print('  python consulta_usd.py "enero 1 2025" "marzo 31 2025"')
        print('  python consulta_usd.py ultimas 20')
        print('  python consulta_usd.py stats')
        print()
        return

    consulta = ConsultaUSD()

    if sys.argv[1].lower() == 'stats':
        consulta.mostrar_estadisticas()

    elif sys.argv[1].lower() == 'ultimas':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        consulta.mostrar_ultimas(n)

    elif len(sys.argv) == 3:
        # Rango de fechas
        fecha_desde = sys.argv[1]
        fecha_hasta = sys.argv[2]
        consulta.consultar_rango(fecha_desde, fecha_hasta)

    else:
        # Fecha única
        fecha = ' '.join(sys.argv[1:])
        consulta.consultar_fecha(fecha)


if __name__ == "__main__":
    main()
