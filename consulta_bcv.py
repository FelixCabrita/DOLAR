"""
Interfaz de Consulta Interactiva para Tipos de Cambio BCV
Permite buscar tasas de cambio por fecha y visualizar tablas
"""

import pandas as pd
import sys
from datetime import datetime


class ConsultaBCV:
    def __init__(self, archivo_csv='tipos_cambio_bcv_consolidado.csv'):
        try:
            self.df = pd.read_csv(archivo_csv, encoding='utf-8-sig')
            print(f"[OK] Base de datos cargada: {len(self.df)} registros")
            print(f"     Periodo: {self.df['fecha'].min()} a {self.df['fecha'].max()}")
            print(f"     Monedas: {self.df['moneda'].nunique()} diferentes\n")
        except FileNotFoundError:
            print(f"[X] No se encontro el archivo: {archivo_csv}")
            print("    Ejecuta primero 'extractor_bcv.py' para generar los datos")
            sys.exit(1)

    def normalizar_fecha(self, fecha_str):
        """Convierte diferentes formatos de fecha a ISO (YYYY-MM-DD)"""
        formatos = [
            '%Y-%m-%d',   # 2025-03-08
            '%d/%m/%Y',   # 08/03/2025
            '%m/%d/%Y',   # 03/08/2025
            '%Y/%m/%d',   # 2025/03/08
            '%d-%m-%Y',   # 08-03-2025
        ]

        # Intentar parseo directo
        for fmt in formatos:
            try:
                fecha = datetime.strptime(fecha_str.strip(), fmt)
                return fecha.strftime('%Y-%m-%d')
            except:
                continue

        # Intentar parseo de texto: "marzo 8 2025"
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

    def consultar_fecha(self, fecha_busqueda):
        """Consulta tipos de cambio por fecha"""
        fecha_iso = self.normalizar_fecha(fecha_busqueda)

        if not fecha_iso:
            print(f"[X] Formato de fecha invalido: {fecha_busqueda}")
            print("    Formatos validos:")
            print("    - 2025-03-08")
            print("    - 08/03/2025")
            print("    - marzo 8 2025")
            return None

        # Filtrar datos
        resultado = self.df[self.df['fecha'] == fecha_iso].copy()

        if resultado.empty:
            print(f"\n[!] No hay datos para la fecha: {fecha_iso}")
            self._sugerir_fechas_cercanas(fecha_iso)
            return None

        # Formatear resultado
        resultado_display = resultado[['moneda', 'pais', 'compra_bs', 'venta_bs']].copy()
        resultado_display.columns = ['Moneda', 'Pais', 'Compra (Bs.)', 'Venta (Bs.)']

        # Calcular promedio
        resultado_display['Promedio (Bs.)'] = (
            resultado_display['Compra (Bs.)'] + resultado_display['Venta (Bs.)']
        ) / 2

        return resultado_display

    def consultar_moneda(self, codigo_moneda, fecha_desde=None, fecha_hasta=None):
        """Consulta histórico de una moneda específica"""
        datos = self.df[self.df['moneda'].str.upper() == codigo_moneda.upper()].copy()

        if datos.empty:
            print(f"[X] Moneda no encontrada: {codigo_moneda}")
            print(f"    Monedas disponibles: {', '.join(sorted(self.df['moneda'].unique()))}")
            return None

        # Filtrar por rango de fechas si se especifica
        if fecha_desde:
            fecha_desde_iso = self.normalizar_fecha(fecha_desde)
            if fecha_desde_iso:
                datos = datos[datos['fecha'] >= fecha_desde_iso]

        if fecha_hasta:
            fecha_hasta_iso = self.normalizar_fecha(fecha_hasta)
            if fecha_hasta_iso:
                datos = datos[datos['fecha'] <= fecha_hasta_iso]

        # Formatear resultado
        resultado = datos[['fecha', 'pais', 'compra_bs', 'venta_bs']].copy()
        resultado.columns = ['Fecha', 'Pais', 'Compra (Bs.)', 'Venta (Bs.)']
        resultado['Promedio (Bs.)'] = (resultado['Compra (Bs.)'] + resultado['Venta (Bs.)']) / 2

        return resultado.sort_values('Fecha', ascending=False)

    def listar_fechas_disponibles(self, anio=None, mes=None):
        """Lista todas las fechas disponibles, opcionalmente filtradas por año/mes"""
        fechas = pd.to_datetime(self.df['fecha'])

        if anio:
            fechas = fechas[fechas.dt.year == anio]

        if mes:
            fechas = fechas[fechas.dt.month == mes]

        fechas_unicas = sorted(fechas.dt.date.unique(), reverse=True)

        return [str(f) for f in fechas_unicas]

    def listar_monedas(self):
        """Lista todas las monedas disponibles con su nombre de país"""
        monedas = self.df[['moneda', 'pais']].drop_duplicates().sort_values('moneda')
        return monedas

    def _sugerir_fechas_cercanas(self, fecha_iso, n=5):
        """Sugiere fechas cercanas a la solicitada"""
        df = self.df.copy()
        df['fecha_dt'] = pd.to_datetime(df['fecha'])
        fecha_dt = pd.to_datetime(fecha_iso)

        fechas_disponibles = df['fecha_dt'].unique()
        fechas_cercanas = sorted(fechas_disponibles, key=lambda x: abs((x - fecha_dt).days))[:n]

        print(f"\n[*] Fechas disponibles mas cercanas:")
        for f in fechas_cercanas:
            fecha_f = pd.to_datetime(f)
            dias_diff = (fecha_f - fecha_dt).days
            if dias_diff > 0:
                diff_str = f"(+{dias_diff} dias)"
            elif dias_diff < 0:
                diff_str = f"({dias_diff} dias)"
            else:
                diff_str = "(mismo dia)"

            print(f"   - {fecha_f.strftime('%Y-%m-%d')} {diff_str}")

    def mostrar_tabla(self, df, titulo=None):
        """Muestra un DataFrame formateado como tabla"""
        if df is None or df.empty:
            return

        if titulo:
            print(f"\n{'='*80}")
            print(f"{titulo:^80}")
            print('='*80)

        # Formatear números con 2 decimales
        df_display = df.copy()
        for col in df_display.columns:
            if df_display[col].dtype in ['float64', 'float32']:
                df_display[col] = df_display[col].map(lambda x: f"{x:,.2f}")

        print(df_display.to_string(index=False))
        print(f"\nTotal de registros: {len(df)}\n")


def menu_interactivo():
    """Menú interactivo para consultas"""
    consulta = ConsultaBCV()

    while True:
        print("\n" + "="*80)
        print(" CONSULTA DE TIPOS DE CAMBIO BCV ".center(80, "="))
        print("="*80)
        print("\n[1] Consultar por fecha")
        print("[2] Consultar historico de una moneda")
        print("[3] Listar todas las monedas disponibles")
        print("[4] Listar fechas disponibles")
        print("[5] Salir")

        opcion = input("\nSelecciona una opcion: ").strip()

        if opcion == '1':
            fecha = input("\nIngresa la fecha (ej: marzo 7 2025, 07/03/2025, 2025-03-07): ").strip()
            resultado = consulta.consultar_fecha(fecha)
            if resultado is not None:
                consulta.mostrar_tabla(resultado, f"TIPOS DE CAMBIO - {fecha}")

        elif opcion == '2':
            moneda = input("\nIngresa el codigo de moneda (ej: USD, EUR, CNY): ").strip()
            fecha_desde = input("Fecha desde (opcional, Enter para todas): ").strip() or None
            fecha_hasta = input("Fecha hasta (opcional, Enter para todas): ").strip() or None

            resultado = consulta.consultar_moneda(moneda, fecha_desde, fecha_hasta)
            if resultado is not None:
                titulo = f"HISTORICO {moneda.upper()}"
                if fecha_desde or fecha_hasta:
                    titulo += f" ({fecha_desde or 'inicio'} - {fecha_hasta or 'hoy'})"
                consulta.mostrar_tabla(resultado, titulo)

        elif opcion == '3':
            monedas = consulta.listar_monedas()
            print(f"\n{'='*60}")
            print(f"{'MONEDAS DISPONIBLES':^60}")
            print('='*60)
            print(monedas.to_string(index=False))
            print(f"\nTotal: {len(monedas)} monedas\n")

        elif opcion == '4':
            anio = input("\nFiltrar por anio (opcional, Enter para todos): ").strip()
            anio = int(anio) if anio else None

            mes = input("Filtrar por mes (1-12, opcional): ").strip()
            mes = int(mes) if mes else None

            fechas = consulta.listar_fechas_disponibles(anio, mes)
            print(f"\n{'='*60}")
            print(f"{'FECHAS DISPONIBLES':^60}")
            print('='*60)

            # Mostrar en columnas
            for i in range(0, len(fechas), 4):
                fila = fechas[i:i+4]
                print("  ".join(f"{f:12}" for f in fila))

            print(f"\nTotal: {len(fechas)} fechas\n")

        elif opcion == '5':
            print("\n[*] Saliendo...\n")
            break

        else:
            print("\n[X] Opcion invalida")


def consulta_rapida(fecha):
    """Función auxiliar para consultas rápidas desde línea de comandos"""
    consulta = ConsultaBCV()
    resultado = consulta.consultar_fecha(fecha)
    if resultado is not None:
        consulta.mostrar_tabla(resultado, f"TIPOS DE CAMBIO - {fecha}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Consulta rápida desde línea de comandos
        fecha = ' '.join(sys.argv[1:])
        consulta_rapida(fecha)
    else:
        # Menú interactivo
        menu_interactivo()
