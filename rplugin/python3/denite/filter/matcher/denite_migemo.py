# ============================================================================
# FILE: matcher/denite_migemo.py
# AUTHOR: nekowasabi
#         Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import re
import subprocess

from denite.base.filter import Base


class Filter(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "matcher/migemo"
        self.description = "migemo matcher"

        self.vars = {
            "command": ["cmigemo"],
            "dict_path": "/usr/share/migemo/utf-8/migemo-dict",
        }

    def filter(self, context):
        if context["input"] == "":
            return context["candidates"]
        candidates = context["candidates"]

        try:
            pattern = subprocess.check_output(
                self.vars["command"] + ["-w", context["input"],
                                        "-d", self.vars["dict_path"]],
            ).decode("utf-8").splitlines()[0]
            # Note: "+" must be escaped
            p = re.compile(pattern.replace("+", r"\+"))

        except Exception as ex:
            self.debug(ex)
            candidates = [x for x in candidates if context["input"] in x["word"]]
            return candidates

        candidates = [x for x in candidates if p.search(x["word"]) or context["input"] in x["word"]]

        return candidates
