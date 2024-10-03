import os
from src.save_results import save_results

def test_save_results():
    # Setup
    output_dir = 'tests/output_test/'
    if not os.path.exists(output_dir):
        os.makedirs(f'{output_dir}/stats/')
        os.makedirs(f'{output_dir}/charts/')

    # Create dummy files for testing
    with open(f"{output_dir}/stats/test_stats.txt", 'w') as f:
        f.write("Dummy stats")
    with open(f"{output_dir}/charts/test_chart.png", 'w') as f:
        f.write("Dummy chart")

    # Test
    presentation_path = save_results(output_dir)

    # Assertions
    assert os.path.exists(presentation_path), "Presentation file was not created"

    # Teardown
    os.remove(presentation_path)
    os.remove(f"{output_dir}/stats/test_stats.txt")
    os.remove(f"{output_dir}/charts/test_chart.png")
