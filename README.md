# PLM_BOT
_¿Cansado de tener que adivinar cúando se subió el último programa de Paren La Mano al canal de Vorterix?  
¿Querés que te llegue una notificación cuando se subió el video, pero no quéres que te lleguen notificaciones del resto de programas del canal?_

¡La solución está acá!

### ¡PLM_BOT!
⬇️ Un bot que te avisa cuando se subió el nuevo programa completo de Paren La Mano ⬇️
![Mensaje enviado por el bot](https://github.com/juanCarrique/PLM_BOT/assets/102698445/fe6824ca-c615-4406-835e-031c52dfb67c, "Mensaje de ejemplo enviado por el bot")


### ¿Cómo funciona?
Un script se ejecuta diariamente a partir de las 21:00 hrs Argentina (00:00 UTC). Cada 30 segundos, comprueba si se subió un nuevo video de Paren La Mano y compara sus IDs con el último video encontrado. Si son diferentes, envía un mensaje vía Telegram con un enlace para verlo. 
> Si a las 01:00 ARG no se ha encontrado nada, se asume que ese día no se subirá un nuevo programa y la búsqueda se detiene para no agotar los créditos de la API de YouTube.

---
### Notas
* Por ahora el bot solo envia mensajes a una persona, a mi :D
* Actualmente la ejecución programada esta hecha via Github Actions, y como bien lo aclaran en la documentacion se puede atrasar el horario de ejecucion, posibles soluciones:
  * Atrasar aun más el inicio de la ejecucion del script -> gastaria mas credios de la API :c
  * Usar programas externos a GitHub para programar la ejecución -> use python anywhere pero en su plan gratuito había que revalidar la programación cada 30 días.   
