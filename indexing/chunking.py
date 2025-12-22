from chonkie import RecursiveChunker

class TextChunker:
    def __init__(self, filePath):
        self.filePath = filePath
        self.chunker = RecursiveChunker()

    def _get_text(self):
        text = ""
        with open(self.filePath, "r", encoding='utf-8') as f:
            text = f.read()
        return text

    def do_chunk(self):
        text = self._get_text()
        chunks = []
        try:
            chunks = self.chunker(text)
            return True, chunks
        except Exception as e:
            print(f"There is an error while do Chunking : {str(e)}")
            return False, chunks
