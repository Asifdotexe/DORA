from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from tqdm import tqdm
import os

def create_table(slide, data, title):
    """Creates a table on the given slide with the provided data and title."""
    rows, cols = len(data), len(data[0])
    left = Inches(1)
    top = Inches(1.5)
    width = Inches(11)
    height = Inches(4)

    # Add title to the slide
    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(24)

    # Create the table
    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # Set column headers with background color
    for col_idx in range(cols):
        cell = table.cell(0, col_idx)
        cell.text = data[0][col_idx]  # Header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 176, 240)  # Light blue background
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Fill the table with data and set left alignment
    for row_idx in range(1, rows):
        for col_idx in range(cols):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(data[row_idx][col_idx])  # Value
            cell.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT  # Left align

            # Apply background color for data rows (optional)
            if row_idx % 2 == 0:  # Example for zebra striping
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)  # White background for even rows
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(220, 230, 241)  # Light gray for odd rows

def create_ppt(output_directory: str, presentation_path: str, template_path: str = None) -> None:
    """Creates a PowerPoint presentation with tqdm support."""
    # Load a template if provided; otherwise, create a new presentation
    prs = Presentation(template_path) if template_path else Presentation()

    # Set slide dimensions for 16:9 aspect ratio (if not using a template)
    if not template_path:
        prs.slide_width = Inches(13.3333)
        prs.slide_height = Inches(7.5)

    # Add a title slide
    title_slide_layout = prs.slide_layouts[0]  # Title slide layout
    title_slide = prs.slides.add_slide(title_slide_layout)
    title = title_slide.shapes.title
    subtitle = title_slide.placeholders[1]
    title.text = "EXPLORATORY DATA ANALYSIS"
    subtitle.text = "MADE BY DORA"

    # Bold the title and subtitle text
    for paragraph in title.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.bold = True

    for paragraph in subtitle.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.bold = True

    # Get statistics and charts file lists with progress bar
    stats_files = os.listdir(f"{output_directory}/stats/")
    charts_files = os.listdir(f"{output_directory}/charts/")
    
    tqdm.write("\033[92mCreating slides for charts...\033[0m")  # Green-colored task start

    # Add slides for each chart
    for chart_file in tqdm(charts_files, desc="\033[94mProcessing Charts\033[0m", ncols=100, unit="chart", colour="#008000"):
        slide_layout = prs.slide_layouts[5]  # Using a title-only layout
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = f"CHART - {chart_file.replace('.png', '').replace('_', ' ').upper()}"

        # Bold the title text
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True

        # Add picture with reduced width
        slide.shapes.add_picture(
            f"{output_directory}/charts/{chart_file}",
            left=Inches(1),
            top=Inches(1.5),
            width=Inches(9),  # Reduced width to fit better on the slide
            height=Inches(0)  # Height set to 0 to maintain the aspect ratio automatically
        )

    # Save the PowerPoint presentation
    prs.save(presentation_path)

def save_results(output_directory: str, template_path: str = None) -> str:
    """Creates a PowerPoint presentation from the given output directory."""
    presentation_path = f"{output_directory}/eda_presentation.pptx"
    create_ppt(output_directory, presentation_path, template_path)
    return presentation_path
