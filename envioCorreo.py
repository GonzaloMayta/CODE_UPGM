import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# correo que enviará los mensajes
EMAIL_EMISOR = "soportecppegess@gmail.com"
PASSWORD = "bosa emcc ivmv rggy"

# servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def enviar_correo(destino, nombre, usuario, password_usuario):

    mensaje = MIMEMultipart()
    mensaje["From"] = EMAIL_EMISOR
    mensaje["To"] = destino
    mensaje["Subject"] = "Credenciales de acceso – Plataforma Virtual Posgrado Medicina - UMSA"

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding:20px;">
    
        <div style="max-width:600px; margin:auto; background:white; border-radius:8px; 
        box-shadow:0 2px 6px rgba(0,0,0,0.1); overflow:hidden;">
        
            <div style="background:#003366; color:white; padding:20px; text-align:center;">
                <h2>Plataforma Virtual</h2>
                <p>Posgrado – Facultad de Medicina UMSA</p>
            </div>

            <div style="padding:25px; color:#333;">
                <p>Estimado(a) <b>{nombre}</b>,</p>

                <p>Le damos la bienvenida a la <b>Plataforma Virtual de Posgrado de la Facultad de Medicina – UMSA</b>.</p>

                <p>A continuación encontrará sus credenciales de acceso a la Plataforma:</p>

                <div style="background:#f1f3f5; padding:15px; border-radius:6px;">
                    <p><b>Usuario:</b> {usuario}</p>
                    <p><b>Contraseña:</b> {password_usuario}</p>
					<p><b><a href="http://45.163.19.133/virtualUpgm/"
					target="_blank"
					rel="noopener noreferrer"
					style="
					background-color:#0b5ed7;
					border-radius:6px;
					color:white;
					display:inline-block;
					font-family:Arial, sans-serif;
					font-size:16px;
					font-weight:bold;
					padding:14px 28px;
					text-align:center;
					text-decoration:none;
					">
					🔐 Ingresar a la plataforma
					</a>
					</b></p>
                </div>

                <p>Si tiene problemas para acceder, contactese al area de sistemas: 
				<a href="https://wa.me/59173597267">Sistemas Upgm</a></p>

            </div>

            <div style="background:#f4f4f4; padding:15px; text-align:center; font-size:12px; color:#666;">
                Unidad de Posgrado – Facultad de Medicina<br>
                Universidad Mayor de San Andrés<br>
                La Paz – Bolivia
            </div>

        </div>

    </body>
    </html>
    """

    mensaje.attach(MIMEText(html, "html"))

    try:
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()
        servidor.login(EMAIL_EMISOR, PASSWORD)

        servidor.send_message(mensaje)
        servidor.quit()

        return "ENVIADO"

    except Exception as e:
        return f"ERROR: {str(e)}"


def enviar_credenciales():
    df = pd.read_csv("usuarios_FBC_prueba.csv", sep = ';')

    print(df)
    resultados = []
    
    for index, fila in df.iterrows():
        nombre = fila["firstname"]
        email = fila["email"]
        usuario = fila["username"]
        password_usuario = fila["password"]
    
        print("Enviando a:", email)
    
        resultado = enviar_correo(email,nombre, usuario, password_usuario)
        resultados.append(resultado)

    df["estado_envio"] = resultados

    df.to_csv("reporte_envios.csv", index=False)

    print("Proceso terminado")



if __name__ == "__main__":
    enviar_credenciales()
