from scipy import signal
import numpy as np
import pandas as pd
import scipy.io
from tkinter import Tk, filedialog
from scipy.fft import fft
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AppPos:
    def __init__(self, dataA, dataB):
        self.dataA = dataA
        self.dataB = dataB
        self.figs = []



    def draw(self):
             

        Ts = 100e-6
        data = self.dataA

        idx = np.where(data[:, -1] == 2.5)[0]
        First_fre = idx[0]
        Last_fre = idx[-1]

        Fs = 1 / Ts
        dirsub_time = 1

        ImpedanceFrequency = np.concatenate([
            np.arange(2.5, 10.0, 0.1),
            np.arange(10, 100, 1),
            np.arange(100, 1010, 10)
        ])
        numFreqs = len(ImpedanceFrequency)
        Csv_WF_ = {}
        ImpedanceData = np.zeros((256, 13), dtype=complex)
        ImpedanceDataVariable_wf = np.zeros((256, 19), dtype=complex)
        Impedance_WF = np.zeros((256, 4), dtype=complex)

        for j in range(numFreqs):
            dataname = f'Csv_{round(ImpedanceFrequency[j] * 10):03d}'
            
            startIndex = int((j) * (dirsub_time * Fs) + First_fre)
            endIndex = int((First_fre) + (j + 1) * dirsub_time * Fs)
            
            Csv_WF_[dataname] = data[startIndex:endIndex, 0:8]
            fft_data = fft(Csv_WF_[dataname], int(Fs), axis=0)
            
            ImpedanceData[j, 0] = ImpedanceFrequency[j]
            
            ImpedanceData[j, 1] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 1]
            ImpedanceData[j, 2] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 2]
            ImpedanceData[j, 3] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 3]
            
            ImpedanceData[j, 4] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 4]
            ImpedanceData[j, 5] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 5]
            ImpedanceData[j, 6] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 6]
            
            ImpedanceData[j, 7] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 4]
            ImpedanceData[j, 8] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 5]
            ImpedanceData[j, 9] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 6]
            
            ImpedanceData[j, 10] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 1]
            ImpedanceData[j, 11] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 2]
            ImpedanceData[j, 12] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 3]
            
            ImpedanceDataVariable_wf[j, 0] = ImpedanceData[j, 0]
            
            Va = ImpedanceData[j, 1]
            Vb = ImpedanceData[j, 2]
            Vc = ImpedanceData[j, 3]
            
            Vp = Va + Vb * np.exp(1j * 2 * np.pi / 3) + Vc * np.exp(1j * 4 * np.pi / 3)
            Vn = Va + Vb * np.exp(1j * 4 * np.pi / 3) + Vc * np.exp(1j * 2 * np.pi / 3)
            
            ImpedanceDataVariable_wf[j, 1] = Vp
            ImpedanceDataVariable_wf[j, 2] = Vn
            
            Ia = ImpedanceData[j, 4]
            Ib = ImpedanceData[j, 5]
            Ic = ImpedanceData[j, 6]
            
            Ip = Ia + Ib * np.exp(1j * 2 * np.pi / 3) + Ic * np.exp(1j * 4 * np.pi / 3)
            In = Ia + Ib * np.exp(1j * 4 * np.pi / 3) + Ic * np.exp(1j * 2 * np.pi / 3)
            
            ImpedanceDataVariable_wf[j, 3] = Ip
            ImpedanceDataVariable_wf[j, 4] = In
            
            Ia = ImpedanceData[j, 7]
            Ib = ImpedanceData[j, 8]
            Ic = ImpedanceData[j, 9]
            
            Ip = Ia + Ib * np.exp(1j * 2 * np.pi / 3) + Ic * np.exp(1j * 4 * np.pi / 3)
            In = Ia + Ib * np.exp(1j * 4 * np.pi / 3) + Ic * np.exp(1j * 2 * np.pi / 3)
            
            Va = ImpedanceData[j, 10]
            Vb = ImpedanceData[j, 11]
            Vc = ImpedanceData[j, 12]
            
            Vp = Va + Vb * np.exp(1j * 2 * np.pi / 3) + Vc * np.exp(1j * 4 * np.pi / 3)
            Vn = Va + Vb * np.exp(1j * 4 * np.pi / 3) + Vc * np.exp(1j * 2 * np.pi / 3)
            
            if ImpedanceDataVariable_wf[j, 0] < 100:
                ImpedanceDataVariable_wf[j, 6] = np.conj(Ip)
                ImpedanceDataVariable_wf[j, 9] = np.conj(Vp)
            else:
                ImpedanceDataVariable_wf[j, 7] = In
                ImpedanceDataVariable_wf[j, 10] = Vn
            
            Vp = ImpedanceDataVariable_wf[j, 1]
            Ip = ImpedanceDataVariable_wf[j, 3]
            
            Vn = ImpedanceDataVariable_wf[j, 10]
            In = ImpedanceDataVariable_wf[j, 7]
            
            Ipp = ImpedanceDataVariable_wf[j, 6]
            Vpp = ImpedanceDataVariable_wf[j, 9]
            
            Ypp = Ip / Vp
            
            if ImpedanceDataVariable_wf[j, 0] < 100:
                Ynp = Ipp / Vp
                Ynn = Ipp / Vpp
                Ypn = Ip / Vpp
            else:
                Ynp = In / Vp
                Ynn = In / Vn
                Ypn = Ip / Vn
            
            Impedance_WF[j, 0] = 1 / Ypp
            
            ImpedanceDataVariable_wf[j, 11] = 20 * np.log10(1 / abs(1 / Impedance_WF[j, 0]))
            ImpedanceDataVariable_wf[j, 12] = 0 - np.angle(1 / Impedance_WF[j, 0]) * (180 / np.pi)

        fig1 = make_subplots(rows=2, cols=1, vertical_spacing=0.1, subplot_titles=('', ''))
        
        # 添加第一个子图 - 幅度图
        fig1.add_trace(
            go.Scatter(
                x=ImpedanceDataVariable_wf[:, 0].real,
                y=ImpedanceDataVariable_wf[:, 11].real,
                mode='lines',
                name='Z-Wf-pos',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # 设置第一个子图的布局
        fig1.update_yaxes(
            title_text='Magnitude/dB',
            title_font=dict(weight='bold', size=30),
            range=[-50, 150],
            tickfont=dict(size=30),
            row=1, col=1
        )
        fig1.update_xaxes(
            type='log',
            range=[np.log10(2.5), np.log10(1000)],
            showticklabels=False,
            row=1, col=1
        )
        
        # 添加第二个子图 - 相位图
        fig1.add_trace(
            go.Scatter(
                x=ImpedanceDataVariable_wf[:, 0].real,
                y=ImpedanceDataVariable_wf[:, 12].real,
                mode='lines',
                name='Z-Wf-pos',
                line=dict(color='blue', width=2)
            ),
            row=2, col=1
        )
        
        # 设置第二个子图的布局
        fig1.update_yaxes(
            title_text='Phase/deg',
            title_font=dict(weight='bold', size=30),
            range=[-200, 200],
            tickfont=dict(size=30),
            row=2, col=1
        )
        fig1.update_xaxes(
            title_text='Frequency/Hz',
            title_font=dict(weight='bold', size=30),
            type='log',
            range=[np.log10(2.5), np.log10(1000)],
            tickfont=dict(size=30),
            row=2, col=1
        )
        
        # 更新整个图表布局
        fig1.update_layout(
            height=800,
            width=960,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=20)
            ),
            template='plotly_white'
        )
        
        # 添加网格
        fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=1, col=1)
        fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=1, col=1)
        fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=2, col=1)
        fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=2, col=1)

        
        
        data =self.dataB

        idx = np.where(data[:, -1] == 2.5)[0]
        First_fre = idx[0]
        Last_fre = idx[-1]

        Fs = 10000
        dirsub_time = 1

        ImpedanceFrequency = np.concatenate([
            np.arange(2.5, 10.0, 0.1),
            np.arange(10, 100, 1),
            np.arange(100, 1010, 10)
        ])
        numFreqs = len(ImpedanceFrequency)
        Csv_DW_ = {}
        ImpedanceData = np.zeros((256, 13), dtype=complex)
        ImpedanceDataVariable_zg = np.zeros((256, 19), dtype=complex)
        Impedance_DW = np.zeros((256, 4), dtype=complex)

        for j in range(numFreqs):
            dataname = f'Csv_{round(ImpedanceFrequency[j] * 10):03d}'
            
            startIndex = int((j) * (dirsub_time * Fs) + First_fre)
            endIndex = int((First_fre) + (j + 1) * dirsub_time * Fs)
            
            Csv_DW_[dataname] = data[startIndex:endIndex, 0:8]
            fft_data = fft(Csv_DW_[dataname], Fs, axis=0)
            
            ImpedanceData[j, 0] = ImpedanceFrequency[j]
            
            ImpedanceData[j, 1] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 1]
            ImpedanceData[j, 2] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 2]
            ImpedanceData[j, 3] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 3]
            
            ImpedanceData[j, 4] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 4]
            ImpedanceData[j, 5] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 5]
            ImpedanceData[j, 6] = fft_data[int(abs(round(ImpedanceFrequency[j]))), 6]
            
            ImpedanceData[j, 7] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 4]
            ImpedanceData[j, 8] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 5]
            ImpedanceData[j, 9] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 6]
            
            ImpedanceData[j, 10] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 1]
            ImpedanceData[j, 11] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 2]
            ImpedanceData[j, 12] = fft_data[int(abs(round(ImpedanceFrequency[j]) - 100)), 3]
            
            ImpedanceDataVariable_zg[j, 0] = ImpedanceData[j, 0]
            
            Va = ImpedanceData[j, 1]
            Vb = ImpedanceData[j, 2]
            Vc = ImpedanceData[j, 3]
            
            Vp = Va + Vb * np.exp(1j * 2 * np.pi / 3) + Vc * np.exp(1j * 4 * np.pi / 3)
            Vn = Va + Vb * np.exp(1j * 4 * np.pi / 3) + Vc * np.exp(1j * 2 * np.pi / 3)
            
            ImpedanceDataVariable_zg[j, 1] = Vp
            ImpedanceDataVariable_zg[j, 2] = Vn
            
            Ia = ImpedanceData[j, 4]
            Ib = ImpedanceData[j, 5]
            Ic = ImpedanceData[j, 6]
            
            Ip = Ia + Ib * np.exp(1j * 2 * np.pi / 3) + Ic * np.exp(1j * 4 * np.pi / 3)
            In = Ia + Ib * np.exp(1j * 4 * np.pi / 3) + Ic * np.exp(1j * 2 * np.pi / 3)
            
            ImpedanceDataVariable_zg[j, 3] = Ip
            ImpedanceDataVariable_zg[j, 4] = In
            
            Ia = ImpedanceData[j, 7]
            Ib = ImpedanceData[j, 8]
            Ic = ImpedanceData[j, 9]
            
            Ip = Ia + Ib * np.exp(1j * 2 * np.pi / 3) + Ic * np.exp(1j * 4 * np.pi / 3)
            In = Ia + Ib * np.exp(1j * 4 * np.pi / 3) + Ic * np.exp(1j * 2 * np.pi / 3)
            
            Va = ImpedanceData[j, 10]
            Vb = ImpedanceData[j, 11]
            Vc = ImpedanceData[j, 12]
            
            Vp = Va + Vb * np.exp(1j * 2 * np.pi / 3) + Vc * np.exp(1j * 4 * np.pi / 3)
            Vn = Va + Vb * np.exp(1j * 4 * np.pi / 3) + Vc * np.exp(1j * 2 * np.pi / 3)
            
            if ImpedanceDataVariable_zg[j, 0] < 100:
                ImpedanceDataVariable_zg[j, 6] = np.conj(Ip)
                ImpedanceDataVariable_zg[j, 9] = np.conj(Vp)
            else:
                ImpedanceDataVariable_zg[j, 7] = In
                ImpedanceDataVariable_zg[j, 10] = Vn
            
            Vp = ImpedanceDataVariable_zg[j, 1]
            Ip = ImpedanceDataVariable_zg[j, 3]
            
            Vn = ImpedanceDataVariable_zg[j, 10]
            In = ImpedanceDataVariable_zg[j, 7]
            
            Ipp = ImpedanceDataVariable_zg[j, 6]
            Vpp = ImpedanceDataVariable_zg[j, 9]
            
            Ypp = Ip / Vp
            
            if ImpedanceDataVariable_zg[j, 0] < 100:
                Ynp = Ipp / Vp
                Ynn = Ipp / Vpp
                Ypn = Ip / Vpp
            else:
                Ynp = In / Vp
                Ynn = In / Vn
                Ypn = Ip / Vn
            
            Impedance_DW[j, 0] = 1 / Ypp
            
            ImpedanceDataVariable_zg[j, 11] = 20 * np.log10(1 / abs(1 / Impedance_DW[j, 0]))
            ImpedanceDataVariable_zg[j, 12] = -np.angle(1 / Impedance_DW[j, 0]) * (180 / np.pi)

        # 添加红色曲线到第一个子图
        fig1.add_trace(
            go.Scatter(
                x=ImpedanceDataVariable_zg[:, 0].real,
                y=ImpedanceDataVariable_zg[:, 11].real,
                mode='lines',
                name='Z-Grid-pos',
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )
        
        # 添加红色曲线到第二个子图
        fig1.add_trace(
            go.Scatter(
                x=ImpedanceDataVariable_zg[:, 0].real,
                y=ImpedanceDataVariable_zg[:, 12].real,
                mode='lines',
                name='Z-Grid-pos',
                line=dict(color='red', width=2)
            ),
            row=2, col=1
        )

        self.figs.append(fig1)
        
        
        Zreal_DW = np.zeros((256, 1))
        Zimag_DW = np.zeros((256, 1))

        for j in range(numFreqs):
            Zreal_DW[j, 0] = np.real(Impedance_DW[j, 0] / Impedance_WF[j, 0])
            Zimag_DW[j, 0] = np.imag(Impedance_DW[j, 0] / Impedance_WF[j, 0])

        fig2 = go.Figure()
        
        # 添加第一条曲线
        fig2.add_trace(
            go.Scatter(
                x=Zreal_DW.flatten(),
                y=Zimag_DW.flatten(),
                mode='lines',
                name='Z',
                line=dict(width=2)
            )
        )
        
        # 添加第二条曲线
        fig2.add_trace(
            go.Scatter(
                x=Zreal_DW.flatten(),
                y=-Zimag_DW.flatten(),
                mode='lines',
                name='-Z',
                line=dict(width=2)
            )
        )
        
        # 更新布局
        fig2.update_layout(
            title='Nyquist Plot',
            xaxis_title='Real(Z)',
            yaxis_title='Imag(I)',
            width=800,
            height=600,
            template='plotly_white'
        )
        
        # 设置坐标轴等比例
        fig2.update_xaxes(scaleanchor="y", scaleratio=1)
        fig2.update_yaxes(scaleanchor="x", scaleratio=1)
        
        # 添加网格
        fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        
        self.figs.append(fig2)
        
        Zreal_DW_1_85 = np.zeros((85, 1))
        Zimag_DW_1_85 = np.zeros((85, 1))

        for j in range(85):
            Zreal_DW_1_85[j, 0] = np.real(Impedance_DW[j, 0] / Impedance_WF[j, 0])
            Zimag_DW_1_85[j, 0] = np.imag(Impedance_DW[j, 0] / Impedance_WF[j, 0])

        fig3 = make_subplots(rows=1, cols=4, subplot_titles=('频段Ⅰ', '频段Ⅱ', '频段Ⅲ', '全频段'))
        
        # 第一个子图
        # 添加曲线
        fig3.add_trace(
            go.Scatter(
                x=Zreal_DW_1_85.flatten(),
                y=Zimag_DW_1_85.flatten(),
                mode='lines',
                line=dict(width=2)
            ),
            row=1, col=1
        )
        
        # 添加单位圆
        theta = np.linspace(0, 2 * np.pi, 100)
        x_circle = np.cos(theta)
        y_circle = np.sin(theta)
        fig3.add_trace(
            go.Scatter(
                x=x_circle,
                y=y_circle,
                mode='lines',
                line=dict(color='red'),
                showlegend=False
            ),
            row=1, col=1
        )
        
        # 添加黑色圆
        theta_circle1 = np.linspace(0, 2 * np.pi, 100)
        x_circle1 = -1 + 0.25 * np.cos(theta_circle1)
        y_circle1 = 0 + 0.25 * np.sin(theta_circle1)
        fig3.add_trace(
            go.Scatter(
                x=x_circle1,
                y=y_circle1,
                mode='lines',
                line=dict(color='black'),
                showlegend=False
            ),
            row=1, col=1
        )
        
        # 设置第一个子图的布局
        fig3.update_xaxes(
            title_text='Real(Z)',
            range=[-1.4, 1.4],
            tickfont=dict(size=20),
            scaleanchor="y",
            scaleratio=1,
            row=1, col=1
        )
        fig3.update_yaxes(
            title_text='Imag(Z)',
            range=[-1.2, 1.2],
            tickfont=dict(size=20),
            scaleanchor="x",
            scaleratio=1,
            row=1, col=1
        )

        Zreal_DW_86_165 = np.zeros((256, 1))
        Zimag_DW_86_165 = np.zeros((256, 1))

        for j in range(85, 165):
            Zreal_DW_86_165[j, 0] = np.real(Impedance_DW[j, 0] / Impedance_WF[j, 0])
            Zimag_DW_86_165[j, 0] = np.imag(Impedance_DW[j, 0] / Impedance_WF[j, 0])

        # 第二个子图
        # 添加曲线
        valid_indices = np.where((Zreal_DW_86_165 != 0) | (Zimag_DW_86_165 != 0))[0]
        fig3.add_trace(
            go.Scatter(
                x=Zreal_DW_86_165[valid_indices].flatten(),
                y=Zimag_DW_86_165[valid_indices].flatten(),
                mode='lines',
                line=dict(width=2)
            ),
            row=1, col=2
        )
        
        # 添加单位圆
        fig3.add_trace(
            go.Scatter(
                x=x_circle,
                y=y_circle,
                mode='lines',
                line=dict(color='red'),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 添加黄色圆
        theta_circle2 = np.linspace(0, 2 * np.pi, 100)
        x_circle2 = -1 + 0.2 * np.cos(theta_circle2)
        y_circle2 = 0 + 0.2 * np.sin(theta_circle2)
        fig3.add_trace(
            go.Scatter(
                x=x_circle2,
                y=y_circle2,
                mode='lines',
                line=dict(color='yellow'),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 设置第二个子图的布局
        fig3.update_xaxes(
            title_text='Real(Z)',
            range=[-1.4, 1.4],
            tickfont=dict(size=20),
            scaleanchor="y",
            scaleratio=1,
            row=1, col=2
        )
        fig3.update_yaxes(
            title_text='Imag(Z)',
            range=[-1.2, 1.2],
            tickfont=dict(size=20),
            scaleanchor="x",
            scaleratio=1,
            row=1, col=2
        )

        Zreal_DW_166_256 = np.zeros((256, 1))
        Zimag_DW_166_256 = np.zeros((256, 1))

        for j in range(165, 256):
            Zreal_DW_166_256[j, 0] = np.real(Impedance_DW[j, 0] / Impedance_WF[j, 0])
            Zimag_DW_166_256[j, 0] = np.imag(Impedance_DW[j, 0] / Impedance_WF[j, 0])

        # 第三个子图
        # 添加曲线
        valid_indices = np.where((Zreal_DW_166_256 != 0) | (Zimag_DW_166_256 != 0))[0]
        fig3.add_trace(
            go.Scatter(
                x=Zreal_DW_166_256[valid_indices].flatten(),
                y=Zimag_DW_166_256[valid_indices].flatten(),
                mode='lines',
                line=dict(width=2)
            ),
            row=1, col=3
        )
        
        # 添加单位圆
        fig3.add_trace(
            go.Scatter(
                x=x_circle,
                y=y_circle,
                mode='lines',
                line=dict(color='red'),
                showlegend=False
            ),
            row=1, col=3
        )
        
        # 添加绿色圆
        theta_circle3 = np.linspace(0, 2 * np.pi, 100)
        x_circle3 = -1 + 0.15 * np.cos(theta_circle3)
        y_circle3 = 0 + 0.15 * np.sin(theta_circle3)
        fig3.add_trace(
            go.Scatter(
                x=x_circle3,
                y=y_circle3,
                mode='lines',
                line=dict(color='green'),
                showlegend=False
            ),
            row=1, col=3
        )
        
        # 设置第三个子图的布局
        fig3.update_xaxes(
            title_text='Real(Z)',
            range=[-1.4, 1.4],
            tickfont=dict(size=20),
            scaleanchor="y",
            scaleratio=1,
            row=1, col=3
        )
        fig3.update_yaxes(
            title_text='Imag(Z)',
            range=[-1.2, 1.2],
            tickfont=dict(size=20),
            scaleanchor="x",
            scaleratio=1,
            row=1, col=3
        )

        Zreal_DW_1_256 = np.zeros((256, 1))
        Zimag_DW_1_256 = np.zeros((256, 1))

        for j in range(256):
            Zreal_DW_1_256[j, 0] = np.real(Impedance_DW[j, 0] / Impedance_WF[j, 0])
            Zimag_DW_1_256[j, 0] = np.imag(Impedance_DW[j, 0] / Impedance_WF[j, 0])

        # 第四个子图
        # 添加曲线
        fig3.add_trace(
            go.Scatter(
                x=Zreal_DW_1_256.flatten(),
                y=Zimag_DW_1_256.flatten(),
                mode='lines',
                line=dict(width=2)
            ),
            row=1, col=4
        )
        
        # 添加单位圆
        fig3.add_trace(
            go.Scatter(
                x=x_circle,
                y=y_circle,
                mode='lines',
                line=dict(color='red'),
                showlegend=False
            ),
            row=1, col=4
        )
        
        # 添加三个圆
        fig3.add_trace(
            go.Scatter(
                x=x_circle1,
                y=y_circle1,
                mode='lines',
                line=dict(color='black'),
                showlegend=False
            ),
            row=1, col=4
        )
        fig3.add_trace(
            go.Scatter(
                x=x_circle2,
                y=y_circle2,
                mode='lines',
                line=dict(color='yellow'),
                showlegend=False
            ),
            row=1, col=4
        )
        fig3.add_trace(
            go.Scatter(
                x=x_circle3,
                y=y_circle3,
                mode='lines',
                line=dict(color='green'),
                showlegend=False
            ),
            row=1, col=4
        )
        
        # 设置第四个子图的布局
        fig3.update_xaxes(
            title_text='Real(Z)',
            range=[-1.4, 1.4],
            tickfont=dict(size=20),
            scaleanchor="y",
            scaleratio=1,
            row=1, col=4
        )
        fig3.update_yaxes(
            title_text='Imag(Z)',
            range=[-1.2, 1.2],
            tickfont=dict(size=20),
            scaleanchor="x",
            scaleratio=1,
            row=1, col=4
        )
        
        # 更新整个图表布局
        fig3.update_layout(
            height=400,
            width=1600,
            title_text='Nyquist Plots by Frequency Bands',
            template='plotly_white'
        )
        
        # 添加网格到所有子图
        for i in range(1, 5):
            fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=1, col=i)
            fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=1, col=i)

        
        self.figs.append(fig3)
        return self.figs
        # plt.show()

