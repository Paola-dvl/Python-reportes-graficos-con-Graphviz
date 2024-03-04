import os
def generar_diagrama_pisos(pisos):
    if len(pisos) == 0:
        print('No hay pisos para mostrar.')
        return

    for i, piso in enumerate(pisos, start=1):
        print(f'Piso {i}:')
        print('Nombre:', piso['nombre'])
        print('Filas:', piso['filas'])
        print('Columnas:', piso['columnas'])
        print('Patrón:', piso['patron'])
        print()

        # Crear archivo DOT
        dot_filename = f'piso_{i}.dot'
        with open(dot_filename, 'w') as dot_file:
            dot_file.write('digraph G {\n')
            dot_file.write('node [shape=plaintext];\n')
            dot_file.write('edge [style=invis];\n')
            dot_file.write(f'label="{piso["nombre"]} - PATRON = {piso["patron"]}"\n')
            dot_file.write('piso [\n')
            dot_file.write('label=<<TABLE border="1" cellspacing="0" cellpadding="10">\n')

            for _ in range(piso['filas']):
                dot_file.write('<tr>')
                for _ in range(piso['columnas']):
                    if piso['patron'] == 'B':
                        dot_file.write('<td bgcolor="black"></td>')
                    elif piso['patron'] == 'N':
                        dot_file.write('<td bgcolor="white"></td>')
                dot_file.write('</tr>\n')

            dot_file.write('</TABLE>>\n')
            dot_file.write('shape=none\n];\n')
            dot_file.write('}\n')

        # Generar PDF
        pdf_filename = f'piso_{i}.pdf'
        system(f'dot -Tpdf {dot_filename} -o {pdf_filename}')
        startfile(pdf_filename)


