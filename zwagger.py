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

class StyleGenerator:
    def __init__(self):
        pass

class Zwagger:
    def __init__(self, input_file: str, output_file: str = None, generate_styles=True, styles_file=None, conf_file=None):
        self.in_file = input_file
        self.out_file = output_file
        self.styles_dir = None
        self.conf_file = None
        if generate_styles:
            self.conf_file = "zwagger.yml" if conf_file is None else conf_file
            self.styles_dir = "/".join(output_file.split("/")[:-1]) + "/zwagger.css" if styles_file is None else styles_file

    def do_magic(self):
            raise NotImplementedError("TODO")

