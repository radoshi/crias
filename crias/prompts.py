import string
from collections import UserDict
from pathlib import Path

import tomli
from pydantic import BaseModel


class Template(BaseModel):
    content: str
    # def message(self, role: str, **kwargs) -> dict[str, str]:
    #     """Return a dictionary that is ready to fed into OpenAI ChatCompletion."""
    #     content = self.content.format(**kwargs)
    #     return {"content": content, "role": role}

    # def user_message(self, **kwargs) -> dict[str, str]:
    #     """Return a dictionary that is ready to fed into OpenAI ChatCompletion."""
    #     return self.message(role="user", **kwargs)

    # def system_message(self, **kwargs) -> dict[str, str]:
    #     """Return a dictionary that is ready to fed into OpenAI ChatCompletion."""
    #     return self.message(role="system", **kwargs)

    # def save(self, filename: Union[str, Path] = "") -> None:
    #     """Save the template to a file."""
    #     if not filename and not self.name:
    #         raise ValueError("Name must be provided to save the template.")
    #     filename = Path(filename or f"{self.name}.json")
    #     with open(filename, "w") as f:
    #         f.write(self.json())

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
            library.add(name, Template.model_validate_json(bytes))
        for filename in dir.glob("**/*.toml"):
            name = filename.parent / filename.stem
            library.add(name, Template.parse_toml(filename))
        return library
