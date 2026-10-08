# Actualización automática desde OneDrive

Site: appgprj_6ac539ef3ed081919bf0a98c6c00968f

URL estable: https://towell-quality-segundas.towel-sa-de-0832.chatgpt.site

Origen local autorizado: C:\Users\gcalidad\OneDrive - Towell\Documentos\AX

La automatización local de este chat revisa cada hora los HTML nuevos o modificados. Necesita este equipo encendido, Codex disponible y OneDrive sincronizado. No hay un disparador de nube ni una carga pública desde el Site. Los cuatro archivos presentes al activar el seguimiento son la línea base del monitor; no se incorporaron al histórico inicial.

## Secuencia de cada ejecución

1. En el checkout ejecutar `ax_updates.py scan` con el Python incluido en el runtime de Codex. Si `changed` está vacío, terminar en silencio sin publicar. No modificar las fuentes.
2. Abrir el mismo Site con Sites y sincronizar su repositorio mediante el workflow antes de editar. Mantener project_id y URL. La audiencia solicitada es pública; nunca añadir otros editores ni publicar claves.
3. Si `updates/pending.json` tiene cargas no reconocidas aún en `updates/state.json`, recuperar esa publicación antes de importar más. Revisar backup y verificar consistencia. No importar de nuevo una carga pendiente.
4. Ejecutar `ax_updates.py plan`. Los encabezados identifican el tipo; el nombre no manda. AX vacío sin columnas identificadoras queda AX_SIN_MOVIMIENTOS, VALIDADO – SIN MOVIMIENTOS, cero registros nuevos. No crear ceros ni borrar históricos.
5. Estructura desconocida, cantidad ambigua, reverso negativo o movimiento novedoso dentro de un periodo validado: detener esa incorporación y notificar con evidencia. Para adaptar el lector a una nueva estructura, auditar primero el archivo real y contrastar las columnas con las hojas del Excel. Nunca adivinar un denominador, departamento o identificador. Mantener InventQty y BomQty separados; Maquila usa InventQty del origen A-RECEPMAQ, como la interpretación histórica validada. Crudo sigue independiente.
6. Ejecutar `ax_updates.py apply` sólo después de un plan válido. El lector acumula registros, conserva las filas iniciales, archiva las fuentes por SHA256, respalda los datasets y registra trazabilidad y duplicados. Los archivos de control y respaldo permanecen en updates/ y no entran en el directorio público dist/. Cantidades repetidas con el mismo identificador de Maquila se cuentan una vez; un ID existente con contenido diferente requiere sustitución explícita.
7. Ejecutar `ax_updates.py verify` para demostrar que todo el histórico inicial está intacto. Comprobar que los totales añadidos son los del plan, que una repetición produce cero nuevos y que las métricas mantienen sus fórmulas. Defectos nuevos sin asignación van SIN CLASIFICAR y generan advertencia. El catálogo actual contiene 36 defectos explícitamente asignados por el usuario.
8. Si hubo nuevos registros, guardar/push del source, empaquetar exactamente ese commit, `save_site_version` y `deploy_site_version` para el mismo Site público. Esperar succeeded, conservar IDs de cualquier resultado incierto y recuperar sin duplicar versiones. En Windows, `.sites-runtime/save-source-native.mjs` conserva las validaciones y autenticación del workflow, omitiendo únicamente el empaquetado Bash no disponible; preparar dist con el helper oficial y empaquetar con ../package_native.py. Las credenciales cortas se obtienen por Sites y se pasan sólo por stdin; nunca guardarlas ni mostrarlas. No reutilizar tokens caducados.
9. Tras succeeded, ejecutar `ax_updates.py ack`. Si no hay registros nuevos (vacío o duplicado), no hace falta publicar: verificar y reconocer la carga directamente. Nunca reconocerla antes de una publicación requerida que haya finalizado correctamente. Registrar las cargas en el control local, no mostrar Cargas ni formularios de escritura al público.
10. Mantener silencio sin cambios. Notificar sólo actualización publicada, error que impida actualizar o asignación necesaria. Las alertas del producto describen detección y evidencia; no causas ni recomendaciones.

La implementación conserva la base estática publicada. Cada actualización válida crea una nueva versión en el mismo enlace. El público consulta; sólo la automatización del propietario escribe.
