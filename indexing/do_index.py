from indexing.vlm import pdfConversion
from indexing.chunking import TextChunker
from indexing.upserting import Upserter

class Indexing:
    def __init__(self, filename="", raw_filename=""):
        self.filename = filename
        self.raw_filename = raw_filename
        self.output_folder = "file_extracted/"
        self.output_extension = ".txt"

    def conversion(self):
        converter = pdfConversion(self.filename, self.raw_filename, self.output_folder, self.output_extension)
        resBool = converter.converting()

        if resBool:
            return "Conversion Success"
        return "Unsuccessful Conversion"
    
    def chunking(self):
        chunked_text = []
        chunker = TextChunker(self.filename)
        resBool, chunked_text = chunker.do_chunk()

        if resBool:
            return "Chunking Success", chunked_text
        return "Unsuccessful Chunking", chunked_text
    
    def upserting(self, doc_id, chunked_docs, collection):
        n_chunk = 5
        print("Upserter Setup")
        upserter = Upserter(doc_id, self.raw_filename, collection, chunked_docs, n_chunk).upsert()

        if upserter:
            return "Upserting Success"
        return "Unsuccessful Upserting"
    


