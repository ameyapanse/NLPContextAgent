import re

class MarkdownTextSplitter:
    def __init__(self):
        self.sections = []

    def split(self, text):
        lines = text.split("\n")
        self._process_lines(lines)

    def get_sections(self):
        return self.sections

    def _process_lines(self, lines):
        section = {"content": [], "metadata": {}}

        for line in lines:
            if line.startswith("#"):
                self._save_section(section)
                section = {"content": [], "metadata": {"heading": self._extract_heading(line)}}
            else:
                section["content"].append(line)

        self._save_section(section)

    def _save_section(self, section):
        if section["metadata"] and section["content"]:
            self.sections.append(section)

    def _extract_heading(self, line):
        heading_match = re.search(r"^#+\s+(.*)$", line)
        if heading_match:
            return heading_match.group(1)
        return ""

