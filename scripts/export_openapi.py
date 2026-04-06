"""Export the FastAPI OpenAPI schema to openapi.json."""

import json
import os
import sys

# Allow running from the repo root without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app  # noqa: E402

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "..", "openapi.json")
    schema = app.openapi()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    print(f"OpenAPI schema written to {os.path.abspath(output_path)}")
