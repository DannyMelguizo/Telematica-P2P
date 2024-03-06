# **ST0263 Topicos Especiales en Telematica**

# **Estudiante**: Daniel Melguizo Roldan, dmelguizor@eafit.edu.co

# **Profesor**: Juan Carlos Montoya Mendoza, jcmontoy@eafit.edu.co

*******

**Tabla de Contenido**
1. [Introduccion](#introduccion)
2. [Requisitos completados y no completados](#requisitos)
3. [Diseño y arquitectura](#arquitectura)
4. [Ambiente de desarrollo](#ambiente)
5. [Ejecucion](#ejecucion)
6. [Referencias](#referencias)

*******

<div id="introduccion" />
  
### **Reto 1 y 2: Red P2P descentralizada**
El reto consiste en crear una red P2P totalmente descentralizada, en la cual, a traves de una interfaz (en este caso desarrollada por consola) los peers podran interactuar con la red, esta interracion sera principalmente para solicitar archivos, la solicitud debera llegar y recorrer los distintos peers conectados en la red en busca del archivo, una vez se encuentre el archivo, se le enviara una lista al peer solicitante de los distintos peers que tienen el archivo en la cual este podra decidir de cual de los peers en la lista descargar el archivo. Cada peer debe tener un archivo config en el cual se establezcan los diferentes datos que se consideren necesarios, minimamente tener, la ip del peer, puerto en el cual estara haciendo listening, directorio en el cual se buscaran los archivos y las ips conocidas por el peer.

*******

<div id="requisitos" />

### ***Requisitos completados***
* La red debe permitir el ingreso de nuevos nodos a la red
* El sistema debe poder encontrar cualquier archivo si lo posee un peer de la red
* Cada peer se debe comportar tanto como servidor como cliente
* El sistema debe ofrecer una interfaz al usuario
* Cada peer debe tener un archivo config
* El sistema debe implementar gRCP como middleware
* El sistema debe implementar MOM como middleware
* Cada peer debe generar un archivo log
* El sistema debe ser capaz de reestructurarse si un nodo abandona la red

### ***Requisitos no completados***
* El sistema debe poder descargar el archivo una vez localizado
* El sistema debe implementar REST API como middleware
* El sistema debe ser totalmente descentralizado
* El sistema debe estar programado en dos lenguajes diferentes

*******

<div id="arquitectura" />

### ***Diseño de alto nivel***
![Diseño de alto nivel](./imgs/DiseñoAltoNivel.png)

### ***Arquitectura***

![Arquitectura](./imgs/Arquitectura.png)

*******

<div id="ambiente" />
  
### ***3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.***

* como se compila y ejecuta.
* detalles del desarrollo.
* detalles técnicos
* descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
* opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
* opcionalmente - si quiere mostrar resultados o pantallazos 

*******

<div id="ejecucion" />
  
#### ***4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.***

IP o nombres de dominio en nube o en la máquina servidor.

descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

como se lanza el servidor.

una mini guia de como un usuario utilizaría el software o la aplicación

opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

*******

<div id="referencias"/>
  
### ***referencias:***
  sitio1-url 
  sitio2-url
  url de donde tomo info para desarrollar este proyecto
