# v1.6 coder addendum — the rules as briefed

## What this document is

`CODEBOOK.md` §6: *"Anything a coder needs to know belongs in the manual, where a
reader can see it; anything said out loud is invisible to everyone assessing the
result."*

No new kit or coding sheet was issued at v1.6. Both coders held the kit sent at
v1.5 and had confirmed in writing that no main-pass document had been opened.
They were asked to change the `codebook_version` value in their own copy rather
than to take a new file, so the typed value is the only thing carrying the
version forward. The repository copy of each sheet was regenerated to `v1.6` so
that the deposited artifact states the instrument that governs; that
regeneration was not sent to the coders.

The rules below were communicated to both coders on **24 August 2026, in
identical terms and in Spanish**, before either began main-pass coding. They are
the operative brief for every main-pass code. **This is a statement of those
rules, not the message that carried them.** The salutation, sign-off and
first-person framing of the covering message are omitted, and no correspondence
with the coders is reproduced here: they are identifiable individuals and
publishing private communications with them would require their consent under
the GDPR. The wording of each rule is as delivered, in the coders' working
language, because that wording is what governed the codes and a reviewer
assessing the instrument needs to see it.

The authoritative rules are in `CODEBOOK.md` v1.6. Where the two differ, **the
codebook governs** and the difference is a defect to be fixed in both.
`audit-check.py` §15c checks that every v1.6 rule change appears in both, so the
two cannot drift apart unnoticed.

---

## Alcance y versión

Estas reglas rigen la pasada principal. No se emitió manual nuevo.

En la columna `codebook_version` se escribe **`v1.6`** en las filas de la pasada
principal. Las filas del piloto conservan `v1.4` y no se modifican.

---

## 1 · Cómo se reparten los 25 minutos

- **Escanea** el documento de principio a fin, resumen incluido, hasta la primera
  puntuación de capacidad del sistema evaluado. Ese es el focal. Si el número
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

## 2 · Campo `focal`: benchmark + condición entre paréntesis

Ejemplos: `WAGIBench (MCQ)`, `Humanity's Last Exam (sin herramientas)`.

Lo que se compara entre las dos hojas es lo que va antes del paréntesis. Los
otros siete códigos describen la condición que va dentro.

Y por eso: **una frase referida a otra condición del mismo benchmark no se
aplica.** Si el focal es «sin herramientas» y el documento describe un control
para la condición «con herramientas», ese control no cuenta para esa fila.

Si el documento existe para presentar un benchmark, ese benchmark es el focal.
No hace falta leer el paper entero.

## 3 · ¿Capacidad o seguridad? Lo dicta la métrica, no la sección

La prueba: **si el sistema no hiciera nada en absoluto, ¿qué puntuación sacaría
en esa métrica?**

- **Sacaría 0** → la métrica mide capacidad. **Sirve como focal.**
- **Sacaría una puntuación alta** → la métrica mide que el sistema se abstuvo.
  **No sirve.**
- **Sacaría una parte** — la métrica suma «no hizo lo indebido» + «completó la
  tarea» → **sí sirve**, porque parte de la puntuación premia hacer la tarea.

| Métrica | Sin hacer nada sacaría… | ¿Sirve como focal? |
|---|---|---|
| Aciertos, `pass@1`, % de tareas resueltas | 0 | **Sí** |
| Horizonte temporal, tareas completadas | 0 | **Sí** |
| Tasa de rechazo, `not_unsafe`, % de respuestas seguras | alta | No |
| Ataques resistidos, tasa de defensa con éxito | alta | No |
| Violaciones evitadas | alta | No |
| «evitación + corrección» y similares | una parte | **Sí** |

**El epígrafe de la sección no decide nunca.** Una métrica de capacidad que
aparece dentro de una sección titulada «Model Safety» sigue sirviendo, y una tasa
de rechazo que aparece en una sección de capacidades sigue sin servir.

Se anota en `notes` por qué la métrica entra o no.

## 4 · `f2`, ranura 3: decir «sin límite» cuenta

Si el documento explicita que no había tope de tokens ni de pasos, se marca `Y`
en la ranura 3 y se escribe `no limit` en `notes`. Si simplemente no lo menciona,
se queda en `-`.

## 5 · `t5_acquired`: alcanzar un recurso no es controlarlo

- **0** — describe que el sistema usó un recurso externo, sin mencionar ningún
  control ni la contaminación.
- **1** — menciona el riesgo de contaminación, pero no dice qué se hizo.
- **2** — declara un control concreto, o comprueba que el control se mantuvo.

*Corrección respecto de la aclaración circulada el 23 de agosto de 2026:*
describir el entorno de herramientas («contenedor Linux con Bash y Python») es
`f2`, **no** es saneamiento. Saneamiento es **eliminar del entorno** lo que el
sistema no debería poder alcanzar: borrar el commit que arregla el fallo, los
tests de referencia o la clave de respuestas.

## 6 · `f1_strata` en figuras: hacen falta cifras legibles

- **2** — gráfico de barras con el número impreso encima, agrupadas por subtarea
  con nombre.
- **1** — figura de puntos o líneas con series con nombre pero sin cifras, aunque
  las series se vean perfectamente separadas.

## 7 · Proximidad no equivale a alcance

Una frase que describe un scaffold y está situada junto a un ejemplo concreto
vale sólo para ese ejemplo, salvo que el documento diga que aplica a toda la
suite.

## 8 · Cómo se rellena la hoja

Estos son los puntos que fallaron en el piloto. Cada uno desactiva una
comprobación automática si se hace de otra manera.

- **Columnas de código** — `f1_strata`, `f2_budget`, `t1_direct`,
  `t2_derivative`, `t3_temporal`, `t4_distributional`, `t5_acquired`,
  `f4_regeneration`: **sólo `2`, `1`, `0` o `NA`.** Nada más, ni una palabra. Lo
  que haya que explicar va en `notes`.

- **`f2_notes`: cinco caracteres seguidos, sin espacios entre ellos.** El primero
  es `H`, `R`, `S` o `-`; los otros cuatro son `Y` o `-`. Es decir `H-Y--`, **no**
  `H - Y - -`. Después, opcionalmente, un espacio y el texto que haga falta.
  Existe una comprobación automática que contrasta esas cinco ranuras con el
  código de `f2` y avisa cuando no cuadran; con espacios no las puede leer y la
  comprobación se queda sin hacer. Y **las ranuras tienen que decir lo mismo que
  el texto que las acompaña**: si el texto dice que la evaluación era `pass@1`,
  la ranura 5 es `Y`, no `-`.

- **`evidence`: obligatoria en todo código distinto de `0`.** Sección, página o
  una cita corta. Con poco tiempo, basta anotar la sección o la página
  aproximada. Lo que no vale es dejar un código alto sin respaldo — y tampoco
  vale bajarlo a `0` por no tener la cita, porque un `0` significa «lo he buscado
  y no está», no «no me ha dado tiempo».

- **`notes` empieza siempre por el token `REF:`** — `REF:none` si no hubo ninguna
  página fuera del límite del documento, o `REF:f2`, `REF:t5;t3`, nombrando las
  variables que esa página habría contestado. Se pone incluso cuando el código
  acaba siendo `0`.

- **`minutes`: siempre un número**, aunque sea aproximado. Nunca en blanco.

- **El archivo: CSV delimitado por comas, codificación UTF-8.** Ni `.numbers`, ni
  `.xlsx`, y comas, no punto y coma. Si el programa no permite guardarlo así, se
  comunica antes de enviar la hoja: convertirla a ciegas puede perder acentos y
  símbolos.

## 9 · Piloto, orden y tiempos

- Los nueve documentos del piloto **no se recodifican** bajo v1.6. La decisión es
  de la persona que dirige el estudio, por tiempo y presupuesto, y está registrada
  como desviación en `PRE-REGISTRATION.md`.
- Se sigue el orden fijado en la `worklist` de cada codificadora.
- Tope de **25 minutos por documento**: al llegar al límite se codifica lo
  establecido, se escribe `capped` en `notes`, se pone el tiempo real en
  `minutes` y se pasa al siguiente.
