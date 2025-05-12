""" Scenario Description
from video: hazard0.mp4
Based on the images provided, here's a list of road conditions and potential hazards:
1. **Traffic Conditions:**
   - Multiple vehicles are on the road, traveling in the same direction.
   - The car directly ahead poses a potential hazard if it brakes suddenly.

2. **Infrastructure:**
   - An overpass is visible, potentially obscuring vision momentarily.

3. **Lane Conditions:**
   - The lanes seem to be clearly marked, reducing confusion.
   - No visible debris or obstructions on the roadway.

4. **Traffic Signals:**
   - A traffic signal is visible, indicating a potential stop if the light changes.

5. **Surrounding Environment:**
   - Palm trees and vegetation line the roadside, but are not infringing on the roadway.
   - Clear weather conditions with good visibility.

6. **Other Vehicles:**
   - Vehicles are present in adjacent lanes, which could cause hazards if sudden lane changes occur.

    scenic ScenicProjects/hazard0.scenic --2d --model scenic.simulators.carla.model --simulate
"""


## SET MAP AND MODEL (i.e. definitions of all referenceable vehicle types, road library, etc)
param map = localPath('../assets/maps/CARLA/Town04.xodr)
param carla_map = 'Town04'
model scenic.simulators.carla.model
