#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tetracoil Magnetic Field Visualisation

Author: Adil Wahab Bhatti
Date: 1st July 2025

This script generates magnetic field plots for a tetracoil configuration based on
the four-coil exposure system described in Gottardi et al. (2003).

Based on the four-coil exposure system described in:
Gottardi, G., et al. (2003). Bioelectromagnetics, 24(2), 125-133.
DOI: 10.1002/bem.10074

Uses VectorFieldPlot library by Geek3
Licensed under GNU General Public License v3.0
"""

from vectorfieldplot import FieldplotDocument, Field, FieldLine


class TetracoilConfig:
    """Configuration parameters for the tetracoil magnetic field simulation.
    
    Based on the optimal design parameters from Gottardi et al. (2003) for
    maximising field uniformity in a four-coil electromagnetic system.
    """
    
    # Output document settings
    DOCUMENT_NAME = 'VFPt_tetracoil'
    MAX_FIELD_RADIUS = 8.0
    
    # Arrow styling for field lines
    ARROW_SPACING = 2.0
    MIN_ARROWS_PER_LINE = 2
    MAX_ARROWS_PER_LINE = 4
    
    # Positioning constants
    CENTRE_POSITION = 0.0
    FULL_OFFSET = 1.0
    HALF_OFFSET = 0.5
    
    # Tetracoil geometry parameters
    INNER_COIL_SCALE = 73 / 107  # Scale factor for inner coils (≈ 0.682)
    INNER_COIL_X = 0.298         # Position of inner coils (closer to centre)
    OUTER_COIL_X = 0.798         # Position of outer coils (further from centre)
    INNER_COIL_RADIUS = 1.0      # Radius of inner coils
    OUTER_COIL_RADIUS = 0.7632   # Radius of outer coils
    
    # Field line boundary positions
    FIELD_BOUNDARY_Y = 0.904
    
    # Current magnitude (normalised)
    UNIT_CURRENT = 1.0


class TetracoilFieldPlotter:
    """Handles the creation and rendering of tetracoil magnetic field plots.
    
    This class implements the tetracoil configuration described in Gottardi et al.
    (2003), which consists of four circular coils arranged to maximise field
    uniformity whilst maintaining accessibility for biological experiments.
    """
    
    def __init__(self):
        """Initialise the plotter with tetracoil configuration."""
        self.config = TetracoilConfig()
        self._setup_field_lines()
        self._setup_coil_configurations()
    
    def _setup_field_lines(self):
        """Define starting positions for magnetic field lines.
        
        Creates a comprehensive set of field line starting points including:
        - Central vertical field lines with varying y-positions
        - Boundary field lines at the edges of the uniform field region
        """
        # Central vertical field lines with carefully chosen y-positions
        # These positions are optimised to show the field structure clearly
        central_y_positions = [
            -0.9102, -0.7447, -0.6053, -0.4701, -0.3357, -0.2014, -0.0671,
            0.0671, 0.2014, 0.3357, 0.4701, 0.6053, 0.7447, 0.9102
        ]
        
        # Boundary field lines (top and bottom edges)
        boundary_positions = [
            (-self.config.INNER_COIL_X, -self.config.FIELD_BOUNDARY_Y, self.config.CENTRE_POSITION),
            (self.config.INNER_COIL_X, -self.config.FIELD_BOUNDARY_Y, self.config.CENTRE_POSITION),
            (-self.config.INNER_COIL_X, self.config.FIELD_BOUNDARY_Y, self.config.CENTRE_POSITION),
            (self.config.INNER_COIL_X, self.config.FIELD_BOUNDARY_Y, self.config.CENTRE_POSITION)
        ]
        
        # Central field lines with appropriate arrow offsets
        central_positions = []
        for i, y_pos in enumerate(central_y_positions):
            # Use half offset for middle region field lines for better arrow placement
            offset = self.config.HALF_OFFSET if 2 <= i <= 11 else self.config.CENTRE_POSITION
            central_positions.append((self.config.CENTRE_POSITION, y_pos, offset))
        
        # Combine all field line starting positions
        self.field_line_starts = boundary_positions[:2] + central_positions + boundary_positions[2:]
    
    def _setup_coil_configurations(self):
        """Define the electromagnetic coil configurations.
        
        Creates the four-coil tetracoil system with:
        - Two inner coils at ±0.298 with unit current and larger radius
        - Two outer coils at ±0.798 with scaled current and smaller radius
        """
        # Create all four coils with their positions, radii, and currents
        self.all_coils = [
            self._create_coil(-self.config.OUTER_COIL_X, self.config.OUTER_COIL_RADIUS, self.config.INNER_COIL_SCALE),  # Left outer
            self._create_coil(-self.config.INNER_COIL_X, self.config.INNER_COIL_RADIUS, self.config.UNIT_CURRENT),      # Left inner
            self._create_coil(self.config.INNER_COIL_X, self.config.INNER_COIL_RADIUS, self.config.UNIT_CURRENT),       # Right inner
            self._create_coil(self.config.OUTER_COIL_X, self.config.OUTER_COIL_RADIUS, self.config.INNER_COIL_SCALE)    # Right outer
        ]
        
        # Separate inner and outer coils for different rendering styles
        self.inner_coils = [self.all_coils[1], self.all_coils[2]]  # Coils at ±0.298
        self.outer_coils = [self.all_coils[0], self.all_coils[3]]  # Coils at ±0.798
    
    def _create_coil(self, x_position, radius, current):
        """Create a ring current coil specification.
        
        Args:
            x_position (float): X-coordinate of coil centre
            radius (float): Coil radius
            current (float): Current magnitude
            
        Returns:
            list: Coil specification for VectorFieldPlot
        """
        return ['ringcurrent', {
            'x': x_position,
            'y': self.config.CENTRE_POSITION,
            'phi': self.config.CENTRE_POSITION,
            'R': radius,
            'I': current
        }]
    
    def _create_arrow_style(self, start_offset):
        """Generate arrow styling parameters for field lines.
        
        Args:
            start_offset (float): Offset for arrow positioning
            
        Returns:
            dict: Arrow style configuration
        """
        return {
            'dist': self.config.ARROW_SPACING,
            'min_arrows': self.config.MIN_ARROWS_PER_LINE,
            'max_arrows': self.config.MAX_ARROWS_PER_LINE,
            'offsets': {
                'start': start_offset,
                'leave_image': self.config.HALF_OFFSET,
                'enter_image': self.config.HALF_OFFSET,
                'end': self.config.FULL_OFFSET - start_offset
            }
        }
    
    def generate_plot(self):
        """Create and save the magnetic field visualisation.
        
        This method:
        1. Initialises the plot document
        2. Creates the magnetic field from all coils
        3. Draws field lines with appropriate arrow styling
        4. Draws current symbols for the coils
        5. Saves the result as an SVG file
        
        Returns:
            str: Output filename
        """
        print("Generating tetracoil magnetic field plot...")
        
        # Initialise the plot document
        document = FieldplotDocument(self.config.DOCUMENT_NAME, digits=5, licence='cc-by')
        magnetic_field = Field(self.all_coils)
        
        # Draw magnetic field lines
        print(f"Drawing {len(self.field_line_starts)} field lines...")
        for x_start, y_start, arrow_offset in self.field_line_starts:
            field_line = FieldLine(
                magnetic_field,
                [x_start, y_start],
                directions='both',
                maxr=self.config.MAX_FIELD_RADIUS
            )
            document.draw_line(field_line, arrows_style=self._create_arrow_style(arrow_offset))
        
        # Draw current symbols for coils
        print("Drawing coil current symbols...")
        # Inner coils (at ±0.298) with unit current
        document.draw_currents(Field(self.inner_coils))
        # Outer coils (at ±0.798) with scaled current
        document.draw_currents(Field(self.outer_coils), scale=self.config.INNER_COIL_SCALE)
        
        # Save the plot
        document.write()
        output_filename = f"{self.config.DOCUMENT_NAME}.svg"
        print(f"✓ Tetracoil magnetic field plot saved as '{output_filename}'")
        
        return output_filename


def main():
    """Main execution function."""
    try:
        plotter = TetracoilFieldPlotter()
        plotter.generate_plot()
        print("Tetracoil visualization completed successfully!")
        
    except ImportError as e:
        print(f"Error: Required module not found - {e}")
        print("Please ensure 'vectorfieldplot' is installed or available in your Python path.")
        print("You can obtain it from: https://commons.wikimedia.org/wiki/User:Geek3/VectorFieldPlot")
        return 1
        
    except Exception as e:
        print(f"Error generating plot: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
