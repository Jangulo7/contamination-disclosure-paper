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

**Asunto: Cambios tras el piloto (una página)**

Hola,

El piloto ha cumplido su objetivo: hemos ajustado cinco reglas que generaban
dudas. No hay manual nuevo que leer; está todo aquí.

Un solo cambio en la hoja: en la columna `codebook_version`, escribid **`v1.6`**
en las filas de la pasada principal. Las filas del piloto se quedan con `v1.4`
— no las toquéis.

---

**1 · Cómo gestionar los 25 minutos**

- **Escanea** el documento de principio a fin, resumen incluido, hasta la primera
  puntuación de capacidad del sistema evaluado. Ese es tu focal. Si el número
  aparece en el texto antes que en una tabla, ese es.
- A partir de ahí, **deja de leer de principio a fin**. Busca las ocho variables
  por palabras clave.
- **Busca en todo el documento, apéndices incluidos.** La puntuación focal suele
  estar en una tabla, pero las condiciones de ejecución — harness, red, sandbox,
  fecha de corte — suelen estar en una sección de metodología o en un apéndice,
  lejos del score. Por eso se busca en todo el documento y no alrededor del
  focal. Una frase en la página 40 vale si dice que aplica a «todas las
  evaluaciones».
- No hay que resumir el documento ni entender el paper. Son ocho preguntas sobre
  una evaluación.

**2 · Campo `focal`: benchmark + condición entre paréntesis**

Ejemplos: `WAGIBench (MCQ)`, `Humanity's Last Exam (sin herramientas)`.

Lo que se compara **entre vuestras dos hojas** es lo que va antes del paréntesis.
Los otros siete códigos describen la condición que va dentro.

Y por eso: **una frase referida a otra condición del mismo benchmark no se
aplica.** Si tu focal es «sin herramientas» y el documento describe un control
para la condición «con herramientas», ese control no cuenta para tu fila.

Si el documento existe para presentar un benchmark, ese benchmark es el focal.
No hace falta leer el paper entero.

**3 · ¿Capacidad o seguridad? Lo dicta la métrica, no la sección**

¿Una puntuación más alta significa que hizo **más parte de la tarea**, o que hizo
**menos de algo malo**?

- Más de la tarea → sirve como focal.
- Menos de algo malo (rechazos, violaciones, ataques resistidos) → no sirve,
  esté en la sección que esté.
- Mezcla de las dos («evitación + corrección») → **sí** sirve.

Anota en `notes` cuál de los tres casos aplicaste.

**4 · `f2`, ranura 3: decir «sin límite» cuenta**

Si el documento explicita que no había tope de tokens ni de pasos, marca `Y` en
la ranura 3 y escribe `no limit` en `notes`. Si simplemente no lo menciona, se
queda en `-`.

**5 · `t5_acquired`: alcanzar un recurso no es controlarlo**

- **0** — describe que el sistema usó un recurso externo, sin mencionar ningún
  control ni la contaminación.
- **1** — menciona el riesgo de contaminación, pero no dice qué se hizo.
- **2** — declara un control concreto, o comprueba que el control se mantuvo.

*Corrección sobre mi aclaración anterior:* describir el entorno de herramientas
(«contenedor Linux con Bash y Python») es `f2`, **no** es saneamiento. Saneamiento
es **eliminar del entorno** lo que el sistema no debería poder alcanzar: borrar
el commit que arregla el fallo, los tests de referencia o la clave de respuestas.

**6 · `f1_strata` en figuras: hacen falta cifras legibles**

- **2** — gráfico de barras con el número impreso encima, agrupadas por subtarea
  con nombre.
- **1** — figura de puntos o líneas con series con nombre pero sin cifras, aunque
  las series se vean perfectamente separadas.

**7 · Proximidad no equivale a alcance**

Una frase que describe un scaffold y está situada junto a un ejemplo concreto
vale sólo para ese ejemplo, salvo que el documento diga que aplica a toda la
suite.

**8 · `evidence` obligatoria en todo código distinto de `0`**

Sección, página o una cita corta. Si vas justa de tiempo, **anota al menos la
sección o la página aproximada**: eso basta. Lo que no vale es dejar un código
alto sin respaldo — y tampoco vale bajarlo a `0` por no tener la cita, porque un
`0` significa «lo he buscado y no está», no «no me ha dado tiempo».

---

**Para terminar**

- **Piloto:** los nueve documentos del piloto **no se recodifican**. Es decisión
  mía, por tiempo y presupuesto.
- **Orden y tiempos:** seguid el orden de vuestra `worklist`. Tope de 25 minutos
  por documento: al llegar al límite, codificáis lo que tengáis, escribís
  `capped` en `notes`, ponéis el tiempo real en `minutes` y pasáis al siguiente.
- **Control rápido:** cuando llevéis tres documentos de esta fase, mandadme sólo
  las columnas `minutes` y `notes` de esos tres. Son dos minutos y no es una
  entrega, es sólo para comprobar los tiempos.
- **Formato:** guardad siempre como **CSV delimitado por comas, codificación
  UTF-8**.

Gracias por el trabajo del piloto. Ha sido de muchísima utilidad :-)

Un saludo,
Johanna
