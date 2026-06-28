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


def read_ts_from_mat(file_path: str) -> float:
    """
    从.mat文件中自动识别并读取采样时间间隔 Ts
    
    识别优先级：
    1. 直接读取 Ts, dt, sampling_time, sample_interval, time_step 等变量
    2. 读取 Fs, sampling_rate, sample_rate 等变量，计算 Ts = 1 / Fs
    3. 从数据的最后一列（时间列）计算相邻时间点的差值的中位数
    4. 使用默认值 100e-6（100微秒）
    
    Parameters
    ----------
    file_path : str
        .mat文件的路径
    
    Returns
    -------
    float
        采样时间间隔 Ts（秒）
    """
    try:
        mat_data = scipy.io.loadmat(file_path)
        
        # 优先级1：直接查找采样时间变量
        ts_keys = ['Ts', 'ts', 'dt', 'sampling_time', 'sample_interval', 'time_step']
        for key in ts_keys:
            if key in mat_data:
                val = mat_data[key]
                if isinstance(val, (int, float)):
                    print(f"从变量 '{key}' 读取 Ts = {val:.2e}s")
                    return val
                elif isinstance(val, np.ndarray) and val.size == 1:
                    ts_val = float(val.flat[0])
                    print(f"从变量 '{key}' 读取 Ts = {ts_val:.2e}s")
                    return ts_val
        
        # 优先级2：查找采样率变量，计算 Ts = 1 / Fs
        fs_keys = ['Fs', 'fs', 'sampling_rate', 'sample_rate', 'f_sampling']
        for key in fs_keys:
            if key in mat_data:
                val = mat_data[key]
                if isinstance(val, (int, float)) and val > 0:
                    ts_val = 1.0 / val
                    print(f"从变量 '{key}' = {val}Hz 计算 Ts = {ts_val:.2e}s")
                    return ts_val
                elif isinstance(val, np.ndarray) and val.size == 1:
                    fs_val = float(val.flat[0])
                    if fs_val > 0:
                        ts_val = 1.0 / fs_val
                        print(f"从变量 '{key}' = {fs_val}Hz 计算 Ts = {ts_val:.2e}s")
                        return ts_val
        
        # 优先级3：从数据的最后一列（时间列）计算采样时间
        data_names = [k for k in mat_data.keys() if not k.startswith('__')]
        if data_names:
            data_name = data_names[0]
            data = mat_data[data_name]
            
            if data.ndim >= 2:
                # 确定时间列（最后一列）
                if data.shape[0] > data.shape[1]:
                    time_column = data[:, -1]
                else:
                    time_column = data[-1, :]
                
                time_column = np.atleast_1d(time_column)
                
                if len(time_column) >= 2:
                    # 计算相邻时间点的差值，取中位数作为 Ts
                    diffs = np.diff(time_column)
                    valid_diffs = diffs[diffs > 0]
                    if len(valid_diffs) > 0:
                        ts_val = np.median(valid_diffs)
                        # 检查是否合理（1e-9 到 1秒之间）
                        if 1e-9 < ts_val < 1.0:
                            print(f"从时间列估算 Ts = {ts_val:.2e}s")
                            return ts_val
        
        # 优先级4：使用默认值
        print(f"未找到采样时间信息，使用默认值 Ts = 100e-6s")
        return 100e-6
        
    except Exception as e:
        print(f"read_ts_from_mat 错误: {e}")
        return 100e-6
    
