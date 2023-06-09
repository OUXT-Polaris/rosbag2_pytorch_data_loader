import glob
import subprocess


def find_test_binary(test: str) -> list[str]:
    for path in glob.glob("./**/" + test, recursive=True):
        print("Test found at" + path)
    return glob.glob("./**/" + test, recursive=True)


def run_tests(test_cases: list[str]) -> None:
    for test_case in test_cases:
        executables = find_test_binary(test_case)
        for executable in executables:
            result = subprocess.run("./" + executable, check=True)


if __name__ == "__main__":
    run_tests(
        # Please check all the test case in CMakeLists.txt was defined.
        ["cache_unittest", "simple_tf2_core", "static_cache_test", "test_time"]
    )
