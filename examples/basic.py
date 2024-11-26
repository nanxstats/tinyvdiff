from tinyvdiff.pdf2svg import PDF2SVG

# Basic usage
converter = PDF2SVG()
converter.convert("input.pdf")  # Creates input.svg

# Specify output path and page number
converter.convert("input.pdf", "output.svg", page=2)

# Custom executable path
converter = PDF2SVG(executable_path="/custom/path/to/pdf2svg")

# Check if pdf2svg is available
if PDF2SVG.is_available():
    print("pdf2svg is installed")
