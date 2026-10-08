# TOWELL SEGUNDAS

Proyecto **Towell Quality Intelligence | Segundas**: consulta y análisis del histórico de producción y segundas de Towell.

## Contenido del repositorio

- `towell-quality/`: proyecto de la aplicación, componentes, scripts, configuración y documentación.
- `towell-quality/dist/`: sitio estático con sus datos históricos, estilos, imágenes y motor de cálculo.
- `towell-quality/updates/`: estado de referencia del seguimiento de informes AX.
- `audit-xlsx.json` y `historical-audit.json`: resultados de auditoría y conciliación.
- Scripts Python y `admin-function.txt`: herramientas de extracción, revisión y ajustes.
- `escala-tiempo-publicada.png`: captura de referencia.
- `towell-quality.tar.gz`: copia empaquetada existente del proyecto.
- `project-documentation.md`: documentación de la etapa inicial. Para la clasificación actual, consultar [la documentación del proyecto](towell-quality/README.md).

Se conserva la estructura de la carpeta original. Los metadatos internos de Git, las cachés de Python y el estado temporal de ejecución de Sites no forman parte de la transferencia.

## Histórico y reglas de cálculo

El histórico inicial procede de **Segundas 2026.xlsx**, del 2 de enero al 30 de septiembre de 2026, con 157,874 registros incorporados:

| Fuente | Registros |
| --- | ---: |
| SEGUNDAS | 36,965 |
| COSTURA | 25,201 |
| MAQUILA | 3,631 |
| Segundas Crudo | 92,077 |

La hoja Tipo de Segundas Costura es un espejo de SEGUNDAS y no se suma nuevamente.

La producción se calcula como **COSTURA.Cantidad + MAQUILA.InventQty**. Incluye la localidad 2DAS3RAS y no suma Consumo. Septiembre contiene 1,000,316 de producción y 26,686 segundas, con una tasa de 2.667756988791542%.

Enero a agosto se reconstruyen con la misma regla. Los registros conservan su trazabilidad; no se eliminan observaciones únicamente por tener atributos iguales. Crudo conserva su cantidad original, incluida la parte decimal, y se analiza por separado.

La documentación actual del proyecto describe un catálogo de **36 defectos** asignados a sus departamentos.

## Consultar el sitio estático

Desde la raíz del repositorio, con Python 3 instalado:

```sh
python -m http.server 8000 --directory towell-quality/dist
```

Abrir `http://localhost:8000` en el navegador.

La superficie estática de esta etapa está en `towell-quality/dist/`. El starter React/Next/Vinext se conserva para evolución futura y dispone de sus propios scripts en `towell-quality/package.json`.

## Validar los datos

Con Node.js instalado:

```sh
cd towell-quality
node check-history.mjs
node update-classification-audit.mjs
```

La comprobación histórica revisa cantidades, porcentajes, agrupaciones, filtros, clasificación y separación de Crudo. El segundo script actualiza la auditoría de clasificación.

## Documentación adicional

- [Documentación actual del proyecto](towell-quality/README.md)
- [Seguimiento de informes AX](towell-quality/UPDATE-AX.md)
- [Documentación de la etapa inicial](project-documentation.md)

La configuración de Sites identifica la publicación original como privada para su propietario. El acceso a este repositorio se gestiona por separado en GitHub.
