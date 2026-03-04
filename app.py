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

# ==================== Internationalization ====================
translations = {
    'en': {
        'page_title': "Time Series Analysis Workstation",
        'app_title': "📊 Time Series Analysis Workstation",
        'config_center': "⚙️ Configuration Center",
        'language_label': "Language",
        'english': "English",
        'chinese': "中文",
        'select_module': "Select Module",
        'data_import': "📥 Data Import",
        'data_overview': "📋 Data Overview",
        'data_cleaning': "🔍 Data Cleaning",
        'visualization': "📈 Visualization",
        'outlier_detection': "⚠️ Anomaly Detection",
        'advanced_analysis': "🔬 Advanced Analysis",
        'upload_file': "Upload Data File",
        'support_file': "Supports CSV or Excel files",
        'detected_datetime': "Automatically detected datetime column:",
        'numeric_cols': "Numeric columns:",
        'data_overview_title': "Data Overview",
        'total_rows': "Total Rows",
        'total_cols': "Total Columns",
        'time_span': "Time Span",
        'first_rows': "First 5 Rows of Data",
        'metadata_info': "Metadata Information",
        'data_types': "**Data Types**",
        'missing_stats': "**Missing Value Statistics**",
        'export_options': "**Export Options**",
        'export_csv': "📥 Export as CSV",
        'download_csv': "Download CSV",
        'export_excel': "📥 Export as Excel",
        'download_excel': "Download Excel",
        'warning_upload_first': "⚠️ Please upload data in the 'Data Import' module first",
        'overview_eda': "📋 Data Overview and Statistics (EDA)",
        'data_preview': "📊 Data Preview",
        'data_shape': "Data Shape",
        'stats_desc': "📈 Statistical Description",
        'select_col_stats': "Select column for detailed stats",
        'mean': "Mean",
        'median': "Median",
        'std': "Std Dev",
        'variance': "Variance",
        'skewness': "Skewness",
        'kurtosis': "Kurtosis",
        'missing_analysis': "🔎 Missing Value Analysis",
        'missing_rate_dist': "Missing Rate Distribution by Column",
        'time_integrity': "🔍 Time Integrity Check and Interpolation",
        'no_datetime_warning': "⚠️ No datetime column detected, ensure data has timestamps",
        'time_continuity': "⏰ Time Continuity Check",
        'main_freq': "Main Frequency",
        'num_breaks': "Number of Breaks",
        'continuity': "Continuity",
        'break_detected': "⚠️ Detected {n} time breaks",
        'time_col': "Time",
        'time_diff': "Time Difference",
        'interpolation_config': "🔧 Intelligent Interpolation Configuration",
        'select_cols_to_interp': "Select columns to interpolate",
        'interp_method': "Choose interpolation method",
        'poly_order': "Polynomial Order",
        'run_interp': "🔄 Execute Interpolation",
        'interp_done': "✅ Interpolation completed!",
        'interp_effect_comparison': "📊 Interpolation Effect Comparison",
        'choose_compare_col': "Choose column to compare",
        'orig_data': "Original Data",
        'after_interp': "After Interpolation",
        'compare_title': "{col} - Interpolation Comparison",
        'dynamic_visualization': "📈 Dynamic Visualization",
        'chart_type': "Chart Type",
        'line_chart': "Line",
        'area_chart': "Area",
        'bar_chart': "Bar",
        'moving_average_window': "Moving average window",
        'show_moving_average': "Show moving average",
        'time_series_data': "Time Series Data",
        'anomaly_detection': "⚠️ Anomaly Detection and Handling",
        'select_analysis_col': "Select column to analyze",
        'detection_method': "Detection method",
        'threshold_sigma': "Threshold (σ)",
        'std_multiplier': "Std multiplier",
        'rolling_window': "Rolling window size",
        'run_detection': "🔍 Execute Anomaly Detection",
        'num_outliers': "Number of outliers",
        'outlier_rate': "Outlier rate (%)",
        'normal_data': "Normal Data",
        'outliers': "Outliers",
        'detection_title': "{col} - Outlier Detection ({method})",
        'handle_outliers': "Handle outliers",
        'delete_rows': "Delete rows",
        'mark_and_interp': "Mark as missing and interpolate",
        'save_clean': "💾 Save cleaned data",
        'cleaning_complete': "✅ Data updated",
        'advanced_analysis': "🔬 Advanced Analysis Extensions",
        'choose_analysis': "Choose analysis type",
        'stl_decomposition': "Seasonal Decomposition (STL)",
        'correlation_heatmap': "Correlation Analysis (Heatmap)",
        'multi_column': "Multi-column Comparison",
        'stl_header': "🔬 STL Decomposition (Trend, Seasonal, Residual)",
        'choose_stl_col': "Choose column to decompose",
        'seasonal_period': "Seasonal period",
        'run_stl': "Execute STL Decomposition",
        'stl_error': "❌ STL decomposition failed, please check data",
        'variable_correlation': "🔗 Variable Correlation Analysis",
        'correlation_heatmap_title': "Variable Correlation Heatmap",
        'strong_pairs': "Strongly correlated pairs (Top 10)",
        'multi_compare_header': "📊 Multi-column Comparison Analysis",
        'normalize': "Normalize display",
        'comparison_title': "Multi-column comparison",
        'comparison_normalized': "Multi-column comparison (normalized)",
        'footer': "⏰ Time Series Analysis Workstation v1.0 | Built with Streamlit & Plotly",
        'data_io': "📥 Data I/O",
        'file_upload_success': "✅ File uploaded successfully!",
        'file_read_error': "❌ File read failed:",
        'data_overview_subtitle': "Data Overview",
        'need_time_col': "⚠️ A time column is required to draw time series charts",
        'handle_outliers_header': "Handle outliers",
        'delete_rows_action': "Delete rows",
        'mark_missing_action': "Mark as missing and interpolate",
        'detected_time_col': "Automatically detected datetime column:",
        'detected_numeric_cols': "Numeric columns:",
        'num_time_breaks': "⚠️ Detected {n} time breaks",
        'stl_decomp_header': "🔬 STL Decomposition (Trend, Seasonal, Residual)",
        'stl_decomp_button': "Execute STL Decomposition",
        'choose_stl_col_label': "Choose column to decompose",
        'seasonal_period_label': "Seasonal period",
        'corr_analysis_header': "🔗 Variable Correlation Analysis",
        'multi_compare_header_label': "📊 Multi-column Comparison Analysis",
        'normalize_label': "Normalize display",
    },
    'zh': {
        'page_title': "时序数据分析工作站",
        'app_title': "📊 时序数据分析工作站",
        'config_center': "⚙️ 配置中心",
        'language_label': "语言 / Language",
        'english': "English",
        'chinese': "中文",
        'select_module': "选择功能模块",
        'data_import': "📥 数据导入",
        'data_overview': "📋 数据概览",
        'data_cleaning': "🔍 数据清洗",
        'visualization': "📈 可视化分析",
        'outlier_detection': "⚠️ 异常检测",
        'advanced_analysis': "🔬 高级分析",
        'upload_file': "上传数据文件",
        'support_file': "支持 CSV 或 Excel 文件",
        'detected_datetime': "自动识别到时间列：",
        'numeric_cols': "数值列：",
        'data_overview_title': "数据概览",
        'total_rows': "总行数",
        'total_cols': "总列数",
        'time_span': "时间跨度",
        'first_rows': "数据前 5 行",
        'metadata_info': "元数据信息",
        'data_types': "**数据类型**",
        'missing_stats': "**缺失值统计**",
        'export_options': "**导出选项**",
        'export_csv': "📥 导出为 CSV",
        'download_csv': "下载 CSV",
        'export_excel': "📥 导出为 Excel",
        'download_excel': "下载 Excel",
        'warning_upload_first': "⚠️ 请先在 '数据导入' 模块上传数据",
        'overview_eda': "📋 数据概览与统计 (EDA)",
        'data_preview': "📊 数据预览",
        'data_shape': "数据形状",
        'stats_desc': "📈 统计描述",
        'select_col_stats': "选择列进行详细统计",
        'mean': "平均值",
        'median': "中位数",
        'std': "标准差",
        'variance': "方差",
        'skewness': "偏度",
        'kurtosis': "峰度",
        'missing_analysis': "🔎 缺失值分析",
        'missing_rate_dist': "各列缺失率分布",
        'time_integrity': "🔍 时间完整性检查与插补",
        'no_datetime_warning': "⚠️ 未检测到时间列，请确保数据中包含时间戳",
        'time_continuity': "⏰ 时间连续性检查",
        'main_freq': "主频率",
        'num_breaks': "断点数",
        'continuity': "连续性",
        'break_detected': "⚠️ 检测到 {n} 个时间断点",
        'time_col': "时间",
        'time_diff': "时间差",
        'interpolation_config': "🔧 智能插补配置",
        'select_cols_to_interp': "选择需要插补的列",
        'interp_method': "选择插补方法",
        'poly_order': "多项式阶数",
        'run_interp': "🔄 执行插补",
        'interp_done': "✅ 插补完成！",
        'interp_effect_comparison': "📊 插补效果对比",
        'choose_compare_col': "选择要对比的列",
        'orig_data': "原始数据",
        'after_interp': "插补后",
        'compare_title': "{col} - 插补效果对比",
        'dynamic_visualization': "📈 动态可视化",
        'chart_type': "图表类型",
        'line_chart': "折线图",
        'area_chart': "区域图",
        'bar_chart': "柱状图",
        'moving_average_window': "移动平均窗口",
        'show_moving_average': "显示移动平均",
        'time_series_data': "时间序列数据",
        'anomaly_detection': "⚠️ 异常检测与处理",
        'select_analysis_col': "选择分析列",
        'detection_method': "检测方法",
        'threshold_sigma': "阈值 (σ)",
        'std_multiplier': "标准差倍数",
        'rolling_window': "滚动窗口大小",
        'run_detection': "🔍 执行异常检测",
        'num_outliers': "异常值数量",
        'outlier_rate': "异常率 (%)",
        'normal_data': "正常数据",
        'outliers': "异常值",
        'detection_title': "{col} - 异常值检测 ({method})",
        'handle_outliers': "处理异常值",
        'delete_rows': "删除异常行",
        'mark_and_interp': "视为缺失值并插补",
        'save_clean': "💾 保存清洗后的数据",
        'cleaning_complete': "✅ 数据已更新",
        'advanced_analysis': "🔬 高级分析扩展",
        'choose_analysis': "选择分析类型",
        'stl_decomposition': "季节性分解 (STL)",
        'correlation_heatmap': "相关性分析 (热力图)",
        'multi_column': "多列对比",
        'stl_header': "🔬 STL 分解（趋势、季节性、残留）",
        'choose_stl_col': "选择分解列",
        'seasonal_period': "季节周期",
        'run_stl': "执行 STL 分解",
        'stl_error': "❌ STL 分解失败，请检查数据",
        'variable_correlation': "🔗 变量相关性分析",
        'correlation_heatmap_title': "变量相关系数热力图",
        'strong_pairs': "强相关变量对 (Top 10)",
        'multi_compare_header': "📊 多列对比分析",
        'normalize': "归一化显示",
        'comparison_title': "多列对比",
        'comparison_normalized': "多列对比（归一化）",
        'footer': "⏰ 时序数据分析工作站 v1.0 | Built with Streamlit & Plotly",
        'data_io': "📥 数据交互 (Data I/O)",
        'file_upload_success': "✅ 文件上传成功！",
        'file_read_error': "❌ 文件读取失败：",
        'data_overview_subtitle': "数据概览",
        'need_time_col': "⚠️ 需要时间列来绘制时间序列图",
        'handle_outliers_header': "处理异常值",
        'delete_rows_action': "删除异常行",
        'mark_missing_action': "视为缺失值并插补",
        'detected_time_col': "自动识别到时间列：",
        'detected_numeric_cols': "数值列：",
        'num_time_breaks': "⚠️ 检测到 {n} 个时间断点",
        'stl_decomp_header': "🔬 STL 分解（趋势、季节性、残留）",
        'stl_decomp_button': "执行 STL 分解",
        'choose_stl_col_label': "选择分解列",
        'seasonal_period_label': "季节周期",
        'corr_analysis_header': "🔗 变量相关性分析",
        'multi_compare_header_label': "📊 多列对比分析",
        'normalize_label': "归一化显示",
    }
}

def t(key):
    lang = st.session_state.get('lang', 'en')
    return translations.get(lang, translations['en']).get(key, key)

# ==================== Page Config ====================
st.set_page_config(
    page_title=t('page_title'),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 20px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Header styling */
    h1 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    h2 {
        color: #2ca02c;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    h3 {
        color: #d62728;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 14px;
        font-weight: 600;
        color: #333;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Metric cards */
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #155a8f;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0f2f6 !important;
        border-radius: 5px;
    }
    
    /* Select box styling */
    .stSelectbox, .stMultiSelect {
        color: #333;
    }
    
    /* Warning and info boxes */
    .stWarning {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        padding: 15px;
    }
    
    .stSuccess {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        padding: 15px;
    }
    
    .stError {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        padding: 15px;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        padding: 15px;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    
    /* Radio button styling */
    .stRadio {
        margin: 15px 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding-top: 20px;
    }
    
    /* Divider line */
    hr {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Helper Functions ====================

def detect_datetime_column(df):
    """Auto-detect datetime column"""
    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            return col
        except:
            pass
    return None

def detect_numeric_columns(df):
    """Detect numeric columns"""
    return df.select_dtypes(include=[np.number]).columns.tolist()

def compute_statistics(df):
    """Compute statistical description"""
    return df.describe(include='all').T

def check_time_continuity(datetime_col, expected_freq=None):
    """Check time series continuity"""
    if len(datetime_col) < 2:
        return None, None
    
    diffs = datetime_col.diff()[1:]
    unique_diffs = diffs.value_counts().head()
    mode_diff = diffs.mode()[0] if len(diffs.mode()) > 0 else diffs.mean()
    
    # Identify breaks
    breaks = diffs[diffs != mode_diff]
    
    return mode_diff, breaks

def detect_outliers(data, method='zscore', threshold=3, window_size=None):
    """Outlier detection
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
    """Interpolation method
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
    """STL Decomposition"""
    if len(data) < 4 or data.isna().sum() == len(data):
        return None
    
    # Remove NaN values
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
    """Correlation Analysis"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].corr()

def moving_average(data, window=5):
    """Moving Average"""
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
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-size: 2.5em; color: #1f77b4; margin: 0;'>📊 Time Series Analysis Workstation</h1>
    <p style='font-size: 1.1em; color: #666; margin-top: 10px;'>Advanced Time Series Data Analysis & Visualization Platform</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ==================== Sidebar Configuration ====================
# Page identifiers for consistent language switching
PAGE_KEYS = {
    'data_import': 'data_import',
    'data_overview': 'data_overview',
    'data_cleaning': 'data_cleaning',
    'visualization': 'visualization',
    'outlier_detection': 'outlier_detection',
    'advanced_analysis': 'advanced_analysis'
}

with st.sidebar:
    # language switch radio
    lang_choice = st.radio(
        t('language_label'),
        [t('english'), t('chinese')],
        index=0 if st.session_state.get('lang', 'en') == 'en' else 1
    )
    st.session_state.lang = 'en' if lang_choice == t('english') else 'zh'

    st.header(t('config_center'))
    page_options = [
        (PAGE_KEYS['data_import'], t('data_import')),
        (PAGE_KEYS['data_overview'], t('data_overview')),
        (PAGE_KEYS['data_cleaning'], t('data_cleaning')),
        (PAGE_KEYS['visualization'], t('visualization')),
        (PAGE_KEYS['outlier_detection'], t('outlier_detection')),
        (PAGE_KEYS['advanced_analysis'], t('advanced_analysis'))
    ]
    
    page = st.radio(
        t('select_module'),
        [label for _, label in page_options],
        index=0
    )
    
    # Convert display text back to page key
    page_key = next((key for key, label in page_options if label == page), PAGE_KEYS['data_import'])

# ==================== Page: Data Import ====================
if page_key == PAGE_KEYS['data_import']:
    st.header(t('data_io'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t('upload_file'))
        uploaded_file = st.file_uploader(
            t('support_file'),
            type=["csv", "xlsx", "xls"]
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                
                # Auto-detect columns
                st.session_state.datetime_col = detect_datetime_column(df)
                st.session_state.numeric_cols = detect_numeric_columns(df)
                
                # Convert datetime column format
                if st.session_state.datetime_col:
                    df[st.session_state.datetime_col] = pd.to_datetime(df[st.session_state.datetime_col])
                    st.session_state.df = df.sort_values(st.session_state.datetime_col)
                
                st.success(t('file_upload_success'))
                st.info(f"{t('detected_time_col')}**{st.session_state.datetime_col}**\n\n{t('detected_numeric_cols')}{', '.join(st.session_state.numeric_cols)}")
                
            except Exception as e:
                st.error(f"{t('file_read_error')}{str(e)}")
    
    with col2:
        st.subheader(t('data_overview_subtitle'))
        if st.session_state.df is not None:
            df = st.session_state.df
            st.metric(t('total_rows'), len(df))
            st.metric(t('total_cols'), len(df.columns))
            
            if st.session_state.datetime_col:
                time_span = df[st.session_state.datetime_col].max() - df[st.session_state.datetime_col].min()
                st.metric(t('time_span'), str(time_span))
    
    # 显示数据预览
    if st.session_state.df is not None:
        st.subheader(t('first_rows'))
        st.dataframe(st.session_state.df.head(5), use_container_width=True)
        
        st.subheader(t('metadata_info'))
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(t('data_types'))
            st.dataframe(pd.DataFrame({
                'Column Name': st.session_state.df.dtypes.index,
                'Type': st.session_state.df.dtypes.values
            }))
        
        with col2:
            st.write(t('missing_stats'))
            missing = pd.DataFrame({
                'Column Name': st.session_state.df.columns,
                'Missing Count': st.session_state.df.isnull().sum(),
                'Missing Rate (%)': (st.session_state.df.isnull().sum() / len(st.session_state.df) * 100).round(2)
            })
            st.dataframe(missing[missing['Missing Count'] > 0] if missing['Missing Count'].sum() > 0 else missing)
        
        with col3:
            st.write(t('export_options'))
            if st.button(t('export_csv')):
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(
                    label=t('download_csv'),
                    data=csv,
                    file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            if st.button(t('export_excel')):
                buffer = io.BytesIO()
                st.session_state.df.to_excel(buffer, index=False)
                st.download_button(
                    label=t('download_excel'),
                    data=buffer.getvalue(),
                    file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# ==================== Page: Data Overview ====================
elif page_key == PAGE_KEYS['data_overview']:
    if st.session_state.df is None:
        st.warning(t('warning_upload_first'))
    else:
        st.header(t('overview_eda'))
        
        df = st.session_state.df
        
        # Real-time preview
        with st.expander(t('data_preview'), expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.dataframe(df.head(10), use_container_width=True)
            with col2:
                st.metric(t('data_shape'), f"{df.shape[0]} × {df.shape[1]}")
        
        # Statistical description
        with st.expander(t('stats_desc'), expanded=True):
            if st.session_state.numeric_cols:
                stats_df = compute_statistics(df[st.session_state.numeric_cols])
                st.dataframe(stats_df, use_container_width=True)
                
                # Detailed statistics
                selected_col = st.selectbox(t('select_col_stats'), st.session_state.numeric_cols)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(t('mean'), f"{df[selected_col].mean():.4f}")
                with col2:
                    st.metric(t('median'), f"{df[selected_col].median():.4f}")
                with col3:
                    st.metric(t('std'), f"{df[selected_col].std():.4f}")
                with col4:
                    st.metric(t('variance'), f"{df[selected_col].var():.4f}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(t('skewness'), f"{df[selected_col].skew():.4f}")
                with col2:
                    st.metric(t('kurtosis'), f"{df[selected_col].kurtosis():.4f}")
        
        # Missing value analysis
        with st.expander(t('missing_analysis'), expanded=True):
            missing_data = pd.DataFrame({
                'Column Name': df.columns,
                'Missing Count': df.isnull().sum(),
                'Missing Rate (%)': (df.isnull().sum() / len(df) * 100).round(2)
            }).sort_values('Missing Rate (%)', ascending=False)
            
            st.dataframe(missing_data, use_container_width=True)
            
            if missing_data['Missing Count'].sum() > 0:
                fig = go.Figure(data=[
                    go.Bar(
                        y=missing_data['列名'],
                        x=missing_data['Missing Rate (%)'],
                        orientation='h',
                        marker_color='#FF6B6B'
                    )
                ])
                fig.update_layout(
                    title=t('missing_rate_dist'),
                    xaxis_title=t('outlier_rate'),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

# ==================== Page: Data Cleaning ====================
elif page_key == PAGE_KEYS['data_cleaning']:
    if st.session_state.df is None:
        st.warning(t('warning_upload_first'))
    else:
        st.header(t('time_integrity'))
        
        if st.session_state.datetime_col is None:
            st.warning(t('no_datetime_warning'))
        else:
            df = st.session_state.df.copy()
            datetime_col = st.session_state.datetime_col
            
            # Time continuity check
            with st.expander(t('time_continuity'), expanded=True):
                mode_diff, breaks = check_time_continuity(df[datetime_col])
                
                if mode_diff is not None:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(t('main_freq'), str(mode_diff))
                    with col2:
                        st.metric(t('num_breaks'), len(breaks))
                    with col3:
                        st.metric(t('continuity'), f"{(1 - len(breaks)/len(df))*100:.2f}%")
                    
                    if len(breaks) > 0:
                        st.warning(t('break_detected').format(n=len(breaks)))
                        st.dataframe(
                            pd.DataFrame({
                                t('time_col'): df[datetime_col][breaks.index],
                                t('time_diff'): breaks.values
                            }).head(10),
                            use_container_width=True
                        )
            
            # Interpolation configuration
            with st.expander(t('interpolation_config'), expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_cols = st.multiselect(
                        t('select_cols_to_interp'),
                        st.session_state.numeric_cols,
                        default=st.session_state.numeric_cols
                    )
                
                with col2:
                    method = st.selectbox(
                        t('interp_method'),
                        ['linear', 'polynomial', 'spline', 'mean', 'ffill', 'bfill']
                    )
                
                if method == 'polynomial':
                    poly_order = st.slider(t('poly_order'), 1, 5, 2)
                else:
                    poly_order = 2
                
                if st.button(t('run_interp')):
                    df_interpolated = df.copy()
                    for col in selected_cols:
                        if col in df.columns:
                            df_interpolated[col] = interpolate_series(
                                df[col],
                                method=method,
                                order=poly_order
                            )
                    
                    st.session_state.df = df_interpolated
                    st.success(t('interp_done'))
                    st.dataframe(df_interpolated.head(10), use_container_width=True)
            
            # Comparison display
            with st.expander(t('interp_effect_comparison')):
                if len(selected_cols) > 0 and selected_cols[0] in df.columns:
                    compare_col = st.selectbox(t('choose_compare_col'), selected_cols)
                    
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
                        title=f"{compare_col} - {t('compare_title').split(' - ')[1]}",
                        xaxis_title=t('time_col'),
                        yaxis_title="Value",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)

# ==================== Page: Visualization ====================
elif page_key == PAGE_KEYS['visualization']:
    if st.session_state.df is None:
        st.warning(t('warning_upload_first'))
    else:
        st.header(t('dynamic_visualization'))
        
        df = st.session_state.df
        datetime_col = st.session_state.datetime_col
        
        if datetime_col is None:
            st.warning(t('need_time_col'))
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_cols = st.multiselect(
                    "Select columns to visualize",
                    st.session_state.numeric_cols,
                    default=st.session_state.numeric_cols[:1] if st.session_state.numeric_cols else []
                )
            
            with col2:
                chart_type = st.selectbox(t('chart_type'), [t('line_chart'), t('area_chart'), t('bar_chart')])
            
            with col3:
                smooth_window = st.number_input(t('moving_average_window'), min_value=1, max_value=len(df)//2, value=5)
            
            if selected_cols:
                fig = go.Figure()
                
                for col in selected_cols:
                    if chart_type == t('line_chart'):
                        fig.add_trace(go.Scatter(
                            x=df[datetime_col],
                            y=df[col],
                            mode='lines',
                            name=col,
                            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
                        ))
                    elif chart_type == t('area_chart'):
                        fig.add_trace(go.Scatter(
                            x=df[datetime_col],
                            y=df[col],
                            fill='tozeroy',
                            name=col,
                            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
                        ))
                    elif chart_type == t('bar_chart'):
                        fig.add_trace(go.Bar(
                            x=df[datetime_col],
                            y=df[col],
                            name=col,
                            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
                        ))
                
                fig.update_layout(
                    title=t('time_series_data'),
                    xaxis_title=t('time_col'),
                    yaxis_title="Value",
                    height=500,
                    hovermode='x unified',
                    template='plotly_white'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Moving average preview
                if st.checkbox(t('show_moving_average')):
                    fig_ma = go.Figure()
                    
                    for col in selected_cols:
                        ma = moving_average(df[col], window=int(smooth_window))
                        fig_ma.add_trace(go.Scatter(
                            x=df[datetime_col],
                            y=ma,
                            mode='lines',
                            name=f'{col} (MA-{int(smooth_window)})',
                            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
                        ))
                    
                    fig_ma.update_layout(
                        title=t('show_moving_average'),
                        xaxis_title=t('time_col'),
                        yaxis_title="Value",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_ma, use_container_width=True)

# ==================== Page: Outlier Detection ====================
elif page_key == PAGE_KEYS['outlier_detection']:
    if st.session_state.df is None:
        st.warning(t('warning_upload_first'))
    else:
        st.header(t('anomaly_detection'))
        
        df = st.session_state.df.copy()
        datetime_col = st.session_state.datetime_col
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_col = st.selectbox(t('select_analysis_col'), st.session_state.numeric_cols)
        
        with col2:
            method = st.selectbox(t('detection_method'), ['zscore', 'iqr', 'rolling'])
        
        with col3:
            if method == 'zscore':
                threshold = st.slider(t('threshold_sigma'), 1, 5, 3)
                window = None
            elif method == 'iqr':
                threshold = 1.5
                window = None
            elif method == 'rolling':
                threshold = st.slider(t('std_multiplier'), 1, 5, 3)
                window = st.slider(t('rolling_window'), 3, len(df)//4, max(3, len(df)//20))
        
        if st.button(t('run_detection')):
            outliers = detect_outliers(df[selected_col], method=method, threshold=threshold, window_size=window)
            st.session_state.outliers_detected[selected_col] = outliers
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(t('num_outliers'), outliers.sum())
            with col2:
                st.metric(t('outlier_rate'), f"{(outliers.sum()/len(df)*100):.2f}%")
            
            # Visualization of outliers
            fig = go.Figure()
            
            # Add original data
            fig.add_trace(go.Scatter(
                x=df[datetime_col] if datetime_col else df.index,
                y=df[selected_col],
                mode='lines',
                name=t('normal_data'),
                line=dict(color='#4ECDC4'),
                hovertemplate='<b>' + t('normal_data') + '</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
            ))
            
            # Add outliers
            if outliers.sum() > 0:
                fig.add_trace(go.Scatter(
                    x=df.loc[outliers, datetime_col] if datetime_col else df.index[outliers],
                    y=df.loc[outliers, selected_col],
                    mode='markers',
                    name=t('outliers'),
                    marker=dict(size=10, color='#FF6B6B', symbol='diamond'),
                    hovertemplate='<b>' + t('outliers') + '</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
                ))
            
            fig.update_layout(
                title=t('detection_title').format(col=selected_col, method=method),
                xaxis_title=t('time_col') if datetime_col else "Index",
                yaxis_title="Value",
                height=450,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Handle outliers
            st.subheader(t('handle_outliers_header'))
            action = st.radio("Choose action", [t('delete_rows_action'), t('mark_and_interp')])
            
            if action == t('delete_rows_action'):
                df_cleaned = df[~outliers]
                records_removed = len(df) - len(df_cleaned)
                st.success(f"✅ Deleted {records_removed} outlier records")
            else:
                df_cleaned = df.copy()
                df_cleaned.loc[outliers, selected_col] = np.nan
                df_cleaned[selected_col] = interpolate_series(df_cleaned[selected_col], method='linear')
                st.success(t('cleaning_complete'))
            
            if st.button(t('save_clean')):
                st.session_state.df = df_cleaned
                st.success(t('cleaning_complete'))

# ==================== Page: Advanced Analysis ====================
elif page_key == PAGE_KEYS['advanced_analysis']:
    if st.session_state.df is None:
        st.warning(t('warning_upload_first'))
    else:
        st.header(t('advanced_analysis'))
        
        df = st.session_state.df
        datetime_col = st.session_state.datetime_col
        
        analysis_type = st.selectbox(
            t('choose_analysis'),
            [t('stl_decomposition'), t('correlation_heatmap'), t('multi_column')]
        )
        
        # STL Decomposition
        if analysis_type == t('stl_decomposition'):
            st.subheader(t('stl_header'))
            
            col1, col2 = st.columns(2)
            with col1:
                selected_col = st.selectbox(t('choose_stl_col_label'), st.session_state.numeric_cols)
            with col2:
                period = st.number_input(t('seasonal_period_label'), min_value=2, max_value=len(df)//2, value=12)
            
            if st.button(t('stl_decomp_button')):
                result = seasonal_decompose_stl(df[selected_col], period=int(period))
                
                if result is not None:
                    # Create subplots
                    fig = go.Figure()
                    
                    # Original data
                    fig.add_trace(go.Scatter(
                        y=df[selected_col],
                        name=t('orig_data'),
                        mode='lines'
                    ))
                    
                    # Create subplot layout
                    fig = make_subplots(
                        rows=4, cols=1,
                        subplot_titles=(t('orig_data'), 'Trend', 'Seasonal', 'Residual'),
                        vertical_spacing=0.1
                    )
                    
                    fig.add_trace(
                        go.Scatter(y=df[selected_col], name=t('orig_data'), mode='lines'),
                        row=1, col=1
                    )
                    fig.add_trace(
                        go.Scatter(y=result.trend, name='Trend', mode='lines', line=dict(color='#FF6B6B')),
                        row=2, col=1
                    )
                    fig.add_trace(
                        go.Scatter(y=result.seasonal, name='Seasonal', mode='lines', line=dict(color='#4ECDC4')),
                        row=3, col=1
                    )
                    fig.add_trace(
                        go.Scatter(y=result.resid, name='Residual', mode='lines', line=dict(color='#95E1D3')),
                        row=4, col=1
                    )
                    
                    fig.update_layout(height=800, title=f"{selected_col} - STL Decomposition", hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(t('stl_error'))
        
        # Correlation Analysis
        elif analysis_type == t('correlation_heatmap'):
            st.subheader(t('corr_analysis_header'))
            
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
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title=t('correlation_heatmap_title'),
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Display correlation matrix
            st.dataframe(corr_matrix, use_container_width=True)
            
            # Find strongest correlation pairs
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
            
            corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False, key=abs)
            st.subheader(t('strong_pairs'))
            st.dataframe(corr_pairs_df.head(10), use_container_width=True)
        
        # Multi-column comparison
        elif analysis_type == t('multi_column'):
            st.subheader(t('multi_compare_header_label'))
            
            selected_cols = st.multiselect(
                "Select columns for comparison",
                st.session_state.numeric_cols,
                default=st.session_state.numeric_cols[:2] if len(st.session_state.numeric_cols) > 1 else st.session_state.numeric_cols
            )
            
            normalize = st.checkbox(t('normalize_label'))
            
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
                        hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Value: %{y:.4f}<extra></extra>'
                    ))
                
                title = t('comparison_title') if not normalize else t('comparison_normalized')
                fig.update_layout(
                    title=title,
                    xaxis_title=t('time_col') if datetime_col else "Index",
                    yaxis_title="Value",
                    height=450,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)

# ==================== Footer ====================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #888; padding: 20px 0;'>
    <p style='margin: 5px 0; font-size: 0.9em;'>⏰ <strong>Time Series Analysis Workstation</strong> v1.0</p>
    <p style='margin: 5px 0; font-size: 0.85em;'>Built with ❤️ using Streamlit & Plotly | Data Science Toolkit</p>
    <p style='margin-top: 15px; font-size: 0.8em; color: #999;'>Advanced analytics for temporal data exploration and forecasting</p>
</div>
""", unsafe_allow_html=True)
