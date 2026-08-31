"""Configuración de personas y sus certificados.

Cada certificado puede ser completamente diferente. No es necesario registrarlo
antes en ningún catálogo: basta con escribir los datos aquí.

Campos editables por certificado:
- programa
- nivel
- fecha_inicio
- fecha_fin
- organizacion
- sede

El número de documento se configura en la persona porque identifica al usuario.
"""

PERSONAS = [
    {
        "tipo_documento": "CC",
        "numero_documento": "1121835789",
        "nombre_completo": "JULIAN ALBERTO GUZMAN MORENO",
        "certificados": [
            {
                "tipo": "primeros_auxilios",
                "programa": "ESPACIOS CONFINADOS",
                "nivel": "BÁSICO",
                "fecha_inicio": "12/07/2025",
                "fecha_fin": "15/07/2025",
                "organizacion": "AGERIS S.A.S.",
                "sede": "AGERIS SEDE PRINCIPAL",
            },
            {
                "tipo": "seguridad_salud_trabajo",
                "programa": "SEGURIDAD Y SALUD EN EL TRABAJO",
                "nivel": "BÁSICO",
                "fecha_inicio": "20/07/2025",
                "fecha_fin": "25/07/2025",
                "organizacion": "CENTROS DE FORMACIÓN EN EMPRESA",
                "sede": "SEDE DE FORMACIÓN PRINCIPAL",
                "categoria": "formacion_empresa",
            },
            {
                # Ejemplo de curso completamente nuevo: NO existe en el catálogo.
                "tipo": "TRABAJO_EN_ALTURAS",
                "programa": "TRABAJO EN ALTURAS",
                "nivel": "REENTRENAMIENTO SECTORIAL 4272",
                "fecha_inicio": "23/04/2026",
                "fecha_fin": "23/04/2026",
                "organizacion": "CERTITAR",
                "sede": "CERTITAR S.A.S.",
            },
        ],
    },

    {
        "tipo_documento": "CC",
        "numero_documento": "987654321",
        "nombre_completo": "María Fernanda López",
        "certificados": [
            {
                "tipo": "espacios_confinados",
                "programa": "Curso en Espacios Confinados",
                "nivel": "ENTRANTE EN ESPACIOS CONFINADOS",
                "fecha_inicio": "10/08/2025",
                "fecha_fin": "12/08/2025",
                "organizacion": "RIESGO CERO-TRABAJOS DE ALTO RIESGO",
                "sede": "RIESGO CERO SEDE PRINCIPAL",
            },
        ],
    },
]
