import argparse
import os


def ensure_test_structure(module_dir, test_dir):
    for root, dirs, files in os.walk(module_dir):
        # Determine the current path relative to the module directory
        rel_path = os.path.relpath(root, module_dir)

        # Create the corresponding path in the test directory
        test_path = os.path.join(test_dir, rel_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(test_path):
            os.makedirs(test_path)
            print(f"Created directory: {test_path}")

        # For each Python file in the module directory, ensure a corresponding test file exists
        for file in files:
            if file.endswith(".py"):
                if file == "__init__.py":
                    test_file_name = file
                else:
                    test_file_name = f"test_{file}"

                test_file_path = os.path.join(test_path, test_file_name)

                if not os.path.exists(test_file_path):
                    # Create the test file
                    with open(test_file_path, "w") as f:
                        if file != "__init__.py":
                            # Write basic test file content, could be expanded with a template
                            f.write("import pytest")
                    print(f"Created test file: {test_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Ensure test structure mirrors the module structure."
    )
    parser.add_argument("-i", "--module_dir", help="Path to the module directory")
    parser.add_argument("-t", "--test_dir", help="Path to the tests directory")

    args = parser.parse_args()

    ensure_test_structure(args.module_dir, args.test_dir)


if __name__ == "__main__":
    main()
