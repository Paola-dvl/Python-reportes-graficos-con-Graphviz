import xml.etree.ElementTree as ET


class Piso:
    def __init__(self, nombre, r, c, f, s):
        self.nombre = nombre
        self.r = r 
        self.c = c
        self.f = f
        self.s = s
        self.patrones = {}
    
    def agregar_patron(self, codigo, patron):
        self.patrones[codigo] = patron
        
    def cambiar_patron(self, codigo_origen, codigo_destino):
        patron_origen = self.patrones[codigo_origen]
        patron_destino = self.patrones[codigo_destino]
        
        costo_minimo, instrucciones = calcular_cambio_minimo(patron_origen, patron_destino, self.f, self.s)
        
        print(f"Costo mínimo para cambiar de {codigo_origen} a {codigo_destino}: {costo_minimo}")
        
        print("Instrucciones:")
        for instr in instrucciones:
            print(instr)
            
        generar_grafica(patron_destino, self.r, self.c, codigo_destino)
        
def calcular_cambio_minimo(patron_origen, patron_destino, f, s):
    # Aquí se implementa la lógica para calcular el costo mínimo 
    # y generar las instrucciones
    
    instrucciones = []
    costo = 0
    
    return costo, instrucciones
    
def generar_grafica(patron, r, c, codigo):
    graph = Digraph(codigo)
    
    # Aquí se genera el gráfico con Graphviz
    
    print(graph.source)
    
def main():
    arbol = ET.parse('pisos.xml')
    raiz = arbol.getroot()

    pisos = []
    for piso_elem in raiz:
        nombre = piso_elem.attrib['nombre']
        r = int(piso_elem.find('R').text)
        c = int(piso_elem.find('C').text)
        f = int(piso_elem.find('F').text)
        s = int(piso_elem.find('S').text)
        
        piso = Piso(nombre, r, c, f, s)
        for patron_elem in piso_elem.find('patrones'):
            codigo = patron_elem.attrib['codigo']
            patron = patron_elem.text
            piso.agregar_patron(codigo, patron)
            
        pisos.append(piso)
        
    # Aquí se muestra el menú de opciones para el usuario
    
    piso = pisos[0]
    codigo_origen = 'cod11'
    codigo_destino = 'cod12'
    
    piso.cambiar_patron(codigo_origen, codigo_destino)
    
if __name__ == '__main__':
    main()