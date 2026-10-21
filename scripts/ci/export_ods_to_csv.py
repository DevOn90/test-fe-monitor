# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "pandas",
#     "odfpy",
# ]
# ///
from pathlib import Path
import re
import pandas as pd  # type: ignore

"""
Sanitize sheet names to be safe for filenames. 
This replaces any character that is not a letter, number, dot, underscore, or hyphen with a hyphen. 
Leading and trailing hyphens are stripped. 
If the resulting name is empty, it defaults to "sheet".
"""
def sanitize_sheet_name(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-")
    return safe or "sheet"
"""
Exclude certain paths from processing.
This is useful for ignoring template files or 
other non-relevant ODS files in the documentation directories
"""
EXCLUDED_PATHS = {
    Path("docs/02_product/discovery/templates"),
    Path("docs/02_product/architecture/templates"),
}

"""
Check if a given path is excluded 
based on the EXCLUDED_PATHS set.
"""
def is_excluded(path: Path) -> bool:
    return any(excluded in path.parents for excluded in EXCLUDED_PATHS)

# Find all ODS files in the current directory and its subdirectories
ods_files = sorted(Path(".").rglob("*.ods"))

# Iterate over each ODS file found and process it
for ods in ods_files:
    
    # Skip processing if the ODS file is in an excluded path.
    if is_excluded(ods):
        continue

    base = ods.with_suffix("")
    export_dir = base.parent / "exportsCSV"
    export_dir.mkdir(exist_ok=True)

    # Remove old exports for this ODS file so renamed/removed sheets do not leave stale CSVs.
    for stale in export_dir.glob(f"{base.name}_*.csv"):
        stale.unlink()

    # Remove legacy exports from the old layout.
    legacy_base = base.with_suffix(".csv")
    if legacy_base.exists():
        legacy_base.unlink()
    for stale in base.parent.glob(f"{base.name}__*.csv"):
        stale.unlink()

    sheets = pd.read_excel(ods, engine="odf", sheet_name=None)
    if not sheets:
        continue

    for sheet_name, df in sheets.items():
        safe_sheet = sanitize_sheet_name(sheet_name)
        out = export_dir / f"{base.name}_{safe_sheet}.csv"
        df.to_csv(out, index=False)
        print(f"Converted {ods} [{sheet_name}] -> {out}")
