
Adobe Hackathon 2025 - Problem 1a: Understand Your Document

This repository contains our team's solution for Problem 1a of the Adobe Hackathon 2025. The goal of this project is to extract a structured outline (Title, H1, H2, H3) from a variety of PDF documents.

Our Approach:

We designed a robust, heuristic-based solution that does not rely on any external ML models, ensuring it is fast, lightweight, and fully compliant with the offline requirement. Our approach works in two main stages:

Table of Contents (TOC) First: The most reliable source of a document's structure is its built-in "bookmarks" or Table of Contents. Our script first checks for this metadata. If it exists, we use it directly to generate a highly accurate outline.

Heuristic-Based Fallback: If a PDF has no built-in TOC, our script switches to a smart heuristic engine. This engine analyzes the document's typography to deduce its structure:

It first determines the body text font size by finding the most common font size in the document.

It then identifies potential heading styles as any font sizes that are significantly larger than the body text.

Finally, it iterates through the document, classifying lines as headings based on their font size and mapping them to H1, H2, or H3 levels. This allows us to build a structural outline even when none is explicitly provided.

This dual-method approach ensures the highest possible accuracy for structured documents while still providing a strong, logical outline for simpler or less-structured PDFs.

How to Build and Run

The entire solution is containerized using Docker for easy and consistent execution.

Prerequisites

Docker must be installed and running on your machine.

Instructions

Place PDFs: Add the PDF files you want to process into the input/ directory.

Build the Docker Image: Open a terminal in the project's root directory and run the build command.
docker build --platform linux/amd64 -t pdf-extractor:1.0 .

Run the Container: Execute the following command to run the script. It will automatically process all PDFs from the input folder and save the resulting JSON files to the output folder.
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none pdf-extractor:1.0
(Note for Windows users: In Command Prompt, replace $(pwd) with %cd%. In PowerShell, use ${pwd}.)

Project Structure

.
├── Dockerfile          # Defines the container for our application.
├── main.py             # The core Python script with all the extraction logic.
├── requirements.txt    # Lists the necessary Python libraries (PyMuPDF).
├── input/              # Folder to place input PDF files.
└── output/             # Folder where the generated JSON files are saved.

Libraries Used

PyMuPDF (fitz): A powerful and high-performance Python library for accessing PDF content, including text, fonts, and metadata.
