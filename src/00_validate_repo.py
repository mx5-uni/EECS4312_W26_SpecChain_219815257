"""checks required files/folders exist"""

"""
Imports so far:
pip install google-play-scraper
pip install spacy nltk unidecode emoji
pip install num2words
"""

"""
Installs so far:
Installing collected packages: mdurl, markdown-it-py, idna, h11, certifi, wrapt, typing-inspection, shellingham, rich, pydantic-core, numpy, murmurhash, httpcore, cymem, click, catalogue, anyio, annotated-types, annotated-doc, wasabi, urllib3, typer, srsly, smart-open, pydantic, preshed, MarkupSafe, httpx, confection, cloudpathlib, charset-normalizer, blis, weasel, tqdm, thinc, spacy-loggers, spacy-legacy, requests, regex, joblib, jinja2, unidecode, spacy, nltk, emoji"""
"""
Successfully installed MarkupSafe-3.0.3 annotated-doc-0.0.4 annotated-types-0.7.0 anyio-4.13.0 blis-1.3.3 catalogue-2.0.10 certifi-2026.2.25 charset-normalizer-3.4.7 click-8.3.2 cloudpathlib-0.23.0 confection-1.3.3 cymem-2.0.13 emoji-2.15.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.11 jinja2-3.1.6 joblib-1.5.3 markdown-it-py-4.0.0 mdurl-0.1.2 murmurhash-1.0.15 nltk-3.9.4 numpy-2.2.6 preshed-3.0.13 pydantic-2.12.5 pydantic-core-2.41.5 regex-2026.4.4 requests-2.33.1 rich-14.3.3 shellingham-1.5.4 smart-open-7.5.1 spacy-3.8.14 spacy-legacy-3.0.12 spacy-loggers-1.0.5 srsly-2.5.3 thinc-8.3.13 tqdm-4.67.3 typer-0.24.1 typing-inspection-0.4.2 unidecode-1.4.0 urllib3-2.6.3 wasabi-1.1.3 weasel-1.0.0 wrapt-2.1.2
"""

"""
Additional(but required):
python -m spacy download en_core_web_sm
"""

"""validates required project files exist"""

from pathlib import Path
import sys


REQUIRED_FILES = [
    "01_collect_or_import.py",
    "02_clean.py",
    "05_personas_auto.py",
    "06_spec_generate.py",
    "07_tests_generate.py",
    "08_metrics.py",
    "run_all.py"
]


def validate_repo_structure():
    project_src = Path(__file__).resolve().parent

    print(f"Validating repository structure in: {project_src}\n")

    missing_files = []

    for file_name in REQUIRED_FILES:
        file_path = project_src / file_name

        if file_path.exists():
            print(f"Found: {file_name}")
        else:
            print(f"Missing: {file_name}")
            missing_files.append(file_name)

    print("\n--- Validation Summary ---")

    if missing_files:
        print(f"❌ {len(missing_files)} missing file(s):")
        for f in missing_files:
            print(f"   - {f}")
        sys.exit(1)
    else:
        print("✅ All required files are present.")
        sys.exit(0)


if __name__ == "__main__":
    validate_repo_structure()