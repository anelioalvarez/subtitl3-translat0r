# subtitl3-translat0r

**(Posteriormente documentar el uso de forma mas prolija)**

En resúmen es un *traductor de subtítulos de Ingles a Español*.

- `translate_subtitle.py <subtitle.srt>`: traduce el archivo de subtítulo `subtitle.srt` al español generando otro archivo con el mismo nombre + _es.srt
- `translate_subs.sh <directory>`: traduce los archivos de subtítulo (.srt) que se encuentran dentro de `directory` y sus subdirectorios, usando el script `translate_subtitle.py`
- para la traducción se usa la api de Google Translator (paquete `deep-translator`)
- durante el proceso se muestra por consola el porcentaje de avance de líneas traducidas (paquete `tqdm`)
