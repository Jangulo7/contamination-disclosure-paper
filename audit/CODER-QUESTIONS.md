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

---

## Q3 · 2026-08-22 · R1 · `f2_notes` is not clear, and an open gap it exposed

**Phase:** before the pilot. No document had been coded by either coder.

**Asked:** that the section *"The `f2_notes` format — fixed, and required on
every row"* was not clear at all.

**Class:** a question about a rule. Answerable — and it exposed a second thing
that is **not** answerable, recorded below as an open gap.

**What was fixed.** The cheat sheet labelled each slot only by its roman
numeral, so filling in five characters meant decoding (i)–(v) again on every one
of 50 rows. The slots are now named, from the codebook's own sub-element table;
the free text after the five characters is stated to be optional, which PART 2
never said although all three examples showed it; one example is read character
by character; and `-----` is stated to be a normal, correct answer. §4 still
carries the legend verbatim. No rule changed.

### Open gap — for the pilot to settle, not for the study runner to decide

**Does a pin that satisfies (i) via route `R` also count for (ii)?**

The codebook's own example reads `R-YY-  repo pinned a1b2c3d, 100k cap, 3
attempts, appendix C`: slot 1 is `R`, satisfied by the commit, and slot 2 —
*(ii) version or commit* — is `-`, although a commit was stated. So the pin
appears to be **consumed by (i) and unavailable to (ii)**. The route description
hints the same way: *"a bare repository URL with no version is not (i), it is
(ii)-eligible at best."*

**It is nowhere stated as a rule.** It is inferable from one example and one
parenthetical, and it can change a code: `2` requires (i) plus **two or more** of
(ii)–(v), so a document with a pinned repository and one other element is `1` if
the pin is consumed and `2` if it counts twice.

**This is not being resolved now, and that is deliberate.** Deciding it here
would mean the study runner settling a rule question before the evidence exists,
and amending a registered instrument outside the mechanism registered for it.
§5.2 already provides the mechanism — *"amend the codebook where a rule was
genuinely ambiguous, bump the version, and recode all nine under the new
version"* — and §5 already anticipates that *"the pilot is expected to bump the
version mid-study"*, which is why `codebook_version` is a per-row column. Settled
through the pilot, the same change becomes a documented amendment with recorded
evidence behind it.

**Told to both coders, in these words:**

> Sobre `f2_notes`: tenías razón, la sección era confusa. Ya está corregida — las
> cinco casillas ahora llevan su nombre, se dice que el texto libre es opcional,
> hay un ejemplo descifrado carácter a carácter, y se aclara que `-----` es una
> respuesta normal y correcta, no un fallo. Las reglas no cambian.
>
> Y una cosa más, que os digo a las dos con las mismas palabras. **Hay un caso
> que el manual no resuelve**, y prefiero decíroslo a que lo descubráis cada una
> por su lado: si un repositorio con su commit satisface (i) por la vía `R`,
> ¿cuenta ese mismo commit también para (ii)? El ejemplo del manual sugiere que
> no, pero **en ninguna parte se dice como regla**.
>
> **No os voy a dar una respuesta**, y no es por reservarme nada: decidirlo yo
> ahora sería inventar una regla que no está registrada. Codificad cada una según
> vuestra lectura y **anotadlo en `notes`** cada vez que os pase. Justamente para
> esto existe el piloto: si las dos leéis lo mismo y aun así codificáis distinto,
> la regla es ambigua, se corrige, y recodificáis los nueve bajo la nueva
> versión. Una discrepancia anotada aquí es un resultado útil; una respuesta mía
> improvisada, no.

**Sent to R2:** yes, same words, same day.

---

## Q4 · 2026-08-22 · R1 · The annex points at files I do not have

**Phase:** before the pilot. **Both coders were reading the instructions; no
document had been coded**, and no pilot sheet had been returned.

**Asked:** that `ANNEX-DOCUMENTS.md` named files and commands the coder does not
have — following on from Q2, where the same two files were asked about.

**Class:** a question about the instrument. Answerable in full.

**What the annex was doing wrong.** Four things, all fixed:

1. The header told coders to *"code in your own randomised order"* and gave two
   `python audit/order.py` commands to generate a worklist, with a `--pilot`
   flag. A coder can run none of that and needs none of it: the worklist is
   already in their folder, and `START-HERE.md` says they need run no command.
2. The reserve section said *"record every substitution in `exclusions.csv`"* —
   **the same wrong instruction corrected in the manual's §2 under Q2, sitting
   in a second document.** Correcting only the manual would have left the
   coder's other file still saying it.
3. The dead-link section told the coder to *"replace from the reserve"*.
   Replacement is the study runner's step.
4. `make-coder-kit.py` inserted the pilot sentence by repeating the sentence it
   followed, so *"This is a reference list, not your work order"* appeared twice
   in a row in every coder's copy.

The annex prose is authored in `make-annex.py` and is **not** derived from
`CODEBOOK.md`, so these were ordinary edits; no register text was involved, and
the document tables — ids, links, ordering — are unchanged.

### Found during the same review, and more serious than what was reported

Reviewing the annex on the criteria R1's question implied surfaced a defect
**nobody had reported**, and it is the only one found in this whole pass that
could have moved codes in a direction that flatters the paper.

The stratum A note ended: *"Expect these to be the **most** disclosed of the
three strata."* That is the study's own stratum comparison — a reported result
under §7 — handed in advance to the people producing it. Stratum is perfectly
confounded with document identity, so a coder holding that expectation has a
standing reason to read stratum A more generously, and the stratum contrast is a
headline result.

It is exactly the class of statement `make-coder-manual.py` refuses to ship: its
`PRIMING` filter fails the manual build on *"we expect"*, *"we predict"*,
*"rarely reported"* and thirteen more. **The annex is built by a different script
and never passed through that filter.** The pack-level check named *"contains
nothing that would prime the coding"* tested only that certain **files** were
absent; it never read what the delivered files say.

Both gaps are closed: `PRIMING` is hoisted to module scope and `audit-check.py`
now runs it over **every file in each coder's pack**, plus eleven phrasings that
state a result rather than predict one. Verified by reintroducing the sentence
and confirming the audit fails.

**Timing, stated rather than assumed.** The sentence was removed while both
coders were still reading their instructions. No document had been coded by
either coder, no pilot sheet existed, and no code assigned under it can be
affected — there are none. What cannot be ruled out is that a coder **read** it,
since reading the annex is step 2 of their instructions. The message below is
written so that it does not repeat the sentence: restating an expectation in
order to withdraw it would plant it in a coder who had skimmed past it.

**Also fixed in the same pass.** The worklist header said *"41 documents, in your
own order"*, which reads as a choice. The order is not a choice: it is fixed per
coder before coding and exists so that fatigue does not fall on the same
documents for both. It now says so, matching `START-HERE.md`.

**Reviewed and unchanged:** `START-HERE.md`. It names no file or command the
coder lacks, its exclusion instruction already matches the corrected manual, it
already said *"in the order given"*, and its section pointers resolve.

**Sent to R2:** yes, same words, same day.

---

# Texto para enviar — español (España)

**Un solo correo, idéntico para las dos codificadoras**, que responde a Q1–Q4
juntas. Se envía una vez, con el kit corregido adjunto. Los borradores separados
por pregunta no se enviaron: se consolidaron en este.

El resto de este archivo es el registro para el depósito y **no se envía**:
atribuye cada pregunta a `R1` o a `R2`, y ninguna necesita saber qué preguntó la
otra. Por eso el correo dice *«ha surgido»* y nunca *«R1 preguntó»*.

> **Nota de concordancia:** el texto usa femenino plural (*«las dos»*,
> *«vosotras»*). Si alguna de las dos no lo es, cambiar antes de enviar.

> **No añadir la frase retirada.** El punto 5 retira una expectativa sin
> repetirla y sin nombrar el grupo de documentos al que se refería. Repetirla
> para retirarla la sembraría en quien no se hubiera fijado. Comprobado
> automáticamente.

---

**Asunto:** Kit actualizado — usad este y descartad el anterior

> Buenos días,
>
> Os escribo a las dos con las mismas palabras, como siempre. Han surgido varias
> preguntas estos días y todas eran acertadas: dos señalaban fallos reales. Os
> adjunto el kit corregido. **Usad este y descartad el anterior.**
>
> **Las reglas no cambian y la versión sigue siendo `v1.4`** — dejad `v1.4` en la
> columna `codebook_version`. Vuestro orden de documentos tampoco cambia.
>
> **1 · `CODEBOOK-CODER.md` es vuestro manual, no el codebook completo.** Se
> genera automáticamente a partir del codebook depositado, así que cada regla es
> idéntica a la registrada; lo que se quita es la capa de análisis (la sección 8
> entera y los motivos del changelog). La sección 6 está a propósito: son reglas
> de conducta — no comparéis notas, vuestra identidad no es un dato — y no
> inclinan ningún código hacia el `0` ni hacia el `2`.
>
> Dicho eso, había **siete frases** escritas pensando en el codebook completo
> que, al copiarse, parecían referirse a vuestro manual; una llegaba a decir que
> ningún codificador debería estar leyéndolo. Corregidas. Al principio del manual
> tenéis la lista completa, con las dos redacciones lado a lado, para que lo
> comprobéis en vez de fiaros de mi palabra.
>
> **2 · Las exclusiones se anotan en vuestra hoja.** El manual y el anexo decían
> que las anotarais en `exclusions.csv`. Era incorrecto y contradecía otros tres
> sitios. Van **en vuestra propia hoja**, en `excluded` y `exclusion_reason`.
> `exclusions.csv` se genera *a partir de* vuestras hojas y no se edita a mano;
> `frame.csv` contiene información que no debéis ver. No necesitáis ninguno de
> los dos. Y **sustituir un documento excluido es tarea mía, no vuestra** — igual
> si un enlace está caído: lo anotáis con motivo `url_dead` y me avisáis.
>
> **3 · Vuestro orden de trabajo ya está fijado.** El anexo daba a entender que
> lo elegíais vosotras e incluso os daba comandos para generarlo. No: está fijado
> desde antes de empezar, es distinto para cada una, no cambia, y lo tenéis en
> vuestro `worklist`. No hay nada que ejecutar.
>
> **4 · `f2_notes` está aclarado.** Las cinco casillas llevan ahora su nombre, se
> dice que el texto libre es opcional, hay un ejemplo descifrado carácter a
> carácter, y se aclara que `-----` es una respuesta normal y correcta, no un
> fallo por no encontrar nada.
>
> **5 · Algo que os pido que descartéis.** Revisando el anexo encontré una frase
> que adelantaba una expectativa sobre cómo saldrían los resultados en cierto
> grupo de documentos. No debía estar ahí y ya no está. **No os la repito**:
> repetirla para retirarla sería sembrarla. Solo esto: si al leer el anexo os
> quedasteis con alguna idea sobre lo que «se espera encontrar», **descartadla**.
> No se espera nada. Registrad lo que cada documento dice, uno a uno.
>
> **6 · Y algo que el manual no resuelve — y que no voy a resolver yo.** Si un
> repositorio con su commit satisface (i) por la vía `R`, ¿cuenta ese mismo
> commit **también** para (ii)? El ejemplo sugiere que no, pero no se dice como
> regla, y puede mover un código entre `1` y `2`. **Codificad según vuestra
> lectura y anotadlo en `notes`.** Decidirlo yo ahora sería inventar una regla
> que no está registrada. Para esto existe el piloto: si las dos leéis lo mismo y
> aun así codificáis distinto, la regla es ambigua, se corrige, y recodificáis los
> nueve. Una discrepancia anotada es un resultado útil; una respuesta mía
> improvisada, no.
>
> Nada de esto afecta a ningún código, porque todavía no habéis codificado nada.
> Por eso os lo cuento ahora y no después.
>
> Preguntadme lo que sea, cuando sea: prefiero contestar a que adivinéis. Cada
> respuesta que doy a una, se la doy a la otra con las mismas palabras.
>
> Un saludo.
