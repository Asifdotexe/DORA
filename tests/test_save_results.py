import os
from PIL import Image
from src.save_results import save_results

def test_save_results():
    # Setup
    output_dir = '../tests/output_test/'
    if not os.path.exists(output_dir):
        os.makedirs(f'{output_dir}/stats/')
        os.makedirs(f'{output_dir}/charts/')

    # Create dummy files for testing
    with open(f"{output_dir}/stats/test_stats.txt", 'w') as f:
        f.write("Dummy stats")
        
    # creates an image with dimensions 100x100 and fills it with a red color. 
    # this is then saved as correlation_matrix.png, so the save_results function 
    # can correctly add this image to the PowerPoint slide.
    image = Image.new('RGB', (100, 100), color='red')
    image.save(f"{output_dir}/charts/correlation_matrix.png")
    
    # Test
    presentation_path = save_results(output_dir)

    # Assertions
    assert os.path.exists(presentation_path), "Presentation file was not created"

    # Teardown
    os.remove(presentation_path)
    os.remove(f"{output_dir}/stats/test_stats.txt")
    os.remove(f"{output_dir}/charts/correlation_matrix.png")
