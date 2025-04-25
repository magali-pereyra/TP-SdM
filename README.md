**Sistema de Matriculaciones (SdM) - Ingeniería Biomédica**

## Descripción

Este sistema está diseñado para automatizar el control de previaturas necesarias para la inscripción a Unidades Curriculares (UCs) o exámenes, enfocado en la carrera de Ingeniería Biomédica (IBIO). 
Fue desarrollado en Python 3.10 o superior, y tiene como objetivo reducir el trabajo administrativo manual y minimizar errores en el proceso de matriculación. 
El sistema se basa en el uso de principios de Programación Orientada a Objetos (POO) para estructurar su funcionalidad.

La prueba inicial del sistema se realizó utilizando el plan de estudios 2021, pero el sistema está preparado para gestionar diferentes 
cohortes de estudiantes matriculados en planes distintos de manera simultánea. La flexibilidad del diseño permite cargar diferentes planes 
de estudio a través de archivos en formato **JSON**, lo que facilita su actualización para años académicos posteriores.

## Características destacadas

- **Automatización** del proceso de inscripción a Unidades Curriculares y Exámenes, validando previaturas automáticamente.
- **Flexible** para trabajar con múltiples planes de estudio.
- Generación de archivos **CSV** con la información relevante de inscripciones y exámenes.
- Separación clara entre la **lógica académica** y las interfaces de interacción, manteniendo el código limpio y fácil de mantener.

## Estructura del código

### Clases principales

Las clases principales que implementan la lógica del sistema son:

- UnidadCurricular: Representa cada unidad curricular del plan de estudios.
- PlanDeEstudio: Contiene la información del plan de estudios y las reglas de previaturas.
- Curso: Representa un curso específico dentro de una Unidad Curricular.
- InstanciaDeExamen: Representa una instancia de examen asociado a una unidad curricular.
  
Estas clases acumulan la lógica del sistema, como la verificación de previaturas, el listado de inscripciones y las reglas de matriculación.

### Clases de interacción

Las clases que representan a los actores del sistema son:

- Estudiante: Permite que un estudiante interactúe con el sistema para inscribirse o desmatricularse de cursos.
- Secretaria: Permite que la secretaria realice matrículas y desmatriculas de estudiantes sin necesidad de conocer las reglas de previaturas.
- Coordinador: Permite al coordinador realizar tareas de gestión sin estar involucrado directamente en las reglas de previaturas.

Estas clases funcionan como interfaces de usuario que delegan las tareas al núcleo lógico del sistema.

## Uso del sistema

### Requisitos

Para utilizar este sistema, se recomienda tener instalado Python 3.10 o superior. Asegúrate de tener las siguientes librerías externas:

- **json** (para leer y escribir archivos JSON)
- **re** (para expresiones regulares)
- **csv** (para generar archivos CSV)

### Archivos necesarios

1. **Archivo Python (.py)**: Contiene todas las clases y la lógica del sistema.
2. **Jupyter Notebook**: Utilizado para realizar pruebas y demostraciones de las funcionalidades del sistema.
3. **Archivo JSON**: Contiene la información del plan de estudios. Para usar un nuevo plan de estudios, asegúrate de que el archivo JSON esté en el formato correcto.

### Instrucciones

1. **Descargar el archivo Python (.py)** que contiene las clases.
2. **Descargar o crear el archivo JSON** con la información del plan de estudios (debería seguir el mismo formato del plan de estudios 2021).
3. **Abrir el Jupyter Notebook** para interactuar con el sistema, ejecutar pruebas o probar el proceso de matriculación.
4. Si deseas trabajar con un nuevo plan de estudios, solo tendrás que cambiar el archivo JSON con el nuevo plan. El sistema cargará y validará la información automáticamente.
