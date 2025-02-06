import arcpy
import json
import os


#Ustawinie ścieżki do geobazy oraz układu współrzędnych na EPSG:2180
arcpy.env.workspace = r"C:\Users\lukas\Documents\programowanie_gis\projekt\projekt_zal.gdb"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2180)
arcpy.env.overwriteOutput = True #Nadpisywanie istniejących plików

#Ścieżka do pliku JSON zawierającego dane autobusów
input_json_file = "C:\Users\lukas\Documents\programowanie_gis\projekt\bus_data.txt"

#Ścieżka do wynikowego pliku shapefile przechowującego punkty autobusowe
output_shapefile = r"C:\Users\lukas\Documents\programowanie_gis\projekt\projekt_zal.gdb\bus_output"

#Funkcja do wczytywania danych z pliku JSON i zwracania listy pojazdów
def read_bus_data(json_path):
  with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
  return data['vehicles']


#Tworzenie warstwy punktowej, jeśli jeszcze nie istnieje
if not arcpy.Exists(output_shapefile):
  arcpy.CreateFeatureclass_managment(
    os.path.dirname(output_shapefile),
    os.path.basename(output_shapefile),
    "POINT"
    spatial_reference=arcpy.SpatialReference(2180) #Ustawienie ukłądu współrzędnych
  )

#Definiowanie pól atrybutów dla warstwy punktowej
fields = [
("tripId", "LONG") #Identyfikator kursu
("kierunek_przejazdu", "TEXT") #Kierunek przejazdu
("opoznienie_przejazdu", "LONG") #Opóźnienie na trasie
("numer_linii", "TEXT") #Numer linii autobusowej
("opoznienie_dla_przystanku", "LONG") #Suma opóźnienia dla danej trasy
("rozpoczecie_kursu", "TEXT") #Czas rozpoczęcia kursu
("moment_zebrania_danych", "TEXT") #Czas zebrania danych GPS
]

#Sprawdzenie czy pola już istnieją, jeśli nie to dodanie ich do warstwy
existings_fields = [f.name for f in arcpy.ListFields(output_shapefile)]
for field name, field_type in fields:
  if field_name not in existing_fields:
    arcpy.AddField_managment(output_shapefile, field_name, field_type)

#Wczytywanie danych o autobusach z pliku JSON
bus_data = read_bus_data(input_json_file)

#Definiowanie układów współrzędnych: źródłowego(WGS84) i doceloweg(CS92)
spatial_ref_wgs84 = arcpy.SpatialReference(4326)
spatial_ref_cs92 = arcpy.SpatialReference(2180)

#Słownik do sumowania dla poszczególnych linii autobusowych
route_delays = {}


#Obliczanie sumy opóźnień dla każdej linii
for vehicle in bus_data:
    numer_linii = vehicle.get("routeShortName", "")
    opoznienie_przejazdu = vehicle.get("delay", 0)
    if numer_linii not in route_delays:
        route_delays[numer_linii] = 0
    route_delays[numer_linii] += opoznienie_przejazdu


#Wstawianie danych do warstwy shapefile
with arcpy.da.InsertCursor(output_shapefile, ["SHAPE@", "tripId", "kierunek_przejazdu", "opoznienie_przejazdu", "numer_linii", "opoznienie_dla_przystanku", "rozpoczecie_kursu", "moment_zebrania_danych"]) as cursor:
    for vehicle in bus_data:
        lat = vehicle.get("lat")
        lon = vehicle.get("lon")
        trip_id = vehicle.get("tripId", 0)
        kierunek_przejazdu = vehicle.get("headsign", "")
        opoznienie_przejazdu = vehicle.get("delay", 0)  #Opóźnienie dla pojazdu
        numer_linii = vehicle.get("routeShortName", "")
        rozpoczecie_kursu = vehicle.get("scheduledTripStartTime", "")  #Czas rozpoczęcia kursu
        
        #Czas kiedy dane gps zostaly pobrane
        moment_zebrania_danych = vehicle.get("generated", "") 
      

        #Pobranie sumy opóźnień dla danej linii
        opoznienie = route_delays.get(numer_linii, None)

        #Sprawdzenie czy współrzędne są dostępne
        if lat is not None and lon is not None:
            # Tworzenie punktu w układzie WGS84
            point_wgs84 = arcpy.PointGeometry(arcpy.Point(lon, lat), spatial_ref_wgs84)
            #przekształcenie współrzędnych do układu CS92
            point_cs92 = point_wgs84.projectAs(spatial_ref_cs92)

            #Debugowanie - wypisanie informacji o dodawanych punktach
            print(f'Punkt: {point_cs92}, TripId: {trip_id}, Opóźnienie przejazdu: {opoznienie_przejazdu}, Kierunek przejazdu: {kierunek_przejazdu}, Numer linii: {numer_linii}, Opóźnienie dla trasy: {opoznienie}, Rozpoczęcie kursu: {rozpoczecie_kursu}, Moment zebrania danych: {moment_zebrania_danych}')

            #Dodanie rekordu do warstwy
            cursor.insertRow([point_cs92, trip_id, kierunek_przejazdu, opoznienie_przejazdu, numer_linii, opoznienie, rozpoczecie_kursu, moment_zebrania_danych])

print("Punkty autobusowe zostały dodane do warstwy mapy wraz z pełnymi atrybutami.")
  
