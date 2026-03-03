import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import signal, stats
from scipy.interpolate import interp1d, UnivariateSpline
from statsmodels.tsa.seasonal import STL
import io
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# ==================== Page Config ====================
st.set_page_config(
    page_title="时序数据分析工作站",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 14px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Helper Functions ====================

def detect_datetime_column(df):
    """自动识别时间列"""
    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            return col
        except:
            pass
    return None

def detect_numeric_columns(df):
    """识别数值列"""
    return df.select_dtypes(include=[np.number]).columns.tolist()

def compute_statistics(df):
    """计算统计描述"""
    return df.describe(include='all').T

def check_time_continuity(datetime_col, expected_freq=None):
    """检查时间连续性"""
    if len(datetime_col) < 2:
        return None, None
    
    diffs = datetime_col.diff()[1:]
    unique_diffs = diffs.value_counts().head()
    mode_diff = diffs.mode()[0] if len(diffs.mode()) > 0 else diffs.mean()
    
    # 识别断点
    breaks = diffs[diffs != mode_diff]
    
    return mode_diff, breaks

def detect_outliers(data, method='zscore', threshold=3, window_size=None):
    """异常检测
    method: 'zscore', 'iqr', 'rolling'
    """
    outliers = pd.Series(False, index=data.index)
    
    if method == 'zscore':
        z_scores = np.abs(stats.zscore(data.dropna()))
        outlier_indices = data.dropna().index[z_scores > threshold]
        outliers[outlier_indices] = True
        
    elif method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = (data < lower_bound) | (data > upper_bound)
        
    elif method == 'rolling':
        if window_size is None:
            window_size = max(3, len(data) // 20)
        rolling_mean = data.rolling(window=window_size, center=True).mean()
        rolling_std = data.rolling(window=window_size, center=True).std()
        outliers = (np.abs(data - rolling_mean) > threshold * rolling_std)
    
    return outliers

def interpolate_series(data, method='linear', order=2):
    """插补方法
    method: 'linear', 'polynomial', 'mean', 'ffill', 'bfill', 'spline'
    """
    result = data.copy()
    mask = data.isna()
    
    if not mask.any():
        return result
    
    if method == 'linear':
        result = result.interpolate(method='linear')
    
    elif method == 'polynomial':
        result = result.interpolate(method='polynomial', order=order)
    
    elif method == 'spline':
        valid_idx = np.where(~mask)[0]
        valid_vals = data.iloc[valid_idx].values
        try:
            spl = UnivariateSpline(valid_idx, valid_vals, k=min(3, len(valid_idx)-1))
            result.iloc[mask] = spl(np.where(mask)[0])
        except:
            result = result.interpolate(method='linear')
    
    elif method == 'mean':
        result = result.fillna(data.mean())
    
    elif method == 'ffill':
        result = result.ffill().bfill()
    
    elif method == 'bfill':
        result = result.bfill().ffill()
    
    return result

def seasonal_decompose_stl(data, period=None):
    """STL 分解"""
    if len(data) < 4 or data.isna().sum() == len(data):
        return None
    
    # 删除 NaN 值
    clean_data = data.dropna()
    if len(clean_data) < 4:
        return None
    
    if period is None:
        period = max(4, len(clean_data) // 12)
    
    try:
        result = STL(clean_data, seasonal=period if period % 2 == 1 else period + 1).fit()
        return result
    except:
        return None

def calculate_correlation_matrix(df):
    """关联性分析"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].corr()

def moving_average(data, window=5):
    """移动平均"""
    return data.rolling(window=window, center=True).mean()

# ==================== Session State ====================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'datetime_col' not in st.session_state:
    st.session_state.datetime_col = None
if 'numeric_cols' not in st.session_state:
    st.session_state.numeric_cols = []
if 'outliers_detected' not in st.session_state:
    st.session_state.outliers_detected = {}

# ==================== Main Application ====================
st.title("📊 时序数据分析工作站")
st.markdown("---")

# ==================== Sidebar Configuration ====================
with st.sidebar:
    st.header("⚙️ 配置中心")
    page = st.radio(
        "选择功能模块",
        [
            "📥 数据导入",
            "📋 数据概览",
            "🔍 数据清洗",
            "📈 可视化分析",
            "⚠️ 异常检测",
            "🔬 高级分析"
        ]
    )

# ==================== Page: Data Import ====================
if page == "📥 数据导入":
    st.header("📥 数据交互 (Data I/O)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("上传数据文件")
        uploaded_file = st.file_uploader(
            "支持 CSV 或 Excel 文件",
            type=["csv", "xlsx", "xls"]
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                
                # 自动识别列
                st.session_state.datetime_col = detect_datetime_column(df)
                st.session_state.numeric_cols = detect_numeric_columns(df)
                
                # 转换时间列格式
                if st.session_state.datetime_col:
                    df[st.session_state.datetime_col] = pd.to_datetime(df[st.session_state.datetime_col])
                    st.session_state.df = df.sort_values(st.session_state.datetime_col)
                
                st.success("✅ 文件上传成功！")
                st.info(f"自动识别到时间列：**{st.session_state.datetime_col}**\n\n数值列：{', '.join(st.session_state.numeric_cols)}")
                
            except Exception as e:
                st.error(f"❌ 文件读取失败：{str(e)}")
    
    with col2:
        st.subheader("数据概览")
        if st.session_state.df is not None:
            df = st.session_state.df
            st.metric("总行数", len(df))
            st.metric("总列数", len(df.columns))
            
            if st.session_state.datetime_col:
                time_span = df[st.session_state.datetime_col].max() - df[st.session_state.datetime_col].min()
                st.metric("时间跨度", str(time_span))
    
    # 显示数据预览
    if st.session_state.df is not None:
        st.subheader("数据前 5 行")
        st.dataframe(st.session_state.df.head(5), use_container_width=True)
        
        st.subheader("元数据信息")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**数据类型**")
            st.dataframe(pd.DataFrame({
                '列名': st.session_state.df.dtypes.index,
                '类型': st.session_state.df.dtypes.values
            }))
        
        with col2:
            st.write("**缺失值统计**")
            missing = pd.DataFrame({
                '列名': st.session_state.df.columns,
                '缺失数': st.session_state.df.isnull().sum(),
                '缺失率(%)': (st.session_state.df.isnull().sum() / len(st.session_state.df) * 100).round(2)
            })
            st.dataframe(missing[missing['缺失数'] > 0] if missing['缺失数'].sum() > 0 else missing)
        
        with col3:
            st.write("**导出选项**")
            if st.button("📥 导出为 CSV"):
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(
                    label="下载 CSV",
                    data=csv,
                    file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            if st.button("📥 导出为 Excel"):
                buffer = io.BytesIO()
                st.session_state.df.to_excel(buffer, index=False)
                st.download_button(
                    label="下载 Excel",
                    data=buffer.getvalue(),
                    file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# ==================== Page: Data Overview ====================
elif page == "📋 数据概览":
    if st.session_state.df is None:
        st.warning("⚠️ 请先在 '数据导入' 模块上传数据")
    else:
        st.header("📋 数据概览与统计 (EDA)")
        
        df = st.session_state.df
        
        # 实时预览
        with st.expander("📊 数据预览", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.dataframe(df.head(10), use_container_width=True)
            with col2:
                st.metric("数据形状", f"{df.shape[0]} × {df.shape[1]}")
        
        # 统计描述
        with st.expander("📈 统计描述", expanded=True):
            if st.session_state.numeric_cols:
                stats_df = compute_statistics(df[st.session_state.numeric_cols])
                st.dataframe(stats_df, use_container_width=True)
                
                # 详细统计
                selected_col = st.selectbox("选择列进行详细统计", st.session_state.numeric_cols)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("平均值", f"{df[selected_col].mean():.4f}")
                with col2:
                    st.metric("中位数", f"{df[selected_col].median():.4f}")
                with col3:
                    st.metric("标准差", f"{df[selected_col].std():.4f}")
                with col4:
                    st.metric("方差", f"{df[selected_col].var():.4f}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("偏度", f"{df[selected_col].skew():.4f}")
                with col2:
                    st.metric("峰度", f"{df[selected_col].kurtosis():.4f}")
        
        # 缺失值分析
        with st.expander("🔎 缺失值分析", expanded=True):
            missing_data = pd.DataFrame({
                '列名': df.columns,
                '缺失数': df.isnull().sum(),
                '缺失率(%)': (df.isnull().sum() / len(df) * 100).round(2)
            }).sort_values('缺失率(%)', ascending=False)
            
            st.dataframe(missing_data, use_container_width=True)
            
            if missing_data['缺失数'].sum() > 0:
                fig = go.Figure(data=[
                    go.Bar(
                        y=missing_data['列名'],
                        x=missing_data['缺失率(%)'],
                        orientation='h',
                        marker_color='#FF6B6B'
                    )
                ])
                fig.update_layout(
                    title="各列缺失率分布",
                    xaxis_title="缺失率 (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

# ==================== Page: Data Cleaning ====================
elif page == "🔍 数据清洗":
    if st.session_state.df is None:
        st.warning("⚠️ 请先在 '数据导入' 模块上传数据")
    else:
        st.header("🔍 时间完整性检查与插补")
        
        if st.session_state.datetime_col is None:
            st.warning("⚠️ 未检测到时间列，请确保数据中包含时间戳")
        else:
            df = st.session_state.df.copy()
            datetime_col = st.session_state.datetime_col
            
            # 时间连续性检查
            with st.expander("⏰ 时间连续性检查", expanded=True):
                mode_diff, breaks = check_time_continuity(df[datetime_col])
                
                if mode_diff is not None:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("主频率", str(mode_diff))
                    with col2:
                        st.metric("断点数", len(breaks))
                    with col3:
                        st.metric("连续性", f"{(1 - len(breaks)/len(df))*100:.2f}%")
                    
                    if len(breaks) > 0:
                        st.warning(f"⚠️ 检测到 {len(breaks)} 个时间断点")
                        st.dataframe(
                            pd.DataFrame({
                                '时间': df[datetime_col][breaks.index],
                                '时间差': breaks.values
                            }).head(10),
                            use_container_width=True
                        )
            
            # 插补方法配置
            with st.expander("🔧 智能插补配置", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_cols = st.multiselect(
                        "选择需要插补的列",
                        st.session_state.numeric_cols,
                        default=st.session_state.numeric_cols
                    )
                
                with col2:
                    method = st.selectbox(
                        "选择插补方法",
                        ['linear', 'polynomial', 'spline', 'mean', 'ffill', 'bfill']
                    )
                
                if method == 'polynomial':
                    poly_order = st.slider("多项式阶数", 1, 5, 2)
                else:
                    poly_order = 2
                
                if st.button("🔄 执行插补"):
                    df_interpolated = df.copy()
                    for col in selected_cols:
                        if col in df.columns:
                            df_interpolated[col] = interpolate_series(
                                df[col],
                                method=method,
                                order=poly_order
                            )
                    
                    st.session_state.df = df_interpolated
                    st.success("✅ 插补完成！")
                    st.dataframe(df_interpolated.head(10), use_container_width=True)
            
            # 对比显示
            with st.expander("📊 插补效果对比"):
                if len(selected_cols) > 0 and selected_cols[0] in df.columns:
                    compare_col = st.selectbox("选择要对比的列", selected_cols)
                    
                    df_interpolated = df.copy()
                    for col in selected_cols:
                        df_interpolated[col] = interpolate_series(df[col], method=method)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df[datetime_col],
                        y=df[compare_col],
                        mode='lines+markers',
                        name='原始数据',
                        line=dict(color='#FF6B6B')
                    ))
                    fig.add_trace(go.Scatter(
                        x=df_interpolated[datetime_col],
                        y=df_interpolated[compare_col],
                        mode='lines',
                        name='插补后',
                        line=dict(color='#4ECDC4')
                    ))
                    fig.update_layout(
                        title=f"{compare_col} - 插补效果对比",
                        xaxis_title="时间",
                        yaxis_title="数值",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)

# ==================== Page: Visualization ====================
elif page == "📈 可视化分析":
    if st.session_state.df is None:
        st.warning("⚠️ 请先在 '数据导入' 模块上传数据")
    else:
        st.header("📈 动态可视化")
        
        df = st.session_state.df
        datetime_col = st.session_state.datetime_col
        
        if datetime_col is None:
            st.warning("⚠️ 需要时间列来绘制时间序列图")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_cols = st.multiselect(
                    "选择要可视化的列",
                    st.session_state.numeric_cols,
                    default=st.session_state.numeric_cols[:1] if st.session_state.numeric_cols else []
                )
            
            with col2:
                chart_type = st.selectbox("图表类型", ['折线图', '区域图', '柱状图'])
            
            with col3:
                smooth_window = st.number_input("移动平均窗口", min_value=1, max_value=len(df)//2, value=5)
            
            if selected_cols:
                fig = go.Figure()
                
                for col in selected_cols:
                    if chart_type == '折线图':
                        fig.add_trace(go.Scatter(
                            x=df[datetime_col],
                            y=df[col],
                            mode='lines',
                            name=col,
                            hovertemplate='<b>%{fullData.name}</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
                        ))
                    elif chart_type == '区域图':
                        fig.add_trace(go.Scatter(
                            x=df[datetime_col],
                            y=df[col],
                            fill='tozeroy',
                            name=col,
                            hovertemplate='<b>%{fullData.name}</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
                        ))
                    elif chart_type == '柱状图':
                        fig.add_trace(go.Bar(
                            x=df[datetime_col],
                            y=df[col],
                            name=col,
                            hovertemplate='<b>%{fullData.name}</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
                        ))
                
                fig.update_layout(
                    title="时间序列数据",
                    xaxis_title="时间",
                    yaxis_title="数值",
                    height=500,
                    hovermode='x unified',
                    template='plotly_white'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 移动平均预览
                if st.checkbox("显示移动平均"):
                    fig_ma = go.Figure()
                    
                    for col in selected_cols:
                        ma = moving_average(df[col], window=int(smooth_window))
                        fig_ma.add_trace(go.Scatter(
                            x=df[datetime_col],
                            y=ma,
                            mode='lines',
                            name=f'{col} (MA-{int(smooth_window)})',
                            hovertemplate='<b>%{fullData.name}</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
                        ))
                    
                    fig_ma.update_layout(
                        title="移动平均（Moving Average）",
                        xaxis_title="时间",
                        yaxis_title="数值",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_ma, use_container_width=True)

# ==================== Page: Outlier Detection ====================
elif page == "⚠️ 异常检测":
    if st.session_state.df is None:
        st.warning("⚠️ 请先在 '数据导入' 模块上传数据")
    else:
        st.header("⚠️ 异常检测与处理")
        
        df = st.session_state.df.copy()
        datetime_col = st.session_state.datetime_col
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_col = st.selectbox("选择分析列", st.session_state.numeric_cols)
        
        with col2:
            method = st.selectbox("检测方法", ['zscore', 'iqr', 'rolling'])
        
        with col3:
            if method == 'zscore':
                threshold = st.slider("阈值 (σ)", 1, 5, 3)
                window = None
            elif method == 'iqr':
                threshold = 1.5
                window = None
            elif method == 'rolling':
                threshold = st.slider("标准差倍数", 1, 5, 3)
                window = st.slider("滚动窗口大小", 3, len(df)//4, max(3, len(df)//20))
        
        if st.button("🔍 执行异常检测"):
            outliers = detect_outliers(df[selected_col], method=method, threshold=threshold, window_size=window)
            st.session_state.outliers_detected[selected_col] = outliers
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("异常值数量", outliers.sum())
            with col2:
                st.metric("异常率 (%)", f"{(outliers.sum()/len(df)*100):.2f}%")
            
            # 可视化异常值
            fig = go.Figure()
            
            # 添加原始数据
            fig.add_trace(go.Scatter(
                x=df[datetime_col] if datetime_col else df.index,
                y=df[selected_col],
                mode='lines',
                name='正常数据',
                line=dict(color='#4ECDC4'),
                hovertemplate='<b>正常数据</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
            ))
            
            # 添加异常点
            if outliers.sum() > 0:
                fig.add_trace(go.Scatter(
                    x=df.loc[outliers, datetime_col] if datetime_col else df.index[outliers],
                    y=df.loc[outliers, selected_col],
                    mode='markers',
                    name='异常值',
                    marker=dict(size=10, color='#FF6B6B', symbol='diamond'),
                    hovertemplate='<b>异常值</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
                ))
            
            fig.update_layout(
                title=f"{selected_col} - 异常值检测 ({method})",
                xaxis_title="时间" if datetime_col else "索引",
                yaxis_title="数值",
                height=450,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 处理选项
            st.subheader("处理异常值")
            action = st.radio("选择处理方式", ['删除异常行', '视为缺失值并插补'])
            
            if action == '删除异常行':
                df_cleaned = df[~outliers]
                records_removed = len(df) - len(df_cleaned)
                st.success(f"✅ 已删除 {records_removed} 条异常记录")
            else:
                df_cleaned = df.copy()
                df_cleaned.loc[outliers, selected_col] = np.nan
                df_cleaned[selected_col] = interpolate_series(df_cleaned[selected_col], method='linear')
                st.success("✅ 已将异常值设为缺失并进行插补")
            
            if st.button("💾 保存清洗后的数据"):
                st.session_state.df = df_cleaned
                st.success("✅ 数据已更新")

# ==================== Page: Advanced Analysis ====================
elif page == "🔬 高级分析":
    if st.session_state.df is None:
        st.warning("⚠️ 请先在 '数据导入' 模块上传数据")
    else:
        st.header("🔬 高级分析扩展")
        
        df = st.session_state.df
        datetime_col = st.session_state.datetime_col
        
        analysis_type = st.selectbox(
            "选择分析类型",
            ['季节性分解 (STL)', '相关性分析 (热力图)', '多列对比']
        )
        
        # STL 分解
        if analysis_type == '季节性分解 (STL)':
            st.subheader("🔬 STL 分解（趋势、季节性、残留）")
            
            col1, col2 = st.columns(2)
            with col1:
                selected_col = st.selectbox("选择分解列", st.session_state.numeric_cols)
            with col2:
                period = st.number_input("季节周期", min_value=2, max_value=len(df)//2, value=12)
            
            if st.button("执行 STL 分解"):
                result = seasonal_decompose_stl(df[selected_col], period=int(period))
                
                if result is not None:
                    # 创建子图
                    fig = go.Figure()
                    
                    # 原始数据
                    fig.add_trace(go.Scatter(
                        y=df[selected_col],
                        name='原始数据',
                        mode='lines'
                    ))
                    
                    # 创建子图布局
                    fig = make_subplots(
                        rows=4, cols=1,
                        subplot_titles=('原始数据', '趋势', '季节性', '残留'),
                        vertical_spacing=0.1
                    )
                    
                    fig.add_trace(
                        go.Scatter(y=df[selected_col], name='原始数据', mode='lines'),
                        row=1, col=1
                    )
                    fig.add_trace(
                        go.Scatter(y=result.trend, name='趋势', mode='lines', line=dict(color='#FF6B6B')),
                        row=2, col=1
                    )
                    fig.add_trace(
                        go.Scatter(y=result.seasonal, name='季节性', mode='lines', line=dict(color='#4ECDC4')),
                        row=3, col=1
                    )
                    fig.add_trace(
                        go.Scatter(y=result.resid, name='残留', mode='lines', line=dict(color='#95E1D3')),
                        row=4, col=1
                    )
                    
                    fig.update_layout(height=800, title=f"{selected_col} - STL 分解", hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("❌ STL 分解失败，请检查数据")
        
        # 相关性分析
        elif analysis_type == '相关性分析 (热力图)':
            st.subheader("🔗 变量相关性分析")
            
            corr_matrix = calculate_correlation_matrix(df)
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu_r',
                zmid=0,
                zmin=-1,
                zmax=1,
                text=corr_matrix.values,
                texttemplate='%{text:.2f}',
                textfont={"size": 10},
                colorbar=dict(title="相关系数")
            ))
            
            fig.update_layout(
                title="变量相关系数热力图",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示相关性矩阵
            st.dataframe(corr_matrix, use_container_width=True)
            
            # 找到最强相关对
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        '变量1': corr_matrix.columns[i],
                        '变量2': corr_matrix.columns[j],
                        '相关系数': corr_matrix.iloc[i, j]
                    })
            
            corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('相关系数', ascending=False, key=abs)
            st.subheader("强相关变量对 (Top 10)")
            st.dataframe(corr_pairs_df.head(10), use_container_width=True)
        
        # 多列对比
        elif analysis_type == '多列对比':
            st.subheader("📊 多列对比分析")
            
            selected_cols = st.multiselect(
                "选择对比列",
                st.session_state.numeric_cols,
                default=st.session_state.numeric_cols[:2] if len(st.session_state.numeric_cols) > 1 else st.session_state.numeric_cols
            )
            
            normalize = st.checkbox("归一化显示")
            
            if selected_cols:
                fig = go.Figure()
                
                for col in selected_cols:
                    data = df[col].copy()
                    if normalize:
                        data = (data - data.min()) / (data.max() - data.min())
                    
                    fig.add_trace(go.Scatter(
                        x=df[datetime_col] if datetime_col else df.index,
                        y=data,
                        name=col,
                        mode='lines',
                        hovertemplate='<b>%{fullData.name}</b><br>时间: %{x}<br>数值: %{y:.4f}<extra></extra>'
                    ))
                
                title = "多列对比" + ("（归一化）" if normalize else "")
                fig.update_layout(
                    title=title,
                    xaxis_title="时间" if datetime_col else "索引",
                    yaxis_title="数值",
                    height=450,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)

# ==================== Footer ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>⏰ 时序数据分析工作站 v1.0 | Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
