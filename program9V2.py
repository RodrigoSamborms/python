"""
Directorio Telefónico Optimizado - Versión con HashMap
========================================================

MEJORA CLAVE: Cambio de complejidad temporal O(n²) a O(n)

Versión anterior:
- Usaba una lista de diccionarios: [{"nombre": "sam", "telefono": "123"}, ...]
- Cada consulta requería recorrer TODA la lista hasta encontrar el nombre
- Complejidad: O(n) por cada consulta × n consultas = O(n²)
- Para 10,000 entradas: ~100,000,000 operaciones de comparación

Versión optimizada (esta):
- Usa un diccionario directo (HashMap/HashTable): {"sam": "123", "tom": "456", ...}
- Cada consulta accede directamente a la clave usando hashing
- Complejidad: O(1) por consulta × n consultas = O(n)
- Para 10,000 entradas: ~10,000 operaciones de hash lookup

Ganancia: Para n=10,000 pasamos de ~100M operaciones a ~10K (10,000x más rápido)
"""

import sys


def main() -> None:
    """
    Función principal que procesa el directorio telefónico y las consultas.
    
    Flujo del programa:
    1. Leer TODA la entrada de una vez (eficiente para grandes volúmenes)
    2. Construir el directorio como diccionario {nombre: telefono}
    3. Procesar todas las consultas usando acceso O(1)
    4. Escribir TODA la salida de una vez (evita múltiples print())
    """
    
    # ============================================================================
    # PASO 1: LECTURA EFICIENTE DE ENTRADA
    # ============================================================================
    # sys.stdin.buffer.read() es MÁS RÁPIDO que múltiples input() porque:
    # - Lee TODO el stream de entrada en UNA SOLA operación del sistema operativo
    # - input() hace una llamada al SO por cada línea (overhead significativo)
    # - buffer.read() trabaja con bytes crudos (más rápido que strings)
    # - splitlines() divide por '\n' eficientemente en memoria
    data = sys.stdin.buffer.read().splitlines()
    
    # Validación: si no hay datos de entrada, terminar inmediatamente
    if not data:
        return

    # ============================================================================
    # PASO 2: PARSEO DE LA CANTIDAD DE ENTRADAS
    # ============================================================================
    # Primera línea contiene 'n': número de entradas del directorio Y consultas
    # .strip() elimina espacios/tabs/newlines al inicio y final
    # Ejemplo: b'3\n' -> b'3' -> 3
    n = int(data[0].strip())
    
    # ============================================================================
    # PASO 3: CONSTRUCCIÓN DEL DIRECTORIO COMO DICCIONARIO (HashMap)
    # ============================================================================
    # ESTRUCTURA CLAVE: dict en Python usa una tabla hash (hash table)
    # 
    # ¿Cómo funciona internamente un dict?
    # 1. Cuando haces directorio["sam"] = "123", Python:
    #    a) Calcula hash("sam") -> un número entero único
    #    b) Usa ese hash como índice en un arreglo interno
    #    c) Guarda "123" en esa posición
    # 
    # 2. Cuando haces directorio.get("sam"), Python:
    #    a) Calcula hash("sam") de nuevo (mismo número)
    #    b) Va DIRECTO a esa posición del arreglo
    #    c) Retorna el valor "123"
    #    d) TODO esto en tiempo O(1) promedio (constante, independiente de n)
    #
    # Comparación con lista [{"nombre": "sam", ...}, ...]:
    # - Lista: Debes recorrer TODOS los elementos hasta encontrar "sam" -> O(n)
    # - Dict: Vas DIRECTO a la posición usando el hash -> O(1)
    directorio = {}
    
    # idx rastrea la posición actual en el arreglo 'data'
    # Comienza en 1 porque data[0] ya fue usado (contenía 'n')
    idx = 1
    
    # Iterar exactamente 'n' veces para leer las entradas del directorio
    # Usamos '_' porque no necesitamos el valor del iterador (estilo pythónico)
    for _ in range(n):
        # data[idx] es del tipo bytes (ej: b'sam 99912222')
        # .decode() convierte bytes a string: b'sam 99912222' -> 'sam 99912222'
        # .split() sin argumentos divide por espacios: ['sam', '99912222']
        # Desempaquetamos directamente en dos variables (pythónico)
        nombre, telefono = data[idx].decode().split()
        
        # Asignación directa al diccionario: CLAVE = nombre, VALOR = telefono
        # Esta operación es O(1) en promedio (gracias al hashing)
        # Si 'nombre' ya existe, se sobrescribe (comportamiento de dict)
        directorio[nombre] = telefono
        
        # Avanzar al siguiente índice para la próxima iteración
        idx += 1
    
    # En este punto:
    # - idx apunta a la primera consulta (después de las n entradas)
    # - directorio contiene TODOS los pares {nombre: telefono}
    # - Complejidad hasta aquí: O(n) por las n inserciones

    # ============================================================================
    # PASO 4: PROCESAMIENTO DE CONSULTAS
    # ============================================================================
    # Creamos una lista para acumular TODAS las respuestas en memoria
    # Esto es más eficiente que hacer print() por cada consulta porque:
    # - print() hace una llamada al SO por cada línea (lento)
    # - Acumular en lista y escribir una vez es más rápido (batch write)
    salida = []
    
    # data[idx:] crea un slice desde idx hasta el final (todas las consultas)
    # Esto es eficiente porque Python usa slicing sin copiar (referencias)
    for raw_query in data[idx:]:
        # Convertir bytes a string y limpiar espacios/newlines
        # Ejemplo: b'sam\n' -> 'sam\n' -> 'sam'
        consulta = raw_query.decode().strip()
        
        # ====================================================================
        # OPERACIÓN CLAVE: dict.get(key, default=None)
        # ====================================================================
        # .get() es un método pythónico que:
        # - Busca 'consulta' como CLAVE en el diccionario (NO como valor)
        # - Si encuentra la clave, retorna el VALOR asociado (el teléfono)
        # - Si NO encuentra la clave, retorna None (en vez de lanzar KeyError)
        # 
        # Complejidad: O(1) promedio (acceso directo por hash)
        #
        # Alternativas menos pythónicas:
        # - if consulta in directorio: telefono = directorio[consulta]
        # - try: telefono = directorio[consulta] except KeyError: ...
        telefono = directorio.get(consulta)
        
        # Verificar si la consulta NO fue encontrada
        # None es el valor por defecto que retorna .get() cuando la clave no existe
        # Usar 'is None' es más pythónico que '== None' porque:
        # - 'is' compara identidad de objetos (más rápido)
        # - '==' compara valores (puede ser sobrescrito en clases custom)
        if telefono is None:
            salida.append("Not found")
        else:
            # f-string (formatted string literal) es la forma más pythónica y rápida
            # de construir strings desde Python 3.6+
            # Más rápido que: consulta + "=" + telefono
            # Más legible que: "{0}={1}".format(consulta, telefono)
            salida.append(f"{consulta}={telefono}")
    
    # En este punto:
    # - salida contiene TODAS las respuestas como lista de strings
    # - Complejidad del procesamiento de consultas: O(q) donde q = número de consultas
    # - Complejidad TOTAL del programa: O(n + q) que es lineal

    # ============================================================================
    # PASO 5: ESCRITURA EFICIENTE DE SALIDA
    # ============================================================================
    # "\n".join(salida) une todos los strings con saltos de línea
    # Ejemplo: ["sam=123", "Not found"] -> "sam=123\nNot found"
    # 
    # sys.stdout.write() escribe TODO de una vez (más rápido que múltiples print())
    # - Una sola llamada al sistema operativo
    # - Menos overhead que print() que hace flush automático
    # 
    # NOTA: No agregamos '\n' al final porque el problema original no lo requiere
    # Si el juez online espera newline final, cambiar a:
    # sys.stdout.write("\n".join(salida) + "\n")
    sys.stdout.write("\n".join(salida))


# ================================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ================================================================================
# Patrón pythónico estándar que permite:
# - Ejecutar el script directamente: python program9V2.py
# - Importarlo como módulo sin ejecutar: import program9V2
# 
# __name__ es una variable especial que Python asigna automáticamente:
# - Si ejecutas el archivo directamente: __name__ == "__main__"
# - Si importas el archivo: __name__ == "program9V2"
if __name__ == "__main__":
    main()


# ================================================================================
# ANÁLISIS DE COMPLEJIDAD TEMPORAL DETALLADO
# ================================================================================
#
# Versión ANTERIOR (O(n²)):
# -------------------------
# for i in range(n):                    # n iteraciones
#     consulta = queries[i]
#     for j in range(n):                # n iteraciones por cada consulta
#         if consulta == Directorio[j]["nombre"]:
#             ...
# Total: n × n = O(n²)
#
# Versión OPTIMIZADA (O(n)):
# --------------------------
# 1. Lectura: O(n) - leer n líneas
# 2. Construcción dict: O(n) - n inserciones a O(1) cada una
# 3. Consultas: O(q) - q lookups a O(1) cada uno (donde q ≈ n)
# Total: O(n + n + n) = O(n)
#
# EJEMPLO COMPARATIVO:
# --------------------
# Para n = 100,000 entradas y consultas:
# - Versión anterior: ~10,000,000,000 comparaciones (10 mil millones)
# - Versión optimizada: ~300,000 operaciones (300 mil)
# - Mejora: ~33,000x más rápido
#
# Tiempo estimado (CPU moderna a 3GHz):
# - Versión anterior: ~3-5 segundos
# - Versión optimizada: ~0.0001 segundos (100 microsegundos)
#
# ================================================================================
# CONCEPTOS PYTHÓNICOS APLICADOS
# ================================================================================
#
# 1. Type hints (-> None): Documenta que la función no retorna valor
# 2. Docstrings ("""..."""): Documentación estándar de funciones
# 3. f-strings: Interpolación moderna de strings (Python 3.6+)
# 4. dict.get(): Método seguro para acceso a diccionarios
# 5. is None: Comparación por identidad (no por valor)
# 6. str.join(): Forma eficiente de concatenar múltiples strings
# 7. sys.stdin.buffer: I/O de bajo nivel para máximo rendimiento
# 8. Slicing (data[idx:]): Operaciones eficientes con listas
# 9. Unpacking (a, b = tuple): Asignación múltiple en una línea
# 10. if __name__ == "__main__": Patrón estándar de punto de entrada
#
# ================================================================================