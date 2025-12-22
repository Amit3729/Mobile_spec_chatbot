from pathlib import Path

PROJECT_NAME = "my-product-rag-app"

# Folder + file structure definition
STRUCTURE = {
    "app": {
        "__init__.py": None,
        "main.py": None,
        "api": {
            "__init__.py": None,
            "routes.py": None,
        },
        "core": {
            "__init__.py": None,
            "config.py": None,
            "security.py": None,
        },
        "services": {
            "__init__.py": None,
            "rag_service.py": None,
            "cache_service.py": None,
            "mongo_service.py": None,
        },
        "utils": {
            "__init__.py": None,
            "helpers.py": None,
        },
    },
    "scripts": {
        "ingest_data.py": None,
        "rebuild_index.py": None,
    },
    "data": {
        "raw": {
            "data.csv": None,
        }
    },
    "tests": {
        "test_rag.py": None,
    },
    ".gitignore": None,
    "Dockerfile": None,
    "requirements.txt": None,
    "render.yaml": None,
    "README.md": None,
}


def create_structure(base_path: Path, structure: dict):
    for name, content in structure.items():
        path = base_path / name

        # File
        if content is None:
            if not path.exists():
                path.touch()
                print(f"📄 Created file: {path}")
            else:
                print(f"⏭️  File already exists: {path}")

        # Directory
        else:
            if not path.exists():
                path.mkdir(parents=True)
                print(f"📁 Created directory: {path}")
            else:
                print(f"⏭️  Directory already exists: {path}")

            create_structure(path, content)


def main():
    root = Path(PROJECT_NAME)

    if not root.exists():
        root.mkdir()
        print(f"🚀 Created project root: {root}")
    else:
        print(f"⚠️  Project root already exists: {root}")

    create_structure(root, STRUCTURE)
    print("\n✅ Project structure setup completed!")


if __name__ == "__main__":
    main()
