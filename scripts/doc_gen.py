from pathlib import Path

docs_path = Path(__file__).parent.parent / "docs"


def create_index_doc():
    # this function copies README.md to docs/index.md
    index_doc_path = docs_path / "index.md"
    readme_path = Path(__file__).parent.parent / "README.md"

    with open(index_doc_path, "w") as f:
        with open(readme_path, "r") as readme:
            # update relative path for asserts
            content = readme.read().replace("docs/assets/", "assets/")
            f.write(content)
