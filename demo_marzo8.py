"""
Demostracion: Busqueda de tipos de cambio para marzo 8, 2025
y fechas alternativas cercanas
"""

from consulta_bcv import ConsultaBCV

def main():
    print("\n" + "="*80)
    print(" DEMOSTRACION: CONSULTA DE TIPOS DE CAMBIO BCV ".center(80, "="))
    print("="*80)

    # Cargar base de datos
    consulta = ConsultaBCV()

    # Consulta 1: Marzo 8, 2025 (fecha no disponible - fin de semana)
    print("\n[CASO 1] Consultando: marzo 8 2025")
    print("-" * 80)
    resultado = consulta.consultar_fecha('marzo 8 2025')

    # Consulta 2: Marzo 7, 2025 (dia anterior - disponible)
    print("\n\n[CASO 2] Consultando fecha alternativa: marzo 7 2025")
    print("-" * 80)
    resultado = consulta.consultar_fecha('marzo 7 2025')
    if resultado is not None:
        consulta.mostrar_tabla(resultado, "TIPOS DE CAMBIO - MARZO 7, 2025")

    # Consulta 3: Marzo 10, 2025 (dia siguiente habil - disponible)
    print("\n[CASO 3] Consultando fecha alternativa: marzo 10 2025")
    print("-" * 80)
    resultado = consulta.consultar_fecha('marzo 10 2025')
    if resultado is not None:
        consulta.mostrar_tabla(resultado, "TIPOS DE CAMBIO - MARZO 10, 2025")

    # Mostrar comparacion USD
    print("\n[COMPARACION] Evolucion del USD en marzo 2025")
    print("-" * 80)
    usd_marzo = consulta.consultar_moneda('USD', 'marzo 1 2025', 'marzo 31 2025')
    if usd_marzo is not None:
        # Mostrar solo primeros 10 registros
        print("\nPrimeros 10 registros de marzo 2025:")
        consulta.mostrar_tabla(usd_marzo.head(10), "HISTORICO USD - MARZO 2025")

        # Estadisticas
        print("\n[ESTADISTICAS USD - MARZO 2025]")
        print(f"  Compra minima: Bs. {usd_marzo['Compra (Bs.)'].astype(str).str.replace(',', '').astype(float).min():,.2f}")
        print(f"  Compra maxima: Bs. {usd_marzo['Compra (Bs.)'].astype(str).str.replace(',', '').astype(float).max():,.2f}")
        print(f"  Promedio:      Bs. {usd_marzo['Promedio (Bs.)'].astype(str).str.replace(',', '').astype(float).mean():,.2f}")

    print("\n" + "="*80)
    print(" FIN DE LA DEMOSTRACION ".center(80, "="))
    print("="*80)
    print("\nPara consultas interactivas, ejecuta: python consulta_bcv.py")
    print("Para consultas rapidas: python consulta_bcv.py \"fecha\"\n")


if __name__ == "__main__":
    main()
