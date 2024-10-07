from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from tqdm import tqdm
import os
import logging

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_table(slide, data, title):
    """Create a table on the given slide with the specified data and title.

    :param slide: The slide where the table will be added.
    :param data: The data for the table, provided as a list of lists.
    :param title: The title of the table.
    """
    rows, cols = len(data), len(data[0])
    left, top, width, height = Inches(1), Inches(1.5), Inches(11), Inches(4)

    slide.shapes.title.text = title
    slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(24)

    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # Populate table header
    for col_idx in range(cols):
        cell = table.cell(0, col_idx)
        cell.text = data[0][col_idx]
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(0, 176, 240)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Populate table body
    # This loop fills in the table with data from the provided data list.
    # Each cell is filled with the corresponding value from the data.
    for row_idx in range(1, rows):
        for col_idx in range(cols):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(data[row_idx][col_idx])
            cell.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 0 else RGBColor(220, 230, 241)

def create_ppt(output_directory: str, presentation_path: str, template_path: str = None) -> None:
    """Create a PowerPoint presentation with analysis results.

    :param output_directory: The directory where analysis results are stored.
    :param presentation_path: The path to save the PowerPoint presentation.
    :param template_path: Optional path to a PowerPoint template.
    """
    prs = Presentation(template_path) if template_path else Presentation()

    # Add scatter plots to the PowerPoint presentation
    charts_dir = os.path.join(output_directory, 'charts')
    chart_files = os.listdir(charts_dir)

    # Loop through each chart file to add it to the presentation
    # For each chart, a new slide is added, and the chart is inserted as an image.
    for chart_file in tqdm(chart_files, desc="Adding charts to presentation", ncols=100, unit="chart"):
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.add_picture(f"{charts_dir}/{chart_file}", Inches(0.5), Inches(0.5), height=Inches(5))
        slide.shapes.title.text = f"Chart: {chart_file}"

    # Add statistical summary table to the presentation
    stats_file = os.path.join(output_directory, 'stats', 'univariate_analysis.txt')
    with open(stats_file, 'r') as f:
        stats_data = [line.split() for line in f.readlines()]

    create_table(prs.slides.add_slide(prs.slide_layouts[5]), stats_data, "Statistical Summary")
    prs.save(presentation_path)
    logging.info("Saved PowerPoint presentation successfully.")

def save_results(output_directory: str, template_path: str = None) -> None:
    """Save results of the analysis into a PowerPoint presentation.

    :param output_directory: The directory where analysis results are stored.
    :param template_path: Optional path to a PowerPoint template.
    """
    presentation_path = os.path.join(output_directory, 'EDA_Results.pptx')
    create_ppt(output_directory, presentation_path, template_path)
