from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

def create_table(slide, data, title):
    """Creates a table on the given slide with the provided data and title.

    :param slide: The slide object where the table will be created.
    :param data: A 2D list containing the table data.
    :param title: The title of the table to be displayed above the table.

    :returns: None
    """
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

    # Note: Borders cannot be directly set in the same way as other properties in python-pptx.
    # They are set by default for table cells.
    
def create_ppt(output_directory: str, presentation_path: str, template_path: str = None) -> None:
    """Creates a PowerPoint presentation from the given output directory.

    This function reads the statistical analysis and chart files from the specified directories,
    adds them as slides in the presentation, and saves the final presentation at the specified path.

    :param output_directory: The directory containing the statistical analysis and chart files.
    :param presentation_path: The path where the final presentation will be saved.
    :param template_path: The path to the PowerPoint template file (optional).

    :returns: None
    """
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

    # Get statistics and charts file lists
    stats_files = os.listdir(f"{output_directory}/stats/")
    charts_files = os.listdir(f"{output_directory}/charts/")

    # Add a slide for each chart file using the appropriate layout from the template
    for chart_file in charts_files:
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
    """Creates a PowerPoint presentation from the given output directory.

    This function reads the statistical analysis and chart files from the specified directories,
    adds them as slides in the presentation, and saves the final presentation at the specified path.

    :param output_directory: The directory containing the statistical analysis and chart files.
    :param template_path: The path to the PowerPoint template file (optional).

    :returns: presentation_path: The path of the saved presentation file.
    """
    presentation_path = f"{output_directory}/eda_presentation.pptx"
    create_ppt(output_directory, presentation_path, template_path)
    return presentation_path