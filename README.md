# PhyloTree Explorer (Penjelajah PhyloTree)

PhyloTree Explorer is a Streamlit-based web application that allows users to build, compare, and visualize phylogenetic trees from DNA or protein sequences. The application provides an intuitive interface for sequence alignment, distance matrix computation, and tree rendering using classical distance-based methods.

*[Aplikasi ini menggunakan bahasa Indonesia pada antarmukanya.]*

## Features

- **Upload FASTA Data**: Users can upload their own FASTA or unaligned sequences, or use the provided sample dataset containing sequences of various primates and mammals.
- **Multiple Sequence Alignment (MSA)**: Built-in support for aligning unaligned sequences using **MUSCLE**.
- **Distance Matrix Calculation**:
  - Calculates genetic distance between pairs of sequences.
  - Supports different substitution models such as **Identity** and **BLOSUM62**.
  - Visualizes the computed distance matrix as a heatmap.
- **Phylogenetic Tree Construction**: Constructs and compares trees using two classical methods simultaneously:
  - **Neighbor-Joining (NJ)**: A widely used distance-based method, unrooted, with no molecular clock assumption.
  - **UPGMA**: A hierarchical clustering method, rooted, based on the assumption of a constant rate of evolution.

## Tech Stack

This project was built using the following technologies:

- **Python**
- **Streamlit**: Web application framework.
- **Biopython**: Handling sequence parsing and executing multiple sequence alignments.
- **Toytree**: Constructing, drawing, and manipulating phylogenetic trees.
- **NumPy & SciPy**: Handling complex numerical operations and matrices.
- **Matplotlib & Plotly**: Rendering visualizations such as distance heatmaps.

## Getting Started

### Prerequisites

You need to have Python installed on your system. Additionally, the project relies on **MUSCLE** for performing sequence alignments.

If you are running this locally:

- You must install MUSCLE and ensure it is available in your system's PATH.

*(Note: On Debian/Ubuntu Linux, MUSCLE can be installed with `sudo apt-get install muscle`. For Streamlit Cloud deployments, it is handled automatically through `packages.txt`.)*

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd phylotree
   ```

2. **Set up a virtual environment (optional but recommended)**

   ```powershell
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\activate
   
   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

## Project Structure

```
phylotree/
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
├── packages.txt       # System-level dependencies (apt-get packages)
├── README.md          # Project documentation
├── src/               # Core application logic
│   ├── alignment.py   # MUSCLE alignment functions
│   ├── parser.py      # Fasta parser and validation
│   ├── tree_builder.py# NJ & UPGMA tree algorithms and matrix calculations
│   └── visualization.py # Functions for plotting the trees and matrices
├── data/              # Storage for sequences or generated outputs
├── tests/             # Unit testing configurations
└── assets/            # Additional project resources
```

## Usage Workflow

1. **Upload your data**: Navigate to the left sidebar and upload a `.fasta`, `.fa`, or `.fas` file. Alternatively, check the option to use the built-in sample dataset.
2. **Settings**: Choose a distance model for matrix calculation (e.g., Identity or BLOSUM62).
3. **Validation & Alignment**: The app validates your sequences. If your uploaded sequences are unaligned (differ in length), you will be prompted to automatically run MUSCLE alignment.
4. **Analysis & Visualization**: Review the auto-rendered Distance Matrix heatmap, and visually compare the resulting UPGMA and Neighbor-Joining phylogenetic trees side-by-side.

## License

This project is licensed under the MIT License.
