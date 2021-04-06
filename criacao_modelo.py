import pickle
import pandas as pd
df = pd.read_parquet('erroshabilidadesmt_grp')

from sklearn.neighbors import NearestNeighbors
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=40, n_jobs=-1)
knn.fit(df)

arquivo = open('modelos/modelo_recsys_mt','wb')
pickle.dump(knn,arquivo)
arquivo.close()