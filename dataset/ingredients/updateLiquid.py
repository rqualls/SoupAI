import pandas as pd

df = pd.read_csv('modified/ingredient-root-was-modified.csv')
dfl = pd.read_csv('modified/liquid-ingredient-root-mod.csv')

liquidRoot = dict()
liquid = []

for i in range(len(dfl)):
    if not dfl['root'][i] in liquidRoot:
        liquidRoot[dfl['root'][i]] = None

for i in range(len(df)):
    if df['root'][i] in liquidRoot:
        liquid.append(True)
    else:
        liquid.append(False)


dfL = pd.DataFrame({'ingredient':df['ingredient'], 'root':df['root'],'liquid':liquid}) 
dfL.to_csv('modified/ingredient-root-was-modified-wliquid.csv', index=False, encoding='utf-8')