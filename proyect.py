import tkinter as tk
from tkinter import messagebox, simpledialog
import re

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def validar_expresion(expresion):
    return re.match(r'^[0-9\+\-\*\/\^\(\)\s√∛a-zA-Z]*$', expresion)

# Función para construir el árbol binario
def construir_arbol(expresion):
    if len(expresion) == 0:
        return None

    operadores = {'+', '-', '*', '/', '^', '√', '∛'}

    idx = -1
    min_precedencia = float('inf')
    parentesis = 0
    for i in range(len(expresion)):
        if expresion[i] == '(':
            parentesis += 1
        elif expresion[i] == ')':
            parentesis -= 1
        elif expresion[i] in operadores and parentesis == 0:
            precedencia = obtener_precedencia(expresion[i])
            if precedencia <= min_precedencia:
                min_precedencia = precedencia
                idx = i

    if idx == -1:
        if expresion.startswith('(') and expresion.endswith(')'):
            return construir_arbol(expresion[1:-1])
        else:
            return Nodo(expresion)

    nodo = Nodo(expresion[idx])
    nodo.izquierda = construir_arbol(expresion[:idx])
    nodo.derecha = construir_arbol(expresion[idx+1:])

    return nodo

def obtener_precedencia(operador):
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '√': 4 }
    return precedencia.get(operador, 0)

# Función para evaluar la expresión matemática
def evaluar_expresion(nodo, variables):
    if nodo is None:
        return None
    if nodo.valor.isdigit() or re.match(r'^\d+\.\d+$', nodo.valor):
        return float(nodo.valor)
    if nodo.valor.isalpha():
        if nodo.valor in variables:
            return variables[nodo.valor]
        else:
            messagebox.showinfo("Error", f"La variable '{nodo.valor}' no ha sido definida")
            return None

    izquierda = evaluar_expresion(nodo.izquierda, variables)
    derecha = evaluar_expresion(nodo.derecha, variables)

    if izquierda is None or derecha is None:
        return None

    if nodo.valor == '+':
        return izquierda + derecha
    elif nodo.valor == '-':
        return izquierda - derecha
    elif nodo.valor == '*':
        return izquierda * derecha
    elif nodo.valor == '/':
        if derecha == 0:
            messagebox.showinfo("Error", "No se puede dividir entre cero")
            return None
        return izquierda / derecha
    elif nodo.valor == '^':
        return izquierda ** derecha
    elif nodo.valor == '√':
        return izquierda ** (1/derecha)
    elif nodo.valor == '∛':
        return izquierda ** (1/3)

# Función para recorrer el árbol en postorden
def postorden(nodo, resultado):
    if nodo:
        postorden(nodo.izquierda, resultado)
        postorden(nodo.derecha, resultado)
        resultado.append(nodo.valor)

def calcular():
    expresion = entrada_expresion.get()
    if not validar_expresion(expresion):
        messagebox.showerror("Error", "La expresion contiene caracteres no permitidos")
        return

    variables = re.findall(r'[a-zA-Z]+', expresion)
    variables = set(variables)

    if variables:
        valores = {}
        for var in variables:
            valor = simpledialog.askstring("Valor de variable", f"Ingrese el valor de '{var}':")
            if valor is None:
                return
            try:
                valores[var] = float(valor)
            except ValueError:
                messagebox.showerror("Error", f"El valor ingresado para '{var}' no es valido")
                return

        arbol = construir_arbol(expresion)
        if arbol:
            resultado = evaluar_expresion(arbol, valores)
            if resultado is not None:
                messagebox.showinfo("Resultado", f"El resultado es: {resultado}")
                recorrido_postorden = []
                postorden(arbol, recorrido_postorden)
                messagebox.showinfo("Recorrido Postorden", f"Recorrido Postorden: {' '.join(recorrido_postorden)}")
        else:
            return
    else:
        arbol = construir_arbol(expresion)
        if arbol:
            resultado = evaluar_expresion(arbol, {})
            if resultado is not None:
                messagebox.showinfo("Resultado", f"El resultado es: {resultado}")
                recorrido_postorden = []
                postorden(arbol, recorrido_postorden)
                messagebox.showinfo("Recorrido Postorden", f"Recorrido Postorden: {' '.join(recorrido_postorden)}")
        else:
            return

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Expresiones Matematicas")

# caja de texto para la expresión
etiqueta_expresion = tk.Label(ventana, text="Expresion:")
etiqueta_expresion.pack()
entrada_expresion = tk.Entry(ventana, width=50)
entrada_expresion.pack()

# botón "Calcular"
boton_calcular = tk.Button(ventana, text="Calcular", command=calcular)
boton_calcular.pack()

ventana.mainloop()
