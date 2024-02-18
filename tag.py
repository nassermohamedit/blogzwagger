from __future__ import annotations



class ZTag:
    def __init__(self, symbol: str, html_tag=None, css_class=None, description = ""):
       self.symbol = symbol
       self.is_html_tag = html_tag is not None
       self.html_tag = html_tag if html_tag is not None else "span"
       self.css_class = css_class
       self.description = description


    def get_html(self):
        return f"<{self.html_tag} class=\"{self.css_class}\">"

    def get_html_tag(self):
        return self.html_tag

    def get_css_class(self):
        return  self.css_class

    def get_closing_tag(self):
        return f"</{self.html_tag[1:]}"