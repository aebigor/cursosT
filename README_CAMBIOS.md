# Configuración de certificados

Ahora cada persona puede tener cualquier cantidad de certificados y cada certificado puede tener datos completamente distintos.

## Campos editables

En `personas_data.py`:

- `tipo_documento`
- `numero_documento`
- `nombre_completo`
- En cada certificado:
  - `programa`
  - `nivel`
  - `fecha_inicio`
  - `fecha_fin`
  - `organizacion`
  - `sede`

## Curso nuevo sin catálogo

No es necesario modificar `generador_certificados.py` para agregar un curso nuevo. Por ejemplo:

```python
{
    "tipo": "curso_belleza_de_feos",
    "programa": "Curso de Belleza de Feos",
    "nivel": "BÁSICO",
    "fecha_inicio": "01/09/2025",
    "fecha_fin": "05/09/2025",
    "organizacion": "MI ORGANIZACIÓN",
    "sede": "SEDE PRINCIPAL",
}
```

También se puede omitir `tipo` y usar solamente los datos del certificado; el sistema le asigna un identificador automáticamente.

## Cantidad de certificados

Puedes dejar uno:

```python
"certificados": [
    {...}
]
```

O agregar los que necesites:

```python
"certificados": [
    {...},
    {...},
    {...},
    {...},
]
```

Cada certificado genera su propio PDF y aparece en la consulta con los datos configurados.

## Ejecución

```powershell
python app.py
```

La base de datos se migra automáticamente si proviene de una versión anterior.
