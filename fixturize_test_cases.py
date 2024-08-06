import os
import re

TEST_CASE_RE = re.compile(r'("""|#|)\s*C(\d+)')

for root, _, files in os.walk("tests"):
    for file in files:
        if file.startswith("test") and file.endswith(".py"):
            case_num = None
            filepath = os.path.join(root, file)
            for line in open(filepath).readlines():
                m = TEST_CASE_RE.match(line.strip())
                if not m:
                    continue
                if case_num and case_num != m[2]:
                    print(filepath)
                    print(f"Found multiple case_nums: {case_num} and {m[2]}")
                case_num = m[2]
            if case_num:
                with open(filepath, "a") as fh:
                    lines = "\n".join(
                        [
                            "import pytest",
                            "@pytest.fixture()",
                            "def test_case():",
                            f'    return "{case_num}"',
                        ]
                    )
                    # fh.write(lines)
                    # print(filepath)
                    # print(lines)
                    # print("-=----=-")
            else:
                print(f"Case not found for {filepath}")
