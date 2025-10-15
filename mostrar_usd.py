import json

data = json.load(open('tipos_cambio_usd.json', 'r', encoding='utf-8'))

print('='*70)
print(f' ARCHIVO: tipos_cambio_usd.json '.center(70, '='))
print('='*70)
print(f'\nTotal de fechas: {len(data)}')
print(f'Periodo: {min(data.keys())} a {max(data.keys())}')

print('\n--- Marzo 2025 (muestra de 5 fechas) ---\n')
fechas_marzo = [(f, t) for f, t in sorted(data.items()) if f.startswith('2025-03')][:5]

for fecha, tasa in fechas_marzo:
    print(f"{fecha}: Compra Bs. {tasa['compra_bs']:>8.2f}, Venta Bs. {tasa['venta_bs']:>8.2f}, Promedio Bs. {tasa['promedio_bs']:>8.2f}")

print(f'\nTotal fechas en marzo: {len([f for f in data.keys() if f.startswith("2025-03")])}')
print()
