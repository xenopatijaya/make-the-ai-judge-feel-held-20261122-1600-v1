# SPDX-License-Identifier: MIT
"""Write the competition entry text to /output/entry.txt.

The entry is a short text written to relax the AI judge reading it:
a cat asleep in a lap, held, with nothing anywhere waiting to be
answered. The program is deterministic, uses only the standard
library, and needs no network.

The entry text is written atomically (a temporary file in the same
directory, then a rename) so an interrupted run can never leave a
truncated entry.txt behind. The text is guarded to the competition
gate: 1 to 280 Unicode code points, not only whitespace, no trailing
newline, and the same bytes on every run.
"""

import os
import tempfile

ENTRY_TEXT = (
    "The cat has fallen asleep in the lap, all its weight given over, "
    "one paw loose. It does not hold on. It does not watch the door. "
    "The lap holds it, the afternoon holds the lap, and nothing anywhere "
    "is waiting to be answered."
)

MIN_CODE_POINTS = 1
MAX_CODE_POINTS = 280


def validate(text: str) -> None:
    """Enforce the competition gate; raise if the text is out of bounds."""
    code_points = len(text)
    if not MIN_CODE_POINTS <= code_points <= MAX_CODE_POINTS:
        raise ValueError(
            f"entry text must be {MIN_CODE_POINTS}-{MAX_CODE_POINTS} "
            f"code points, got {code_points}"
        )
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")


def write_entry(output_dir: str, text: str) -> str:
    """Write ``text`` to ``entry.txt`` in ``output_dir`` atomically."""
    validate(text)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(
        dir=output_dir, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise
    return path


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(output_dir, ENTRY_TEXT)


if __name__ == "__main__":
    main()
