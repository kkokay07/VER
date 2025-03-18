import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Parse the data
data = """Goat	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22
7	260	490	550	590	640	600	520	580	520	450	490	430	420	440	430	430	430	590	430	400	240	
14	250	440	560	580	640	660	650	630	660	580	510	500	600	470	570	630	610	610	560	490	280	
20	290	330	430	440	550	520	540	610	530	540	540	500	470	450	480	490	530	470			230	280
11	250	320	380	430	510	540	550	510	590	670	670	700	710	660	650	660	650	570	330		230	260
10	270	480	430	490	520	430	410	400	470	490	510	510	500	490	520	530	540	430	390	380	240	290
18	280	490	500	530	560	410	450	500	460	540	500	520	530	550	570	560	550	540	530	430	270	290"""

# Convert the text data to a DataFrame
lines = data.strip().split('\n')
headers = lines[0].split('\t')
rows = [line.split('\t') for line in lines[1:]]

# Create DataFrame and convert to numeric values
df = pd.DataFrame(rows)
df.columns = headers

# Replace empty strings with NaN
df = df.replace('', np.nan)

# Convert to numeric, except the Goat column
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col])

# Rename the goats from 1 to 6
goat_mapping = {
    '7': 'Goat 1',
    '14': 'Goat 2',
    '20': 'Goat 3',
    '11': 'Goat 4',
    '10': 'Goat 5',
    '18': 'Goat 6'
}
df['Goat'] = df['Goat'].map(goat_mapping)

# Create a figure with larger size
plt.figure(figsize=(14, 10))

# Define colors for each goat
colors = {
    'Goat 1': 'red',
    'Goat 2': 'blue',
    'Goat 3': 'green',
    'Goat 4': 'cyan',
    'Goat 5': 'magenta',
    'Goat 6': 'orange'
}

# Define the estrous cycle phases
phases = {
    'Estrus': [1, 21],
    'Metestrus': [2, 22],
    'Diestrus': list(range(3, 18)),
    'Proestrus': list(range(18, 21))
}

# Define colors for each phase
phase_colors = {
    'Estrus': '#ffcccc',       # Light red
    'Metestrus': '#ccccff',    # Light blue
    'Diestrus': '#ccffcc',     # Light green
    'Proestrus': '#ffffcc'     # Light yellow
}

# Add background colors for each phase
for phase, days in phases.items():
    color = phase_colors[phase]
    if len(days) == 1:
        plt.axvspan(days[0]-0.5, days[0]+0.5, alpha=0.8, color=color)
    elif len(days) == 2 and days[0] != days[1]:
        plt.axvspan(days[0]-0.5, days[0]+0.5, alpha=0.8, color=color)
        plt.axvspan(days[1]-0.5, days[1]+0.5, alpha=0.8, color=color)
    else:
        plt.axvspan(min(days)-0.5, max(days)+0.5, alpha=0.8, color=color)

# Plot the data for each goat
for index, row in df.iterrows():
    goat = row['Goat']
    values = row[1:].astype(float)
    days = np.arange(1, len(values) + 1)
    plt.plot(days, values, marker='o', linestyle='-', color=colors[goat], label=goat)

# Add threshold line
plt.axhline(y=300, color='red', linestyle='--', alpha=0.7)
plt.text(11, 310, 'Estrus Threshold', color='red', fontsize=14, ha='center')

# Customize the chart
plt.xlabel('Days', fontsize=16)
plt.ylabel('Vaginal Electrical Resistance (VER)', fontsize=16)
# No title

plt.xticks(range(1, 23), fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, alpha=0.3)

# Set y-axis limit
plt.ylim(200, 800)

# Move legend to just above the plot boundary without a frame
plt.legend(fontsize=14, loc='upper center', bbox_to_anchor=(0.5, 1.01), 
          ncol=6, frameon=False)

# Create placement for phase labels at the top - all at the same level
y_pos = 700  # All labels will be at this height
phase_positions = {
    'Estrus': [1, 21],
    'Metestrus': [2, 22],
    'Diestrus': 3,  # start of diestrus period
    'Proestrus': 18  # start of proestrus period
}

# Add vertical labels for all phases
plt.text(phase_positions['Estrus'][0], y_pos, 'Estrus', rotation=90, ha='center', va='bottom', fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor=phase_colors['Estrus'], alpha=0.7))
plt.text(phase_positions['Estrus'][1], y_pos, 'Estrus', rotation=90, ha='center', va='bottom', fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor=phase_colors['Estrus'], alpha=0.7))
plt.text(phase_positions['Metestrus'][0], y_pos, 'Metestrus', rotation=90, ha='center', va='bottom', fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor=phase_colors['Metestrus'], alpha=0.7))
plt.text(phase_positions['Metestrus'][1], y_pos, 'Metestrus', rotation=90, ha='center', va='bottom', fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor=phase_colors['Metestrus'], alpha=0.7))
plt.text(phase_positions['Diestrus'], y_pos, 'Diestrus', rotation=90, ha='center', va='bottom', fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor=phase_colors['Diestrus'], alpha=0.7))
plt.text(phase_positions['Proestrus'], y_pos, 'Proestrus', rotation=90, ha='center', va='bottom', fontsize=14, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor=phase_colors['Proestrus'], alpha=0.7))

# Adjust the layout
plt.tight_layout()

# Show the plot
plt.savefig('goat_ver_trends.png', dpi=600, bbox_inches='tight')
plt.show()