from tag import SimpleHtmlTag

tags = {
    "p": SimpleHtmlTag("p", "p", "p", "Normal text"),
    "b": SimpleHtmlTag("b", "span", "b", "Bold text"),
    "i": SimpleHtmlTag("i", "span", "i", "Italic text"),
    "c": SimpleHtmlTag("c", "span", "c", "Centered text"),
    "q1": SimpleHtmlTag("q1", "span", "q1", "Quote with quotes"),
    "q2": SimpleHtmlTag("q2", "span", "q2", "Quote without quotes"),
    "u": SimpleHtmlTag("u", "span", "u", "Underlined text"),
    "z": SimpleHtmlTag("z", "span", "z", "Line through text"),
    "h1": SimpleHtmlTag("h1", "h1", description="Heading 1"),
    "h2": SimpleHtmlTag("h2", "h2", description="Heading 2"),
    "h3": SimpleHtmlTag("h3", "h3", description="Heading 3")
}


def generate_html_tag(current_tag):
    sub_tags = []
    for sub_tag in current_tag.split(','):
        if sub_tag in tags:
            sub_tags.append(sub_tag)
        else:
            sub_tags += sub_tag.split()
    return  f"<span class=\"{' '.join([tags.get(tag, tags.get('p')).css_class for tag in sub_tags])}\""


class Zwagger:
    def __init__(self, input_file: str, output_file: str, generate_styles=True, conf_file=None):
        self.in_file_name = input_file
        self.out_file_name = output_file
        self.in_file = None
        self.out_file = None
        self.conf_file = None
        self.swp_file = None
        self.temp_html = None
        if generate_styles:
            self.conf_file = "zwagger.yml" if conf_file is None else conf_file

    def do_magic(self):
        self.in_file = open(self.in_file_name, 'r')
        self.temp_html = open("temp.html", 'w')
        self.generate_html()

        self.out_file = open(self.out_file_name, 'r')
        self.swp_file = open(f"{self.out_file_name}.swp", 'w')
        self._copy_content()

    def _copy_content(self):
        zwagger_mark = "{{}}"
        for line in self.out_file.lines():
            index = line.find(zwagger_mark)
            if index == -1:
                self.swp_file.write(line)
                continue
            self.swp_file.write(line[:index])
            self.swp_file.write()
            self.swp_file.write(line[index + 4:])

    def generate_html(self):
        for line in self.in_file:
            self._interpret(line)

    def _interpret(self, line):
        reading_tag = False
        current_tag = ""
        for i, char in enumerate(line):
            if not reading_tag and char != '<':
                self.temp_html.write(char)
            elif not reading_tag:
                reading_tag = True
                current_tag = ""
            elif char != '>':
                current_tag += char
            else:
                self.temp_html.write(generate_html_tag(current_tag))
                current_tag = ""
                reading_tag = False

if __name__ == "__main__":
    pass