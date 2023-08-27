from pathlib import Path

import pytest

from crias.prompts import Template, TemplateLibrary


def write_toml_file(path):
    with open(path / "toml_greeting.toml", "w") as f:
        f.write(
            """
            content = "Hello, World!"
            """
        )
    return Template(content="Hello, World!")


# Unit test for extract_format_inputs
def test_inputs():
    # Test case 1: Format string with two field names
    template = Template(content="{hello} {world}")
    inputs1 = template.inputs()
    assert inputs1 == ["hello", "world"]

    # Test case 2: Format string with no field names
    template = Template(content="Hello, World!")
    inputs2 = template.inputs()
    assert inputs2 == []

    # Test case 4: Format string with repeated field names
    template = Template(content="{greeting}, {name}. My name is also {name}.")
    inputs3 = template.inputs()
    assert inputs3 == ["greeting", "name"]


# Test function for the `parse_toml` method
def test_parse_toml(tmp_path):
    parsed_template = write_toml_file(tmp_path)
    assert parsed_template == Template(content="Hello, World!")


def test_getitem_setitem():
    library = TemplateLibrary()
    template = Template(content="Hello, World!")
    library["greeting"] = template  # Calls __setitem__
    assert library["greeting"] == template  # Calls __getitem__


def test_del_item():
    library = TemplateLibrary()
    template = Template(content="Hello, World!")
    library["greeting"] = template
    del library["greeting"]  # Calls __del_item__
    with pytest.raises(KeyError):
        _ = library["greeting"]


def test_add():
    library = TemplateLibrary()
    template = Template(content="Hello, World!")
    library.add("greeting", template)
    assert library["greeting"] == template


def test_from_file(tmp_path):
    template = Template(content="Hello, World!")
    filename = tmp_path / "greeting.json"
    filename.write_text(template.model_dump_json())
    library = TemplateLibrary.from_directory(tmp_path)
    name = str(tmp_path / "greeting")
    assert library[name] == template


def test_from_toml_file(tmp_path):
    template = write_toml_file(tmp_path)
    library = TemplateLibrary.from_directory(tmp_path)
    name = str(tmp_path / "toml_greeting")
    assert library[name] == template


def test_from_nonexistent_directory():
    with pytest.raises(FileNotFoundError):
        _ = TemplateLibrary.from_directory("nonexistent_dir")


def test_from_file_instead_of_dir(tmp_path):
    name: Path = tmp_path / "test"
    name.write_text("Hello, World!")
    with pytest.raises(ValueError):
        _ = TemplateLibrary.from_directory(name)


def test_add_must_have_a_name():
    library = TemplateLibrary()
    template = Template(content="Hello, World!")
    with pytest.raises(ValueError):
        library.add("", template)
