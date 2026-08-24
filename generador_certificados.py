"""Generador de certificados PDF configurables por persona."""

from pathlib import Path
from html import escape
from copy import deepcopy

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BASE_DIR = Path(__file__).parent
CERTIFICADOS_DIR = BASE_DIR / "static" / "certificados"

# Valores predeterminados de los certificados que ya existían.
# Estos son opcionales: cualquier curso nuevo puede crearse sin agregarlo aquí.
CERTIFICADOS = {
    "1": {
        "etiqueta": "CURSO EN ESPACIOS CONFINADOS",
        "programa": "Curso en Espacios Confinados",
        "nivel": "ENTRANTE EN ESPACIOS CONFINADOS",
        "organizacion": "RIESGO CERO-TRABAJOS DE ALTO RIESGO",
        "sede": "RIESGO CERO SEDE PRINCIPAL",
        "categoria": "constancia",
    },
    "2": {
        "etiqueta": "PRIMEROS AUXILIOS",
        "programa": "Curso de Primeros Auxilios",
        "nivel": "BÁSICO",
        "organizacion": "AGERIS S.A.S.",
        "sede": "AGERIS SEDE PRINCIPAL",
        "categoria": "constancia",
    },
    "3": {
        "etiqueta": "SEGURIDAD Y SALUD EN EL TRABAJO",
        "programa": "Curso de Seguridad y Salud en el Trabajo",
        "nivel": "BÁSICO",
        "organizacion": "CENTROS DE FORMACIÓN EN EMPRESA",
        "sede": "SEDE DE FORMACIÓN PRINCIPAL",
        "categoria": "formacion_empresa",
    },
}

ALIASES_CERTIFICADOS = {
    "espacios_confinados": "1",
    "primeros_auxilios": "2",
    "seguridad_salud_trabajo": "3",
    "seguridad_y_salud_en_el_trabajo": "3",
}


def _texto_seguro(valor):
    return escape(str(valor or ""))


def _normalizar_certificado(certificado, indice):
    """Acepta certificados existentes y también cursos completamente nuevos."""
    if isinstance(certificado, str):
        original = certificado.strip()
        clave = ALIASES_CERTIFICADOS.get(original.lower(), original.lower())
        if clave in CERTIFICADOS:
            datos = deepcopy(CERTIFICADOS[clave])
            datos["tipo"] = clave
        else:
            # Un texto desconocido también es válido: se convierte en un programa nuevo.
            datos = {
                "tipo": clave or f"personalizado_{indice}",
                "programa": original,
                "etiqueta": original.upper(),
                "nivel": "",
                "organizacion": "",
                "sede": "",
                "categoria": "constancia",
            }
    elif isinstance(certificado, dict):
        datos = {}
        tipo_original = str(certificado.get("tipo", "")).strip().lower()
        clave = ALIASES_CERTIFICADOS.get(tipo_original, tipo_original)

        if clave in CERTIFICADOS:
            datos.update(deepcopy(CERTIFICADOS[clave]))
        else:
            datos.update({
                "tipo": clave or f"personalizado_{indice}",
                "programa": "",
                "etiqueta": "",
                "nivel": "",
                "organizacion": "",
                "sede": "",
                "categoria": "constancia",
            })

        datos.update({k: v for k, v in certificado.items() if v is not None})
        datos["tipo"] = clave or f"personalizado_{indice}"
    else:
        raise ValueError(f"Configuración de certificado inválida en posición {indice}.")

    # Compatibilidad con la versión anterior: titulo/empresa -> programa/organizacion.
    if not datos.get("programa"):
        datos["programa"] = datos.get("titulo", "")
    if not datos.get("organizacion"):
        datos["organizacion"] = datos.get("empresa", "")

    datos["programa"] = str(datos.get("programa") or "Programa de formación")
    datos["titulo"] = datos["programa"]
    datos["etiqueta"] = str(datos.get("etiqueta") or datos["programa"]).upper()
    datos["nivel"] = str(datos.get("nivel") or "")
    datos["organizacion"] = str(datos.get("organizacion") or "")
    datos["sede"] = str(datos.get("sede") or "")
    datos["fecha_inicio"] = str(datos.get("fecha_inicio") or "")
    datos["fecha_fin"] = str(datos.get("fecha_fin") or "")
    datos["categoria"] = str(datos.get("categoria") or "constancia")
    datos["archivo"] = str(datos.get("archivo") or f"constancia_{indice}.pdf")
    return datos


def generar_certificado(
    nombre_completo,
    tipo_documento,
    numero_documento,
    nombre_archivo,
    programa,
    nivel="",
    organizacion="",
    sede="",
    fecha_inicio="",
    fecha_fin="",
):
    """Genera un PDF usando exclusivamente los datos configurados."""
    carpeta_persona = CERTIFICADOS_DIR / f"{tipo_documento}-{numero_documento}"
    carpeta_persona.mkdir(parents=True, exist_ok=True)
    ruta_pdf = carpeta_persona / nombre_archivo

    documento = SimpleDocTemplate(
        str(ruta_pdf), pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()
    estilo_encabezado = ParagraphStyle("Encabezado", parent=estilos["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#1B4D72"), spaceAfter=5)
    estilo_titulo = ParagraphStyle("Titulo", parent=estilos["Title"], fontName="Helvetica-Bold", fontSize=28, leading=34, alignment=TA_CENTER, textColor=colors.HexColor("#1B4D72"), spaceAfter=15)
    estilo_subtitulo = ParagraphStyle("Subtitulo", parent=estilos["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=12)
    estilo_normal = ParagraphStyle("NormalCertificado", parent=estilos["Normal"], fontName="Helvetica", fontSize=12, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=10)
    estilo_nombre = ParagraphStyle("Nombre", parent=estilos["Normal"], fontName="Helvetica-Bold", fontSize=23, leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#111111"), spaceBefore=10, spaceAfter=10)
    estilo_curso = ParagraphStyle("Curso", parent=estilos["Normal"], fontName="Helvetica-Bold", fontSize=17, leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#1B4D72"), spaceBefore=10, spaceAfter=10)
    estilo_fecha = ParagraphStyle("Fecha", parent=estilos["Normal"], fontName="Helvetica", fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=5)
    estilo_datos = ParagraphStyle("Datos", parent=estilos["Normal"], fontName="Helvetica", fontSize=11, leading=17, alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=5)

    elementos = [
        Paragraph("CENTROS DE FORMACIÓN EN EMPRESA", estilo_encabezado),
        Paragraph("CERTIFICACIÓN DE FORMACIÓN", estilo_encabezado),
        Spacer(1, 0.7 * cm),
        Paragraph("CERTIFICADO", estilo_titulo),
        Paragraph("Se certifica que", estilo_subtitulo),
        Spacer(1, 0.3 * cm),
        Paragraph(_texto_seguro(nombre_completo).upper(), estilo_nombre),
        Paragraph(f"Identificado(a) con <b>{_texto_seguro(tipo_documento)}</b> No. <b>{_texto_seguro(numero_documento)}</b>", estilo_normal),
        Spacer(1, 0.5 * cm),
        Paragraph("Ha realizado satisfactoriamente el", estilo_normal),
        Paragraph(_texto_seguro(programa).upper(), estilo_curso),
    ]

    if nivel:
        elementos.append(Paragraph(f"NIVEL: <b>{_texto_seguro(nivel).upper()}</b>", estilo_datos))
    if organizacion:
        elementos.append(Paragraph(f"NOMBRE DE LA ORGANIZACIÓN: <b>{_texto_seguro(organizacion).upper()}</b>", estilo_datos))
    if sede:
        elementos.append(Paragraph(f"NOMBRE DE LA SEDE: <b>{_texto_seguro(sede).upper()}</b>", estilo_datos))
    if fecha_inicio or fecha_fin:
        elementos.append(Paragraph(f"PERÍODO DE FORMACIÓN: <b>{_texto_seguro(fecha_inicio) or '-'} a {_texto_seguro(fecha_fin) or '-'}</b>", estilo_datos))

    elementos.extend([
        Spacer(1, 0.7 * cm),
        Paragraph("La presente constancia se expide para los fines que estime convenientes.", estilo_normal),
        Spacer(1, 0.7 * cm),
    ])

    firmas = Table(
        [["____________________________", "____________________________"], ["Firma responsable", "Firma responsable"]],
        colWidths=[7 * cm, 7 * cm],
    )
    firmas.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elementos.append(firmas)
    elementos.append(Spacer(1, 0.8 * cm))
    elementos.append(Paragraph("Documento generado automáticamente por el sistema de Centros de Formación en Empresa.", estilo_fecha))

    documento.build(elementos, onFirstPage=decorar_pagina)
    return ruta_pdf


def decorar_pagina(canvas, documento):
    ancho, alto = A4
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#1B4D72"))
    canvas.setLineWidth(3)
    canvas.rect(1 * cm, 1 * cm, ancho - 2 * cm, alto - 2 * cm)
    canvas.setStrokeColor(colors.HexColor("#7FA9C5"))
    canvas.setLineWidth(1)
    canvas.rect(1.3 * cm, 1.3 * cm, ancho - 2.6 * cm, alto - 2.6 * cm)
    canvas.restoreState()


def generar_certificados_persona(nombre_completo, tipo_documento, numero_documento, certificados_seleccionados=None):
    """Genera 1..N certificados. Los cursos nuevos no requieren catálogo previo."""
    if certificados_seleccionados is None:
        raise ValueError(f"No se indicaron certificados para {nombre_completo}")
    if isinstance(certificados_seleccionados, (str, dict)):
        certificados_seleccionados = [certificados_seleccionados]
    certificados_seleccionados = list(certificados_seleccionados)
    if not certificados_seleccionados:
        raise ValueError(f"{nombre_completo} no tiene certificados seleccionados.")

    resultados = []
    for indice, item in enumerate(certificados_seleccionados, start=1):
        certificado = _normalizar_certificado(item, indice)
        # Cada certificado tiene su propio archivo. Así se pueden agregar cursos nuevos
        # sin depender de que exista una clave en CERTIFICADOS.
        certificado["archivo"] = f"constancia_{indice}.pdf"

        generar_certificado(
            nombre_completo=nombre_completo,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            nombre_archivo=certificado["archivo"],
            programa=certificado["programa"],
            nivel=certificado["nivel"],
            organizacion=certificado["organizacion"],
            sede=certificado["sede"],
            fecha_inicio=certificado["fecha_inicio"],
            fecha_fin=certificado["fecha_fin"],
        )

        resultados.append({
            "tipo": certificado["tipo"],
            "etiqueta": certificado["etiqueta"],
            "archivo": f"{tipo_documento}-{numero_documento}/{certificado['archivo']}",
            "programa": certificado["programa"],
            "titulo": certificado["programa"],
            "nivel": certificado["nivel"],
            "numero_documento": numero_documento,
            "fecha_inicio": certificado["fecha_inicio"],
            "fecha_fin": certificado["fecha_fin"],
            "organizacion": certificado["organizacion"],
            "sede": certificado["sede"],
            "categoria": certificado["categoria"],
            # Compatibilidad con versiones anteriores.
            "empresa": certificado["organizacion"],
            "hora_inicio": certificado["fecha_inicio"],
            "hora_fin": certificado["fecha_fin"],
        })

    return resultados
