## 1. Objetivo

Desarrollar un modelo que pueda clasificar la personalidad de un usuario (mbti type) mediante análisis de texto

## 2. Planteamiento del problema 

Para construir el modelo se necesitarán textos de usuarios y sus respectivos mbti para plantear un problema de tipo aprendizaje supervisado (clasificación concretamente). 

El MBTI consta de 4 dimensiones de personalidad:

>  Introversion (I) – Extroversion (E)

>  Intuition (N) – Sensing (S)

>  Thinking (T) – Feeling (F)

>  Judging (J) – Perceiving (P)

Por lo que puede ser planteado de 3 formas distintas: 

- Clasificación binaria: Tratar de predecir cada dimension por separado (4 modelos). 

  Ej: [1,0]

- Clasificación multiclase: Tomando todas las combinaciones posibles (16 tipos) 

  Ej: [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]

- Clasificación multilabel: Único modelo para predecir 4 dimensiones por separado (4 outputs)

  Ej [1,1,1,0]

## 4. Metodología 

 Se ha tratado de construir un modelo para el inglés y otro para el español mediante 3 bases de datos extraidas de distintas fuentes (Forum of PersonalityCafe, Reddit y Twitter). 

### Limitaciones e inconvenientes con el modelo y los datos:

- The MBTI model (Myers-Briggs) : El modelo de personalidad mbti es bastante antiguo, su desarrollo comenzó en 1917. 

  La psicología científica todavía no estaba bien consolidada en aquella época donde la mayor parte de ésta poseía una base en el psicoanálisis. El modelo ha sido [duramente criticado](https://journals.sagepub.com/doi/abs/10.3102/00346543063004467) por la comunidad científica y actualmente no es respaldado (El modelo de personalidad predominante actual es el Big Five ).  No obstante pese a todo lo dicho, en la población de habla inglesa el MBTI se encuentra mucho mas difundido y apreciado que el Big Five, por lo que es realmente dificil (Si no, imposible) conseguir textos de un gran volumen de personas y si respectivo indicador de BigFive, por lo que para poder desarrollar este proyecto se ha tenido que utilizar el MBTI por la disponibilidad de datos, aunque debe de tenerse en cuenta las limitaciones del propio modelo como tal. 

- Idiosincracia de los datos: A excepción de PersonalityCafe forum donde se conoce con exactitud que el mbti de dichos usuarios corresponde al real, los datos extraidos tanto de Twitter como de Reddit son "self-reporting", es decir, son los propios usuarios quienes dicen cual es su MBTI type y se da por hecho que "ese es el real", más allá de la falta de veracidad del reporte, no se poseen datos sobre la fuente de extracción del mismo, si realizaron algún "test por internet" o realmente fueron evaluados por un profesional (improbable).  

  Otro aspecto a tener en cuenta es que la personalidad es considerada una dimension, esto significa que es erroneo decir que por ejemplo una persona es extrovertida o introvertida, lo correcto sería decir que esa persona es un "64%" extrovertida, pues se es más o menos, pero no se "es". Los datos usados para entrenar el modelo simplemente marcan las etiquetas como "extrovertido" o "introvertido", lo cual supone una alta pérdida de información, esto significa que se  puede estar tratando a una persona con 51% como extrovertida y 49% como introvertida sin ir más allá. 

  Por último cabe mencionar el alto desbalance de los datos, para los 16 tipos de personalidad:

  ![img](data:image/png;base64,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)

  Y para cada dimensión, encontrandose el mayor desbalance entre introversión y extraversión, siendo el primer tipo mas de 3 veces más grande que el primero (3,11 aprox):

  ![img](data:image/png;base64,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)

Si se juntan todas las limitaciones, se puede  imaginar algo como lo siguiente: 

*Supongamos que queremos crear un clasificador de imagenes de perros/gatos/monos.  Para ello le pasamos al modelo 700 imagenes de perros, 200 de gatos y 100 de monos para entrenarlo...aunque realmente de las 700 imagenes de perros 100 son de gatos mal clasificadas, de los monos 20 son imagenes de gatos: **Vamos a entrenar un modelo con poca muestra y asumiendo que una gran parte de la muestra puede estar mal clasificada.** 

Todas estas limitaciones, tanto por separado como juntas suponen razones suficientes como para invalidar cualquier investigación científica seria utilizando los datos recolectados, por lo que **la finalidad de este proyecto es puramente académico y de autoaprendizaje.**

### 1.  Recolección de datos
> En el presente repositorio se comparte el código utilizado pero no las bases de datos ni los diccionarios de LIWC (Bien porque no estoy autorizado a compartirlo o porque no son de dominio público)
- Datos en Inglés: 

  -Reddit: Los datos en inglés fueron solicitados al Dr. Matej Gjurković y su equipo de la Universidad de Zagreb, referentes al paper  [Reddit: A Gold Mine for Personality Prediction](https://www.researchgate.net/publication/325445581_Reddit_A_Gold_Mine_for_Personality_Prediction). Donde se recoge la personalidad de 13 mil usuarios de Reddit quienes mostraron su personalidad en posts públicamente para posteriormente hacer un scrappling de dichos usuarios y recolectar sus posts. 

  ***Los datos pueden solicitarse en: https://psy.takelab.fer.hr/

  -PersonalityCafe: El  [foro de PersonalityCafe](https://www.personalitycafe.com/) va dirigido a aficionados al modelo MBTI de personalidad, a compartir y discutir sus semejanzas y diferencias según a su tipo. Se extrajeron los últimos 50 posts de 8600 usuarios del foro. 

  El dataset se puede encontrar públicamente en [kaggle](https://www.kaggle.com/datasnaek/mbti-type)

- Datos en español: Para los datos en Español se realizó un scrapping mediante los ID de usuarios de Twitter utilizando su API , los ID de usuarios y su tipo de personalidad fueron extraídos del dataset "TWISTY", referente al paper [TWISTY: a Multilingual Twitter Stylometry Corpus for Gender and Personality Profiling](https://www.aclweb.org/anthology/L16-1258.pdf).

  El dataset con ID de usuarios puede descargarse [aqui](https://www.uantwerpen.be/en/research-groups/clips/research/datasets/)

  > Dimensiones de los datos iniciales: (comentarios | autores)

  Reddit: 22.939.193 | 13.631

  PersonalityCafe: 430.000 | 8600

  Twitter:  12.995.504 | 8900

### 2. Preprocesado de datos

- English Model: 

  - Reddit: 

    Los datos de Reddit pese a tener una gran cantidad (casi 23 millones) la mayor parte de estos no resultan aptos y se requirió un filtrado pasando por las siguientes fases:

    - Eliminar comentarios repetidos; casi la mitad de los comentarios (10 millones) eran comentarios repetidos o "spam"
    - Eliminar "autores repetidos", algunos autores constaban en algunos posts con un tipo de personalidad y en otro tipo con otro (Aquí una muestra de la baja fiabilidad de los datos)
    - Eliminar comentarios con un numero de palabras superior a 40 palabras o inferior a 5. Esto debido a que la mayor parte de la muestra (más del 90%) de los comentarios se encontraban por debajo de las 50 palabras, además se filtró hasta 40 para poder compararlo con el dataset de PersonalityCafe donde la mayoría de comentarios tenían ésta longitud maxima, también teniendo en cuenta que la mayoría de tweets (con los que se utilizará la app) rara vez sobrepasan esta longitud.
    - Codificar menciones de personalidad, dado que la muesta es extraida de "self-reported" muchos usuarios menciona su personalidad en algun post, por lo que cualquier mención de personalidad a algún tipo del mbti  ha sido codificada como "typemention". 
    - Juntar datos por usuario, se recogieron al azar 50 comentarios y se agruparon, todo esto para obtener un dataset lo mas similar al de PersonalityCafe y poder concatenar los dos. 
    - El dataset en su resultado final tenía las dimensiones de 469.850 comentarios de 9347 autores

  - PersonalityCafe:
    
    - Dado que se toma como dataset de referiencia no se requirió un alto procesamiento, solo se codificarón las menciones de personalidad como "typemention". 

  Una vez preparados los dos datasets se juntaron en un único data y se le aplicó un procesamiento básico de texto:

  - Aplicar un lower (todas las palabras en minisculas)
  - Eliminar carácteres de puntuación no alfabéticos como:   ^)#%;´{
  - Quitar espacios en blanco 
  - Construir un tokenizador (diccionario con palabras presentes) y filtrar embeddings pre-entrandos de glove (300 dimensiones)

  Es importante señalar qué sin el procesamiento mencionado, los resultados de entrenamiento en el modelo son hasta un 30% mejores, alcanzandose un accuracy de casi el 90% en algunas dimensiones. No obstante cabe recalcar que dicho modelo haría "trampas" puesto que aprendería a identificar el propio tipo mencionado por un usuario como su personalidad o identificar patrones de spam realizados por el mismo usuario. 

- Spanish Model: Para el modelo en Español se juntaron los tweets de usuarios y se filtraron los usuarios de los que se pudo extraer al menos 500 Tweets. El preprocesado de texto fue igual que con el dataset en inglés a excepción de no eliminar las palabras con acento y la "ñ".

También se realizaron pruebas aplicando un preprocesado con métodos con lemmatizacion or stemming, pero sin mejoras.

### 3. Entrenamiento

Se probaron distintos tipos de modelos, a mencionar:

- Para la codificación: Bag of Words (CountVectorizer), TF-IDF Vectorizer, Embeddings Preentrenados, Embeddings Aprendidos, LIWC vectors, estadísticos del texto (n_words, n_unique_words, verbs, nouns...)
- Para entrenar el modelo: Regresión Logística, SVM, Random Forest, XGBoost, Light Gradient Boost (LGBM), redes con capas densas totalmente conectadas, capas recurrentes (LSTM), de convolución 1D y 2D.

> **¿Qué son los LIWC vectors?** No es mas que un diccionario con más de diez mil palabras agrupadas en categorías semánticas, como por ejemplo: Guerra, Amor, Familia, Animales etc (63-73 categorías en total). Así por ejemplo con la frase "Me gustan los perros y los gatos", se obtendría en la categoría de animales un 2, un 1 en la categoría de afiliación otro 1 en positivo etc.", en resumen, la salida sería un OneHotEncoding con las categorías semánticas. 
>
> Se puede encontrar un aproximación similar y gratuita con la libreria [EMPATH](https://github.com/Ejhfast/empath-client)

Para la codificación el bag of words dió mejores resultados que el TF-IDF, los vectores LIWC se quedaron muy cerca, los embeddings preentrenados dieron resultados similares a los entrenados y los estadísticos de texto no superaron ni siquiera la linea base del 50%.

De todos los modelos probados (SVM, LOGREG, Random Forest and XGBoost) el LGBM dio los mejores resultados y con un entrenamiento hasta 10 veces más rápido que el resto. 

**El mejor modelo, con mejor AUC y más rápido fue el LGBM con un CountVectorizer y ngrams (1,3) con max_features=5000**

En cuanto a las redes, se desechó el uso de capas LSTM por ser demasiado lentas y no aportar mejoras a las capas de convolución, las capas densas tampoco lo hicieron. El mejor auc se obtuvo con un modelo de convolución con branches como el propuesto por Yoon Kim [paper](https://www.aclweb.org/anthology/D14-1181.pdf) aunque para poder aplicarlo se siguieron dos estrategias: 

1. Separar nuevamente los comentarios de cada autor para pasar a la red un comentario como ejemplo de entrenamiento (pasando un max_len de 50 para los embeddings y entrenar con 430 mil samples) o pasar directamente los comentarios agrupados (con un max_len=1500 y entrenar con 18 mil samples). 

   En el primer caso al tener muchos samples para entrenar la red era estable pero debido al desbalance de los datos tendía a sobreajustar y clasificar a todos los comentarios como "infj" (con 16 salidas) o a todos como introvertidos (con una salida), para corregir esto se probaron dos procedimientos, el primero pasar el mismo numero de types of personality (balanceado) y el segundo o bien pasar pesos ponderados para cada clase en un diccionario (class_weights) o pasar ponderaciones para cada muestra (sample_weights) para corregir la función de pérdida. En el primero caso no se superó el 50% y en el segundo la red era muy lenta y apenas llegaba al 55% (con el mismo procedimiento LGBM conseguía un 56%).

2. Pasar directamente los comentarios agrupados: Se disponía de muy pocos samples (18 mil ) para alimentar una red, y debido a lo desbalanceado que estaba, no resultaba estable, se procuró hacer un stratify k fold, pero la desviación era demasiado alta y en cualquier caso apenas conseguía alcanzar al LGBM model, y esto hablando del accuracy, con un roc_auc no superaba el 51% por lo que fue desechado completamente.

En conjunto ninguna red pudo vencer al modelo base LGBM con n-grams mencionado que obtuvo los mejores y más rápidos resultados: 

| roc_auc_score mean | E-I          | S-N          | T-F          | J-P          |
| :----------------: | ------------ | ------------ | ------------ | ------------ |
|        CV13        | **0.662692** | 0.656516     | **0.791028** | **0.640405** |
|        TF13        | 0.656171     | **0.656572** | 0.788312     | 0.635755     |
|        LIWC        | 0.630212     | 0.606550     | 0.750429     | 0.587492     |

***CV13 = CountVectorizer (1,3) n-grams, TF13 = TF-IDF (1,3) n-grams***

Cabe destacar la cercanía de los vectores LIWC que ofrecen un rendimiento similar pese a ser solo 63 categorías, lo cual lo convertiría en un modelo con una gran relación accuracy/velocidad 

>  En el repositorio se encuentra el código necesario para replicar los resultados del mejor modelo (aunque no se comparte la base de datos de Reddit). 
>
> Debido al alto numero de variables de modelos de redes (docenas de combinaciones), se comparten solo los de la red de convolución con embeddings preentrenados, que fue la que mejor resultados dió, pero sin llegar a superar al modelo LGBM (como máximo llegando a un 0.55)

Para el modelo en Español se replicaron los mismos procedimientos que en el Modelo en Inglés, nuevamente los resultados son prácticamente iguales, el mejor   fue el LGBM con n-gramas, con los siguientes resultados de un stratified K Fold con 5 splits:

| roc_auc_score mean | E-I          | S-N          | T-F          | J-P          |
| -----------------: | ------------ | :----------- | :----------- | :----------- |
|               CV13 | 0.647423     | **0.601979** | 0.613047     | **0.584833** |
|               TF13 | **0.651896** | 0.593516     | **0.617540** | 0.583497     |
|               LIWC | 0.622816     | 0.579548     | 0.601328     | 0.562347     |

***CV13 = CountVectorizer (1,3) n-grams, TF13 = TF-IDF (1,3) n-grams***

## 4. FRONT END 

Para subir el modelo final se utilizó streamlit.

Se creó un repositorio privado donde poder conectarlo a la API de Twitter (claves personales) y a los diccionarios de LIWC (pues no pueden hacerse públicos), además la app fue subida con heroku para poder acceder desde cualquier dispositivo. Solo se subió el modelo en inglés pues el modelo en español apenas llegaba al 60%; con un poder estadístico del 10% el modelo apenas vence al azar. 

## Conclusiones

Debido a la  falta de validez de los datos y la escasez de los mismos no ha sido posible desarrollar modelos más avanzados de tipo DeepLearning, debido a: 

1. No se pueden tomar los posts por usuario y separarlos puesto que los samples al ser de mismos autores guardan características en el estilo de escritura y lenguaje; la red termina aprendiendo antes estos estilos que la personalidad del autor, como muletillas, frases hechas, spam etc. 
2. Al no poder separarse los posts, queda muy poca muestra (18 mil) para poder entrenarlo con una red realizando sus convenientes splits (train/val/test), haciendo que la red sea inestable sin clarificar cuantos epochs necesita; La red tiende a sobrentrenarse o no aprender en absoluto con poca muestra. Al probarlo con k-folds y un numero limitado de epochs (entre 5 y 20) la desviación para cada predicción en cada k-fold alcanza el 20% (Ej: 55% en un kfold y 75% en otro), algo inviable. 
3. Al tener poca muestra (los mencionados 18 mil) no es conveniente realizar una clasificación de tipo multiclase, pues tratar de aprender 16 categorías distintas resulta inviable para cualquier tipo de modelo, ya sea uno simple basado en bolsas de palabras o de DeepLearning. El estar la variable criterio tan inbalanceada se traduce en que quedan menos de 200 samples para algunos niveles de la variable y más de 2000 para otras. 
4.  El mejor abordamiento y con mejores resultados es entrenar un modelo para cada clase, esto ayuda a compensar el desbalance: De 1/10 para algunas clases a como mucho 1/3.

En conclusión, debido a las limitaciones encontradas principalmente por la tipología de los datos para el problema planteado el mejor acercamiento ha resultado en un simple bolsa de palabras con n-gramas aunque cabe destacar la cercanía de los vectores de LIWC, que siendo tan pocos (63) y obteniendose de forma rápida, obtienen unos resultados similares a los n-gramas.

En cualquier caso ha sido un proyecto interesante que permite introducirse en todo tipo tipo de campos dentro del NLP, desde las bolsas de palabras a embeddings, diccionarios semánticos (como LIWC o EMPATH) o el uso de modelos de red tipo multientrada/multisalida  y/con distintas ramas. 

