from datetime import date

class NodoArbol:
   
   def __init__(self,clave,valor,izquierdo=None,derecho=None,padre=None):
        self.clave = clave
        self.carga_util = valor
        self.izq = izquierdo
        self.der = derecho
        self.padre = padre
        
   def __iter__(self):
      if self:
          if self.tiene_hijo_izquierdo():
                for elem in self.izq:
                    yield elem
          yield self
          if self.tiene_hijo_derecho():
              for elem in self.der:
                  yield elem

   def tiene_hijo_izquierdo(self):
        return self.izq

   def tiene_hijo_derecho(self):
       return self.der

   def eshijo_izquierdo(self):
       return self.padre and self.padre.izq == self

   def eshijo_derecho(self):
       return self.padre and self.padre.der == self

   def es_raiz(self):
       return not self.padre

   def esHoja(self):
       return not (self.der or self.izq)

   def tieneAlgunHijo(self):
       return self.der or self.izq

   def tieneAmbosHijos(self):
       return self.der and self.izq

   def reemplazar_dato_de_nodo(self,clave,valor,hizq,hder):
       self.clave = clave
       self.carga_util = valor
       self.izq = hizq
       self.der = hder
       if self.tiene_izq():
           self.izq.padre = self
       if self.tiene_der():
           self.der.padre = self
            
class ArbolAVL:

    def __init__(self):
        self.raiz = None
        self.tamano = 0

    def longitud(self):
        return self.tamano

    def __len__(self):
        return self.tamano
    
    def __iter__(self):
        return self.raiz.__iter__()
   

    def agregar(self,clave,valor):
        if self.raiz:
            self._agregar(clave,valor,self.raiz)
        else:
            self.raiz = NodoArbol(clave,valor)
        self.tamano = self.tamano + 1

    def _agregar(self,clave,valor,nodoActual):
        if clave < nodoActual.clave:
            if nodoActual.tiene_hijo_izquierdo():
                   self._agregar(clave,valor,nodoActual.izq)
            else:
                   nodoActual.izq = NodoArbol(clave,valor,padre=nodoActual)
        else:
            if nodoActual.tiene_hijo_derecho():
                   self._agregar(clave,valor,nodoActual.der)
            else:
                   nodoActual.der = NodoArbol(clave,valor,padre=nodoActual)

    def __setitem__(self,c,v):
       self.agregar(c,v)

    def obtener(self,clave):
       if self.raiz:
           res = self._obtener(clave,self.raiz)
           if res:
                  return res.carga_util
           else:
                  return None
       else:
           return None

    def _obtener(self,clave,nodoActual):
       if not nodoActual:
           return None
       elif nodoActual.clave == clave:
           return nodoActual
       elif clave < nodoActual.clave:
           return self._obtener(clave,nodoActual.izq)
       else:
           return self._obtener(clave,nodoActual.der)

    def __getitem__(self,clave):
       return self.obtener(clave)

    def __contains__(self,clave):
       if self._obtener(clave,self.raiz):
           return True
       else:
           return False

    def eliminar(self,clave):
      if self.tamano > 1:
         nodoAEliminar = self._obtener(clave,self.raiz)
         if nodoAEliminar:
             self.remover(nodoAEliminar)
             self.tamano = self.tamano-1
         else:
             raise KeyError('Error, la clave no está en el árbol')
      elif self.tamano == 1 and self.raiz.clave == clave:
         self.raiz = None
         self.tamano = self.tamano - 1
      else:
         raise KeyError('Error, la clave no está en el árbol')

    def __delitem__(self,clave):
       self.eliminar(clave)


    def empalmar(self):
       if self.esHoja():
           if self.eshijo_izquierdo():
                  self.padre.izq = None
           else:
                  self.padre.der = None
       elif self.tieneAlgunHijo():
           if self.tiene_hijo_izquierdo():
                  if self.eshijo_izquierdo():
                     self.padre.izq = self.izq
                  else:
                     self.padre.der = self.izq
                  self.izq.padre = self.padre
           else:
                  if self.eshijo_izquierdo():
                     self.padre.izq = self.der
                  else:
                     self.padre.der = self.der
                  self.der.padre = self.padre


    def encontrarSucesor(self):
      suc = None
      if self.tiene_hijo_derecho():
          suc = self.der.encontrarMin()
      else:
          if self.padre:
                 if self.eshijo_izquierdo():
                     suc = self.padre
                 else:
                     self.padre.der = None
                     suc = self.padre.encontrarSucesor()
                     self.padre.der = self
      return suc


    def encontrarMin(self):
      actual = self
      while actual.tiene_hijo_izquierdo():
          actual = actual.izq
      return actual


    def remover(self,nodoActual):
         if nodoActual.esHoja(): #hoja
           if nodoActual == nodoActual.padre.izq:
               nodoActual.padre.izq = None
           else:
               nodoActual.padre.der = None
         elif nodoActual.tieneAmbosHijos(): #interior
           suc = nodoActual.encontrarSucesor()
           suc.empalmar()
           nodoActual.clave = suc.clave
           nodoActual.carga_util = suc.carga_util

         else: # este nodo tiene un (1) hijo
           if nodoActual.tiene_hijo_izquierdo():
             if nodoActual.eshijo_izquierdo():
                 nodoActual.izq.padre = nodoActual.padre
                 nodoActual.padre.izq = nodoActual.izq
             elif nodoActual.eshijo_derecho():
                 nodoActual.izq.padre = nodoActual.padre
                 nodoActual.padre.der = nodoActual.izq
             else:
                 nodoActual.reemplazar_dato_de_nodo(nodoActual.izq.clave,
                                    nodoActual.izq.carga_util,
                                    nodoActual.izq.izq,
                                    nodoActual.izq.der)
           else:
             if nodoActual.eshijo_izquierdo():
                 nodoActual.der.padre = nodoActual.padre
                 nodoActual.padre.izq = nodoActual.der
             elif nodoActual.eshijo_derecho():
                 nodoActual.der.padre = nodoActual.padre
                 nodoActual.padre.der = nodoActual.der
             else:
                 nodoActual.reemplazar_dato_de_nodo(nodoActual.der.clave,
                                    nodoActual.der.carga_util,
                                    nodoActual.der.izq,
                                    nodoActual.der.der)


    def actualizarEquilibrio(self,nodo):
        if nodo.factorEquilibrio > 1 or nodo.factorEquilibrio < -1:
            self.reequilibrar(nodo)
            return
        if nodo.padre != None:
            if nodo.eshijo_izquierdo():
                    nodo.padre.factorEquilibrio += 1
            elif nodo.eshijo_derecho():
                    nodo.padre.factorEquilibrio -= 1
    
            if nodo.padre.factorEquilibrio != 0:
                    self.actualizarEquilibrio(nodo.padre)
                    

    def rotar_derecha(self,rot_raiz):
        nueva_raiz = rot_raiz.izq
        rot_raiz.izq = nueva_raiz.der
        if rot_raiz.padre is None:
            self.raiz = nueva_raiz 
        else:
            if rot_raiz.es_izq():
                rot_raiz.padre.izq = nueva_raiz
            elif rot_raiz.es_der():
                rot_raiz.padre.der = nueva_raiz 
        nueva_raiz.der = rot_raiz 
        
        rot_raiz.factor_equilibrio = rot_raiz.factor_equilibrio + 1
        - min (0,nueva_raiz.factor_equilibrio)
        nueva_raiz.factorEquilibrio = nueva_raiz.factor_equilibrio + 1
        + max (0,rot_raiz.factor_equilibrio)


    def rotar_izquierda(self,rot_raiz):
        nuevaRaiz = rot_raiz.der
        rot_raiz.der = nuevaRaiz.izq
        if nuevaRaiz.izq != None:
            nuevaRaiz.izq.padre = rot_raiz
        nuevaRaiz.padre = rot_raiz.padre
        if rot_raiz.es_raiz():
            self.raiz = nuevaRaiz
        else:
            if rot_raiz.eshijo_izquierdo():
                    rot_raiz.padre.izq = nuevaRaiz
            else:
                rot_raiz.padre.der = nuevaRaiz
        nuevaRaiz.izq = rot_raiz
        rot_raiz.padre = nuevaRaiz
        rot_raiz.factorEquilibrio = rot_raiz.factorEquilibrio + 1 - min(nuevaRaiz.factorEquilibrio, 0)
        nuevaRaiz.factorEquilibrio = nuevaRaiz.factorEquilibrio + 1 + max(rot_raiz.factorEquilibrio, 0)


        
    def reequilibrar(self,nodo):
      if nodo.factorEquilibrio < 0:
              if nodo.der.factorEquilibrio > 0:
                self.rotarDerecha(nodo.der)
                self.rotarIzquierda(nodo)
              else:
                self.rotarIzquierda(nodo)
      elif nodo.factorEquilibrio > 0:
              if nodo.izq.factorEquilibrio < 0:
                self.rotarIzquierda(nodo.izq)
                self.rotarDerecha(nodo)
              else:
                self.rotarDerecha(nodo)
                
                
class Iterador:
    def __init__(self, arbol, clave_inicio):
        self.arbol = arbol
        self.nodo_inicio = arbol._obtener(clave_inicio, self.arbol.raiz)
    
    def __next__(self):
        nodo_salida = self.nodo_inicio
        self.nodo_inicio = self.nodo_inicio.encontrarSucesor()
        if self.nodo_inicio == None:
            raise StopIteration
        return nodo_salida
    
    def __iter__(self):
        return self
        
                
if __name__ == "__main__":
    mediciones = ArbolAVL()
    mediciones.agregar(date(2021,11,9),23)
    mediciones.agregar(date(2022,10,21),24)
    mediciones.agregar(date(2022,12,11),19)
    mediciones.agregar(date(2022,12,1),18)
    mediciones.agregar(date(2021,3,13),16)    
    mediciones.agregar(date(2019,4,19),11)    
    
    print(mediciones.tamano)
    print(mediciones.raiz.clave)
    print()
    
    for nodo in mediciones:
        print (nodo.clave, nodo.carga_util)
        
    iterador = Iterador(mediciones, date(2021,11,9))
    
    for nodo in iterador:
        print (nodo)
    
