#!/usr/bin/env python3
"""
Medical Intelligence Platform - Startup Script
"""

import subprocess
import sys
import os

def main():
    """Launch Medical Intelligence Platform"""
    
    print("🧠 Starting Medical Intelligence Platform...")
    print("=" * 50)
    
    # Check if required file exists
    if not os.path.exists("medical_intelligence.py"):
        print("❌ Error: medical_intelligence.py not found")
        sys.exit(1)
    
    try:
        # Start Streamlit application
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "medical_intelligence.py", 
            "--server.port", "8501",
            "--server.headless", "true"
        ]
        
        print("🚀 Launching Medical Intelligence...")
        print("📍 Platform will be available at: http://localhost:8501")
        print("🔄 Starting application...")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n⏹️  Medical Intelligence Platform stopped by user")
    except Exception as e:
        print(f"❌ Error starting platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()