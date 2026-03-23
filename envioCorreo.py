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
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f5f7fa; margin:0; padding:20px;">
        <table align="center" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow:hidden;">
          <tr>
            <td style="background:#003366; padding:25px; text-align:center; color:#ffffff;">
              <h1 style="margin:0; font-size:24px; font-weight:700;">Plataforma Virtual</h1>
              <p style="margin:5px 0 0; font-size:14px; font-weight:500;">Posgrado – Facultad de Medicina UMSA</p>
            </td>
          </tr>
          <tr>
            <td style="padding:30px; color:#555555; font-size:16px; line-height:1.5;">
              <p>Estimado(a) <strong>{nombre}</strong>,</p>
              <p>Le damos la bienvenida a la <strong>Plataforma Virtual de Posgrado de la Facultad de Medicina – UMSA</strong>.</p>
              <p>A continuación encontrará sus credenciales de acceso a la Plataforma:</p>
                <div style="background:#d9e6fb; border-radius:6px; padding:15px; margin:20px 0; width:100%;box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">

                  <div style="margin-bottom:10px;">
                    <span style="font-weight:600; color:#555555;">Usuario:</span>
                    <span style="font-weight:700; color:#003366;">{usuario}</span>
                  </div>

                  <div>
                    <span style="font-weight:600; color:#555555;">Contraseña:</span>
                    <span style="font-weight:700; color:#003366;">{password_usuario}</span>
                  </div>

                </div>
                          <!-- BOTÓN PRINCIPAL MEJORADO -->
                <table align="center" cellpadding="0" cellspacing="0" style="margin:30px auto;">
                  <tr>
                    <td align="center" style="border-radius:8px; background: linear-gradient(90deg, #003366, #0056b3); box-shadow: 0 4px 10px rgba(0,51,102,0.3);">
                      <a href="http://45.163.19.133/virtualUpgm/login/"
                         target="_blank"
                         style="font-size:16px; font-family: Arial, sans-serif; color:#ffffff; text-decoration:none; padding:14px 30px; display:inline-block; font-weight:600;">
                        🔐 Ingresar a la plataforma
                      </a>
                    </td>
                  </tr>
                </table>

                <!-- BOTÓN TUTORIAL ESTILO COMPLEMENTARIO -->
                <table align="center" cellpadding="0" cellspacing="0" style="margin-bottom:20px;">
                  <tr>
                    <td align="center" style="border-radius:8px; border:2px solid #0056b3;">
                      <a href="https://www.tiktok.com/@upgumsa/video/7619077920568397057"
                         target="_blank"
                         style="font-size:14px; font-family: Arial, sans-serif; color:#0056b3; text-decoration:none; padding:12px 26px; display:inline-block; font-weight:600;">
                        ▶ Ver tutorial de acceso
                      </a>
                    </td>
                  </tr>
                </table>	  
              <p style="font-size:13px; color:#666666; text-align:center;">
                Si tiene problemas para acceder, contacte al área de sistemas: <a href="https://wa.me/59173597267" target="_blank" style="color:#0056b3; text-decoration:none;">Sistemas Upgm</a>
              </p>
            </td>
          </tr>
          <tr>
            <td style="background:#f9fafc; text-align:center; padding:15px; font-size:12px; color:#999999;">
              Unidad de Posgrado – Facultad de Medicina<br>
              Universidad Mayor de San Andrés (UMSA)<br>
              La Paz, Bolivia
            </td>
          </tr>
        </table>
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
    df = pd.read_csv("enviarCorreoUsuarios.csv", sep = ',')

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

    df.to_csv("reporte_envios_usuarios.csv", index=False)

    print("Proceso terminado")



if __name__ == "__main__":
    enviar_credenciales()
