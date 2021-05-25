from pathlib import Path
from typing import Union


class Storage:
    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, Path):
            self.path = path
        else:
            self.path = Path(path)

        self.mkdir()

    # def create(self):
    #     self.path.mak

    def mkdir(self):
        self.path.mkdir(parents=True, exist_ok=True)

    def rmdir(self):
        import shutil

        shutil.rmtree(self.path)

    def foler(self, path):
        return Storage(self.path / path)

    def write(self, file: str, content, mode="w") -> Path:
        path = self.path / file
        with open(str(path), mode="w") as f:
            f.write(content)
        return path

    def load(self, file: str) -> str:
        path = self.path / file
        with open(str(path)) as f:
            content = f.read()
        return content

    def load_or_blank(self, file: str) -> str:
        try:
            content = self.load(file)
        except FileNotFoundError:
            content = ""
        except:
            raise

        return content

    def __iter__(self):
        for x in (x for x in self.path.glob("**/*") if x.is_file()):
            with open(str(x)) as f:
                content = f.read()
            yield content


datalake = Storage("datalake")
datalake.mkdir()
