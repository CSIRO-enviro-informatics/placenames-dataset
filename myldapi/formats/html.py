from format import 

class HTML(Format):
    def __init__(
            self,
            template
    ):
        self.label = "HTML Formatter"
        self.comment = "Converts the graph in html"
        self.mediaType = "text/html"
        self.template = template

    def render(request, graph):
        pass