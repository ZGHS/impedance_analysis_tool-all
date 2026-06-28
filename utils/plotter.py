# utils/plotter.py
import plotly.express as px

def plot_to_plotly(arr):
    # fig = px.scatter(df, x="x_col", y="y_col", color="category")
    fig = px.line(x=arr[:, 0], y=arr[:, 1])   # 第 0 列当 x，第 1 列当 y
    # fig.show()
    return fig.to_json()  # 前端可直接用
