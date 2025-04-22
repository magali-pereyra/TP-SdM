class UnidadCurricular:
    def __init__(self, codigo, nombre, creditos, previas):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.previas = previas

import json
import re 
class PlanDeEstudio:
    def __init__(self, nombre_plan, ruta_json):
        self.nombre_plan = nombre_plan
        self.materias = []
        self._cargar_desde_json(ruta_json)

    def _agregar_materia(self, unidad_curricular):
        """Método privado para agregar una materia (uso interno)."""
        self.materias.append(unidad_curricular)

    def agregar_materia_manual(self, nombre, creditos, semestre, previas=None):
        """
        Método público para agregar una unidad curricular de forma manual.
        Realiza validaciones antes de agregarla.
        """
        # Validar que se proporcionen todos los argumentos necesarios
        if not nombre or creditos is None or semestre is None:
            raise ValueError("Todos los campos (nombre, créditos y semestre) son obligatorios.")
        
        # Validar que el semestre esté entre 1 y 10
        if semestre < 1 or semestre > 10:
            raise ValueError("El semestre debe estar entre 1 y 10.")

        # Contar cuántas materias ya existen en el semestre indicado
        num_materias_semestre = sum(1 for uc in self.materias if uc.codigo.endswith(f"S{semestre}"))
        
        # Generar el código para la nueva materia
        codigo = f"UC{num_materias_semestre + 1}S{semestre}"

        # Si no se especifican previas, asignar lista vacía
        if previas is None:
            previas = []

        # Crear la UnidadCurricular y agregarla a la lista de materias
        uc = UnidadCurricular(
            codigo=codigo,
            nombre=nombre.lower().capitalize(),
            creditos=creditos,
            previas=previas
        )
        self._agregar_materia(uc)
        print(f"Materia agregada manualmente: {codigo} - {uc.nombre}")
        
    def quitar_materia(self, codigo):
        """Método para quitar una materia dado su código."""
        materia = self.buscar_uc_por_codigo(codigo)
        if materia:
            self.materias.remove(materia)
            print(f"✔ Materia eliminada: {codigo} - {materia.nombre}")
        else:
            print(f"Materia con el código {codigo} no encontrada.")

    def buscar_uc_por_codigo(self, codigo):
        for uc in self.materias:
            if uc.codigo == codigo:
                return uc
        return None

    def _cargar_desde_json(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        for semestre, materias in datos.items():
            for codigo, materia in materias.items():
                uc = UnidadCurricular(
                    codigo=codigo,
                    nombre=materia["nombre"],
                    creditos=materia["creditos"],
                    previas=materia["previas"]
                )
                self._agregar_materia(uc)

    def ver(self):
        print(f"Plan de Estudio: {self.nombre_plan}")
        print("-" * 40)
        for materia in self.materias:
            print(f"{materia.codigo} - {materia.nombre} ({materia.creditos} créditos)")
            if materia.previas:
                print(f"  ↳ Previas: {', '.join(materia.previas)}")
        print("-" * 40)
