import Plot from "react-plotly.js";
import { Data, Layout } from "plotly.js";

export interface Props {
  data?: Data[]; // Plotly data array
  layout?: Partial<Layout>; // Plotly layout object
}
const customLayout = {
  width: 800, // 设置宽度，单位像素
  height: 500, // 设置高度，单位像素
  // 其它布局选项...
};

function PlotlyChart({ data, layout = customLayout }: Props) {
  if (!data || data.length === 0) {
    return <div>No valid Plotly data to render.</div>;
  }

  return (
    <Plot
      data={data}
      layout={layout}
      //   frames={plotlyData.frames}
      config={{ responsive: true }}
      style={{ width: "100%", height: "100%" }}
      useResizeHandler={true}
    />
  );
}

export default PlotlyChart;
