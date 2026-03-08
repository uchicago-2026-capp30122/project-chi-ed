# Import all other modules in this file and run everything here
import sys 
from chi_ed.spatial.dashboard import app
from chi_ed.reports.reports import create_report


if __name__ == "__main__":
    num_args = len(sys.argv)

    if num_args < 2:
        raise ValueError("Brother what should I do?")
    
    task = str(sys.argv[1])

    if task == "dashboard":
        app.run(debug=True)

