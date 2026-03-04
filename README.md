# 📊 时序数据分析工作站

> **🌐 Language:** [English](README_EN.md) | **简体中文**

一个初步 Web 数据分析平台，专为时序数据处理与分析设计。

[![Streamlit App](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://laowu-code-timeseriesdataprocessanalysis-app-oyidri.streamlit.app/)
[![Python Version](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🌍 在线演示
**可以直接访问云端版本进行测试：** 👉 **[点击进入：时序数据分析工作站](https://laowu-code-timeseriesdataprocessanalysis-app-oyidri.streamlit.app/)**

---

## ✨ 核心功能

### 1. 📥 数据交互 (Data I/O)
- ✅ 支持上传 **CSV/Excel** 文件
- ✅ **自动识别**时间列（DateTime Column）和数值列
- ✅ 支持清洗数据**导出为 CSV/XLSX**

### 2. 📋 数据概览与统计 (EDA)
- ✅ **实时预览**：显示数据前 5 行及元数据（形状、数据类型）
- ✅ **统计描述**：自动计算 7 个统计指标
  - 均值 (Mean)
  - 中位数 (Median)
  - 标准差 (Std Dev)
  - 方差 (Variance)
  - 偏度 (Skewness)
  - 峰度 (Kurtosis)
  - 四分位数 (Quartiles)
- ✅ **缺失率分析**：统计各字段的缺失百分比及可视化

### 3. 🔍 时间完整性检查与插补 (Data Cleaning)
- ✅ **频率检测**：检测时间戳是否连续（如每 5 分钟一条）
- ✅ **断点识别**：自动找出时间序列中的缺失间隔
- ✅ **智能插补**：提供 6 种算法选择
  - Linear（线性插补）
  - Polynomial（多项式插补）
  - Spline（样条曲线插补）
  - Mean（均值填充）
  - FFill（前向填充）
  - BFill（后向填充）
- ✅ **效果对比**：可视化原始数据与插补结果的对比

### 4. 📈 动态可视化 (Visualization)
- ✅ **Plotly 交互式图表**
  - 支持 3 种图表类型：折线图、区域图、柱状图
  - **缩放、平移、数值查看**等交互功能
- ✅ **多变量对比显示**
- ✅ **移动平均（MA）预览**

### 5. ⚠️ 异常检测与处理 (Outlier Detection)
- ✅ **检测算法**（3 种）：
  - **3σ 原则**（Z-Score）
  - **IQR（四分位距）法**
  - **滚动窗口异常检测**
- ✅ **可视化标记**：在图表中以不同颜色/散点标记异常值位置
- ✅ **处理选项**：
  - 删除异常行
  - 视为缺失值并使用插补算法修复

### 6. 🔬 高级分析扩展 (Advanced Analysis)
- ✅ **季节性分解 (STL)**：分离趋势、季节性、残留分量
- ✅ **相关性分析**：
  - 显示变量间相关系数热力图
  - 列出强相关变量对 Top 10
- ✅ **多列对比**：
  - 支持归一化显示
  - 便于观察不同量级数据的变化趋势

---

## 🚀 快速开始

### ☁️ 云端运行（无需安装）
直接访问我们的在线版本：[Streamlit Cloud Link](https://laowu-code-timeseriesdataprocessanalysis-app-oyidri.streamlit.app/)

### 💻 本地运行
如果你需要在本地处理私密数据或大型文件，请按照以下步骤操作：

#### 环境要求
- Python 3.8 - 3.13
- pip (Python 包管理器)

#### 安装与运行
1. **克隆仓库**
   ```bash
   git clone [https://github.com/laowu-code/TimeSeriesDataProcessAnalysis.git](https://github.com/laowu-code/TimeSeriesDataProcessAnalysis.git)
   cd TimeSeriesDataProcessAnalysis

### 安装与运行

#### 步骤 1：安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤 2：启动应用
```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址：`http://localhost:8501`

---

## 📁 文件结构

```
DataPrecess/
├── app.py                    # 主应用程序
├── requirements.txt          # Python 依赖
├── README.md                 # 本文档
└── sample_data.csv          # 示例数据（可选）
```

---

## 📊 使用场景

### 1. **金融时序分析**
- 股票价格、汇率、加密货币数据分析
- 自动识别价格异常波动

### 2. **物联网/传感器数据**
- 温度、湿度、压力等多参数监测
- 处理传感器故障导致的数据缺失

### 3. **能源负荷预测**
- 电力负荷时序分析
- 峰值检测与异常告警

### 4. **气象数据分析**
- 温度、降水量等气象要素分析
- 季节性模式识别

### 5. **工业设备监控**
- 振动、温度等关键指标监控
- 故障预检测

---

## 🛠️ 技术栈

| 组件 | 库 | 用途 |
|------|----|----|
| **Web 框架** | Streamlit | 快速构建高性能 Web UI |
| **数据处理** | Pandas, NumPy | 表格数据处理与数值计算 |
| **统计分析** | SciPy, Statsmodels | 统计测试、时序分解 |
| **可视化** | Plotly | 交互式动态图表 |
| **Excel 支持** | Openpyxl | 读写 Excel 文件 |

---

## 📝 示例工作流

### 场景：分析温度传感器数据

```
1. 📥 数据导入
   └─ 上传 temperature_data.csv (时间列: timestamp, 数值列: temperature)

2. 📋 数据概览
   └─ 查看数据形状、类型、缺失情况
   └─ 显示均值: 25.3°C, 标准差: 3.2°C

3. 🔍 时间完整性检查
   └─ 检测到主频率: 5 分钟/条
   └─ 发现 3 个时间断点（传感器故障）
   └─ 使用线性插补修复缺失数据

4. 📈 可视化
   └─ 绘制原始温度时间序列
   └─ 添加 12 小时移动平均
   └─ 观察温度日变化规律

5. ⚠️ 异常检测
   └─ 使用 3σ 原则检测异常
   └─ 发现 5 处异常高温（传感器故障/环境异常）
   └─ 标记异常点，选择"视为缺失并插补"修复

6. 🔬 高级分析
   └─ STL 分解显示 24 小时季节性
   └─ 相关性分析：温度与湿度的相关系数 = 0.85
   └─ 结论：高温时相对湿度偏低

7. 💾 导出
   └─ 下载清洗后的数据为 CSV
```

---

## 🎨 配置提示

### 运行 app.py 之前的可选配置

#### 增加上传文件大小限制（如需要）
编辑 `~/.streamlit/config.toml`：
```toml
[server]
maxUploadSize = 500
```

#### 修改应用主题
编辑 `~/.streamlit/config.toml`：
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

---

## 🔧 常见问题

### Q1: 上传后没有自动识别时间列？
**A**: 确保时间列格式为标准的日期格式（如 `YYYY-MM-DD`、`YYYY-MM-DD HH:MM:SS`）

### Q2: 插补后数据为 NaN？
**A**: 这通常是因为：
- 时间序列过短（少于 4 行）
- 所有数据都是缺失值
- 请尝试使用 "mean" 或 "ffill" 方法

### Q3: STL 分解失败？
**A**: 检查：
- 数据长度是否足够（至少 4 个周期）
- 是否应调整季节周期参数

### Q4: 如何处理多个时间列？
**A**: 应用会自动识别第一个时间列，如需修改，请在上传前调整 CSV 列顺序

---

## 📖 详细功能说明

### 插补算法对比

| 算法 | 优点 | 缺点 | 适用场景 |
|------|------|------|--------|
| **Linear** | 简单快速 | 忽略趋势 | 短期缺失 |
| **Polynomial** | 拟合曲线 | 容易过拟合 | 平滑变化 |
| **Spline** | 光滑连续 | 需要足量数据 | 复杂趋势 |
| **Mean** | 不改变分布 | 丢失时间信息 | 随机缺失 |
| **FFill** | 保留最后值 | 可能过时 | 缓变量 |
| **BFill** | 保留后续值 | 可能提前 | 突变识别 |

### 异常检测算法对比

| 算法 | 原理 | 参数 | 适用场景 |
|------|------|------|--------|
| **Z-Score** | 正态分布离差 | σ 倍数（通常 3） | 近似正态分布数据 |
| **IQR** | 四分位距方法 | 固定 1.5 倍 IQR | 无参数、robust |
| **Rolling** | 滚动窗口离差 | 窗口大小、σ 倍数 | 非平稳时序、局部异常 |

---

## 🎯 改进方向（Future Features）

- [ ] 实时数据流接入（WebSocket）
- [ ] 自动异常告警对接（邮件/钉钉）
- [ ] 预测模型集成（ARIMA、Prophet）
- [ ] 多文件批量处理
- [ ] 自定义插值算法
- [ ] 数据库直连

---

## 📄 许可证

MIT License - 自由使用与修改

---

## 💬 反馈与支持

如有问题或建议，欢迎提出 Issues 或 Discussions！

---

**祝您使用愉快！** 📊✨
