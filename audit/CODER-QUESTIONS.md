# Coders' questions and the answers given

`CODEBOOK.md` §5.4 requires that every answer to a coder goes to **both** coders
in the same words, and is logged: *"Keep the questions and answers in one file,
dated; it goes into the deposit with everything else."* This is that file.

Two constraints govern every entry, and they are the whole of the rule:

1. **Every answer goes to both coders, in the same words.** An answer given to
   one and not the other is an asymmetric calibration: it makes the two sheets
   more alike for a reason that has nothing to do with the manual, and the
   agreement statistic can no longer be read as evidence about the manual.
2. **Answers are about *rules*, never about *cases*.** *"What counts as a named
   harness?"* is answerable. *"Is `A03` a `1` or a `2`?"* is not.

Questions are recorded as asked. Coder identity is a role label (`R1`, `R2`) and
nothing else, consistent with §6.

---

## Q1 · 2026-08-22 · R2 · Which document am I holding, and does §6 compromise the study?

**Phase:** before the pilot. No document had been coded by either coder.

**Asked (verbatim, Spanish):**

> Una cosa, el archivo que se subió como codebook-coder.md es el manual recortado
> para codificadores o el codebook completo? Yo soy R2 verdad? El propio texto de
> la sección 6 dice que quien lee el codebook completo es el adjudicador,
> coméntame aquí que hago. Si soy R2 coger códigos con esa sección delante
> compromete el estudio, creo!

**Class:** a question about the instrument, not about a document. Answerable in
full under constraint 2.

**Answer sent to both coders, in these words:**

> Buenos días,
>
> Efectivamente, eres R2, y has hecho exactamente lo que pide el manual:
> preguntarme a mí :-)
>
> **Nota aclaratoria sobre el documento.** `CODEBOOK-CODER.md` es el manual de
> codificación, no el codebook completo. No está «recortado» a mano, sino que se
> genera automáticamente con un script a partir del codebook depositado. Así nos
> aseguramos de que cada regla de codificación sea idéntica a la versión oficial
> registrada.
>
> **Lo que no está.** Hemos eliminado toda la capa de análisis: la sección 8
> entera (estadísticos) y los motivos del changelog. De hecho, el script da error
> y se niega a compilar si detecta alguna frase que dé pistas sobre un resultado
> esperado. Puedes estar segura de que no tienes nada de eso a la vista.
>
> **Lo que sí está (sección 6).** Está incluida a propósito porque recoge las
> reglas de conducta: no comparéis notas, cero calibración verbal, vuestra
> identidad no es un dato. Conocer esto no va a sesgar vuestros códigos hacia el
> `0` o el `2`; no os condiciona en ninguna dirección. Lo que sí comprometería
> vuestra independencia sería saber el resultado esperado o cómo se ponderan los
> desacuerdos, y esa información no está en vuestro archivo.
>
> **Dicho esto, tienes toda la razón y has cazado un fallo real de redacción.**
> Esa frase se redactó pensando en el codebook completo y se copió tal cual. Al
> leer «este codebook completo» en tu manual, parece referirse a sí mismo y da a
> entender que no deberías estar leyéndolo. **No eran un par de frases: eran
> siete.** La peor, en la sección 5, decía «ningún codificador lee este archivo»
> dentro del propio archivo del codificador.
>
> **Cómo lo hemos corregido.** El codebook completo está registrado y depositado
> con su huella digital, así que **no se toca**: corregirlo invalidaría el
> registro. La corrección se hace en el script que genera vuestro manual, donde
> queda a la vista y se puede comprobar. Una verificación automática confirma que
> al deshacer las siete correcciones reaparece exactamente el texto del codebook
> registrado — es decir, que **solo cambió la redacción**.
>
> **La versión no cambia: sigue siendo `v1.4`.** Dejad `v1.4` en la columna
> `codebook_version`, y vuestro orden de documentos tampoco cambia. Os envío el
> manual corregido; usad ese. Las siete frases están listadas una por una en
> `CODER-MANUAL-REWRITES.md`, que va dentro de vuestra carpeta, para que podáis
> verlas en lugar de fiaros de mi palabra.
>
> Codifica con total tranquilidad.

**What was done as a result:** seven sentences re-pointed at derivation time;
`CODEBOOK.md` untouched and still byte-identical to the deposited copy; two build
checks and `audit-check.py` §6b added; recorded as a dated row in the
`PRE-REGISTRATION.md` deviations table and listed in `CODER-MANUAL-REWRITES.md`.

**Sent to R1:** yes, same words, same day.

---

## Q2 · 2026-08-22 · R1 · Why are `exclusions.csv` and `frame.csv` not in the kit?

**Phase:** before the pilot. No document had been coded by either coder.

**Asked:** whether `exclusions.csv` and `frame.csv` should have been included,
since the manual's §2 talks about exclusions.

**Class:** a question about the instrument, not about a document. Answerable.

**Answer sent to both coders, in these words:**

> Buena pregunta, y la respuesta es que ninguno de los dos os hace falta — y uno
> de ellos ni siquiera existe todavía como dato.
>
> **`exclusions.csv` es una salida, no una entrada.** Lo genera `score.py` **a
> partir de vuestras hojas**, después de codificar. Ahora mismo está vacío: cero
> filas. Las exclusiones las registráis vosotras en vuestra propia hoja, en las
> columnas `excluded` y `exclusion_reason`, como dice §2: *«ambos codificadores
> registran `excluded` y `exclusion_reason` en su propia hoja para cada
> documento, siempre»*. Nadie decide por la otra qué documentos entran. Si os
> diera ese archivo, estaría invirtiendo el sentido de los datos.
>
> **`frame.csv` sí tiene información que no debéis ver.** Lleva una columna
> `cluster` que agrupa los documentos por organización, y una columna `status`
> que marca cuáles quedaron fuera por el tope por organización y cuáles son
> reservas. Saber que quince documentos son de la misma organización invita a
> codificarlos «en bloque» en lugar de uno a uno, que es justo lo que mide este
> estudio; y saber que existen reservas abarata mentalmente la decisión de
> excluir un documento. Además forma parte del depósito registrado, que ningún
> codificador recibe.
>
> **Lo que sí necesitáis ya lo tenéis:** los 50 documentos con sus enlaces y los
> nueve del piloto marcados están en `ANNEX-DOCUMENTS.md`.

**Sent to R2:** yes, same words, same day.
