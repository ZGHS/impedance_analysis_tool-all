import { useState } from "react";
import "./App.css";
import { UploadOutlined } from "@ant-design/icons";
import type { UploadProps } from "antd";
import { Button, message, Upload, Flex } from "antd";
import PlotlyChart from "./PlotlyChart"; // 导入上面的图表组件
import { Data, Layout } from "plotly.js";
import { Radio } from "antd";
import type { RadioChangeEvent } from "antd";
import type { FormProps } from 'antd';
import { Form,Space} from 'antd';
import { InputNumber } from "antd";


const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};
// 【新增】定义一个接口来描述 plotlyObjs 数组中每个对象的结构
interface PlotlyObject {
  data: Data[];
  layout: Layout;
  // 如果你的对象还有其他属性，比如 id 或 title，也可以加在这里
  // id: string;
}
type FieldType = {
  username?: string;
  password?: string;
  remember?: string;
  BaseFrequencyOffset?: number;
  DisturbTime?: number;
  Ts1?: number;
  Ts2?: number;
};
function App() {
  const [posFlow, setPosFlow] = useState<number>(1); // 新增状态管理
  const [plotlyObjs, setPlotlyObjs] = useState<PlotlyObject[]>([]); // 新增状态管理
  const [uploadedFilePaths, setUploadedFilePaths] = useState<string[]>([]); // ✅ 新增：保存所有文件路径

  const props: UploadProps = {
    name: "file",
    multiple: true, // ✅ 允许一次选择多个文件
    action: "http://localhost:8000/api/upload",
    headers: {
      authorization: "authorization-text",
    },
    onChange(info) {
      const { file } = info;
      const { status, response } = info.file;

      if (status !== "uploading") {
        console.log(file, info.fileList);
      }
      if (status === "done") {
        console.log("服务端返回:", response);

        // 1. ✅ 处理服务端返回的文件路径（假设字段为 saved_path）
        const serverFilePath = response.saved_path; // ✅ 你要的文件路径字符串
        if (serverFilePath) {
          // 将路径添加到数组中（去重或直接追加，根据需求）
          setUploadedFilePaths((prev) => [...prev, serverFilePath]);
          message.success(
            `${file.name} 上传成功，路径已保存: ${serverFilePath}`
          );
        } else {
          message.warning(`文件 ${file.name} 上传成功，但未返回文件路径`);
        }
        message.success(`${file.name} file uploaded successfully`);
      } else if (info.file.status === "error") {
        message.error(`${file.name} file upload failed.`);
      }
    },
  };

  // ✅ 新增：点击按钮，将 uploadedFilePaths 发送到后端
  const handleSendPathsToBackend = async () => {
    if (uploadedFilePaths.length === 0) {
      message.warning("没有已上传的文件路径可发送");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          file_paths: uploadedFilePaths, // 发送整个路径数组
          pos_flow: posFlow,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const result = await response.json();

      try {
        // const parsedData = result.plotly_jsons[0];
        // const obj = JSON.parse(parsedData);

        const parsed = (result.plotly_jsons as string[]).map((str) =>
          JSON.parse(str)
        );
        setPlotlyObjs(parsed);

        // alert("parsedData:==" + parsedData);
        // setPlotlyData(obj.data);
      } catch (e) {
        console.error("解析plotly_json失败:", e);
        message.warning("图表数据解析失败");
        // setPlotlyData(null);
      }

      console.log("后端返回结果:", result);
      message.success("文件路径已成功发送至后端，并处理完成！");
    } catch (error) {
      console.error("发送文件路径失败:", error);
      message.error("发送文件路径到后端失败，请检查网络或后端接口");
    }
  };

  const resetAllPlots = async () => {
    if (uploadedFilePaths.length === 0) {
      message.warning("没有已上传的文件路径可发送");
      return;
    }
    setPlotlyObjs([]);
    setUploadedFilePaths([]);
  };

  const onRadioChange = (e: RadioChangeEvent) => {
    setPosFlow(e.target.value);
  };


const onFinish: FormProps<FieldType>['onFinish'] = (values) => {
  console.log('Success:', values);
};

const onFinishFailed: FormProps<FieldType>['onFinishFailed'] = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

  return (
    <>
    <Flex gap="large" wrap vertical>
    <Form
    name="basic"
    labelCol={{ span: 12 }}
    wrapperCol={{ span: 12 }}
    style={{ maxWidth: 1200 }}
    initialValues={{ remember: true }}
    onFinish={onFinish}
    onFinishFailed={onFinishFailed}
    autoComplete="off"
  >
    <Form.Item<FieldType> name="remember" valuePropName="checked" label={"数据文件"}>
      <Upload {...props}>
          <Button icon={<UploadOutlined />}>上传</Button>
    </Upload>
    </Form.Item>
    <Form.Item<FieldType>
      label="Ts1"
      name="Ts1"
    >
    <InputNumber min={1} max={10} step="0.00000000000001" defaultValue={1} style={{ width: '100%' }}/>
    </Form.Item>

    <Form.Item<FieldType>
      label="Ts2"
      name="Ts2"
    >
    <InputNumber min={1} max={10} step="0.00000000000001" defaultValue={1} style={{ width: '100%' }}/>
    </Form.Item>
    <Form.Item<FieldType> name="remember" valuePropName="checked" label={"电力类型"}
    rules={[{ required: true, message: 'Please input your username!' }]}
    >
        <Radio.Group
          value={posFlow}
          onChange={onRadioChange}
          options={[
            { value: 1, label: "pos" },
            { value: 0, label: "neg" },
          ]}
        />
    </Form.Item>
    
    <Form.Item<FieldType>
      label="DisturbTime"
      name="DisturbTime"
    >
    <InputNumber min={1} max={10} defaultValue={1} style={{ width: '100%' }}/>
    </Form.Item>
    
    <Form.Item<FieldType>
      label="BaseFrequencyOffset"
      name="BaseFrequencyOffset"
    >
    <InputNumber min={1} max={10} defaultValue={1} style={{ width: '100%' }}/>
    </Form.Item>

    <Form.Item {...tailLayout}>
        <Space>
          <Button type="primary" onClick={handleSendPathsToBackend}>
          生成
        </Button>
        <Button type="primary" onClick={resetAllPlots}>
          重置
        </Button>
        </Space>
      </Form.Item>
  </Form>
</Flex>
      {/* <PlotlyChart data={plotlyData} /> */}
      {/* 如果你用的是自己封装的 PlotlyChart，就这样： */}
      {/* {plotlyObjs.map((plotlyObj, idx) => (
        <PlotlyChart data={plotlyObj.data} layout={plotlyObj.layout} />
      ))} */}

      {plotlyObjs.length > 0 ? (
        plotlyObjs.map((plotlyObj, idx) => (
          <PlotlyChart
            key={idx}
            data={plotlyObj.data}
            layout={plotlyObj.layout}
          />
        ))
      ) : (
        <p>暂无图表数据</p>
      )}
    </>
  );
}

export default App;
