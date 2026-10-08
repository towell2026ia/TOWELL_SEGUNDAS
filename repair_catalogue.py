from pathlib import Path
import json
p=Path('towell-quality/dist/app.js');s=p.read_text(encoding='utf8')
s=s.replace("countCard('Sin clasificar · segmento'", "countCard('Departamento pendiente'")
s=s.replace('Asignaciones expresamente definidas','Clasificación completa recuperada del proyecto')
s=s.replace('Los demás defectos quedan SIN CLASIFICAR. Se conservan sus nombres y cantidades.', 'Catálogo recuperado del chat «Dashboard de segundas costura»: 19 defectos de Tejido, 5 de Tintorería y 4 de Costura. Se normalizan mayúsculas, acentos y espacios alrededor de las diagonales. Todo registro conserva su defecto original.')
s=s.replace('segundas del segmento están SIN CLASIFICAR.', 'segundas tienen defecto identificado y están pendientes de asignación departamental en el catálogo del Site.')
p.write_text(s,encoding='utf8')
p=Path('towell-quality/README.md');s=p.read_text(encoding='utf8')
s=s.replace('El catálogo sólo asigna los siete defectos expresamente definidos por el usuario. El resto permanece SIN CLASIFICAR.', 'El catálogo recupera los 28 defectos definidos por el usuario en el chat «Dashboard de segundas costura» (mensaje 40d4540e-f97d-48bf-a1b5-33f7a687421c, conversación 6ac528b2-d980-83e8-8914-962ff8cb3417). Se normalizan mayúsculas, acentos y espacios junto a diagonales. Los ocho nombres históricos adicionales conservan su defecto y sólo tienen pendiente la asignación departamental.')
p.write_text(s,encoding='utf8')
