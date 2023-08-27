import string
from collections import UserDict
from pathlib import Path

import tomli
from pydantic import BaseModel


class Template(BaseModel):
    content: str

    def inputs(self) -> list[str]:
        """Return a list of field names in the contents."""
        formatter = string.Formatter()
        field_names = []
        for _, field_name, _, _ in formatter.parse(self.content):
            if field_name is not None:
                field_names.append(field_name)
        return sorted(list(set(field_names)))

    @classmethod
    def parse_toml(cls, filename: Path | str) -> "Template":
        """Parse a TOML file and return a Template object."""
        with open(filename, "rb") as f:
            toml_dict = tomli.load(f)
            return cls.model_validate(toml_dict)


class TemplateLibrary(UserDict):
    def add(self, name: str, template: Template) -> None:
        """Add a template to the library."""
        if not name:
            raise ValueError("Template must have a name.")
        self.data[name] = template

    @classmethod
    def from_directory(cls, dir: str | Path) -> "TemplateLibrary":
        """Load templates from a file or directory."""
        dir = Path(dir)
        if not dir.exists():
            raise FileNotFoundError(f"{dir} does not exist.")
        if not dir.is_dir():
            raise ValueError(f"{dir} is not a directory.")

        library = cls()
        for filename in dir.glob("**/*.json"):
            name = filename.parent / filename.stem
            bytes = filename.read_bytes()
            library.add(str(name), Template.model_validate_json(bytes))
        for filename in dir.glob("**/*.toml"):
            name = filename.parent / filename.stem
            library.add(str(name), Template.parse_toml(filename))
        return library
