import json
import pandas as pd

# — Ajusta las rutas según dónde tengas los JSON —
PRODUCTS_PATH   = 'data/products.json'
STORES_PATH     =  'data/stores.json'
WAREHOUSES_PATH = 'data/warehouses.json'

# Carga
with open(STORES_PATH,     encoding='utf-8') as f: stores     = json.load(f)
with open(WAREHOUSES_PATH, encoding='utf-8') as f: warehouses = json.load(f)

# Normaliza demanda y stock
stores_demand_df = pd.json_normalize(
    stores,
    record_path=['demand'],
    meta=['id'],
    record_prefix='demand_'
)[['demand_productId', 'demand_size', 'demand_quantity']]

warehouses_stock_df = pd.json_normalize(
    warehouses,
    record_path=['stock'],
    meta=['id'],
    record_prefix='stock_'
)[['stock_productId', 'stock_size', 'stock_quantity']]

# Suma totales por producto+talla
demand_summary = (
    stores_demand_df
    .groupby(['demand_productId', 'demand_size'], as_index=False)
    .agg(total_demand=('demand_quantity', 'sum'))
)

stock_summary = (
    warehouses_stock_df
    .groupby(['stock_productId', 'stock_size'], as_index=False)
    .agg(total_stock=('stock_quantity', 'sum'))
)

# Fusiona y calcula brecha
summary = pd.merge(
    demand_summary,
    stock_summary,
    left_on=['demand_productId','demand_size'],
    right_on=['stock_productId','stock_size'],
    how='outer'
).fillna(0)

summary['gap'] = summary['total_stock'] - summary['total_demand']
summary = summary.rename(columns={
    'demand_productId':'productId',
    'demand_size':'size'
})[['productId','size','total_demand','total_stock','gap']]

# Imprime y guarda
print(summary.to_string(index=False))
summary.to_csv('brecha_stock_vs_demanda.csv', index=False, encoding='utf-8-sig')

print("\n✅ Guardado en brecha_stock_vs_demanda.csv")



