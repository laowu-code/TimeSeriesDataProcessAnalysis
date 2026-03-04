#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time Series Analysis Workstation - Streamlit Launch Script
"""

import subprocess
import sys
import os

def main():
    """Launch Streamlit Application"""
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    
    print()
    print("=" * 50)
    print("  📊 Time Series Analysis Workstation - Quick Start")
    print("=" * 50)
    print()
    print("🚀 Starting application...")
    print()
    print("📌 After startup, please open in your browser:")
    print("   http://localhost:8501")
    print()
    print("💡 Tip: Press Ctrl+C to stop the application")
    print()
    print("=" * 50)
    print()
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path], check=True)
    except KeyboardInterrupt:
        print("\n\n✓ Application stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Launch failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
