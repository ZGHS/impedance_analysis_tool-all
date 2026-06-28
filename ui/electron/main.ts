import { app, BrowserWindow } from "electron";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { spawn, ChildProcessWithoutNullStreams } from "node:child_process"; // 【新增】导入 child_process 模块


const __dirname = path.dirname(fileURLToPath(import.meta.url));

// The built directory structure
//
// ├─┬─┬ dist
// │ │ └── index.html
// │ │
// │ ├─┬ dist-electron
// │ │ ├── main.js
// │ │ └── preload.mjs
// │
process.env.APP_ROOT = path.join(__dirname, "..");

// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
export const VITE_DEV_SERVER_URL = process.env["VITE_DEV_SERVER_URL"];
export const MAIN_DIST = path.join(process.env.APP_ROOT, "dist-electron");
export const RENDERER_DIST = path.join(process.env.APP_ROOT, "dist");

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL
  ? path.join(process.env.APP_ROOT, "public")
  : RENDERER_DIST;

let win: BrowserWindow | null;

// --- 新增：Python 子进程管理 ---
let pythonProcess: ChildProcessWithoutNullStreams | null = null;

/**
 * 启动Python后台服务
 */
function startPythonServer() {
  const exePy=false;
  // 确定Python可执行文件的路径
  let pythonExecutable;
  // const pythonDir = path.join(process.env.APP_ROOT, "python", "dist"); // Python打包后的目录
  const pythonDir = app.isPackaged
    ? path.join(process.resourcesPath, "python")
    : path.join(process.env.APP_ROOT, "python", "dist");
  if (app.isPackaged) {
    // 生产环境：运行打包好的可执行文件
    const executableName = process.platform === "win32" ? "main.exe" : "main";
    pythonExecutable = path.join(pythonDir, executableName);
    console.log("Starting packaged Python server:", pythonExecutable);
    pythonProcess = spawn(pythonExecutable);
  } else {
    // 开发环境：直接用Python解释器运行源码
    // const scriptPath = path.join(__dirname, "..", "..", "python", "main.py"); // 假设你的Python源码在项目根目录的 python_server 文件夹下
    if(exePy){
    const scriptPath = path.join(process.env.APP_ROOT, "python", "main.py");

    console.log("Starting development Python server:", scriptPath);
    pythonProcess = spawn("python", [scriptPath]); // 使用 'python3' 如果你的系统默认是python3
    }else{
    const executableName = process.platform === "win32" ? "main.exe" : "main";
    pythonExecutable = path.join(pythonDir, executableName);
    console.log("Starting packaged Python server:", pythonExecutable);
    pythonProcess = spawn(pythonExecutable);
    }
  }

  // 监听Python的输出，方便调试
  pythonProcess.stdout.on("data", (data) => {
    console.log(`[Python Server] stdout: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`[Python Server] stderr: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python server process closed with code ${code}`);
    pythonProcess = null;
  });
  pythonProcess.on("error", (err) => {
    console.error("Failed to start Python server:", err);
  });
}

/**
 * 停止Python后台服务
 */
function stopPythonServer() {
  if (pythonProcess) {
    console.log("Stopping Python server...");
    pythonProcess.kill();
    // pythonProcess = null;
  }
}
// --- 新增结束 ---

function createWindow() {
  win = new BrowserWindow({
    icon: path.join(process.env.VITE_PUBLIC, "electron-vite.svg"),
    title: "阻抗分析工具",
    webPreferences: {
      preload: path.join(__dirname, "preload.mjs"),
    },
  });

  // Test active push message to Renderer-process.
  win.webContents.on("did-finish-load", () => {
    win?.webContents.send("main-process-message", new Date().toLocaleString());
  });

  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL);
  } else {
    // win.loadFile('dist/index.html')
    win.loadFile(path.join(RENDERER_DIST, "index.html"));
  }
  // 打开开发者工具（控制台）
  // win.webContents.openDevTools();
}

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    stopPythonServer();
    app.quit();
    win = null;
  }
});

app.on("activate", () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    // startPythonServer();
    createWindow();
  }
});
// app.whenReady().then(createWindow);
app.whenReady().then(() => {
  // startPythonServer();
  createWindow();
});
