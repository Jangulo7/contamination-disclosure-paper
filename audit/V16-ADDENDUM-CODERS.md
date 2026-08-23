# v1.6 coder addendum — the brief the coders actually received

Deposited under `CODEBOOK.md` section 6: *"Anything a coder needs to know belongs
in the manual, where a reader can see it; anything said out loud is invisible to
everyone assessing the result."*

No new kit or coding sheet was issued at v1.6. Both coders had the kit sent at
v1.5 and had confirmed in writing that they had not opened a main-pass document.
They were asked to change the `codebook_version` value in their own copy rather
than to take a new file, so the typed value is the only thing carrying the
version forward. The repository copy of each sheet was regenerated to `v1.6` so
that the deposited artifact states the instrument that governs; that regeneration
was not sent to the coders. The text below is what they were sent, in
full and unedited, and it is the operative brief for every main-pass code. The
authoritative rules are in `CODEBOOK.md` v1.6; this restates them in the words
the coders read. Where the two differ, the codebook governs and the difference is
a defect to be fixed in both.

Sent 2026-08-23, identical to both coders.

---

**Asunto: Cambios del piloto — una página, y ya está**

Hola,

El piloto ha servido para lo que tenía que servir: cinco reglas no decidían y las
hemos arreglado. **No hay manual nuevo que leeros.** Está todo aquí.

Un solo cambio en la hoja: en `codebook_version` escribid **`v1.6`** en las filas
de la pasada principal. Las del piloto se quedan con `v1.4` — no las toquéis.

---

**1 · Cómo repartir los 25 minutos**

- Encuentra el focal **leyendo** de principio a fin, resumen incluido. Para en la
  primera puntuación de capacidad del sistema evaluado. Si el número aparece en
  el texto antes que en una tabla, ese es el focal.
- A partir de ahí **deja de leer**. Busca por palabras clave las ocho variables.
- Busca en **todo** el documento, apéndices incluidos. Una frase a 40 páginas
  vale si dice «todas las evaluaciones».
- No tienes que resumir el documento ni entender el paper. Son ocho preguntas
  sobre una evaluación.

**2 · En `focal`: benchmark + condición entre paréntesis**

`WAGIBench (MCQ)`, `Humanity's Last Exam (sin herramientas)`.

Lo que tiene que coincidir entre las dos es **lo de antes del paréntesis**. Los
otros siete códigos hablan de la condición del paréntesis.

Si el documento es un paper que presenta un benchmark, ese benchmark es el focal.
No hace falta leerse el paper entero.

**3 · ¿Capacidad o seguridad? Lo dice la métrica, no la sección**

¿Más puntuación significa que hizo **más de la tarea**, o que hizo **menos de
algo malo**?

- Más de la tarea → sirve como focal.
- Menos de algo malo (rechazos, violaciones, ataques resistidos) → no sirve,
  esté en la sección que esté.
- Si mezcla las dos («evitación + corrección») → **sí** sirve.

**4 · F2, ranura 3: decir «sin límite» cuenta**

Si el documento dice que no había tope de tokens ni de pasos, pon `Y` en la
ranura 3 y escribe `no limit` en `notes`. Si simplemente no lo dice, sigue
siendo `-`.

**5 · `t5_acquired`: alcanzar algo no es controlarlo**

- Describe que el sistema usó algo externo, sin control y sin hablar de
  contaminación → **0**.
- Nombra el riesgo sin decir qué hizo → **1**.
- Declara un control, o comprueba que el control se mantuvo → **2**.

Y corrijo una cosa de mi aclaración anterior: describir el **entorno de
herramientas** («contenedor Linux con Bash y Python») **no** es saneamiento. Eso
es `f2`. Saneamiento es **quitar de dentro** lo que el sistema no debería
alcanzar: borrar el commit que arregla el fallo, los tests de referencia, la
clave de respuestas.

**6 · `f1_strata` en figuras: hacen falta cifras legibles**

- Barras con el número impreso encima, agrupadas por subtarea con nombre → **2**.
- Figura de puntos con series con nombre y sin cifras → **1**, aunque las series
  se vean perfectamente separadas.

**7 · Estar al lado no es tener alcance**

Una frase que describe un scaffold y está junto a un ejemplo concreto vale sólo
para ese ejemplo, salvo que el documento diga que vale para toda la suite.

**8 · `evidence` en todo código distinto de `0`**

Sección, página o una frase corta. Si no da tiempo a anotar la cita, es mejor
bajar el código que dejarlo sin respaldo.

---

Los nueve del piloto **no se recodifican**. La decisión es mía, por tiempo y
presupuesto.

Orden fijo, el de vuestro `worklist`. 25 minutos por documento: al llegar al
tope, codificáis lo que tengáis, `capped` en `notes`, tiempo real en `minutes` y
al siguiente.

Cuando llevéis tres documentos, mandadme sólo `minutes` y `notes` de esos tres.
Son dos minutos, no es una entrega.

Guardad siempre como **CSV UTF-8 delimitado por comas**.

Gracias por el piloto. Ha hecho exactamente lo que tenía que hacer.

Un saludo,
Johanna
