# Patterned-PDF-Generator
Generate customized PDF documents with various grid, dotted, ruled, and blank patterns


Here's a detailed documentation and inline comments for the `PatternedPDF` class and its usage.

## Documentation

### Overview
The `PatternedPDF` class generates PDF documents with customizable grid patterns. The patterns can include grids, dots, ruled lines, or be blank. Additional features like table structures and cue lines can also be added. The class offers extensive customization options for sizes, colors, and margins.

### Class Initialization
```python
class PatternedPDF:
    def __init__(self, output_folder, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                 background_color, table_color, grid_size, grid_line_width, line_width, cue_perc_left, cue_perc_right, summary_perc, title_perc,
                 rows, columns, margin):
```
- **Parameters**:
  - `output_folder` (str): The folder to save the generated PDF.
  - `pdf_name` (str): The name of the generated PDF file.
  - `paper_width` (float): Width of the paper in mm.
  - `paper_height` (float): Height of the paper in mm.
  - `pattern` (str): The type of pattern ('grid', 'dotted', 'ruled', 'blank').
  - `pattern2` (str): Secondary pattern, mainly for tables ('table').
  - `grid_color` (array): Color of the grid lines in RGB.
  - `line_color` (array): Color of the cue and additional lines in RGB.
  - `background_color` (array): Background color of the PDF in RGB.
  - `table_color` (array): Color of the table lines in RGB.
  - `grid_size` (float): Size of the grid cells in mm.
  - `grid_line_width` (float): Width of the grid lines in mm.
  - `line_width` (float): Width of the cue and additional lines in mm.
  - `cue_perc_left` (float): Percentage position of the left cue line.
  - `cue_perc_right` (float): Percentage position of the right cue line.
  - `summary_perc` (float): Percentage position of the summary line.
  - `title_perc` (float): Percentage position of the title line.
  - `rows` (int): Number of rows in the table.
  - `columns` (int): Number of columns in the table.
  - `margin` (array): Margins of the PDF in mm [left, top, right, bottom].

### Methods

#### `create_patterned_pdf`
Creates and returns a PDF canvas with the specified patterns and features.
- **Returns**: A `canvas.Canvas` object with the generated PDF content.

#### `create_meshgrid`
Creates a meshgrid for the pattern based on the provided grid size and paper dimensions.

#### `draw_horizontal_lines`
Draws horizontal lines on the PDF.

#### `draw_grid`
Draws a grid pattern on the PDF.

#### `draw_dotted`
Draws a dotted pattern on the PDF.

#### `draw_ruled`
Draws ruled lines on the PDF.

#### `draw_blank`
Leaves the PDF blank.

#### `draw_table`
Draws a table structure on the PDF with specified rows and columns.

#### `draw_title_line`
Draws the title line on the PDF.

#### `draw_summary_line`
Draws the summary line on the PDF.

#### `draw_cue_line`
Draws cue lines on the PDF.

## Example Usage

```python
output_folder = 'A4_template_2.5 mm'
pdf_name = 'template 2.5 mm'
paper_width = 210
paper_height = 297
pattern = 'grid'  # Options: 'grid', 'dotted', 'ruled', 'blank'
pattern2 = 'table'
grid_color = np.array([210, 210, 210, 255]) / 255
line_color = np.array([0, 0, 0, 255]) / 255
background_color = np.array([255, 255, 255, 255]) / 255
table_color = np.array([210, 210, 210, 255]) / 255
grid_size = 2.5
grid_line_width = 0.1
line_width = 0.25
title_perc = np.array([0,4])
cue_perc_left = np.array([0,5])
cue_perc_right = np.array([0,5])
summary_perc = np.array([0,15])
rows = 1
columns = 2
margin = np.array([0, 0, 0, 0])

# Create and save the PDF
patterned_pdf = PatternedPDF(output_folder, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                             background_color, table_color, grid_size, grid_line_width, line_width, cue_perc_left, cue_perc_right, summary_perc, title_perc,
                             rows, columns, margin)
doc = patterned_pdf.create_patterned_pdf()
doc.save()
```

## Generating Multiple PDFs

### For Different Patterns and Configurations

```python
patterns = ['grid', 'dotted', 'blank', 'ruled']
for title in title_perc:
    for cue_left in cue_perc_left:
        for cue_right in cue_perc_right:
            for summary in summary_perc:
                for pattern in patterns:
                    if pattern2 == 'table':
                        pdf_name = f'title_{title}_cue_{cue_left}_{cue_right}_summary_{summary}_column_{rows}x{columns}_{pattern}'
                    else:
                        pdf_name = f'title_{title}_cue_{cue_left}_{cue_right}_summary_{summary}_{pattern}'

                    patterned_pdf = PatternedPDF(output_folder, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                                                background_color, table_color, grid_size, grid_line_width, line_width, cue_left, cue_right, summary, title,
                                                rows, columns, margin)
                    doc = patterned_pdf.create_patterned_pdf()
                    doc.save()
```

### For Cornell Note-Taking System

```python
title_perc = np.array([4])
cue_perc_left = np.array([0,15])
cue_perc_right = np.array([0,15])
summary_perc = np.array([0,15])
output_folder2 = f'{output_folder}/cornell'

for title in title_perc:
    for cue_left in cue_perc_left:
        for cue_right in cue_perc_right:
            for summary in summary_perc:
                for pattern in patterns:
                    if cue_left != cue_right:
                        if pattern2 == 'table':
                            pdf_name = f'title_{title}_cue_{cue_left}_{cue_right}_summary_{summary}_column_{rows}x{columns}_{pattern}'
                        else:
                            pdf_name = f'title_{title}_cue_{cue_left}_{cue_right}_summary_{summary}_{pattern}'
                        
                        patterned_pdf = PatternedPDF(output_folder2, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                                                    background_color, table_color, grid_size, grid_line_width, line_width, cue_left, cue_right, summary, title,
                                                    rows, columns, margin)
                        doc = patterned_pdf.create_patterned_pdf()
                        doc.save()
```

### For Table Pattern

```python
title_perc = np.array([4])
cue_perc_left = np.array([5])
cue_perc_right = np.array([5])
summary_perc = np.array([0])
rows = 1
columns = 2
output_folder2 = f'{output_folder}/table'
table_color = np.array([0, 0, 0, 255]) / 255

for title in title_perc:
    for cue_left in cue_perc_left:
        for cue_right in cue_perc_right:
            for summary in summary_perc:
                for pattern in patterns:
                    pdf_name = f'{pattern}_column_{rows}x{columns}'
                    
                    patterned_pdf = PatternedPDF(output_folder2, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                                                background_color, table_color, grid_size, grid_line_width, line_width, cue_left, cue_right, summary, title,
                                                rows, columns, margin)
                    doc = patterned_pdf.create_patterned_pdf()
                    doc.save()
```

