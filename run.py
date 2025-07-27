#!/usr/bin/env python3
"""
MediClin Platform - Startup Script
"""

import subprocess
import sys
import os

def main():
    """Launch MediClin Platform"""
    
    print("🧠 Starting MediClin Platform...")
    print("=" * 50)
    
    # Check if required file exists
    if not os.path.exists("mediclin.py"):
        print("❌ Error: mediclin.py not found")
        sys.exit(1)
    
    try:
        # Start Streamlit application
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "mediclin.py", 
            "--server.port", "8501",
            "--server.headless", "true"
        ]
        
        print("🚀 Launching MediClin...")
        print("📍 Platform will be available at: http://localhost:8501")
        print("🔄 Starting application...")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n⏹️  MediClin Platform stopped by user")
    except Exception as e:
        print(f"❌ Error starting platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()