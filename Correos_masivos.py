import smtplib
import os
import base64
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
from bs4 import BeautifulSoup
    

def cargar_html(ruta_archivo):
    """Carga el contenido HTML desde un archivo usando ruta absoluta o relativa"""
    try:
        # Obtener la ruta absoluta del archivo
        ruta_absoluta = Path(ruta_archivo).resolve()
        
        with open(ruta_absoluta, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo '{ruta_archivo}'")
        print(f"   Ruta buscada: {Path(ruta_archivo).resolve()}")
        return None
    """
    Busca etiquetas <img src="archivo.png"> en el HTML y las reemplaza con base64
    """
    
    # Buscar todas las rutas de imágenes locales
    patron = r'src=["\']([^"\']*\.(png|jpg|jpeg|gif|svg))["\']'
    imagenes = re.findall(patron, html, re.IGNORECASE)
    
    for imagen_info in imagenes:
        ruta_original = imagen_info[0]
        
        # Construir ruta completa
        if not os.path.isabs(ruta_original):
            ruta_completa = os.path.join(directorio_imagenes, ruta_original)
        else:
            ruta_completa = ruta_original
        
        # Convertir a base64
        imagen_base64 = imagen_a_base64(ruta_completa)
        
        if imagen_base64:
            # Reemplazar en el HTML
            html = html.replace(f'src="{ruta_original}"', f'src="{imagen_base64}"')
            html = html.replace(f"src='{ruta_original}'", f"src='{imagen_base64}'")
            print(f"  ✓ Imagen incrustada: {ruta_original}")
    
    return html

def enviar_correo():
    remitente = "operacion@reprocamsas.com"
    contraseña = "xmpriwgpgecaykfu"

    if not contraseña:
        print("Ejemplo: export EMAIL_PASSWORD='tu_contraseña_de_aplicacion'")
        return
    
    destinatarios = [
        "gerencia@motorshop.com.co",
    ]
    
    asunto = "Transforma tus residuos en oportunidades con Reprocam ♻"
    html = None
    
    # Cargar HTML desde archivo (mismo nivel que el .py)
    print("📄 Cargando HTML...")
    html = cargar_html('intento.html')
    
    if not html:
        return 'Error'
    
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = asunto
    msg.attach(MIMEText(html, 'html'))
    
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.send_message(msg)
        print(f"✓ Correo enviado exitosamente")
        servidor.quit()
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    # Mostrar directorio actual
    print(f"📁 Directorio actual: {Path.cwd()}")
    print("-" * 60)
    
    enviar_correo()