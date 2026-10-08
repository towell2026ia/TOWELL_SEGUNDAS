# Towell Quality Intelligence | Segundas

Primera etapa: Site privado de consulta basado exclusivamente en Segundas 2026.xlsx, del 2 de enero al 30 de septiembre de 2026. Los HTML no se incorporaron.

La superficie publicada está en dist/ y se declara en .openai/hosting.json. Esta etapa utiliza archivos históricos inmutables, versionados junto con el Site. No emplea almacenamiento del navegador como base de datos. El starter queda disponible para la futura etapa de ingesta con almacenamiento persistente y permisos; no participa en esta publicación estática.

## Fuente y conciliación

157,874 filas: 36,965 de SEGUNDAS, 25,201 de COSTURA, 3,631 de MAQUILA y 92,077 de Segundas Crudo. La hoja Tipo de Segundas Costura es un espejo exacto de SEGUNDAS y no se incorpora otra vez.

Producción histórica = COSTURA.Cantidad + MAQUILA.InventQty. Incluye localidad 2DAS3RAS, como el libro. No suma Consumo. Septiembre: 1,000,316 de producción y 26,686 segundas; tasa exacta 2.667756988791542%. Las agrupaciones fecha/modelo/tamaño/color coinciden con %Segundas!A:G. Los controles son %Segundas!AG8:AG10.

Enero–agosto se reconstruyen con la misma regla y se identifican como tales. Los registros iguales no se eliminan por coincidencia de atributos: carecen de evidencia suficiente para distinguir duplicado erróneo de observación legítima. Cada registro conserva hoja, fila y huella del archivo fuente, disponible en Cargas.

El catálogo sólo asigna los siete defectos expresamente definidos por el usuario. El resto permanece SIN CLASIFICAR. Crudo conserva la cantidad original, incluida su parte decimal, sin declarar piezas ni aplicar el denominador de producción terminada.

## Validación

node check-history.mjs contrasta cantidades, porcentajes, grupos de dimensiones, filtros, denominador cero, clasificación y separación de Crudo. La vista previa valida filtros en cascada, cambio entre procesos, Crudo, conciliación y herramientas de consulta asistida. Los gráficos, tablas, detalle y alertas comparten la selección.

No hay cargas, edición del histórico, programación de actualizaciones ni perfiles de administración en esta etapa. La publicación utiliza acceso privado del propietario. Para iniciar una nueva etapa de ingesta se debe preservar este histórico y migrar a D1/R2 con autorización en el servidor.
