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


  
