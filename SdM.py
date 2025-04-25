import csv
import re
import json

class Persona:
    """
    Clase para representar a una persona con nombre y apellido.

    Métodos:
    nombre_completo():
        Retorna el nombre completo de la persona en formato 'Nombre Apellido'.
    """
    def __init__(self, nombre, apellido):
        
        """
        Inicializa una nueva instancia de la clase Persona.

        Parámetros:
        nombre : str
            El nombre de la persona. No debe estar vacío ni ser solo espacios.
        apellido : str
            El apellido de la persona. No debe estar vacío ni ser solo espacios.

        Raise:
        ValueError:
            Si el nombre o el apellido no son cadenas válidas no vacías.
        """

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")

        if not isinstance(apellido, str) or not apellido.strip():
            raise ValueError("El apellido debe ser una cadena no vacía.")

        self.nombre = nombre.strip().title()
        self.apellido = apellido.strip().title()
    
    def nombre_completo(self):
        """
        Retorna el nombre completo de la persona en formato 'Nombre Apellido'.

        Retorna:
        str
            El nombre completo de la persona.
        """
        return f"{self.nombre} {self.apellido}"
    
class UnidadCurricular:
    """
    Representa una unidad curricular dentro de un plan de estudios.

    Atributos:
        codigo (str): Código único que identifica la unidad curricular.
        nombre (str): Nombre de la unidad curricular.
        creditos (int): Cantidad de créditos otorgados por la unidad.
        previas (list of str): Lista de códigos de unidades curriculares que deben aprobarse previamente.
    """
    def __init__(self, codigo, nombre, creditos, previas):
        """
        Inicializa una nueva instancia de la clase UnidadCurricular.

        Args:
            codigo (str): Código de la unidad curricular.
            nombre (str): Nombre de la unidad curricular.
            creditos (int): Créditos asignados a la unidad curricular.
            previas (list of str): Unidades curriculares que deben aprobarse antes (requisitos previos).
        """
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.previas = previas

class PlanDeEstudio:
    """
    Clase que representa un plan de estudio compuesto por varias materias (unidades curriculares).
    
    Atributos:
        nombre_plan (str): Nombre del plan de estudio.
        materias (list): Lista de objetos UnidadCurricular que forman parte del plan.
    """
    def __init__(self, nombre_plan, ruta_json):
        """
        Constructor que inicializa el plan de estudio cargando las materias desde un archivo JSON.
        
        Args:
            nombre_plan (str): Nombre del plan de estudio.
            ruta_json (str): Ruta del archivo JSON que contiene la estructura del plan.
        """

        self.nombre_plan = nombre_plan
        self.materias = []
        self._cargar_desde_json(ruta_json)

    def _agregar_materia(self, unidad_curricular):
        """
        Método privado para agregar una unidad curricular a la lista de materias. Es de uso interno
        
        Args:
            unidad_curricular (UnidadCurricular): Objeto de tipo UnidadCurricular a agregar.
        """
        self.materias.append(unidad_curricular)

    def buscar_uc_por_codigo(self, codigo):
        """
        Busca una materia en el plan según su código.
        
        Args:
            codigo (str): Código de la unidad curricular a buscar.
        
        Returns:
            UnidadCurricular o None: Devuelve la unidad si la encuentra, sino devuelve None.
        """
        for uc in self.materias:
            if uc.codigo == codigo:
                return uc
        return None

    def _cargar_desde_json(self, ruta_archivo):
        """
        Método privado que carga las materias desde un archivo JSON estructurado por semestre.
        
        Args:
            ruta_archivo (str): Ruta del archivo JSON a leer.
        """
        with open(ruta_archivo, "r", encoding="utf-8") as f: # Abre el archivo JSON en modo lectura
            datos = json.load(f)  # Se carga el contenido del archivo en un diccionario
        
        # Itera sobre cada semestre y sus materias
        for semestre, materias in datos.items():
            for codigo, materia in materias.items():
                # Se crea una nueva instancia de UnidadCurricular con los datos del JSON
                uc = UnidadCurricular(
                    codigo=codigo,
                    nombre=materia["nombre"],
                    creditos=materia["creditos"],
                    previas=materia["previas"]
                )
                self._agregar_materia(uc)

    def ver(self):
        """
        Imprime en consola la lista completa de materias del plan de estudio.
        Muestra código, nombre, créditos y previas si las hay.
        """
        print(f"Plan de Estudio: {self.nombre_plan}")
        print("-" * 40)
        for materia in self.materias:
            print(f"{materia.codigo} - {materia.nombre} ({materia.creditos} créditos)")
            if materia.previas:
                print(f"  ↳ Previas: {', '.join(materia.previas)}")
        print("-" * 40)

class Curso:
    
    """
    Representa un curso dictado en un año y semestre determinado, asociado a una unidad curricular.

    Atributos:
        codigo_uc (str): Código de la unidad curricular asociada.
        nombre_uc (str): Nombre de la unidad curricular.
        año (int): Año en que se dicta el curso (mayor a 2000).
        semestre (int): Semestre en que se dicta el curso (entre 1 y 10).
        estudiantes (list of Estudiante): Lista de estudiantes inscritos en el curso.
        archivo_csv (str): Ruta al archivo CSV que contiene la información del curso.
        uc (UnidadCurricular): Objeto de unidad curricular vinculada al curso, obtenido del plan.
    """

    def __init__(self, codigo_uc, año, semestre, plan: PlanDeEstudio):
        """
        Inicializa una nueva instancia de la clase Curso.

        Args:
            codigo_uc (str): Código de la unidad curricular.
            año (int): Año del curso (debe ser mayor a 2000).
            semestre (int): Semestre del curso (entre 1 y 10).
            plan (PlanDeEstudio): Objeto que contiene todas las unidades curriculares disponibles.

        Raises:
            TypeError: Si alguno de los parámetros no tiene el tipo esperado.
            ValueError: Si el año es inválido, el semestre está fuera de rango,
                        o el código no coincide con el semestre declarado.
        """
        try:
            if not isinstance(codigo_uc, str):
                raise TypeError("El código de unidad curricular debe ser un string.")

            if not isinstance(año, int) or año < 2000:
                raise ValueError("El año debe ser un número entero válido (mayor a 2000).")

            if not isinstance(semestre, int) or not (1 <= semestre <= 10):
                raise ValueError("El semestre debe ser un entero entre 1 y 10.")

            if not isinstance(plan, PlanDeEstudio):
                raise TypeError("Plan inexistente")

            # Buscar la unidad curricular en el plan
            self.uc = plan.buscar_uc_por_codigo(codigo_uc) 
            if not self.uc:
                raise ValueError(f"No se encontró la unidad curricular con código {codigo_uc} en el plan de estudios.")

            # Verificar que el código coincida con el semestre (por ejemplo: UC3S2 -> semestre 2)
            match = re.search(r"S(\d+)$", self.uc.codigo)
            if match:
                semestre_codificado = int(match.group(1))
                if semestre != semestre_codificado:
                    raise ValueError(f"El semestre proporcionado ({semestre}) no coincide con el código ({self.uc.codigo}).")

            # Atributos principales
            self.codigo_uc = self.uc.codigo
            self.nombre_uc = self.uc.nombre
            self.año = año
            self.semestre = semestre
            self.estudiantes = []
            self.archivo_csv = f"curso_{self.codigo_uc}_{self.año}_sem{self.semestre}.csv"

            self.generar_csv()
            print(f"✔ Curso creado para {self.nombre_uc} ({self.codigo_uc}) - {self.año}, Semestre {self.semestre}")

        except (ValueError, TypeError) as e:
            print(f"✖ Error al crear el curso: {e}")
            self.uc = None  # para impedir operaciones posteriores

    def curso_valido(self):
        """
        Indica si el curso se creó correctamente.

        Returns:
            bool: True si el curso tiene una unidad curricular asociada, False en caso contrario.
        """
        return self.uc is not None

    def generar_csv(self):
        """
        Genera un archivo CSV inicial del curso con los datos principales y encabezados.
        """
        try:
            with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["Código UC", "Nombre UC", "Año", "Semestre", "Estudiantes Inscritos"])
                writer.writerow([self.codigo_uc, self.nombre_uc, self.año, self.semestre, ""])
        except Exception as e:
            print(f"✖ Error al generar el archivo CSV: {e}")

    def agregar_estudiante(self, estudiante):

        """
        Agrega un estudiante al curso, si no está ya inscrito.

        Args:
            estudiante (Estudiante): Objeto de tipo Estudiante.

        Raises:
            TypeError: Si el objeto no es una instancia de Estudiante.
        """

        if not self.curso_valido():
            print("✖ Este curso no es válido. No se puede agregar estudiantes.")
            return

        try:
            if not isinstance(estudiante, Estudiante):
                raise TypeError(f"{estudiante} no es un Estudiante")

            if estudiante not in self.estudiantes:
                self.estudiantes.append(estudiante)
                self.actualizar_csv()
                print(f"✔ Estudiante {estudiante.nombre} {estudiante.apellido} agregado al curso.")
            else:
                print("⚠ El estudiante ya está inscrito en este curso.")
        except TypeError as e:
            print(f"✖ Error al agregar estudiante: {e}")

    def actualizar_csv(self):
        """
        Actualiza el archivo CSV con la lista actualizada de estudiantes inscritos.

        """
        try:
            with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["Código UC", "Nombre UC", "Año", "Semestre", "Estudiantes Inscritos"])
                nombres_estudiantes = [f"{e.nombre} {e.apellido}" for e in self.estudiantes]
                writer.writerow([self.codigo_uc, self.nombre_uc, self.año, self.semestre, ', '.join(nombres_estudiantes)])
        except Exception as e:
            print(f"✖ Error al actualizar el CSV: {e}")

    def mostrar_estudiantes(self):
        """
        Muestra los estudiantes inscritos en el curso por consola.
        """
        if not self.curso_valido():
            print("✖ Este curso no es válido. No hay estudiantes que mostrar.")
            return

        if not self.estudiantes:
            print("No hay estudiantes inscritos en este curso.")
        else:
            print(f"Estudiantes inscritos en {self.nombre_uc}:")
            for e in self.estudiantes:
                print(f"- {e.nombre} {e.apellido}")

class InstanciaDeExamen:
    """
    Representa una instancia de examen para una unidad curricular específica en una fecha y hora determinadas.

    Atributos:
        codigo_uc (str): Código de la unidad curricular del examen.
        fecha (str): Fecha en formato 'YYYY-MM-DD'.
        hora (str): Hora en formato 'HH:MM'.
        estudiantes (list of Estudiante): Lista de estudiantes inscritos en el examen.
    """
    def __init__(self, codigo_uc, fecha, hora):
        """
        Inicializa una nueva instancia del examen con su código UC, fecha y hora.

        Args:
            codigo_uc (str): Código de la unidad curricular.
            fecha (str): Fecha del examen (formato 'YYYY-MM-DD').
            hora (str): Hora del examen (formato 'HH:MM').
        """
        self.codigo_uc = codigo_uc
        self.fecha = fecha
        self.hora = hora
        self.estudiantes = []  # Lista para almacenar instancias de estudiantes

        self.generar_csv()

    def generar_csv(self):
        """
        Genera un archivo CSV con la información de la instancia del examen, incluyendo los estudiantes inscritos.
        El archivo se crea con nombre 'examen_<codigo_uc>_<fecha>.csv'.
        """
        # Crear el nombre del archivo basado en el código de la UC y la fecha
        archivo_csv = f"examen_{self.codigo_uc}_{self.fecha}.csv"
        # Convertir la fecha y hora en un formato adecuado
        fecha_hora = f"{self.fecha} {self.hora}" 
        
        # Crear o sobrescribir el archivo CSV con la información de la instancia de examen
        with open(archivo_csv, mode='w', newline='') as file: # Abre (o crea) el archivo CSV en modo escritura ('w'), sin agregar líneas nuevas adicionales (newline='')
            writer = csv.writer(file)   # Crea un escritor CSV que escribirá en el archivo abierto
            # Escribe la primera fila del archivo con los nombres de las columnas
            writer.writerow(["Código UC", "Fecha y Hora", "Estudiantes Inscritos"])
            writer.writerow([self.codigo_uc, fecha_hora, ', '.join([str(estudiante) for estudiante in self.estudiantes])]) # para cada estudiante en la lista de estudiantes, paso estudiante a str y une cada estudiante a una cadena de texto separada con ,
        
        print(f"Examen para UC {self.codigo_uc} creado en el archivo {archivo_csv} con éxito.")

    def agregar_estudiante(self, estudiante):
        """
        Inscribe a un estudiante en la instancia del examen, si está regular en la unidad curricular correspondiente.

        Args:
            estudiante (Estudiante): Objeto estudiante a inscribir.

        Validaciones:
            - Verifica que el objeto sea una instancia de Estudiante.
            - Verifica que el estudiante esté regular en la UC del examen.
            - Verifica que el estudiante no esté ya inscripto.

        Actualiza el archivo CSV al agregar exitosamente un estudiante.
        """
        # Verificar si el objeto es una instancia válida de la clase Estudiante
        if isinstance(estudiante, Estudiante): #Primero verifico que el estudiante sea un objeto estudiante
            # Verificar si el estudiante está regular en la UC correspondiente
            uc_en_registro = None 
            for uc in estudiante.ucs_regulares: #para cada uc en las ucs en las que el estudiante esta regular
                if uc.codigo == self.codigo_uc: #si el codigo de la uc es igual al codigo de la uc que se hace el examen
                    uc_en_registro = uc #asigno la uc
                    break

            if uc_en_registro: #si uc en registro no es None
                # Verificar si el estudiante ya está inscrito en el examen
                if estudiante not in self.estudiantes: #y el estudiante no esta en la lista de estudiantes inscriptos al examen
                    self.estudiantes.append(estudiante) #lo agrego
                    self.actualizar_csv()  # Actualizar el CSV con la lista de estudiantes
                    print(f"Estudiante {estudiante.nombre} {estudiante.apellido} inscrito al examen de {uc_en_registro.nombre} con éxito.")
                else: #si ya estaba inscripto
                    print(f"El estudiante {estudiante.nombre} {estudiante.apellido} ya está inscrito en el examen.")
            else: #si no estaba regular
                print(f"El estudiante {estudiante.nombre} {estudiante.apellido} no está regular en la UC {self.codigo_uc}. No puede inscribirse al examen.")
        else:
            print("El objeto proporcionado no es una instancia válida de la clase Estudiante.") #si no es objeto estudiante 

    def actualizar_csv(self): #esto cada vez q un estudiante nuevo se inscribe 
        """
        Actualiza el archivo CSV de la instancia de examen con la lista actual de estudiantes inscritos.
        """
        # Crear el nombre del archivo basado en el código de la UC y la fecha
        archivo_csv = f"examen_{self.codigo_uc}_{self.fecha}.csv" #el nombre del archivo
        # Convertir la fecha y hora en un formato adecuado
        fecha_hora = f"{self.fecha} {self.hora}"
        
        # Sobrescribir el archivo CSV con la lista actualizada de estudiantes inscritos
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Código UC", "Fecha y Hora", "Estudiantes Inscritos"])
            writer.writerow([self.codigo_uc, fecha_hora, ', '.join([str(estudiante) for estudiante in self.estudiantes])])
        
        print(f"Archivo CSV actualizado con los estudiantes inscritos en {archivo_csv}.")

    def mostrar_estudiantes(self):
        """
        Muestra por consola la lista de estudiantes inscritos en la instancia del examen.
        """
        # Mostrar la lista de estudiantes inscritos
        if not self.estudiantes:
            print("No hay estudiantes inscritos en este examen.")
        else:
            print("Estudiantes inscritos:")
            for estudiante in self.estudiantes:
                print(estudiante)

class Estudiante(Persona):
    """
    Representa a un estudiante, heredando de la clase Persona.

    Atributos:
        _cedula (str): Cédula de identidad del estudiante.
        año_ingreso (int): Año en que ingresó a la carrera.
        plan (PlanDeEstudio): Plan de estudios asociado.
        ucs_aprobadas (list): Lista de unidades curriculares aprobadas.
        ucs_regulares (list): Lista de unidades curriculares regulares.
        ucs_a_examen (list): Lista de unidades curriculares para las que se ha inscripto a examen.
        ucs_cursando (list): Lista de unidades curriculares que está cursando actualmente.
    """
    def __init__(self, nombre, apellido, cedula, año_ingreso, plan: PlanDeEstudio):
        """
        Inicializa una instancia de Estudiante.

        Args:
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            cedula (str): Cédula de identidad.
            año_ingreso (int): Año de ingreso.
            plan (PlanDeEstudio): Plan de estudio que cursa el estudiante.

        Raises:
            ValueError: Si la cédula no es un número entero válido.
        """
        super().__init__(nombre, apellido)
        self._cedula=cedula
        try:
            cedula = int(cedula)
        except (ValueError, TypeError):
            raise ValueError("La cédula debe ser un número entero válido.")
        self.año_ingreso = año_ingreso
        self.plan = plan
        self.ucs_aprobadas = []
        self.ucs_regulares = []
        self.ucs_a_examen = []
        self.ucs_cursando = []
    @property
    def cedula(self):
        """Devuelve la cédula del estudiante."""
        return self._cedula
    
    def __str__(self):
        """Representación textual del estudiante."""
        return f"{self.nombre} {self.apellido} {self.cedula}"
    
    def ver_ucs_aprobadas(self): 
        """Imprime por pantalla las unidades curriculares aprobadas."""
        if not self.ucs_aprobadas: # si no hay ucs_aprobadas 
            print("No tenés UCs aprobadas.")
        else:
            print("UCs aprobadas:")
            for uc in self.ucs_aprobadas: #para cada uc en la lista
                print(f"- {uc.codigo}: {uc.nombre}") #como es una uc puedo usar los atributos de la clas uc
    
    def ver_ucs_regulares(self):
        """Imprime por pantalla las unidades curriculares regulares."""
        if not self.ucs_regulares:
            print("No estás regular en ninguna UC.")
        else:
            print("UCs regulares:")
            for uc in self.ucs_regulares:
                print(f"- {uc.codigo}: {uc.nombre}")
    
    def ver_ucs_cursando(self):
        """Imprime por pantalla las unidades curriculares que está cursando."""
        if not self.ucs_cursando:
            print("No estás cursando ninguna UC.")
        else:
            print("UCs que estás cursando:")
            for uc in self.ucs_cursando:
                print(f"- {uc.codigo}: {uc.nombre}")
    
    def _puede_inscribirse(self, codigo_uc):
        """
        Verifica si el estudiante puede inscribirse a una unidad curricular.

        Args:
            codigo_uc (str): Código de la unidad curricular.

        Returns:
            bool: True si puede inscribirse, False en caso contrario.
        """
        uc = self.plan.buscar_uc_por_codigo(codigo_uc) #obtengo la uc a partir del codigo de la uc
        codigos_aprobadas = [u.codigo for u in self.ucs_aprobadas] #guardo en una lista los codigos de las uc que el alumno tiene aprobadas
        codigos_cursando = [u.codigo for u in self.ucs_cursando] #guardo en una lista los codigos de las uc que el alumno esta cursando
        previas_faltantes = [] 
        for previa_codigo in uc.previas: #para cada codigo de previa en la lista de previas de la uc
            previa = self.plan.buscar_uc_por_codigo(previa_codigo) #obtengo la uc previa a partir del codigo
            if previa.codigo not in codigos_aprobadas: #si el codigo de la previa no esta en las materias aprobadas del paciente
                previas_faltantes.append(previa) #guardo esa previa en la lista
        
        if previas_faltantes: #en la lista de previas que el alumno no tiene
            print(f"No puedes inscribirte en la UC {uc.nombre} porque te faltan las siguientes previas:")
            for previa in previas_faltantes:
                print(f"- {previa.nombre}") #imprimo el nombre de cada previa que imposibilita al alumno cursar la uc
            return False #retorno falso para poder usar este metodo en otros metodos
        
        if uc.codigo in codigos_cursando: #si el codigo de la uc que el alumno quiere cursar esta dentro de las materias que esta cursando
            print("Ya está cursando esta UC.")
            return False
        
        if uc.codigo in codigos_aprobadas: #si el codigo de la uc que el alumno quiere cursar esta dentro de las materias que ya aprobo
            print("Ya aprobó esta UC.")
            return False
        return True
    
    def inscribirse_a_examen(self, instancia_examen: InstanciaDeExamen): 
        """
        Inscribe al estudiante a una instancia de examen si cumple con los requisitos.

        Args:
            instancia_examen (InstanciaDeExamen): Examen al que desea inscribirse.
        """
        if isinstance(instancia_examen, InstanciaDeExamen): #si el examen al q se quiere inscribir es un objeto de instancia de examen
            codigo_uc = instancia_examen.codigo_uc #esta es la uc al que el alumno se quiere inscribir al examen
            for uc in self.ucs_regulares: #para las uc dentro de las ucs que el alumno tiene regulares
                if uc.codigo == codigo_uc: #si el codigo de esa uc es igual al codigo de la uc a examen
                    instancia_examen.agregar_estudiante(self) #inscribo al estudiante al examen
                    print(f"Estas inscripto al examen de {uc.nombre}")
                    return
            for uc in self.ucs_aprobadas:
                if uc.codigo ==codigo_uc:
                    print("Esa materia ya la aprobaste naboleti")
                    return
            print(f"No cumple con los requisitos para inscribirse a {codigo_uc}")
        else:
            print("Instancia de examen no válida.")
    
    def inscribirse_a_curso(self, curso: Curso):
        """
        Inscribe al estudiante a un curso si cumple con los requisitos.

        Args:
            curso (Curso): Curso al que desea inscribirse.
        """
        if not curso.curso_valido():
            print("Curso no válido.")
            return
        if self._puede_inscribirse(curso.codigo_uc):
            self.ucs_cursando.append(curso.uc)
            curso.agregar_estudiante(self)  
    
    def ver_plan(self):
        """Muestra el plan de estudio del estudiante."""
        self.plan.ver()

class Coordinadora(Persona):
    """
    Representa a una persona que cumple el rol de coordinadora académica, 
    encargada de gestionar planes de estudio, cursos y exámenes.

    Atributos heredados:
        - nombre (str): Nombre de la persona.
        - apellido (str): Apellido de la persona.
    """
    def __init__(self, nombre, apellido):
        """
        Inicializa una instancia de la clase Coordinadora.

        Args:
            nombre (str): Nombre de la coordinadora.
            apellido (str): Apellido de la coordinadora.
        """
        super().__init__(nombre, apellido)

    def crear_plan(self, nombre_plan, ruta_json):
        """
        Crea un nuevo plan de estudio con el nombre y la ruta especificados.

        Args:
            nombre_plan (str): Nombre del plan de estudio.
            ruta_json (str): Ruta al archivo JSON con los detalles del plan.

        Returns:
            PlanDeEstudio: Un objeto PlanDeEstudio creado.
        """
        plan = PlanDeEstudio(nombre_plan, ruta_json)
        print(f"{self.nombre} ha creado el plan '{nombre_plan}'.")
        return plan
        
    def inscribir_a_examen(self, estudiante, examen):
        """
        Inscribe a un estudiante a un examen si cumple con los requisitos.

        Args:
            estudiante (Estudiante): Estudiante que desea inscribirse al examen.
            examen (InstanciaDeExamen): Examen al que desea inscribirse.
        """
        if isinstance(estudiante, Estudiante):
            uc = estudiante.plan.buscar_uc_por_codigo(examen.codigo_uc)
            if uc and uc in estudiante.ucs_regulares:
                estudiante.inscribirse_a_examen(examen)
            else:
                print(f"{estudiante.nombre} no está regular en la UC {uc.codigo}, no puede inscribirse al examen.")
        else:
            print("No existe estudiante.")

        
    def inscribir_a_curso(self, estudiante, curso):
        """
        Inscribe a un estudiante a un curso si cumple con los requisitos.

        Args:
            estudiante (Estudiante): Estudiante que desea inscribirse al curso.
            curso (Curso): Curso al que desea inscribirse.
        """
        if not isinstance(estudiante, Estudiante):
            print("El objeto proporcionado no es un Estudiante.")
            return

        if not isinstance(curso, Curso) or not curso.curso_valido():
            print("El curso no es válido.")
            return

        if estudiante._puede_inscribirse(curso.codigo_uc):
            estudiante.ucs_cursando.append(curso.uc)
            curso.agregar_estudiante(estudiante)
        else:
            print(f"{estudiante.nombre} no puede inscribirse al curso {curso.codigo_uc}")

    def ver_plan(self, plan):
        """
        Muestra el plan de estudio de un estudiante.

        Args:
            plan (PlanDeEstudio): El plan de estudio a mostrar.
        """
        plan.ver()

    def ver_estudiantes_curso(self,curso):
        """
        Muestra los estudiantes inscritos en un curso.

        Args:
            curso (Curso): Curso del que se desea ver los estudiantes inscritos.
        """
        curso.mostrar_estudiantes()
    
    def ver_estudiantes_examen(self,examen):
        """
        Muestra los estudiantes inscritos en un examen.

        Args:
            examen (InstanciaDeExamen): Examen del que se desea ver los estudiantes inscritos.
        """
        examen.mostrar_estudiantes()
    
    def quitar_uc_regular(self, estudiante, codigo_uc):
        """
        Elimina una unidad curricular de las regulares de un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le eliminará la UC regular.
            codigo_uc (str): Código de la unidad curricular a eliminar.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc in estudiante.ucs_regulares:
            estudiante.ucs_regulares.remove(uc)
            print(f"✔ {uc.nombre} fue removida de las UCs regulares de {estudiante.nombre}.")
        else:
            print(f"✖ {uc.nombre} no está en las UCs regulares de {estudiante.nombre}.")
    
    def quitar_uc_aprobada(self, estudiante, codigo_uc):
        """
        Elimina una unidad curricular de las aprobadas de un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le eliminará la UC regular.
            codigo_uc (str): Código de la unidad curricular a eliminar.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc in estudiante.ucs_aprobadas:
            estudiante.ucs_aprobadas.remove(uc)
            print(f"✔ {uc.nombre} fue removida de las UCs aprobadas de {estudiante.nombre}.")
        else:
            print(f"✖ {uc.nombre} no está en las UCs aprobadas de {estudiante.nombre}.")
                
    def agregar_uc_aprobada(self, estudiante, codigo_uc):
        """
        Añade una unidad curricular aprobada a un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le agregará la UC aprobada.
            codigo_uc (str): Código de la unidad curricular aprobada.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc not in estudiante.ucs_aprobadas:
            estudiante.ucs_aprobadas.append(uc)
            print(f"✔ {uc.nombre} fue agregada correctamente a las UCs aprobadas de {estudiante.nombre}.")
        else:
            print(f"✖ {estudiante.nombre} ya había aprobado la UC {uc.nombre}.")
    
    def agregar_uc_regular(self, estudiante, codigo_uc):
        """
        Añade una unidad curricular regular a un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le agregará la UC aprobada.
            codigo_uc (str): Código de la unidad curricular aprobada.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc not in estudiante.ucs_regulares:
            estudiante.ucs_regulares.append(uc)
            print(f"✔ {uc.nombre} fue agregada correctamente a las UCs regulares de {estudiante.nombre}.")
        else:
            print(f"✖ {estudiante.nombre} ya estaba regular en la UC {uc.nombre}.")


    def crear_curso(self, codigo_uc, año, semestre, plan):
        """
        Crea un curso para una unidad curricular en un determinado año y semestre.

        Args:
            codigo_uc (str): Código de la unidad curricular.
            año (int): Año en que se ofrecerá el curso.
            semestre (str): Semestre en el que se ofrecerá el curso (por ejemplo, '1' o '2').
            plan (PlanDeEstudio): Plan de estudio al que pertenece la unidad curricular.

        Returns:
            Curso: El curso creado si es válido, o None si no es válido.
        """

        curso = Curso(codigo_uc, año, semestre, plan)
        if curso.curso_valido():
            return curso
        else:
            print("No se pudo crear el curso.")
            return None
    
    def crear_instancia_examen(self, codigo_uc, fecha,hora, plan):
        """
        Crea una instancia de examen para una unidad curricular.

        Args:
            codigo_uc (str): Código de la unidad curricular.
            fecha (str): Fecha del examen (formato 'DD/MM/YYYY').
            hora (str): Hora del examen (formato 'HH:MM').
            plan (PlanDeEstudio): Plan de estudio al que pertenece la unidad curricular.

        Returns:
            InstanciaDeExamen: La instancia de examen creada si la unidad curricular existe en el plan, o None si no se encuentra.
        """
        uc = plan.buscar_uc_por_codigo(codigo_uc)
        if uc:
            examen = InstanciaDeExamen(codigo_uc, fecha,hora)
            return examen
        else:
            print(f"No se encontró la unidad curricular {codigo_uc} en el plan.")
            return None

class Secretaria(Persona):
    def __init__(self, nombre, apellido):
        super().__init__(nombre, apellido)

    def inscribir_a_examen(self, estudiante, examen):
        """
        Inscribe a un estudiante a un examen si cumple con los requisitos.

        Args:
            estudiante (Estudiante): Estudiante que desea inscribirse al examen.
            examen (InstanciaDeExamen): Examen al que desea inscribirse.
        """
        if isinstance(estudiante, Estudiante):
            uc = estudiante.plan.buscar_uc_por_codigo(examen.codigo_uc)
            if uc and uc in estudiante.ucs_regulares:
                estudiante.inscribirse_a_examen(examen)
            else:
                print(f"{estudiante.nombre} no está regular en la UC {uc.codigo}, no puede inscribirse al examen.")
        else:
            print("No existe estudiante.")

        
    def inscribir_a_curso(self, estudiante, curso):
        """
        Inscribe a un estudiante a un curso si cumple con los requisitos.

        Args:
            estudiante (Estudiante): Estudiante que desea inscribirse al curso.
            curso (Curso): Curso al que desea inscribirse.
        """
        if not isinstance(estudiante, Estudiante):
            print("El objeto proporcionado no es un Estudiante.")
            return

        if not isinstance(curso, Curso) or not curso.curso_valido():
            print("El curso no es válido.")
            return

        if estudiante._puede_inscribirse(curso.codigo_uc):
            estudiante.ucs_cursando.append(curso.uc)
            curso.agregar_estudiante(estudiante)
        else:
            print(f"{estudiante.nombre} no puede inscribirse al curso {curso.codigo_uc}")

    def ver_plan(self, plan):
        """
        Muestra el plan de estudio de un estudiante.

        Args:
            plan (PlanDeEstudio): El plan de estudio a mostrar.
        """
        plan.ver()

    def ver_estudiantes_curso(self,curso):
        """
        Muestra los estudiantes inscritos en un curso.

        Args:
            curso (Curso): Curso del que se desea ver los estudiantes inscritos.
        """
        curso.mostrar_estudiantes()
    
    def ver_estudiantes_examen(self,examen):
        """
        Muestra los estudiantes inscritos en un examen.

        Args:
            examen (InstanciaDeExamen): Examen del que se desea ver los estudiantes inscritos.
        """
        examen.mostrar_estudiantes()
    
    def quitar_uc_regular(self, estudiante, codigo_uc):
        """
        Elimina una unidad curricular de las regulares de un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le eliminará la UC regular.
            codigo_uc (str): Código de la unidad curricular a eliminar.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc in estudiante.ucs_regulares:
            estudiante.ucs_regulares.remove(uc)
            print(f"✔ {uc.nombre} fue removida de las UCs regulares de {estudiante.nombre}.")
        else:
            print(f"✖ {uc.nombre} no está en las UCs regulares de {estudiante.nombre}.")
    
    def quitar_uc_aprobada(self, estudiante, codigo_uc):
        """
        Elimina una unidad curricular de las aprobadas de un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le eliminará la UC regular.
            codigo_uc (str): Código de la unidad curricular a eliminar.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc in estudiante.ucs_aprobadas:
            estudiante.ucs_aprobadas.remove(uc)
            print(f"✔ {uc.nombre} fue removida de las UCs aprobadas de {estudiante.nombre}.")
        else:
            print(f"✖ {uc.nombre} no está en las UCs aprobadas de {estudiante.nombre}.")
                
    def agregar_uc_aprobada(self, estudiante, codigo_uc):
        """
        Añade una unidad curricular aprobada a un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le agregará la UC aprobada.
            codigo_uc (str): Código de la unidad curricular aprobada.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc not in estudiante.ucs_aprobadas:
            estudiante.ucs_aprobadas.append(uc)
            print(f"✔ {uc.nombre} fue agregada correctamente a las UCs aprobadas de {estudiante.nombre}.")
        else:
            print(f"✖ {estudiante.nombre} ya había aprobado la UC {uc.nombre}.")
    
    def agregar_uc_regular(self, estudiante, codigo_uc):
        """
        Añade una unidad curricular regular a un estudiante.

        Args:
            estudiante (Estudiante): Estudiante al que se le agregará la UC aprobada.
            codigo_uc (str): Código de la unidad curricular aprobada.
        """
        uc = estudiante.plan.buscar_uc_por_codigo(codigo_uc)
        if uc not in estudiante.ucs_regulares:
            estudiante.ucs_regulares.append(uc)
            print(f"✔ {uc.nombre} fue agregada correctamente a las UCs regulares de {estudiante.nombre}.")
        else:
            print(f"✖ {estudiante.nombre} ya estaba regular en la UC {uc.nombre}.")
