import pandas as pd
import re


def leerArchivo(dirArchivo):
    #Leer archivo 
    df = pd.read_excel(dirArchivo, skiprows= 1, sheet_name="Hoja1")
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
    df.dropna(how='all', inplace=True)
    # Eliminar columnas completamente vacías
    df.dropna(axis=1, how='all', inplace=True)

    # Resetear índice
    df.reset_index(drop=True, inplace=True)
    # Mostrar Contenido
    #print(df)
    return df

def corregirEmail(email):
    email = str(email).strip().lower()
    if '@' not in email:
        # intentar colocar @ antes de gmail.com
        if 'gmail.com' in email:
            email = email.replace('gmail.com', '@gmail.com')
    # validar
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return email
    else:
        return ''  # no reparable

def procesar(df):
    
     #Crear CSV
    titulos = ['username',
        'password',
        'firstname',
        'lastname',
        'email',
        'course1']
    
    dfCsv = pd.DataFrame(columns=titulos)
    
    
    #Separar nombres
    partes = df['APELLIDOS Y NOMBRES'].str.split(' ', n=2, expand = True)
    df['APELLIDO_PATERNO'] = partes[0]
    df['APELLIDO_MATERNO'] = partes[1]
    df['NOMBRES'] = partes[2]
    
    #Username
    dfCsv['username'] = (
        df['NOMBRES'].str.split().apply(lambda x: ''.join(i[0] for i in x[:2])) +
        df['APELLIDO_PATERNO']+df['APELLIDO_MATERNO'].str[0]
    ).str.lower().str.replace('ñ', 'n')
    
    #Generar contraseña    
    dfCsv['password']=df['APELLIDO_PATERNO'].str[0].str.upper()+df['APELLIDO_MATERNO'].str[0].str.lower()+df['C.I.'].astype(str)+'+'
    
    dfCsv['firstname']=df['NOMBRES']
    dfCsv['lastname']= df.apply(lambda x: f"{x['APELLIDO_PATERNO']} {x['APELLIDO_MATERNO']}", axis=1)
    
    #Corregir Emails . . .
    dfCsv['email']=df['CORREO'].apply(corregirEmail)
    
    #Curso  MAE_ENF/TERAPIA-OUTI-vXIV2026
    course ='MAE_SP-GERENCIA-FSP-vXXIV2026'
    dfCsv['course1']=course    
    
    #Exportar a csv
    dir=r"OUTPUT\usuarios_GERENCIA 2026.csv"
    dfCsv.to_csv(dir, index=False, encoding='utf-8-sig')

    print("CSV generado exitosamente: usuarios_limpios.csv")
        
        
    print(dfCsv)
   
    
def main():
    dirArchivo = r"INPUT\GERENCIA 2026.xlsx"
    
    procesar(leerArchivo(dirArchivo))


main()