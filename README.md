# EcoVision

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.1-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-model-D00000?logo=keras&logoColor=white)](https://keras.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-DGONZRO27%2FPROYECTO_ABP_ECO-181717?logo=github&logoColor=white)](https://github.com/DGONZRO27/PROYECTO_ABP_ECO)

Aplicación educativa que utiliza un modelo de **TensorFlow/Keras** para reconocer una imagen de **plástico, papel y cartón, metal o vidrio** y orientar su separación. Incluye una interfaz de clasificación en Streamlit y una landing page estática para publicar en GitHub Pages.

> **Separación en Colombia:** las cuatro clases del modelo son materiales aprovechables y se depositan en la **caneca blanca** cuando están limpios y secos. La aplicación no asigna una caneca diferente a cada material.

---
# ENLACE LANDING: https://dgonzro27.github.io/PROYECTO_ABP_ECO/

---

## Contenido

- [Características](#características)
- [Objetivo del proyecto](#objetivo-del-proyecto)
- [Autor y repositorio](#autor-y-repositorio)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Ejecución local](#ejecución-local)
- [Pruebas](#pruebas)
- [Despliegue en Streamlit Community Cloud](#despliegue-en-streamlit-community-cloud)
- [Publicar la landing page en GitHub Pages](#publicar-la-landing-page-en-github-pages)
- [Modelo y limitaciones](#modelo-y-limitaciones)
- [Uso responsable y licencia](#uso-responsable-y-licencia)
- [Fuentes](#fuentes)
- [Documentación del proyecto](#documentación-del-proyecto)

## Características

- Captura una foto desde la cámara o carga una imagen JPG, PNG o WebP.
- Ejecuta el modelo Keras exportado y muestra la clase estimada, su confianza y una recomendación de separación.
- Advierte cuando la confianza estimada es menor al 60 %.
- Mantiene las reglas del dominio, el caso de uso, la inferencia y la interfaz en módulos separados.
- Incluye una landing page responsive, con ilustraciones SVG propias y CSS y JavaScript separados.

## Objetivo del proyecto

Construir un prototipo educativo que reciba una imagen, identifique una de cuatro clases de material aprovechable con el modelo Keras suministrado y muestre una recomendación de separación coherente con el código de colores colombiano. El objetivo actual es integrar y demostrar inferencia; el entrenamiento de nuevos pesos queda pendiente hasta contar con datos etiquetados, permisos y un protocolo experimental.

## Estado de entrenamiento y evaluación

El artefacto disponible contiene una CNN con backbone convolucional tipo MobileNetV2, Global Average Pooling, una capa densa de 100 neuronas con ReLU y una salida de cuatro neuronas con Softmax. Recibe tensores RGB de `224 × 224 × 3`; el modelo tiene **538 708 parámetros** y normaliza la imagen en el código de inferencia al rango `[-1, 1]`.

El archivo HDF5 registra Keras 2.4.0 y TensorFlow como backend, pero no incluye `training_config`, dataset, historial de entrenamiento ni particiones. Por ello no se reporta accuracy, F1, matriz de confusión ni desempeño por clase. Las pruebas unitarias y la inferencia de humo comprueban integración de software, no exactitud del clasificador.

## Autor y repositorio

- **Autor:** Daniel Alejandro Gonzalez
- **Repositorio público:** [DGONZRO27/PROYECTO_ABP_ECO](https://github.com/DGONZRO27/PROYECTO_ABP_ECO)
- **Clonar el proyecto:**

  ```bash
  git clone https://github.com/DGONZRO27/PROYECTO_ABP_ECO.git
  cd PROYECTO_ABP_ECO
  ```

## Arquitectura

```text
.
├── app.py                         # Punto de entrada de Streamlit
├── index.html                     # Landing page para GitHub Pages
├── assets/
│   ├── css/styles.css             # Estilos de la landing page
│   ├── img/                       # Ilustraciones SVG originales
│   └── js/main.js                 # Interacciones de la landing page
├── models/
│   ├── keras_model.h5             # Modelo Keras entregado
│   └── labels.txt                 # Etiquetas en el orden de salida del modelo
├── src/ecovision/
│   ├── domain/                    # Guías y entidades de clasificación
│   ├── application/               # Caso de uso de clasificación
│   ├── infrastructure/           # Carga del modelo, preprocesamiento y etiquetas
│   └── presentation/              # Interfaz Streamlit
├── tests/                         # Pruebas unitarias del caso de uso
├── .github/skills/documentation/  # Skill de documentación del repositorio
├── .streamlit/config.toml         # Tema y límites de carga
├── requirements.txt
└── README.md
```

El paquete `ecovision` se instala desde `src/` al instalar `requirements.txt`. El sitio de GitHub Pages es estático y no carga ni ejecuta el modelo.

## Requisitos

- Python 3.11
- `pip`
- Para ejecutar la aplicación: TensorFlow, Streamlit, NumPy y Pillow (instalados desde `requirements.txt`)

## Ejecución local

Desde la raíz del repositorio:

1. Crea y activa un entorno virtual:

   **Windows (PowerShell)**

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

2. Instala las dependencias:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Inicia la aplicación:

   ```bash
   streamlit run app.py
   ```

4. Streamlit abrirá la aplicación en `http://localhost:8501`. Toma una foto o carga una imagen para obtener la predicción.

El modelo requiere una imagen RGB de 224 × 224 píxeles y el código normaliza sus canales al rango [-1, 1], como en la exportación de Keras entregada. `models/labels.txt` debe conservar el orden de las salidas del modelo.

## Pruebas

Las pruebas unitarias del caso de uso no necesitan cargar TensorFlow:

```bash
python -m unittest discover -s tests -v
```

## Despliegue en Streamlit Community Cloud

1. Publica el repositorio en GitHub y comprueba que `app.py`, `requirements.txt` y `models/` estén en la raíz del repositorio.
2. Inicia sesión en [Streamlit Community Cloud](https://share.streamlit.io/) con GitHub y autoriza el repositorio público.
3. Crea una aplicación nueva, selecciona el repositorio y la rama, e indica `app.py` como archivo principal.
4. Selecciona Python 3.11 en la configuración avanzada del despliegue.
5. Despliega y espera a que se instalen TensorFlow y las demás dependencias.
6. Abre la URL asignada por Streamlit y prueba una imagen de cada clase.

No se necesitan secretos para ejecutar este prototipo. Si en el futuro se añaden credenciales, guárdalas en los secretos de Streamlit y no en el código ni en el repositorio.

## Publicar la landing page en GitHub Pages

1. En GitHub, abre **Settings → Pages** del repositorio.
2. En **Build and deployment**, elige **Deploy from a branch**.
3. Selecciona la rama pública que contiene el proyecto y la carpeta `/(root)`.
4. Guarda la configuración y espera a que GitHub publique `index.html`.

La landing page usa rutas relativas (`assets/...`), por lo que funciona tanto desde la raíz de un dominio como desde la ruta de un repositorio. Sus botones enlazan a la documentación de despliegue de Streamlit; cuando la aplicación esté publicada, se puede sustituir ese destino por la URL real asignada al proyecto.

## Modelo y limitaciones

El archivo `models/keras_model.h5` es el modelo convertido entregado para el proyecto. El archivo de etiquetas contiene las clases `Plastico`, `Papel_Carton`, `Metal` y `Vidrio`, en el orden en que el modelo produce sus puntuaciones.

Este repositorio permite **inferir**, pero no incluye el conjunto de datos original ni un flujo de entrenamiento. Por tanto, no reentrena ni actualiza los pesos del modelo. La predicción depende de la calidad y el encuadre de la foto; objetos mezclados, sucios, tapados o fuera de las clases pueden generar resultados incorrectos. La confianza que se muestra es la salida del modelo, no una garantía de acierto. Verifica siempre la separación local y las instrucciones de gestión de residuos aplicables.

## Uso responsable y licencia

EcoVision es una herramienta educativa, no un sistema de gestión de residuos ni una certificación de reciclabilidad. No analiza si un objeto está contaminado ni sustituye las reglas del operador local. El código de colores blanco para aprovechables, negro para no aprovechables y verde para orgánicos se estableció en Colombia mediante la [Resolución 2184 de 2019](https://www.minambiente.gov.co/wp-content/uploads/2021/08/resolucion-2184-de-2019.pdf).

La aplicación no guarda intencionalmente las imágenes en archivos; al usar una instancia desplegada, la imagen se transmite al servicio que ejecuta Streamlit. Evita cargar fotos con personas, documentos u otra información sensible y consulta las condiciones de la plataforma donde se publique.

Este repositorio aún no declara una licencia de software. Antes de reutilizar o redistribuir el código o el modelo, confirma con el autor los permisos aplicables, en particular los del modelo y sus datos de entrenamiento, cuya procedencia no está incluida.

## Fuentes

- Goodfellow, Bengio y Courville, [*Deep Learning*](https://www.deeplearningbook.org/), MIT Press.
- Sandler et al., [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://openaccess.thecvf.com/content_cvpr_2018/html/Sandler_MobileNetV2_Inverted_Residuals_CVPR_2018_paper.html), CVPR 2018. Referencia arquitectónica; no acredita el origen ni la licencia del artefacto suministrado.
- [TensorFlow](https://www.tensorflow.org/), [Keras](https://keras.io/) y [Streamlit](https://docs.streamlit.io/), documentación oficial.
- Ministerio de Ambiente y Desarrollo Sostenible, [Resolución 2184 de 2019](https://www.minambiente.gov.co/wp-content/uploads/2021/08/resolucion-2184-de-2019.pdf).

## Documentación del proyecto

El skill local de documentación está en [`.github/skills/documentation/SKILL.md`](.github/skills/documentation/SKILL.md). Orienta futuras ediciones del README y preserva los datos verificados sobre el modelo y el código de colores.
