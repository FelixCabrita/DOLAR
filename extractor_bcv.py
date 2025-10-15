"""
Extractor de Tipos de Cambio del BCV
Consolida datos de archivos Excel trimestrales en un dataset unificado
"""

import pandas as pd
import os
import re
from datetime import datetime
from pathlib import Path


class ExtractorBCV:
    def __init__(self, directorio_data='Data_xls'):
        self.directorio = directorio_data
        self.datos_consolidados = []

    def extraer_fecha_hoja(self, nombre_hoja):
        """
        Extrae la fecha del nombre de la hoja (formato DDMMYYYY)
        Ejemplo: '02012025' -> '2025-01-02'
        """
        try:
            if len(nombre_hoja) == 8 and nombre_hoja.isdigit():
                dia = nombre_hoja[:2]
                mes = nombre_hoja[2:4]
                anio = nombre_hoja[4:]
                return f"{anio}-{mes}-{dia}"
        except:
            pass
        return None

    def extraer_fecha_celda(self, df, texto_buscar='Fecha Valor:'):
        """
        Extrae la fecha de las celdas del encabezado (formato DD/MM/YYYY)
        Busca en las primeras filas por 'Fecha Valor:' o 'Fecha Operacion:'
        """
        try:
            # Buscar en las primeras 10 filas
            for idx in range(min(10, len(df))):
                for col in df.columns:
                    valor = str(df.iloc[idx, col])
                    if texto_buscar in valor:
                        # Extraer fecha con regex: DD/MM/YYYY
                        match = re.search(r'(\d{2})/(\d{2})/(\d{4})', valor)
                        if match:
                            dia, mes, anio = match.groups()
                            return f"{anio}-{mes}-{dia}"
        except:
            pass
        return None

    def procesar_hoja(self, archivo, nombre_hoja):
        """
        Procesa una hoja individual del archivo Excel
        """
        try:
            # Leer la hoja completa sin procesar
            df = pd.read_excel(archivo, sheet_name=nombre_hoja, header=None)

            # 1. Obtener fecha (priorizar Fecha Valor)
            fecha = None
            origen_fecha = None

            # Intentar obtener de Fecha Valor
            fecha = self.extraer_fecha_celda(df, 'Fecha Valor:')
            if fecha:
                origen_fecha = 'fecha_valor'
            else:
                # Intentar Fecha Operación
                fecha = self.extraer_fecha_celda(df, 'Fecha Operacion:')
                if fecha:
                    origen_fecha = 'fecha_operacion'
                else:
                    # Usar nombre de hoja como último recurso
                    fecha = self.extraer_fecha_hoja(nombre_hoja)
                    if fecha:
                        origen_fecha = 'sheet_name'

            if not fecha:
                print(f"  [!] No se pudo extraer fecha de {nombre_hoja}")
                return []

            # 2. Encontrar la fila donde empiezan los datos
            # Buscar la fila que contiene "Moneda/País" o "Bs./M.E."
            inicio_datos = None
            for idx in range(min(15, len(df))):
                fila_str = ' '.join([str(x) for x in df.iloc[idx].values if pd.notna(x)])
                if 'Compra (BID)' in fila_str and 'Venta (ASK)' in fila_str:
                    inicio_datos = idx + 1  # Los datos empiezan en la siguiente fila
                    break

            if inicio_datos is None:
                print(f"  [!] No se encontro estructura de datos en {nombre_hoja}")
                return []

            # 3. Leer los datos desde la fila identificada
            # Estructura: Col B=Moneda, Col C=País, Col F=Compra Bs, Col G=Venta Bs
            registros = []

            for idx in range(inicio_datos, len(df)):
                fila = df.iloc[idx]

                # Verificar que hay datos en las columnas esperadas
                moneda = fila.iloc[1] if len(fila) > 1 else None
                pais = fila.iloc[2] if len(fila) > 2 else None
                compra_bs = fila.iloc[5] if len(fila) > 5 else None
                venta_bs = fila.iloc[6] if len(fila) > 6 else None

                # Validar que tenemos datos válidos
                if pd.isna(moneda) or pd.isna(compra_bs) or pd.isna(venta_bs):
                    continue

                # Verificar que compra y venta son números
                try:
                    compra_bs = float(compra_bs)
                    venta_bs = float(venta_bs)
                except:
                    continue

                # Crear registro
                registro = {
                    'fecha': fecha,
                    'moneda': str(moneda).strip(),
                    'pais': str(pais).strip() if pd.notna(pais) else '',
                    'compra_bs': compra_bs,
                    'venta_bs': venta_bs,
                    'fuente': os.path.basename(archivo),
                    'origen_fecha': origen_fecha
                }

                registros.append(registro)

            return registros

        except Exception as e:
            print(f"  [X] Error procesando {nombre_hoja}: {e}")
            return []

    def procesar_archivo(self, ruta_archivo):
        """
        Procesa todas las hojas de un archivo Excel trimestral
        """
        print(f"\n[*] Procesando: {os.path.basename(ruta_archivo)}")

        try:
            xls = pd.ExcelFile(ruta_archivo)
            print(f"   Hojas encontradas: {len(xls.sheet_names)}")

            for nombre_hoja in xls.sheet_names:
                registros = self.procesar_hoja(ruta_archivo, nombre_hoja)
                self.datos_consolidados.extend(registros)

                if registros:
                    print(f"   [OK] {nombre_hoja}: {len(registros)} monedas extraidas")

        except Exception as e:
            print(f"   [X] Error: {e}")

    def procesar_todos_archivos(self):
        """
        Procesa todos los archivos .xls del directorio
        """
        print(">> Iniciando extraccion de datos del BCV\n")

        # Buscar archivos .xls
        archivos = list(Path(self.directorio).glob('*.xls'))

        if not archivos:
            print(f"[X] No se encontraron archivos .xls en {self.directorio}")
            return None

        print(f"[*] Archivos encontrados: {len(archivos)}")

        for archivo in sorted(archivos):
            self.procesar_archivo(str(archivo))

        # Convertir a DataFrame
        if self.datos_consolidados:
            df = pd.DataFrame(self.datos_consolidados)

            # Ordenar por fecha y moneda
            df = df.sort_values(['fecha', 'moneda'])

            print(f"\n[OK] Extraccion completa: {len(df)} registros consolidados")
            print(f"   Fechas: {df['fecha'].min()} a {df['fecha'].max()}")
            print(f"   Monedas unicas: {df['moneda'].nunique()}")

            return df
        else:
            print("\n[X] No se extrajeron datos")
            return None

    def consultar_fecha(self, df, fecha_busqueda):
        """
        Consulta los tipos de cambio de una fecha específica

        Parámetros:
        - fecha_busqueda: string en formato 'YYYY-MM-DD', 'DD/MM/YYYY' o 'mes dia año'
        """
        # Normalizar formato de fecha
        fecha_iso = self._normalizar_fecha(fecha_busqueda)

        if not fecha_iso:
            print(f"[X] Formato de fecha no valido: {fecha_busqueda}")
            return None

        # Filtrar datos
        resultado = df[df['fecha'] == fecha_iso].copy()

        if resultado.empty:
            print(f"\n[!] No hay datos para la fecha: {fecha_iso}")

            # Sugerir fechas cercanas
            df['fecha_dt'] = pd.to_datetime(df['fecha'])
            fecha_dt = pd.to_datetime(fecha_iso)

            fechas_disponibles = df['fecha_dt'].unique()
            fechas_cercanas = sorted(fechas_disponibles, key=lambda x: abs((x - fecha_dt).days))[:3]

            print("\n[*] Fechas disponibles mas cercanas:")
            for f in fechas_cercanas:
                print(f"   - {f.strftime('%Y-%m-%d')}")

            return None

        # Formatear para mostrar
        resultado_display = resultado[['moneda', 'pais', 'compra_bs', 'venta_bs']].copy()
        resultado_display.columns = ['Moneda', 'País', 'Compra (Bs.)', 'Venta (Bs.)']

        return resultado_display

    def _normalizar_fecha(self, fecha_str):
        """
        Convierte diferentes formatos de fecha a ISO (YYYY-MM-DD)
        """
        formatos = [
            '%Y-%m-%d',           # 2025-03-08
            '%d/%m/%Y',           # 08/03/2025
            '%m/%d/%Y',           # 03/08/2025
            '%Y/%m/%d',           # 2025/03/08
            '%d-%m-%Y',           # 08-03-2025
        ]

        # Intentar parseo directo
        for fmt in formatos:
            try:
                fecha = datetime.strptime(fecha_str.strip(), fmt)
                return fecha.strftime('%Y-%m-%d')
            except:
                continue

        # Intentar parseo de texto en español: "marzo 8 2025"
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


def main():
    # Crear extractor
    extractor = ExtractorBCV('Data_xls')

    # Procesar todos los archivos
    df = extractor.procesar_todos_archivos()

    if df is None:
        return

    # Guardar a CSV
    archivo_salida = 'tipos_cambio_bcv_consolidado.csv'
    df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    print(f"\n[*] Datos guardados en: {archivo_salida}")

    # Ejemplos de consulta
    print("\n" + "="*70)
    print("CONSULTAS DE EJEMPLO")
    print("="*70)

    # Consulta 1: Fecha específica
    print("\n[1] Consulta: marzo 8 2025")
    resultado = extractor.consultar_fecha(df, 'marzo 8 2025')
    if resultado is not None:
        print(f"\n{resultado.to_string(index=False)}")

    return df, extractor


if __name__ == "__main__":
    df, extractor = main()
