import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool
import numpy as np
import math

# Define Zodiac signs & degrees
zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
zodiac_degrees = {sign: i * 30 for i, sign in enumerate(zodiac_signs)}

# Define Nakshatras with ruling planets
nakshatras_with_planets = [
    "Ashwini \n(Ketu)", "Bharani \n(Venus)", "Krittika \n(Sun)", "Rohini \n(Moon)", "Mrigashira \n(Mars)",
    "Ardra \n(Rahu)", "Punarvasu \n(Jupiter)", "Pushya \n(Saturn)", "Ashlesha \n(Mercury)",
    "Magha \n(Ketu)", "Purva Phalguni \n(Venus)", "Uttara Phalguni \n(Sun)", "Hasta \n(Moon)",
    "Chitra \n(Mars)", "Swati \n(Rahu)", "Vishakha \n(Jupiter)", "Anuradha \n(Saturn)", "Jyeshtha \n(Mercury)",
    "Moola \n(Ketu)", "Purvashada \n(Venus)", "Uttarashada \n(Sun)", "Shravana \n(Moon)", "Dhanishta \n(Mars)",
    "Shatabhisha \n(Rahu)", "Purva Bhadrapada \n(Jupiter)", "Uttara Bhadrapada \n(Saturn)", "Revati \n(Mercury)"
]

# Define 108 Pada rulers (each Nakshatra has 4 Padas)
pada_rulers_full = [
    ["Mars", "Venus", "Mercury", "Moon"], ["Sun", "Mercury", "Venus", "Mars"],
    ["Jupiter", "Saturn", "Saturn", "Jupiter"], ["Mars", "Venus", "Mercury", "Moon"],
    ["Sun", "Mercury", "Venus", "Mars"], ["Jupiter", "Saturn", "Saturn", "Jupiter"],
    ["Mars", "Venus", "Mercury", "Moon"], ["Sun", "Mercury", "Venus", "Mars"],
    ["Jupiter", "Saturn", "Saturn", "Jupiter"], ["Mars", "Venus", "Mercury", "Moon"],
    ["Sun", "Mercury", "Venus", "Mars"], ["Jupiter", "Saturn", "Saturn", "Jupiter"],
    ["Mars", "Venus", "Mercury", "Moon"], ["Sun", "Mercury", "Venus", "Mars"],
    ["Jupiter", "Saturn", "Saturn", "Jupiter"], ["Mars", "Venus", "Mercury", "Moon"],
    ["Sun", "Mercury", "Venus", "Mars"], ["Jupiter", "Saturn", "Saturn", "Jupiter"],
    ["Mars", "Venus", "Mercury", "Moon"], ["Sun", "Mercury", "Venus", "Mars"],
    ["Jupiter", "Saturn", "Saturn", "Jupiter"], ["Mars", "Venus", "Mercury", "Moon"],
    ["Sun", "Mercury", "Venus", "Mars"], ["Jupiter", "Saturn", "Saturn", "Jupiter"],
    ["Mars", "Venus", "Mercury", "Moon"], ["Sun", "Mercury", "Venus", "Mars"],
    ["Jupiter", "Saturn", "Saturn", "Jupiter"]
]


# Create Bokeh figure
p = figure(width=800, height=800,
           x_range=(-1.2, 1.2), y_range=(-1.2, 1.2),
           tools="reset", toolbar_location=None)

p.toolbar.active_drag = None
# **Hide axis & grid for cleaner look**
p.axis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None  # Remove border

# **Draw Zodiac sectors & Labels**
for i, sign in enumerate(zodiac_signs):
    start_angle = math.radians(i * 30)
    end_angle = math.radians((i + 1) * 30)
    mid_angle = (start_angle + end_angle) / 2
    x_label = math.cos(mid_angle) * .5  # Position label outside the circle
    y_label = math.sin(mid_angle) * .5

    # Draw sector
    p.annular_wedge(x=0, y=0, inner_radius=0, outer_radius=1.0, 
                    start_angle=start_angle, end_angle=end_angle, 
                    fill_color="blue" if i % 2 == 0 else "lightblue", alpha=0.4)

    # Add Zodiac sign label
    p.text(x_label, y_label, text=[sign], text_align="center", text_baseline="middle", text_color="black", text_font_size="10pt")

# **Add Nakshatra labels**
nakshatra_angles = np.linspace(0, 2 * np.pi, 28)
for i, (nakshatra, start_angle) in enumerate(zip(nakshatras_with_planets, nakshatra_angles[:-1])):
    mid_angle = (start_angle + nakshatra_angles[i + 1]) / 2
    x_label = math.cos(mid_angle) * 1.15
    y_label = math.sin(mid_angle) * 1.05
    p.text(x_label, y_label, text=[nakshatra], text_align="center", text_baseline="middle", text_color="purple", text_font_size="8pt")

# Draw lines for Nakshatra boundaries (Thicker Dashed Lines)
for start_angle in nakshatra_angles[:-1]:
    x_start, y_start = 0, 0  # Center of the circle
    x_end, y_end = math.cos(start_angle), math.sin(start_angle)*0.9  # Edge of the circle
    p.line([x_start, x_end], [y_start, y_end], line_color="black", line_width=1.5, line_dash=[2, 2])  # Thicker dashes

# Draw lines from the center to the circumference marking Pada boundaries
nakshatra_angles = np.linspace(0, 2 * np.pi, 28)  # 27 Nakshatras + closing
for i, start_angle in enumerate(nakshatra_angles[:-1]):
    for j in range(4):  # Each Nakshatra has 4 Padas
        pada_angle = start_angle + ((nakshatra_angles[i + 1] - start_angle) / 4) * j
        x_start, y_start = 0, 0  # Center of the circle
        x_end, y_end = math.cos(pada_angle), math.sin(pada_angle)*0.9  # Edge of the circle

        p.line([x_start, x_end], [y_start, y_end], line_color="gray", line_width=1, line_dash=[2, 2])

# Add Pada ruler labels rotated along the Pada lines
for i, (nakshatra, start_angle) in enumerate(zip(nakshatras_with_planets, nakshatra_angles[:-1])):
    for j in range(4):  # Each Nakshatra has 4 Padas
        pada_angle = start_angle + ((nakshatra_angles[i + 1] - start_angle) / 4) * (j + 0.5)
        x_pada = math.cos(pada_angle) * 1  # Position text slightly outside the circle
        y_pada = math.sin(pada_angle) * 0.9

        # Determine angle adjustment for text readability
        text_rotation = math.degrees(pada_angle)  
        if text_rotation > 90 and text_rotation < 270:  # Flip text in bottom half
            text_rotation += 180  

        # Add rotated text
        p.text(
            x_pada, y_pada, 
            text=[pada_rulers_full[i][j]], 
            text_align="center", 
            text_baseline="middle", 
            text_color="red", 
            text_font_size="7pt", 
            angle=math.radians(text_rotation)  # Rotate label to match line
        )



# Define planetary positions (Example Data)
planet_positions = {
    "Asc": ("Virgo", 5 + 33/60),
    "Sun": ("Sagittarius", 4 + 43/60),
    "Moon": ("Sagittarius", 20 + 34/60),
    "Mercury": ("Scorpio", 17 + 41/60),
    "Venus": ("Capricorn", 3 + 58/60),
    "Mars": ("Leo", 17 + 53/60),
    "Jupiter": ("Leo", 16 + 34/60),
     "🪐 Sat": ("Virgo", 3 + 10/60),
    "Rahu": ("Aquarius", 8 + 45/60),
    "Ketu": ("Leo", 8 + 45/60),
}

# Convert planetary positions to radians
planet_angles = {planet: math.radians(zodiac_degrees[sign] + degree) for planet, (sign, degree) in planet_positions.items()}

# Plot planetary positions
for planet, angle in planet_angles.items():
    if (planet == "Asc"):
        continue
    x = math.cos(angle) * 0.75
    y = math.sin(angle) * 0.7
    p.circle(x, y, size=5, color="red")
    p.text(x, y + 0.02, text=[planet], text_align="center", text_baseline="middle", text_color="black", text_font_size="8pt")

# **Draw the Ascendant line (Green, Thicker)**
x_start, y_start = 0, 0  # Center of the chart
x_end, y_end = math.cos(planet_angles["Asc"]), math.sin(planet_angles["Asc"])  # Edge of the circle

p.line([x_start, x_end], [y_start, y_end], line_color="green", line_width=2, line_dash="solid")  # Ascendant Line


# Add interactivity
# hover = HoverTool(tooltips=[("Planet", "@name")])
# p.add_tools(hover)

# Show chart in Streamlit
st.bokeh_chart(p, use_container_width=True)
