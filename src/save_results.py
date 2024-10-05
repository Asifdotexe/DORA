from pptx import Presentation
from pptx.util import Inches
import os

def create_ppt(output_directory: str, presentation_path: str) -> None:
    """This function creates a PowerPoint presentation from the given output directory.
    It reads the statistical analysis and chart files from the specified directories,
    adds them as slides in the presentation, and saves the final presentation at the specified path.

    :param output_directory: The directory containing the statistical analysis and chart files.
    :param presentation_path: The path where the final presentation will be saved.

    :returns: The function does not return any value, but it saves the presentation at the specified path.
    :rtype: None
    """
    prs = Presentation()

    # Set slide size to 16:9 aspect ratio (1920x1080 pixels)
    prs.slide_width = Inches(13.3333)  # 1920 pixels / 144 pixels per inch (PPI)
    prs.slide_height = Inches(7.5)      # 1080 pixels / 144 pixels per inch (PPI)

    # Add a title slide
    title_slide_layout = prs.slide_layouts[0]  # Title slide layout
    title_slide = prs.slides.add_slide(title_slide_layout)
    title = title_slide.shapes.title
    subtitle = title_slide.placeholders[1]  # Placeholder for subtitle
    title.text = "Exploratory Data Analysis"
    subtitle.text = "Insights from the Dataset"

    # Get statistics and charts file lists
    stats_files = os.listdir(f"{output_directory}/stats/")
    charts_files = os.listdir(f"{output_directory}/charts/")

    # Add a slide for each statistical analysis file
    for stats_file in stats_files:
        slide_layout = prs.slide_layouts[1]  # Title and content layout
        slide = prs.slides.add_slide(slide_layout)
        with open(f"{output_directory}/stats/{stats_file}") as file:
            stats_content = file.read()
        slide.shapes.title.text = f"Statistical Analysis - {stats_file}"
        
        # Adjust textbox height for better formatting
        text_box = slide.shapes.add_textbox(
            left=Inches(1),
            top=Inches(1.5),
            width=Inches(11),
            height=Inches(4),  # Adjusted height to provide better text alignment
        )
        text_frame = text_box.text_frame
        text_frame.text = stats_content  # Set the content to the text box

        # Optional: Set font size and formatting if desired
        for paragraph in text_frame.paragraphs:
            paragraph.font.size = Inches(0.24)  # Set font size (example: 0.24 inches = approx. 18pt)

    # Add a slide for each chart file
    for chart_file in charts_files:
        slide_layout = prs.slide_layouts[5]  # Title only layout
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = f"Chart - {chart_file}"
        
        # Add picture with reduced width
        slide.shapes.add_picture(
            f"{output_directory}/charts/{chart_file}",
            left=Inches(1),
            top=Inches(1.5),
            width=Inches(9),  # Reduced width to fit better on the slide
            height=Inches(0)   # Height set to 0 to maintain the aspect ratio automatically
        )

    # Save the PowerPoint presentation
    prs.save(presentation_path)

def save_results(output_directory: str) -> str:
    """
    This function creates a PowerPoint presentation from the given output directory.
    It reads the statistical analysis and chart files from the specified directories,
    adds them as slides in the presentation, and saves the final presentation at the specified path.

    :param output_directory: The directory containing the statistical analysis and chart files.

    :returns: presentation_path: The path of the saved presentation file.
    """
    presentation_path = f"{output_directory}/eda_presentation.pptx"
    create_ppt(output_directory, presentation_path)
    return presentation_path
