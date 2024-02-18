

class Html:
    def __init__(self, tag_name, classes=None):
        self.tag_name = tag_name
        self.classes = [] if classes is None else classes

    def add_class(self, c):
        self.classes.append(c)

    def remove_class(self, c):
        self.classes.remove(c)

    def get_html(self):
        if len(self.classes) == 0:
            return f"<{self.tag_name}>"
        return f"<{self.tag_name} class=\"{' '.join(self.classes)}\">"

    def get_closing(self):
        return f"</{self.tag_name}>"