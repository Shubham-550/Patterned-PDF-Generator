import numpy as np
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import Color

class PatternedPDF:
    def __init__(self, output_folder, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                 background_color, table_color, grid_size, grid_line_width, line_width, cue_perc_left, cue_perc_right, summary_perc, title_perc,
                 rows, columns, margin):
        """
        Initialize the PatternedPDF object with given parameters.

        :param output_folder: Directory to save the PDF
        :param pdf_name: Name of the PDF file
        :param paper_width: Width of the paper in mm
        :param paper_height: Height of the paper in mm
        :param pattern: Pattern type ('grid', 'dotted', 'ruled', 'blank')
        :param pattern2: Additional pattern type ('table' or None)
        :param grid_color: Color of the grid lines (list of RGB values)
        :param line_color: Color of the lines (list of RGB values)
        :param background_color: Background color of the page (list of RGB values)
        :param table_color: Color of the table lines (list of RGB values)
        :param grid_size: Size of the grid cells in mm
        :param grid_line_width: Width of the grid lines in mm
        :param line_width: Width of the lines in mm
        :param cue_perc_left: Percentage position of the left cue line
        :param cue_perc_right: Percentage position of the right cue line
        :param summary_perc: Percentage position of the summary line
        :param title_perc: Percentage position of the title line
        :param rows: Number of rows for the table
        :param columns: Number of columns for the table
        :param margin: Page margins (list of 4 values: left, top, right, bottom)
        """
        self.output_folder = output_folder
        self.pdf_name = pdf_name
        self.paper_width = paper_width * mm
        self.paper_height = paper_height * mm
        self.pattern = pattern
        self.pattern2 = pattern2
        self.grid_color = grid_color
        self.line_color = line_color
        self.background_color = background_color
        self.table_color = table_color
        self.grid_size = grid_size * mm
        self.grid_line_width = grid_line_width * mm
        self.line_width = line_width * mm
        self.cue_perc_left = cue_perc_left
        self.cue_perc_right = cue_perc_right
        self.summary_perc = summary_perc
        self.title_perc = title_perc
        self.rows = rows
        self.columns = columns
        self.margin = margin * mm
        self.pdf_path = f'{output_folder}/{pdf_name}.pdf'

    def create_patterned_pdf(self):
        # Create the PDF with the specified pattern and parameters
        os.makedirs(self.output_folder, exist_ok=True)
        pdf = canvas.Canvas(self.pdf_path, pagesize=[self.paper_width, self.paper_height])
        pdf.translate(0, self.paper_height)
        pdf.scale(1, -1)
        
        # Set the background color
        pdf.setFillColorRGB(*self.background_color)
        pdf.rect(0, 0, self.paper_width, self.paper_height, fill=1, stroke=0)

        # Calculate the number of grid columns and rows
        self.grid_columns = int(self.paper_width / self.grid_size)
        self.grid_rows = int(self.paper_height / self.grid_size)

        # if self.pattern2 == 'table' and self.pattern != 'blank':
        #     if self.pattern != 'ruled':
        #         if self.grid_columns % self.columns != 0:
        #             self.grid_columns = self.grid_columns // self.columns * self.columns
        #     if self.grid_rows % self.rows != 0:
        #         self.grid_rows = self.grid_rows // self.rows * self.rows
                
        # Adjust grid columns and rows based on margin and pattern
        self.pattern_width = self.paper_width - (self.margin[0] + self.margin[2])
        self.pattern_height = self.paper_height - (self.margin[1] + self.margin[3])
        
        self.margin_horizontal = self.margin[0] + self.margin[2]
        self.margin_vertical = self.margin[1] + self.margin[3]
        self.grid_columns = int(self.pattern_width / self.grid_size)
        self.grid_rows = int(self.pattern_height / self.grid_size)
        
        # Create the mesh grid for the pattern
        self.create_meshgrid()
        
        self.x_mesh_extended = self.x_mesh_extended + self.margin[0]
        self.y_mesh_extended = self.y_mesh_extended + self.margin[1]
        
        # Set the grid color and line width
        pdf.setStrokeColor(Color(*self.grid_color))
        pdf.setFillColor(Color(*self.grid_color))
        pdf.setLineWidth(self.grid_line_width)
        r = self.line_width / 2

        # Draw the specified pattern
        if self.pattern == 'grid':
            self.draw_grid(pdf)
        elif self.pattern == 'dotted':
            self.draw_dotted(pdf)
        elif self.pattern == 'ruled':
            self.draw_ruled(pdf)
        elif self.pattern == 'blank':
            self.draw_blank(pdf)
        
        # Calculate line positions
        title_index = (self.title_perc * (self.grid_rows)) // 100
        summary_index = self.grid_rows - (self.summary_perc * (self.grid_rows)) // 100
        cue_index_left = int((self.cue_perc_left * (self.grid_columns)) // 100)
        cue_index_right = self.grid_columns - int((self.cue_perc_right * (self.grid_columns)) // 100)
        self.cue_y1 = self.y_mesh_extended[0, 0]
        self.cue_y2 = self.y_mesh_extended[-1, 0]

        # Draw lines
        pdf.setStrokeColor(Color(*self.line_color))
        pdf.setLineWidth(self.line_width)
        
        self.draw_title_line(pdf, title_index)
        self.draw_summary_line(pdf, summary_index)
        self.draw_cue_line(pdf, cue_index_left, self.cue_y1, self.cue_y2)
        self.draw_cue_line(pdf, cue_index_right, self.cue_y1, self.cue_y2)
        
        # Draw table if pattern2 is 'table'
        pdf.setStrokeColor(Color(*self.table_color))
        
        if self.pattern2 == 'table':
            self.draw_table(pdf, title_index, cue_index_left, cue_index_right, summary_index)
        
        pdf.showPage()
        
        return pdf
        
    def create_meshgrid(self):
        # Create a mesh grid based on the pattern width and height
        self.x_coordinates = np.arange(0, self.pattern_width, self.grid_size)
        self.y_coordinates = np.arange(0, self.pattern_height, self.grid_size)

        self.x_mesh, self.y_mesh = np.meshgrid(self.x_coordinates, self.y_coordinates)
        self.x_mesh_extended = np.concatenate([self.x_mesh, np.ones_like(self.x_mesh[:, 0:1]) * self.pattern_width], axis=1)
        self.y_mesh_extended = np.concatenate([self.y_mesh, np.ones_like(self.y_mesh[0:1, :]) * self.pattern_height], axis=0)
        self.x_mesh_extended = np.concatenate([self.x_mesh_extended, self.x_mesh_extended[0:1, :]], axis=0)
        self.y_mesh_extended = np.concatenate([self.y_mesh_extended, self.y_mesh_extended[:, 0:1]], axis=1)

    def draw_horizontal_lines(self, pdf):
        # Draw horizontal lines based on the mesh grid
        for row in self.y_mesh_extended[:, 0]:
            y = row

            if self.margin[0] == 0 and y == 0:
                pass
            elif self.margin[2] == 0 and y == self.paper_height:
                pass
            else:
                pdf.line(self.x1, y, self.x2, y)

    def draw_grid(self, pdf):
        # Draw a grid pattern
        
        # Horizontal lines
        self.x1 = self.x_mesh_extended[0, 0]
        self.x2 = self.x_mesh_extended[0, -1]
        self.draw_horizontal_lines(pdf)

        # Vertical lines
        self.y1 = self.y_mesh_extended[0, 0]
        self.y2 = self.y_mesh_extended[-1, 0]

        for col in self.x_mesh_extended[0, :]:
            x = col

            if self.margin[1] == 0 and x == 0:
                pass
            elif self.margin[3] == 0 and x == self.paper_width:
                pass
            else:
                pdf.line(x, self.y1, x, self.y2)

    def draw_dotted(self, pdf):
        # Draw a dotted pattern
        pdf.setLineCap(1)
        pdf.setDash([0.0000001, self.grid_size], 0)
        pdf.setLineWidth(self.line_width)

        # Horizontal dotted lines
        self.x1 = self.x_mesh_extended[0, 0]
        self.x2 = self.x_mesh_extended[0, -1]

        if self.margin[1] == 0:
            self.x1 = self.x_mesh_extended[0, 1]
        if self.margin[3] == 0 and self.x2 == self.paper_width:
            self.x2 = self.x_mesh_extended[0, -1]
        if self.margin[1] == 0:
            self.x2 = self.x_mesh_extended[0, -1] + self.grid_size

        self.draw_horizontal_lines(pdf)
        
        pdf.setLineCap(0)
        pdf.setDash([])

    def draw_ruled(self, pdf):
        # Draw ruled lines
        self.x1 = self.x_mesh_extended[0, 0]
        self.x2 = self.x_mesh_extended[0, -1]
        self.draw_horizontal_lines(pdf)

    def draw_blank(self, pdf):
        # Draw a blank page (no pattern)
        pass
    
    def draw_table(self, pdf, title_index, cue_index_left, cue_index_right, summary_index):
        # Draw a table within the pattern
        if title_index != 0 and summary_index != 0:
            row_height = (self.y_mesh_extended[summary_index, 0] - self.y_mesh_extended[title_index, 0]) / self.rows
        elif title_index != 0:
            row_height = (self.y_mesh_extended[-1, 0] - self.y_mesh_extended[title_index, 0]) / self.rows
        elif summary_index != 0:
            row_height = (self.y_mesh_extended[summary_index, 0] - self.y_mesh_extended[0, 0]) / self.rows
        else:
            row_height = self.pattern_height / self.rows
        
        if cue_index_left != 0 and cue_index_right != self.x_mesh_extended[0, -1]:
            column_width = (self.x_mesh_extended[0, cue_index_right] - self.x_mesh_extended[0, cue_index_left]) / self.columns
        elif cue_index_left != 0 and cue_index_right == self.x_mesh_extended[0, -1]:
            column_width = (self.x_mesh_extended[0, -1] - self.x_mesh_extended[0, cue_index_left]) / self.columns
        elif cue_index_left == 0 and cue_index_right != self.x_mesh_extended[0, -1]:
            column_width = (self.x_mesh_extended[0, cue_index_right] - self.x_mesh_extended[0, 0]) / self.columns
        else:
            column_width = self.pattern_width / self.columns
        
        aa2 = round(column_width / self.grid_size - column_width // self.grid_size, 5)
        
            
        if aa2 < 0.5:
            column_width = column_width // self.grid_size * self.grid_size
        elif aa2 >= 0.5:
            column_width = (column_width // self.grid_size + 1) * self.grid_size
        elif aa2 == 0.5:
            pass
        
        
        row_height = -(row_height // -self.grid_size + 1) * self.grid_size        
        
        
        # draw horizontal lines
        x2 = self.x_mesh_extended[0,-1]
        
        if cue_index_left == 0:
            x1 = self.x_mesh_extended[0,0]
        else:
            x1 = self.x_mesh_extended[0, cue_index_left]
        
        if cue_index_right == 0:
            x2 = self.x_mesh_extended[0,-1]
        else:
            x2 = self.x_mesh_extended[0, cue_index_right]
        
        for i in np.arange(self.rows - 1):
            y = self.y_mesh_extended[0,0] + row_height * (i + 1)
            pdf.line(x1, y, x2, y)
        
        # draw vertical lines
        if cue_index_left == 0:
            x1 = self.x_mesh_extended[0,0]
        else:
            x1 = self.x_mesh_extended[0, cue_index_left]
        
        if title_index == 0:
            y1 = self.y_mesh_extended[0, 0]
        else:
            y1 = self.y_mesh_extended[title_index, 0] + self.line_width/2

        if summary_index == self.grid_rows:
            y2 = self.y_mesh_extended[-1, 0]
        else:
            y2 = self.y_mesh_extended[summary_index, 0]  - self.line_width/2

        for j in np.arange(self.columns - 1):
            x = x1 + column_width * (j + 1)
            pdf.line(x, y1, x, y2)

    def draw_title_line(self, pdf, title_index):
        if title_index != 0:
            x1 = self.x_mesh_extended[0, 0]
            x2 = self.x_mesh_extended[0, -1]
            y1 = self.y_mesh_extended[title_index, 0]
            pdf.line(x1, y1, x2, y1)        # title line
            
            self.cue_y1 = y1 + self.line_width/2

    def draw_summary_line(self, pdf, summary_index):
        if summary_index != self.grid_rows:
            x1 = self.x_mesh_extended[0, 0]
            x2 = self.x_mesh_extended[0, -1]
            y1 = self.y_mesh_extended[summary_index, 0]
            pdf.line(x1, y1, x2, y1)        # summary line
            
            self.cue_y2 = y1 - self.line_width/2

    def draw_cue_line(self, pdf, cue_index, cue_y1, cue_y2):
        if cue_index != 0 and cue_index != self.grid_columns:
            x1 = self.x_mesh_extended[0, cue_index]
            y1 = self.cue_y1
            y2 = self.cue_y2
            pdf.line(x1, y1, x1, y2)        # cue line


# Example Usage:
output_folder = 'templates/A4 5mm white'
pdf_name = 'template 5 mm'      # if only single pdf is to be created

paper_width = 210
paper_height = 297

pattern = 'grid'  # 'grid' 'dotted' 'ruled' 'blank'
pattern2 = 'table'

grid_color = np.array([210, 210, 210, 255]) / 255
line_color = np.array([0, 0, 0, 255]) / 255
background_color = np.array([255, 255, 255, 255]) / 255
table_color = np.array([210, 210, 210, 255]) / 255
grid_color[3] = 1               # grid opacity    
line_color[3] = 1               # line opacity
background_color[3] = 1         # background opacity
table_color[3] = 1              # table opacity

grid_size = 5
grid_line_width = 0.1
line_width = 0.25

title_perc = np.array([0,4])
cue_perc_left = np.array([0,5])
cue_perc_right = np.array([0,5])
summary_perc = np.array([0,15])

rows = 1
columns = 2
margin = np.array([0, 0, 0, 0])

''' For single pdf '''

# title_perc = np.array([5])
# cue_perc_left = np.array([5])
# cue_perc_right = np.array([10])
# summary_perc = np.array([10])
# patterned_pdf = PatternedPDF(output_folder, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
#                                 background_color, table_color, grid_size, grid_line_width, line_width, cue_perc_left, cue_perc_right, summary_perc, title_perc,
#                                 rows, columns, margin)
# doc = patterned_pdf.create_patterned_pdf()
# doc.save()


''' For multiple pdf '''

patterns = ['grid', 'dotted', 'blank', 'ruled']

for title in title_perc:
    for cue_left in cue_perc_left:
        for cue_right in cue_perc_right:
            for summary in summary_perc:
                for pattern in patterns:
                    pdf_name = f'{pattern} - (title, cue (L-R), summary) - ({title}, {cue_left}-{cue_right}, {summary})%'

                    patterned_pdf = PatternedPDF(output_folder, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                                                background_color, table_color, grid_size, grid_line_width, line_width, cue_left, cue_right, summary, title,
                                                rows, columns, margin)
                    doc = patterned_pdf.create_patterned_pdf()
                    doc.save()


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
                        pdf_name = f'{pattern} - (title, cue (L-R), summary) - ({title}, {cue_left}-{cue_right}, {summary})%'
                        
                        patterned_pdf = PatternedPDF(output_folder2, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                                                    background_color, table_color, grid_size, grid_line_width, line_width, cue_left, cue_right, summary, title,
                                                    rows, columns, margin)
                        doc = patterned_pdf.create_patterned_pdf()
                        doc.save()


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
                    pdf_name = f'{pattern} - table {rows}x{columns}'
                    
                    patterned_pdf = PatternedPDF(output_folder2, pdf_name, paper_width, paper_height, pattern, pattern2, grid_color, line_color,
                                                background_color, table_color, grid_size, grid_line_width, line_width, cue_left, cue_right, summary, title,
                                                rows, columns, margin)
                    doc = patterned_pdf.create_patterned_pdf()
                    doc.save()

