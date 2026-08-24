"""Capa SQLite para personas y sus certificados configurables."""

import sqlite3
from pathlib import Path
from generador_certificados import generar_certificados_persona

DB_PATH = Path(__file__).parent / "centros_formacion.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_documento TEXT NOT NULL,
            numero_documento TEXT NOT NULL,
            nombre_completo TEXT NOT NULL,
            UNIQUE(tipo_documento, numero_documento)
        );

        CREATE TABLE IF NOT EXISTS certificados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER NOT NULL,
            etiqueta TEXT NOT NULL,
            archivo TEXT NOT NULL,
            programa TEXT,
            nivel TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            organizacion TEXT,
            sede TEXT,
            categoria TEXT DEFAULT 'constancia',
            orden INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(persona_id) REFERENCES personas(id) ON DELETE CASCADE
        );
    """)

    # Migración automática de instalaciones anteriores.
    columnas = {row["name"] for row in conn.execute("PRAGMA table_info(certificados)").fetchall()}
    migraciones = {
        "programa": "ALTER TABLE certificados ADD COLUMN programa TEXT",
        "nivel": "ALTER TABLE certificados ADD COLUMN nivel TEXT",
        "fecha_inicio": "ALTER TABLE certificados ADD COLUMN fecha_inicio TEXT",
        "fecha_fin": "ALTER TABLE certificados ADD COLUMN fecha_fin TEXT",
        "organizacion": "ALTER TABLE certificados ADD COLUMN organizacion TEXT",
        "sede": "ALTER TABLE certificados ADD COLUMN sede TEXT",
        "categoria": "ALTER TABLE certificados ADD COLUMN categoria TEXT DEFAULT 'constancia'",
        # Compatibilidad con la base anterior.
        "titulo": "ALTER TABLE certificados ADD COLUMN titulo TEXT",
        "empresa": "ALTER TABLE certificados ADD COLUMN empresa TEXT",
        "hora_inicio": "ALTER TABLE certificados ADD COLUMN hora_inicio TEXT",
        "hora_fin": "ALTER TABLE certificados ADD COLUMN hora_fin TEXT",
        "horas": "ALTER TABLE certificados ADD COLUMN horas INTEGER",
    }
    for columna, sql in migraciones.items():
        if columna not in columnas:
            conn.execute(sql)

    # Si existían datos de la versión anterior, copiarlos a los nuevos campos.
    conn.execute("""
        UPDATE certificados
        SET programa = COALESCE(NULLIF(programa, ''), titulo),
            organizacion = COALESCE(NULLIF(organizacion, ''), empresa),
            fecha_inicio = COALESCE(NULLIF(fecha_inicio, ''), hora_inicio),
            fecha_fin = COALESCE(NULLIF(fecha_fin, ''), hora_fin)
        WHERE programa IS NULL OR programa = ''
           OR organizacion IS NULL OR organizacion = ''
           OR fecha_inicio IS NULL OR fecha_inicio = ''
           OR fecha_fin IS NULL OR fecha_fin = ''
    """)
    conn.commit()
    conn.close()


def buscar_persona(tipo_documento: str, numero_documento: str):
    conn = get_connection()
    persona = conn.execute(
        "SELECT * FROM personas WHERE tipo_documento = ? AND numero_documento = ?",
        (tipo_documento, numero_documento),
    ).fetchone()

    if not persona:
        conn.close()
        print(f"⚠ No se encontró la persona: {tipo_documento}-{numero_documento}")
        return None

    certificados = conn.execute(
        """
        SELECT *,
               COALESCE(programa, titulo, etiqueta) AS programa,
               COALESCE(organizacion, empresa, '') AS organizacion,
               COALESCE(fecha_inicio, hora_inicio, '') AS fecha_inicio,
               COALESCE(fecha_fin, hora_fin, '') AS fecha_fin,
               COALESCE(categoria, 'constancia') AS categoria
        FROM certificados
        WHERE persona_id = ?
        ORDER BY orden ASC, id ASC
        """,
        (persona["id"],),
    ).fetchall()

    resultado = {
        "persona": dict(persona),
        "certificados": [dict(certificado) for certificado in certificados],
    }

    print(f"✓ Consulta: {persona['nombre_completo']}")
    print(f"✓ Certificados encontrados: {len(resultado['certificados'])}")
    for certificado in resultado["certificados"]:
        print(f"   → {certificado['programa']} | {certificado['archivo']}")

    conn.close()
    return resultado


def sembrar_personas(personas: list):
    for p in personas:
        tipo_documento = p["tipo_documento"]
        numero_documento = p["numero_documento"]
        nombre_completo = p["nombre_completo"]
        certificados_seleccionados = p.get("certificados", [])

        print(f"Procesando persona: {nombre_completo} ({tipo_documento}-{numero_documento})")
        print(f"→ Certificados configurados: {len(certificados_seleccionados)}")

        certificados = []
        if certificados_seleccionados:
            certificados = generar_certificados_persona(
                nombre_completo=nombre_completo,
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                certificados_seleccionados=certificados_seleccionados,
            )

        agregar_persona(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            nombre_completo=nombre_completo,
            certificados=certificados,
        )

        print(f"✓ Persona registrada correctamente: {nombre_completo}")
        print(f"✓ Certificados generados: {len(certificados)}")
        for certificado in certificados:
            print(f"   → {certificado['programa']}")


def agregar_persona(tipo_documento: str, numero_documento: str, nombre_completo: str, certificados: list):
    conn = get_connection()
    cur = conn.cursor()

    existente = cur.execute(
        "SELECT id FROM personas WHERE tipo_documento = ? AND numero_documento = ?",
        (tipo_documento, numero_documento),
    ).fetchone()

    if existente:
        persona_id = existente["id"]
        cur.execute("UPDATE personas SET nombre_completo = ? WHERE id = ?", (nombre_completo, persona_id))
        cur.execute("DELETE FROM certificados WHERE persona_id = ?", (persona_id,))
    else:
        cur.execute(
            "INSERT INTO personas (tipo_documento, numero_documento, nombre_completo) VALUES (?, ?, ?)",
            (tipo_documento, numero_documento, nombre_completo),
        )
        persona_id = cur.lastrowid

    for i, cert in enumerate(certificados):
        cur.execute(
            """
            INSERT INTO certificados (
                persona_id, etiqueta, archivo, programa, nivel,
                fecha_inicio, fecha_fin, organizacion, sede, categoria, orden,
                titulo, empresa, hora_inicio, hora_fin
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                persona_id,
                cert.get("etiqueta", cert.get("programa", "").upper()),
                cert["archivo"],
                cert.get("programa", cert.get("titulo", "")),
                cert.get("nivel", ""),
                cert.get("fecha_inicio", ""),
                cert.get("fecha_fin", ""),
                cert.get("organizacion", cert.get("empresa", "")),
                cert.get("sede", ""),
                cert.get("categoria", "constancia"),
                i,
                cert.get("programa", cert.get("titulo", "")),
                cert.get("organizacion", cert.get("empresa", "")),
                cert.get("fecha_inicio", ""),
                cert.get("fecha_fin", ""),
            ),
        )

    conn.commit()
    conn.close()
    return persona_id
