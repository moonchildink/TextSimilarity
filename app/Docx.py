import docx


class Docx:
    def __init__(self, file_path):
        try:
            self.graphs = []
            self.file = docx.Document(file_path)
            for graph in self.file.paragraphs:
                self.graphs.append(graph.text)
            for table in self.file.tables:
                for row in table.rows:
                    for cell in row.cells:
                        self.graphs.append(cell.text)
        except FileNotFoundError:
            pass

    @property
    def text(self):
        """
        :return:all texts in document,in the format of list
        """
        return self.graphs
