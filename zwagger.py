import os
from tag import ZTag
from html import Html


tags = {
    "default": ZTag("", html_tag="span"),
    "p": ZTag("p", html_tag="p", css_class="p", description="Normal text"),
    "b": ZTag("b", css_class="b", description="Bold text"),
    "i": ZTag("i", css_class="i", description="Italic text"),
    "c": ZTag("c", css_class="c", description="Centered text"),
    "q1": ZTag("q1", css_class="q1", description="Quote with quotes"),
    "q2": ZTag("q2", css_class="q2", description="Quote without quotes"),
    "u": ZTag("u", css_class="u", description="Underlined text"),
    "z": ZTag("z", css_class="z", description="Line through text"),
    "h1": ZTag("h1", html_tag="h1", description="Heading 1"),
    "h2": ZTag("h2", html_tag="h2", description="Heading 2"),
    "h3": ZTag("h3", html_tag="h3", description="Heading 3"),
    "resume": ZTag("resume", html_tag="p", css_class="resume", description="blog resume")
}


class ZwaggerConvert:
    def __init__(self, zwg_file: str, out: str = None):
        self.zwg_name = zwg_file
        self.out_name = zwg_file + ".html" if out is None else out

    def convert(self):
        self._generate_html()

    def _generate_html(self):
        self.zwg_file = open(self.zwg_name, 'r')
        self.out_file = open(self.out_name, 'w')
        self.html_tag_queue = []
        for line in self.zwg_file:
            self._interpret(line)
        self.out_file.close()
        self.zwg_file.close()

    def _interpret(self, line):
        skip_tag = False
        for i, char in enumerate(line):
            if char == '\n' and len(self.html_tag_queue) == 0:
                continue
            if skip_tag:
                if char == '>' and line[i-1] != '\\':
                    skip_tag = False
                continue
            if char != '<' or (char == '<' and line[i-1] == '\\'):
                n = len(self.html_tag_queue)
                if n == 0: self.out_file.write(self._generate_html_tag("p"))
                if char == '\n' and self.html_tag_queue[n-1].get_name() == "p" and line[i-1] == '\n':
                    self.out_file.write(self._generate_html_tag("/"))
                self.out_file.write(char)
            else:
                tag = ZwaggerConvert._read_tag(line[i+1:])
                self.out_file.write(self._generate_html_tag(tag))
                skip_tag = True

    def _generate_html_tag(self, tag):
        if tag == '/':
            html_tag = self.html_tag_queue.pop()
            return html_tag.get_closing_tag()
        ztag, modifiers = ZwaggerConvert._get_ztag_modifiers(tag)
        html_tag = Html(ztag.get_html_tag())
        css_class = ztag.get_css_class()
        if css_class is not None:
            html_tag.add_class(css_class)
        self.html_tag_queue.append(html_tag)
        for m in modifiers:
            html_tag.add_class(m.get_css_class())
        html_tag.add_class("zwg")
        return html_tag.get_html()

    @classmethod
    def _read_tag(cls, line):
        tag = ""
        for c in line:
            if c == '>': break
            tag += c
        tag = tag.replace(" ", "").replace("\t", "")
        if '\n' in tag: raise Exception("invalid tag")
        if tag[0] == '/': return '/'
        return tag

    @classmethod
    def _get_ztag_modifiers(cls, tag):
        elements = tag.split(',')
        ztag = None
        modifiers = []
        for e in elements:
            t = tags.get(e, None)
            if t is not None:
                if t.is_html_tag and ztag is None:
                    ztag = t
                elif not t.is_html_tag: modifiers.append(t)
            else:
                ms = filter(lambda x: x in tags, e.split())
                ms = map(lambda x: tags.get(x), ms)
                modifiers += list(ms)
        if ztag is None: ztag = tags.get("default")
        return ztag, modifiers





class Zwagger:
    zwg_container_open_tag = '<div class="container zwg">'

    def __init__(self, zwg_in_name: str, html_in_name: str, out_name: str = None, generate_styles=True, conf_file=None):
        self._converter = ZwaggerConvert(zwg_in_name, "temp.html")
        self.html_in_name = html_in_name
        self.out_name = html_in_name if out_name is None else out_name
        if generate_styles: self.conf_file = "zwagger.yml" if conf_file is None else conf_file

    def do_magic(self):
        self._copy_content()


    def _copy_content(self):
        self.html_in = open(self.html_in_name, 'r')
        self.out_file = open(self.out_name, 'w')
        zwagger_mark = "{{}}"
        found = False
        for line in self.html_in.readlines():
            index = line.find(zwagger_mark)
            if index == -1: self.out_file.write(line)
            else:
                found = True
                self.out_file.write(line[:index])
                self.out_file.write(Zwagger.zwg_container_open_tag)
                self._converter.convert()
                self._copy_zwg_html()
                self.out_file.write("</div>")
                self.out_file.write(line[index + 4:])
        if not found: os.remove(self.out_name)

    def _copy_zwg_html(self):
        self.out_file.write(open("temp.html", 'r').read())


if __name__ == "__main__":
    zwg = Zwagger("./test/test.zwg", "./test/zwagger_test.html", "./test/out.html")
    zwg.do_magic()

