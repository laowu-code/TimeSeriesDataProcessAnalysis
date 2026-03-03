#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
时序数据分析工作站 - Streamlit 启动脚本
"""

import subprocess
import sys
import os

def main():
    """启动 Streamlit 应用"""
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    
    print()
    print("=" * 50)
    print("  📊 时序数据分析工作站 - 快速启动")
    print("=" * 50)
    print()
    print("🚀 正在启动应用...")
    print()
    print("📌 应用启动后，请在浏览器打开：")
    print("   http://localhost:8501")
    print()
    print("💡 提示：按 Ctrl+C 可停止应用")
    print()
    print("=" * 50)
    print()
    
    # 启动 Streamlit
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path], check=True)
    except KeyboardInterrupt:
        print("\n\n✓ 应用已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动失败：{str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
