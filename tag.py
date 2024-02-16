from __future__ import annotations


class Tag:
    def __init__(self, symbol: str, html: str, description: str = None):
        self.symbol = symbol
        self.html = html
        self.description = description
        self.opening = f"<{self.symbol}>"
        self.closing = f"</{self.symbol}>"

    def get_opening(self):
        return self.opening

    def get_closing(self):
        return self.closing

    def get_html(self, content: str):
        return self.html.format(content)


class SimpleHtmlTag(Tag):
    def __init__(self, symbol: str, html_tag, css_class="", description: str = None):
        self.css_class = css_class
        self.html_tag = html_tag
        self.html_opening = f"<{html_tag} class=\"{css_class}\">"
        self.html_closing = f"</{html_tag}>"
        html = self.html_opening + "{}" + self.html_closing
        super().__init__(symbol, html, description)


    def get_html_opening(self):
        return self.html_opening

    def get_html_closing(self):
        print(self.html_closing)
        return self.html_closing
