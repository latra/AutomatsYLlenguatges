#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Programa destinado a la minimzación de autómatos finitos deterministas.

Hecho por: Marta Albets Mitjaneta y Paula Gallucci Zurita
'''

import time
from copy import deepcopy
def main():
    '''
    Función principal del programa
    '''
    try:
        #Lee de teclado los datos del autómata finito determista no minimizado
        print("Información: Se considera que los estados seran numerados empezando por el 0,")
        print("y que al alfabeto se le han asignado letras empezando por la 'a'.\n")
        status = int(input("Introduce el número de estados: "))
        if status == 0:
            print("¡Se trata de un autómato vacío!")
            exit(0)
        elif status < 0:
            raise ValueError()
        alphabet = int(input("Introduce el tamaño del alfabeto: "))
        if alphabet == 0:
            print("¡Se trata de un alfabeto vacío!")
            exit(0)
        elif alphabet < 0:
            raise ValueError()
        original_status = int(input("Indica el estado inicial: "))
        if original_status > status - 1 or original_status < 0:
            raise ValueError()

        final_status = input("Introduce, separados por espacios, los estados finales: ")
        final_status = final_status.split()
        # Utilizamos el for para transformar los status finales de string a enteros
        for i in range (len(final_status)):
            final_status[i] = int(final_status[i])
            if final_status[i] > status - 1 or final_status[i] < 0:
                raise ValueError()

        #Creamos una transition_matrix que almacenará las transitiones
        transition_matrix =  [[0 for x in range(alphabet)] for y in range(status)] 
        for i in range (status):
            print("Estado " + str(i))
            for x in range (alphabet):
                transition_matrix[i][x] = int(input("Con la letra " + chr(x + 97) +  ": ¿A qué estado (en número) va? "))
                if transition_matrix[i][x] > status - 1:
                    raise ValueError()
    except ValueError:
        print("Los valores introducidos no son válidos.")
        exit(1)
    #Guardamos aquellos status no finales para crear la equivalencia equivalecy 0
    not_final_status = get_not_final_status(transition_matrix, final_status)
    #Copiamos los no finales en otra variable, debido a que "final_status" se verá modificada
    original_final_status = deepcopy(final_status)
    #Creamos la equivalencia equivalecy0
    new_equivalency = ((not_final_status, final_status))

    #Se van calculando las distintas equivalencias hasta que llegar a las dos últimas iguales
    while (True):
        old_equivalency = deepcopy(new_equivalency)
        #Get_equivalencia calcula la siguiente equivalencia
        new_equivalency = get_equivalencia(new_equivalency, transition_matrix)
        #Si la transition_group_compared y la anterior equivalencia son iguales, finaliza el bucle
        if new_equivalency == old_equivalency:
            break
    if has_been_minimized(new_equivalency) == True:
        #Miramos en que conjunto del AFD Minimizado corresponde al transition original_status
        min_ini = get_min_original_status(new_equivalency, original_status)
        print("El estado inicial es: " + str(min_ini))
        #Miramos en que conjunto o conjuntos del AFD Minimizado corresponde/n al final
        min_fin = get_min_final(new_equivalency, original_final_status)
        print("El estado o estados finales son: " + str(min_fin))
        #Finalmente, se guardan las transitiones del AFD Minimizado
        transition = get_transition(transition_matrix, new_equivalency)
        #Se muestran los nuevos status y sus respectivas transitiones
        show_transition(transition, new_equivalency, alphabet)
        exit(0)
    else: 
        print("El autómata introducido ya es un AFD mínimo.")
        exit(0)
    #FIN DEL PROGRAMA

# ---------------- FUNCIONES AUXILIARES ------------------ #
def has_been_minimized(new_equivalency):
    for status in new_equivalency:
        if len(status) > 1:
            return True
    return False
def show_transition(transition, equivalecy, alphabet):
    '''Funcion destinada a mostrar por pantalla los status y transitiones del AFD Minimizado'''

    alphabet_char_list = []
    #Se guarda en alphabet_char_list las diferentes alphabet del alfabeto
    for i in range (alphabet):
        alphabet_char_list.append(chr(i+97))
    alphabet_char_list = "\t |\t".join(alphabet_char_list)
    #Muestra la cabecera de la group_table
    print( "|" + ("================"*(alphabet+ 1)) +"|")
    print("|     Estado\t |\t" + alphabet_char_list + "\t |")
    print( "|" + ("================"*(alphabet+ 1)) +"|")
    #Para cada uno de los status del AFD Minimizado (llamados "status") se indicarán los status resultados de la transición
    for status in equivalecy:
        #minimized_status irá indicando cada uno de los status del AFD Minimizado
        minimized_status = ""
        for i in status:
            minimized_status += str(i)
        #minimzed_transition irá mostrando cada uno de los status resultantes de la transición desde "status"
        minimzed_transition = ""
        for i in transition[equivalecy.index(status)]:
            number = ""
            for j in i:
                number += str(j)

            minimzed_transition += ','.join(number)
            minimzed_transition += "\t\t |"
        #Muestra el transition al que llega "status" para cada uno de los caracteres del alfabeto
        print("|" + ','.join(minimized_status)+"\t\t |" + (minimzed_transition))


    print( "|" + ("================"*(alphabet+ 1)) +"|")
def get_min_original_status(equivalecy, original_status):
    #Revisa cual de los conjuntos de status contienen el transition original_status del AFD original y lo devuelve
    for status in equivalecy:
        if original_status in status:
            return status
def get_min_final(equivalecy, finales):
    #Revisa cual (o cuales) de los conjuntos de status contienen algún transition final del AFD original y los devuelve
    minimized_final_status = []
    for status in equivalecy:
        for final in finales:
            if final in status:
                minimized_final_status.append(status)
                break
    return minimized_final_status

def get_transition(transition_matrix, equivalecy):
    ''' Indica el índice del transition resultante de aplicar cada una de 
    las alphabet del alfabeto en cada uno de los status finales del AFD Minimizado'''
    transition = []
    #Cada transition del resultado minimizado será "status"
    for status in equivalecy:
        #transition_index 
        transition_index = transition_matrix[status[0]]
        #transition_status son los status del AFD original al que va el primer transition de cada grupo para cada letra
        next_status = transition_status(transition_index, equivalecy)
        status_group = []
        #status_group indicará el grupo al que pertenecen esos status resultantes 
        for i in next_status:
            status_group.append(equivalecy[i])
        #Se guardará status_group en una fila de transición
        #Transición se utilizará para guardar el conjunto de status_groups
        transition.append(status_group)

    return transition
def get_equivalencia(equivalecy, transition_matrix):
    ''' Esta función devuelve la siguiente equivalencia (siendo la anterior "equivalecy") '''
    new_equivalency = []
    for status in equivalecy:
        '''Si el conjunto de la equivalencia solo tiene un elemento, no es necesario comprarlo con los demás, 
        será añadido directamente a la siguiente equivalencia'''
        if len(status) > 1:
            #Creamos group_table para guardar el índice del grupo al que pertenece cada transition 
            group_table = []
            for transition in status:
                group_table.append(transition_status(transition_matrix[transition], equivalecy))
            #Vamos mirando si los status de cada uno de los conjuntos deben seguir en el mismo conjunto o no
            while len(status) != 0:
                #Guardamos en "status_group" la primera transition_indexición de cada conjunto
                status_group = []
                status_group.append(status[0])
                #"transition_group" indica a que grupo de status pertenece el transition resultante de la transición
                transition_group = group_table[0]
                #Si el conjunto de transition transition_group_compared solo tiene un transition restante, no entra en el if
                if len(status) > 1:
                    i = 1
                    for transition_group_compared in group_table[1:]:
                        #Para cada transition adicional del conjunto transition_group_compared miramos si las transitiones para cada
                        # caracter del alfabeto coinciden con "transition_group"
                        if transition_group_compared == transition_group:
                            #Si coincide, pertenecerán al mismo grupo de la siguiente equivalencia (i+1)
                            status_group.append(status[i])
                            #Para evitar repeticiones, eliminamos el transition añadido
                            status.pop(i)
                            group_table.pop(i)
                        else:
                            i += 1
                #Finalmente, eliminamos el primer transition del grupo y lo añadimos. Si quedan más status,
                #se seguirá con el bucle
                status.pop(0)
                group_table.pop(0)
                new_equivalency.append(status_group)
        else:
            #Si el grupo solo tiene un transition, se mantendría igual, añadiendolo directamente a la equivalencia siguiente.
            new_equivalency.append(status)
    return new_equivalency
def transition_status(status_group_transition, equivalecy):
    '''Revisa para cada transition objetivo de "status_group transition" a que grupo de status pertenece en equivalecy'''
    transition_status = []
    for valor in status_group_transition:
        #para cada transition objetivo "valor":
        for status in equivalecy:
            #Mira en cada una de los grutransition_index de transition "status"
            if valor in status:
                #Cuando coincidem el índice equivalente a "sección" en "equivalecy" es añadido a transition_status
                transition_status.append(equivalecy.index(status))
                break
    return transition_status

def get_not_final_status(totales, finales):
    '''Lee los status totales y coge aquellos que no pertenecen a finales'''
    not_final_status=[]
    for transition in range(len(totales)):
        if transition not in finales:
            not_final_status.append(transition)
    return not_final_status
if __name__ == "__main__":
    main()