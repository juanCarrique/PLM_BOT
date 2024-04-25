# PLM_BOT
_¿Cansado de tener que adivinar cuándo se subió el último programa de Paren La Mano al canal de Vorterix?  
¿Querés que te llegue una notificación cuando se subió el video, pero no querés que te lleguen notificaciones del resto de programas del canal?_

¡La solución está acá!

### ¡PLM_BOT!
⬇️ Un bot que te avisa cuando se subió el nuevo programa completo de Paren La Mano ⬇️
![Mensaje enviado por el bot](https://github.com/juanCarrique/PLM_BOT/assets/102698445/fe6824ca-c615-4406-835e-031c52dfb67c, "Mensaje de ejemplo enviado por el bot")


### ¿Cómo funciona?
Un script se ejecuta diariamente a partir de las 21:00 hrs Argentina (00:00 UTC). Cada 30 segundos, comprueba si se subió un nuevo video de Paren La Mano y compara sus IDs con el último video encontrado. Si son diferentes, envía un mensaje vía Telegram con un enlace para verlo. 
> Si a las 01:00 ARG no se ha encontrado nada, se asume que ese día no se subirá un nuevo programa y la búsqueda se detiene para no agotar los créditos de la API de YouTube.

---
### Notas
* Por ahora el bot solo envía mensajes a una persona, a mí :D
* Actualmente la ejecución programada esta hecha vía GitHub Actions, y como bien lo aclaran en la documentación se puede atrasar el horario de ejecución, posibles soluciones:
  * Atrasar aún más el inicio de la ejecución del script, para que esté corriendo lo antes posible-> gastaría más créditos de la API :c
  * Usar programas externos a GitHub para programar la ejecución -> usé [PythonAnywhere](https://www.pythonanywhere.com "Página de PythonAnywhere") pero en su plan gratuito había que revalidar la programación de la ejecución cada 30 días.   
