# vehicle_identification_IMAV_2026
Repo for detection and vehicle indentification algorithm for IMAV 2026 competition mission. 

### Mission description
Context: "In the context of a wildfire, having an accurate map of the operational area, including the location
of intervention teams, is essential. The objective of this mission is to generate a map of the area and
to identify both the position and the designation of the emergency vehicles deployed on the field."

__Important info__
- Within these areas, a number of fire brigade and military vehicles will be positioned (the exact
distribution between fire and military vehicles will be specified on the day of the competition). -> we know its 8 to detect but we do not know the split
- Points will be awarded if GPS positions are provided with an accuracy of within 5 meters and
if the vehicle will correctly be identified.
- The GPS coordinates must be provided no later than 5 minutes after landing.
- the table is required:

| Vehicle Identification | GPS coordinates                         |
|------------------------|-----------------------------------------|
| 67-CCF-M-ING           | 48.8095202082736 ; 7.85202741622925     |
| GBC                    | 180 48.8084886157098 ; 7.85187721252441 |

__Type of the vehicles__
1. Fire birgade trucks (CCF):

![alt text](images/image.png)

- red / yellow colors
- black lettered identifiers in yelllow or white bg 

2. VLTT: light off road

![alt text](images/image-1.png)

- mainly red
- yellow  or white bg / red letters with identifier

3. 4x4 VT4 

![alt text](images/image-2.png)

- different colors possible
- rather not red

4. VBL light armoured vehicle 
![alt text](images/image-3.png)

- rather military colors

5. Truck (GBC 180)

![alt text](images/image-4.png)