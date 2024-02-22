import os
from tag import ZTag
from html import Html


tags = {
    "p": ZTag("p", css_class="p", description="Normal text"),
    "b": ZTag("b", css_class="b", description="Bold text"),
    "i": ZTag("i", css_class="i", description="Italic text"),
    "c": ZTag("c", css_class="c", description="Centered text"),
    "q1": ZTag("q1", css_class="q1", description="Quote with quotes"),
    "q2": ZTag("q2", css_class="q2", description="Quote without quotes"),
    "u": ZTag("u", css_class="u", description="Underlined text"),
    "z": ZTag("z", css_class="z", description="Line through text"),
    "h1": ZTag("h1", html_tag="h1", description="Heading 1"),
    "h2": ZTag("h2", html_tag="h2", description="Heading 2"),
    "h3": ZTag("h3", html_tag="h3", description="Heading 3")
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
            if skip_tag:
                if char == '>' and line[i-1] != '\\':
                    skip_tag = False
                continue
            if char != '<' or char == '<' and line[i-1] == '\\': self.out_file.write(char)
            else:
                tag = ZwaggerConvert._read_tag(line[i+1:])
                self.out_file.write(self._generate_html_tag(tag))
                skip_tag = True

    def _generate_html_tag(self, tag):
        if tag == '/':
            html_tags = self.html_tag_queue.pop()
            return f"{''.join([t.get_closing() for t in html_tags[::-1]])}"
        global tags
        sub_tags = []
        for t in tag.split(','):
            if t in tags:
                sub_tags.append(t)
            else:
                for r in t:
                    if r in tags:
                        sub_tags.append(r)
        for i in range(len(sub_tags)):
            z = tags.get(sub_tags[i])
            if z.is_html_tag:
                sub_tags = (sub_tags[i],) + tuple(sub_tags[:i]) + tuple(sub_tags[i+1:])
                break
        html = tuple()
        for t in sub_tags:
            z = tags.get(t)
            if z.is_html_tag:
                h = Html(z.get_html_tag())
                h.add_class("zwg")
                html += (h,)
            elif len(html) == 0: html += (Html(z.get_html_tag(), [z.get_css_class()]),)
            else: html[len(html) - 1].add_class(z.get_css_class())
        self.html_tag_queue.append(html)
        html_string = ""
        for h in html: html_string += h.get_html()
        return html_string

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

