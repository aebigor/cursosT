"""
Script para REGISTRAR PERSONAS y sus certificados en la base de datos.

CÓMO USARLO
-----------
1. Crea una carpeta para la persona dentro de static/certificados/ con el
   nombre  <tipo_documento>-<numero_documento>, ejemplo:

       static/certificados/CC-123456789/

2. Copia ahí los 3 PDF que te entregue el Ministerio (constancia 1,
   constancia 2 y la constancia de formación en empresa).

3. Agrega un diccionario a la lista PERSONAS más abajo con sus datos y el
   nombre exacto de cada archivo PDF.

4. Corre:   python seed_data.py

   Se puede correr las veces que quieras: si la cédula ya existe, actualiza
   el nombre y reemplaza los certificados por los nuevos.
"""
from pathlib import Path

from database import init_db, agregar_persona

CERTIFICADOS_DIR = Path(__file__).parent / "static" / "certificados"

# ---------------------------------------------------------------------------
# 👇👇👇  AGREGA / EDITA AQUÍ LAS PERSONAS  👇👇👇
#
#   tipo_documento     -> CC, CE, TI, PA o PEP (debe coincidir con el <select>)
#   numero_documento   -> solo números, sin puntos ni espacios
#   nombre_completo    -> nombre tal como debe verse en el resultado
#   archivos           -> nombre EXACTO de cada PDF ya copiado en
#                          static/certificados/<tipo>-<numero>/
# ---------------------------------------------------------------------------
PERSONAS = [
    {
        "tipo_documento": "CC",
        "numero_documento": "123456789",
        "nombre_completo": "Juan Pérez Gómez",
        "archivos": {
            "constancia_1": "constancia1.pdf",
            "constancia_2": "constancia2.pdf",
            "formacion_empresa": "constancia_formacion_empresa.pdf",
        },
    },
    # Copia y pega este bloque para agregar otra persona:
    # {
    #     "tipo_documento": "CC",
    #     "numero_documento": "987654321",
    #     "nombre_completo": "María Fernanda López",
    #     "archivos": {
    #         "constancia_1": "constancia1.pdf",
    #         "constancia_2": "constancia2.pdf",
    #         "formacion_empresa": "constancia_formacion_empresa.pdf",
    #     },
    # },
]

# Etiquetas que se muestran en pantalla para cada tipo de archivo
# (coinciden con lo que pide el diseño: dos "CONSTANCIAS" + una de formación).
ETIQUETAS = {
    "constancia_1": "CONSTANCIAS",
    "constancia_2": "CONSTANCIAS",
    "formacion_empresa": "CONSTANCIAS FORMACION EN EMPRESA",
}


def main():
    init_db()

    for p in PERSONAS:
        carpeta = f'{p["tipo_documento"]}-{p["numero_documento"]}'
        ruta_carpeta = CERTIFICADOS_DIR / carpeta

        certificados = []
        for clave, nombre_archivo in p["archivos"].items():
            ruta_pdf = ruta_carpeta / nombre_archivo
            if not ruta_pdf.exists():
                print(f"  ⚠  No existe el archivo: {ruta_pdf}  (revisa que lo copiaste)")
                continue
            certificados.append(
                {
                    "etiqueta": ETIQUETAS.get(clave, clave.upper()),
                    "archivo": f"{carpeta}/{nombre_archivo}",
                }
            )

        if not certificados:
            print(f'✗ {p["nombre_completo"]} ({p["numero_documento"]}): sin certificados, no se registró.')
            continue

        agregar_persona(
            p["tipo_documento"],
            p["numero_documento"],
            p["nombre_completo"],
            certificados,
        )
        print(
            f'✓ {p["nombre_completo"]} ({p["tipo_documento"]} {p["numero_documento"]}) '
            f"registrado con {len(certificados)} certificado(s)."
        )


if __name__ == "__main__":
    main()
