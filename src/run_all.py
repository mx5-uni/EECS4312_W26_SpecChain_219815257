"""runs the full pipeline end-to-end"""

import subprocess
import sys
from pathlib import Path


def run_script(script_path):
    print(f"\nRunning: {script_path.name}\n" + "-" * 50)

    result = subprocess.run([sys.executable, str(script_path)])

    if result.returncode != 0:
        print(f"\n❌ Script failed: {script_path.name}")
        sys.exit(1)


def main():
    project_root = Path(__file__).resolve().parent  # src folder

    scripts = [
        #project_root / "01_collect_or_import.py",  #comment out for now to not cause a refresh in the reviews
        project_root / "02_clean.py",
        #project_root / "03_manual_coding_template.py",
    ]

    for script in scripts:
        run_script(script)

    print("\n✅ All scripts completed successfully!")


if __name__ == "__main__":
    main()