# Import Library
from docling.datamodel import vlm_model_specs
from docling.datamodel.base_models import InputFormat
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.pipeline_options import VlmPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from rich.console import Console
console = Console()

# Conversion
class pdfConversion:
    def __init__(self, filename, raw_filename, output_folder, output_extension):
        self.filename = filename
        self.raw_filename = raw_filename

        self.input_extension = ".pdf"
        self.output_folder = output_folder
        self.output_extension = output_extension
        self.output_filename = self.output_folder + self.raw_filename + self.output_extension
    
    def converting(self):
        console.log("Preparing Model!")
        pipeline_options = VlmPipelineOptions(
            vlm_options=vlm_model_specs.SMOLDOCLING_MLX,
        )
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=VlmPipeline,
                    pipeline_options=pipeline_options,
                ),
            }
        )

        console.log("Converting PDF!")
        try:
            result = converter.convert(source=self.filename).document
            with open(self.output_filename,"w", encoding="utf-8") as f:
                f.write(result.export_to_text())
            return True
        except Exception as e:
            console.log(f"Error while converting {self.raw_filename} document with error : {e}")
            return False