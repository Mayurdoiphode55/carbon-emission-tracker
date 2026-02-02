# Project Documentation

This directory contains technical documentation for the Carbon Emission Tracker project.

## Files

### project_report.tex
LaTeX source file for the comprehensive technical report. Contains:
- Abstract and introduction
- System architecture details
- Implementation specifications
- Machine learning model documentation
- Performance metrics and results
- Real-world applications
- Conclusions and future work
- References

**To compile (requires LaTeX installation):**
```bash
pdflatex project_report.tex
```

### project_report.pdf
Pre-compiled PDF version of the technical report. Can be viewed directly without LaTeX installation.

### generate_pdf_report.py
Python script to generate the PDF report using the reportlab library. This provides an alternative to LaTeX compilation.

**To regenerate the PDF:**
```bash
pip install reportlab
python generate_pdf_report.py
```

## Report Contents

The technical report includes:

1. **Introduction** - Background on climate change and transportation emissions
2. **System Architecture** - Detailed component specifications and data flow
3. **Implementation** - Technology stack, ML model, and integration details
4. **Results** - Model performance (R²=0.94), system metrics (<950ms latency)
5. **Applications** - Smart cities, policy making, corporate sustainability
6. **Conclusion** - Summary and future enhancements

## Viewing the Report

- **PDF**: Open `project_report.pdf` with any PDF viewer
- **LaTeX**: Edit `project_report.tex` with a LaTeX editor like Overleaf, TeXworks, or VS Code with LaTeX extension

## Report Statistics

- **Pages**: ~15 pages
- **Sections**: 7 major sections with subsections
- **Tables**: 5 comprehensive tables
- **Format**: Professional academic/technical report style
