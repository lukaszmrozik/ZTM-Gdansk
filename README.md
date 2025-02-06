# 🚍 **Analiza przystanków o największym opóźnieniu w Gdańsku**  

Projekt przetwarzania danych autobusowych przy użyciu skryptu Python oraz środowiska ArcGIS. Celem projektu jest wizualizacja danych GPS autobusów miejskich i przypisanie atrybutów takich jak opóźnienie, numer linii czy moment zbierania danych na mapie w układzie CS92 (EPSG:2180).  

---

## 🎯 **Funkcjonalności**  
- Wczytywanie danych GPS autobusów z pliku JSON  
- Transformacja współrzędnych z WGS84 (EPSG:4326) na CS92 (EPSG:2180)  
- Tworzenie punktowej warstwy mapy z pełnymi atrybutami pojazdów  
- Obliczanie sumarycznego opóźnienia dla tras autobusowych  
- Dodawanie danych do shapefile’a w ArcGIS  

---

## 🛠️ **Wykorzystane technologie**  
- **Język programowania:** Python  
- **Biblioteki GIS:** ArcPy  
- **Format danych wejściowych:** JSON  
- **Oprogramowanie GIS:** ArcGIS  

---

## **Instrukcja uruchomienia projektu**  

### 1. **Skonfiguruj środowisko pracy**
- Upewnij się, że masz zainstalowany ArcGIS Pro z aktywną biblioteką `ArcPy`.

### 2. **Przygotuj dane wejściowe**  
- Umieść plik `bus_data.json` w odpowiednim katalogu.  

### 3. **Skonfiguruj ścieżki w kodzie**  
Zaktualizuj ścieżki do danych wejściowych i wynikowych w skrypcie:  
```python
arcpy.env.workspace = r"C:\ścieżka_do_gdb"
input_json_file = r"C:\ścieżka_do_danych\bus_data.json"
output_shapefile = r"C:\ścieżka_do_wyniku\bus_output"
