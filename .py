import pandas as pd
import xml.etree.ElementTree as ET

# Your input data
data = {
    'ID_Value': [201, 202, 203],
    'Name_Value': ['e', 'e', 'e'],
    'City_Value': ['Mumbai', 'Pune', 'Nagpur'],
    'Pincode_Value_PL': [400001, 411001, 440001],
    'Region_Value': ['West', 'West', 'East'],
    'ID_Value_PL': [301, 302, 303],
    'Name_Value_PL': ['a', 'b', 'c'],
    'City_Value_LL': ['Mumbai', 'Pune', 'Nagpur'],
    'Pincode_Value': [400001, 411001, 440001],
    'Region_Value_PL': ['West', 'West', 'East'],
}

df = pd.DataFrame(data)

# Load XML
tree = ET.parse("input.xml")
root = tree.getroot()

# Separate columns based on suffix
newrisk_cols = [col for col in df.columns if not col.endswith('_PL')]
oldrisk_cols = [col for col in df.columns if col.endswith('_PL')]

# Map to XML sections
sections = {
    'newrisk': root.find('.//NewRisk/Level3/Vaehicles'),
    'oldrisk': root.find('.//oldRisk/Level3/Vaehicles')
}

# Update function
def update_vehicles(section_key, cols, is_oldrisk=False):
    vehicle_nodes = sections[section_key].findall('./Vaehicle')

    for idx, row in df.iterrows():
        if idx >= len(vehicle_nodes):
            break  # Avoid overflow
        vehicle = vehicle_nodes[idx]

        for col in cols:
            xml_tag = col.replace('_PL', '')  # Normalize tag name
            tag_elem = vehicle.find(xml_tag)
            if tag_elem is not None:
                tag_elem.set('value', str(row[col]))

# Update newrisk and oldrisk vehicles
update_vehicles('newrisk', newrisk_cols)
update_vehicles('oldrisk', oldrisk_cols)

# Save result
tree.write("updated_output.xml", encoding="utf-8", xml_declaration=True)
