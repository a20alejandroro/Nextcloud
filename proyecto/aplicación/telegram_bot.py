# ==========================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================

import docker              # Esta librería permite conectarse y controlar Docker desde Python
import asyncio             # Sirve para ejecutar funciones en segundo plano (de forma asíncrona)
from telegram import Update                  # Representa un mensaje o comando recibido en Telegram
from telegram.ext import Application, CommandHandler, ContextTypes  
# 'Application' gestiona el bot, 'CommandHandler' permite reaccionar a comandos como /start

# ==========================================================
# CONFIGURACIÓN DE DOCKER Y VARIABLES INICIALES DEL PROGRAMA
# ==========================================================

# Creamos un cliente que se conecta al motor Docker instalado en el mismo sistema
docker_client = docker.from_env()

# Diccionario que relaciona un nombre corto (alias) con el nombre real del contenedor en Docker
# Esto es útil para que el usuario del bot escriba algo sencillo (ej. "server1")
CONTAINERS = {
    "server1": "server1",  # Primer contenedor
    "server2": "server2",   # Segundo contenedor
    "server3": "server3"   # Tercer contenedor
}

# ID de Telegram del usuario autorizado para usar el bot (solo esta persona puede controlar los contenedores)
AUTHORIZED_CHAT_ID = 1351766993

# Almacena el estado anterior de los contenedores (ej. si estaban "running" o "exited")
# Esto se usa para detectar cuándo cambian de estado (por ejemplo, si se apagan)
previous_status = {alias: None for alias in CONTAINERS}

# ====================================================
# FUNCIÓN QUE MONITOREA CONTENEDORES CADA 10 SEGUNDOS
# ====================================================
async def monitor_containers(application: Application) -> None:
    global previous_status  # Usamos la variable global para guardar los estados previos
    while True:
        for alias, container_name in CONTAINERS.items():  # Recorremos cada contenedor
            container = docker_client.containers.get(container_name)  # Obtenemos el contenedor por su nombre
            current_status = container.status  # Obtenemos su estado actual

            # Comprobamos si antes estaba "running" y ahora no lo está (se cayó)
            if previous_status[alias] == "running" and current_status != "running":
                # Si se apagó, enviamos un mensaje de alerta por Telegram al usuario
                await application.bot.send_message(
                    chat_id=AUTHORIZED_CHAT_ID,
                    text=f"⚠️ El contenedor {alias} se ha detenido."
                )

            # Guardamos el estado actual para usarlo en la siguiente comprobación
            previous_status[alias] = current_status

        # Esperamos 10 segundos antes de revisar otra vez
        await asyncio.sleep(10)

# ======================================
# FUNCIÓN PARA COMPROBAR SI EL USUARIO ESTÁ AUTORIZADO
# ======================================
def is_authorized(update: Update) -> bool:
    # Comprobamos si el ID del usuario que envió el mensaje es el autorizado
    return update.effective_chat and update.effective_chat.id == AUTHORIZED_CHAT_ID

# =========================
# COMANDO /status - Ver estado de todos los contenedores
# =========================
async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ Acceso denegado.")  # Bloqueamos acceso a usuarios no autorizados
        return

    mensaje = []  # Lista donde guardaremos los mensajes sobre el estado de cada contenedor
    for alias, container_name in CONTAINERS.items():
        container = docker_client.containers.get(container_name)
        if container.status == "running":
            mensaje.append(f"{alias} está ENCENDIDO ✅")
        else:
            mensaje.append(f"{alias} está APAGADO ❌")

    # Enviamos el resumen de estados por Telegram
    await update.message.reply_text("\n".join(mensaje))

# =========================
# COMANDO /start - Iniciar un contenedor específico
# =========================
async def start_container(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ Acceso denegado.")
        return

    # Comprobamos si el usuario escribió correctamente el comando
    if len(context.args) != 1 or context.args[0] not in CONTAINERS:
        await update.message.reply_text("Uso: /start <server1|server2|server3>")
        return

    nombre = context.args[0]  # Extraemos el nombre del contenedor a iniciar
    container = docker_client.containers.get(CONTAINERS[nombre])  # Obtenemos el contenedor de Docker

    # Si ya está corriendo, avisamos; si no, lo iniciamos
    if container.status == "running":
        await update.message.reply_text(f"{nombre} ya está en ejecución ✅")
    else:
        container.start()
        await update.message.reply_text(f"{nombre} se ha INICIADO ✅")

# =========================
# COMANDO /stop - Detener un contenedor específico
# =========================
async def stop_container(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ Acceso denegado.")
        return

    # Comprobamos que el comando tenga un argumento válido
    if len(context.args) != 1 or context.args[0] not in CONTAINERS:
        await update.message.reply_text("Uso: /stop <server1|server2|server3>")
        return

    nombre = context.args[0]
    container = docker_client.containers.get(CONTAINERS[nombre])

    # Si ya está detenido, lo decimos; si no, lo detenemos
    if container.status != "running":
        await update.message.reply_text(f"{nombre} ya está detenido ❌")
    else:
        container.stop()
        await update.message.reply_text(f"{nombre} se ha DETENIDO ❌")

# =========================
# COMANDO /help - Muestra los comandos disponibles
# =========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("⛔ Acceso denegado.")
        return

    # Enviamos un mensaje con la lista de comandos disponibles
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/status - Ver el estado de los contenedores\n"
        "/start <server1|server2|server3> - Iniciar un contenedor\n"
        "/stop <server1|server2|server3> - Detener un contenedor"
    )

# ===================================
# FUNCIÓN PRINCIPAL: INICIA EL BOT DE TELEGRAM Y EL MONITOREO
# ===================================
def main():
    # Token único del bot (obtenido desde BotFather en Telegram)
    TOKEN = "7747995833:AAFqkAe74mM9UAws26ljShyE6r_j9o3MbUk"

    # Creamos la aplicación del bot con ese token
    app = Application.builder().token(TOKEN).build()

    # Registramos los comandos del bot (qué función ejecutar para cada uno)
    app.add_handler(CommandHandler("status", check_status))
    app.add_handler(CommandHandler("start", start_container))
    app.add_handler(CommandHandler("stop", stop_container))
    app.add_handler(CommandHandler("help", help_command))

    # Iniciamos la función de monitoreo en segundo plano
    app.job_queue.run_once(lambda _: asyncio.create_task(monitor_containers(app)), when=0)

    # Comenzamos a recibir mensajes y comandos en Telegram
    app.run_polling()

# ===================================================
# INICIO DEL PROGRAMA (cuando se ejecuta el archivo directamente)
# ===================================================
if __name__ == "__main__":
    main()
