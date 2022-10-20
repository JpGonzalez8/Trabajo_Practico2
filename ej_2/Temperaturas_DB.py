from datetime import date

class NodoArbol:
   
   def __init__(self,clave,valor,izquierdo=None,derecho=None,padre=None):
        self.clave = clave
        self.carga_util = valor
        self.hijo_izquierdo = izquierdo
        self.hijo_derecho = derecho
        self.padre = padre
        
   def __iter__(self):
      if self:
          if self.tiene_hijo_izquierdo():
                for elem in self.hijo_izquierdo:
                    yield elem
          yield self
          if self.tiene_hijo_derecho():
              for elem in self.hijo_derecho:
                  yield elem

   def tiene_hijo_izquierdo(self):
        return self.hijo_izquierdo

   def tiene_hijo_derecho(self):
       return self.hijo_derecho

   def eshijo_izquierdo(self):
       return self.padre and self.padre.hijo_izquierdo == self

   def eshijo_derecho(self):
       return self.padre and self.padre.hijo_derecho == self

   def es_raiz(self):
       return not self.padre

   def esHoja(self):
       return not (self.hijo_derecho or self.hijo_izquierdo)

   def tieneAlgunHijo(self):
       return self.hijo_derecho or self.hijo_izquierdo

   def tieneAmbosHijos(self):
       return self.hijo_derecho and self.hijo_izquierdo

   def reemplazar_dato_de_nodo(self,clave,valor,hizq,hder):
       self.clave = clave
       self.carga_util = valor
       self.hijo_izquierdo = hizq
       self.hijo_derecho = hder
       if self.tiene_hijo_izquierdo():
           self.hijo_izquierdo.padre = self
       if self.tiene_hijo_derecho():
           self.hijo_derecho.padre = self
            
class ArbolAVL:

    def __init__(self):
        self.raiz = None
        self.tamano = 0

    def longitud(self):
        return self.tamano

    def __len__(self):
        return self.tamano
    
    def __iter__(self):
        return self.raiz._iter_()
   

    def agregar(self,clave,valor):
        if self.raiz:
            self._agregar(clave,valor,self.raiz)
        else:
            self.raiz = NodoArbol(clave,valor)
        self.tamano = self.tamano + 1

    def _agregar(self,clave,valor,nodoActual):
        if clave < nodoActual.clave:
            if nodoActual.tiene_hijo_izquierdo():
                   self._agregar(clave,valor,nodoActual.hijo_izquierdo)
            else:
                   nodoActual.hijo_izquierdo = NodoArbol(clave,valor,padre=nodoActual)
        else:
            if nodoActual.tiene_hijo_derecho():
                   self._agregar(clave,valor,nodoActual.hijo_derecho)
            else:
                   nodoActual.hijo_derecho = NodoArbol(clave,valor,padre=nodoActual)

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
           return self._obtener(clave,nodoActual.hijo_izquierdo)
       else:
           return self._obtener(clave,nodoActual.hijo_derecho)

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
                  self.padre.hijo_izquierdo = None
           else:
                  self.padre.hijo_derecho = None
       elif self.tieneAlgunHijo():
           if self.tiene_hijo_izquierdo():
                  if self.eshijo_izquierdo():
                     self.padre.hijo_izquierdo = self.hijo_izquierdo
                  else:
                     self.padre.hijo_derecho = self.hijo_izquierdo
                  self.hijo_izquierdo.padre = self.padre
           else:
                  if self.eshijo_izquierdo():
                     self.padre.hijo_izquierdo = self.hijo_derecho
                  else:
                     self.padre.hijo_derecho = self.hijo_derecho
                  self.hijo_derecho.padre = self.padre

    def encontrarSucesor(self):
      suc = None
      if self.tiene_hijo_derecho():
          suc = self.hijo_derecho.encontrarMin()
      else:
          if self.padre:
                 if self.eshijo_izquierdo():
                     suc = self.padre
                 else:
                     self.padre.hijo_derecho = None
                     suc = self.padre.encontrarSucesor()
                     self.padre.hijo_derecho = self
      return suc

    def encontrarMin(self):
      actual = self
      while actual.tiene_hijo_izquierdo():
          actual = actual.hijo_izquierdo
      return actual

    def remover(self,nodoActual):
         if nodoActual.esHoja(): #hoja
           if nodoActual == nodoActual.padre.hijo_izquierdo:
               nodoActual.padre.hijo_izquierdo = None
           else:
               nodoActual.padre.hijo_derecho = None
         elif nodoActual.tieneAmbosHijos(): #interior
           suc = nodoActual.encontrarSucesor()
           suc.empalmar()
           nodoActual.clave = suc.clave
           nodoActual.carga_util = suc.carga_util

         else: # este nodo tiene un (1) hijo
           if nodoActual.tiene_hijo_izquierdo():
             if nodoActual.eshijo_izquierdo():
                 nodoActual.hijo_izquierdo.padre = nodoActual.padre
                 nodoActual.padre.hijo_izquierdo = nodoActual.hijo_izquierdo
             elif nodoActual.eshijo_derecho():
                 nodoActual.hijo_izquierdo.padre = nodoActual.padre
                 nodoActual.padre.hijo_derecho = nodoActual.hijo_izquierdo
             else:
                 nodoActual.reemplazar_dato_de_nodo(nodoActual.hijo_izquierdo.clave,
                                    nodoActual.hijo_izquierdo.carga_util,
                                    nodoActual.hijo_izquierdo.hijo_izquierdo,
                                    nodoActual.hijo_izquierdo.hijo_derecho)
           else:
             if nodoActual.eshijo_izquierdo():
                 nodoActual.hijo_derecho.padre = nodoActual.padre
                 nodoActual.padre.hijo_izquierdo = nodoActual.hijo_derecho
             elif nodoActual.eshijo_derecho():
                 nodoActual.hijo_derecho.padre = nodoActual.padre
                 nodoActual.padre.hijo_derecho = nodoActual.hijo_derecho
             else:
                 nodoActual.reemplazar_dato_de_nodo(nodoActual.hijo_derecho.clave,
                                    nodoActual.hijo_derecho.carga_util,
                                    nodoActual.hijo_derecho.hijo_izquierdo,
                                    nodoActual.hijo_derecho.hijo_derecho)


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
                    
    def rotarIzquierda(self,rotRaiz):
        nuevaRaiz = rotRaiz.hijo_derecho
        rotRaiz.hijo_derecho = nuevaRaiz.hijo_izquierdo
        if nuevaRaiz.hijo_izquierdo != None:
            nuevaRaiz.hijo_izquierdo.padre = rotRaiz
        nuevaRaiz.padre = rotRaiz.padre
        if rotRaiz.es_raiz():
            self.raiz = nuevaRaiz
        else:
            if rotRaiz.eshijo_izquierdo():
                    rotRaiz.padre.hijo_izquierdo = nuevaRaiz
            else:
                rotRaiz.padre.hijo_derecho = nuevaRaiz
        nuevaRaiz.hijo_izquierdo = rotRaiz
        rotRaiz.padre = nuevaRaiz
        rotRaiz.factorEquilibrio = rotRaiz.factorEquilibrio + 1 - min(nuevaRaiz.factorEquilibrio, 0)
        nuevaRaiz.factorEquilibrio = nuevaRaiz.factorEquilibrio + 1 + max(rotRaiz.factorEquilibrio, 0)

        
    def reequilibrar(self,nodo):
      if nodo.factorEquilibrio < 0:
              if nodo.hijo_derecho.factorEquilibrio > 0:
                self.rotarDerecha(nodo.hijo_derecho)
                self.rotarIzquierda(nodo)
              else:
                self.rotarIzquierda(nodo)
      elif nodo.factorEquilibrio > 0:
              if nodo.hijo_izquierdo.factorEquilibrio < 0:
                self.rotarIzquierda(nodo.hijo_izquierdo)
                self.rotarDerecha(nodo)
              else:
                self.rotarDerecha(nodo)
                
                
                
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