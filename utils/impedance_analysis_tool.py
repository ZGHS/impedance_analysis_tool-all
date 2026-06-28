import traceback
from typing import List
import pandas as pd
import scipy.io
from utils.app_pos import AppPos
from utils.app_neg import AppNeg

def fetch_data(file_path):
    try:
        # 读取全部数据
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            data = df.values
        else:
            mat_data = scipy.io.loadmat(file_path)
            name = [k for k in mat_data.keys() if not k.startswith('__')][0]
            data = mat_data[name].T
        return data
    except Exception as e:
        traceback.print_exc()
        print(f"impedance_analysis_tool,fetch_data,错误，文件读取失败:{e}")
        return None
    

def plot_fun(file_paths:List[str],pos_flow:int):
    try:
        dataA = fetch_data(file_path=file_paths[0])
        dataB = fetch_data(file_path=file_paths[1])
        print(dataA.shape)
        print(dataB.shape)
        
        if(pos_flow==1):
            app = AppPos(dataA, dataB)
        else:
            app = AppNeg(dataA, dataB)
        
        # print("figs size:",len(figs))
        return _show_plots(app)
    except Exception as e:
        print("绘图错误",e)



def _show_plots(app):
    try:
        figs = app.draw()
    except Exception as e:
        traceback.print_exc()
        print(f"impedance_analysis_tool,_show_plots,app.draw错误:{e}")
    try:
        
        res=[]
        for i, fig in enumerate(figs):
            res.append(fig.to_json())
        return res
    except Exception as e:
        print("_show_plots错误",e)


