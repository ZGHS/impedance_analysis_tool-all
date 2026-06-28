import pandas as pd

from sklearn.cluster import KMeans


def analyze(df) -> pd.DataFrame:
    # 示例：简单聚类
    # model = KMeans(n_clusters=3)
    # df["cluster"] = model.fit_predict(df[0],df[1])
    return df