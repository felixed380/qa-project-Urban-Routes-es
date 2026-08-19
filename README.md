# Urban Routes — Pruebas Automatizadas con Selenium

## Descripción del proyecto

Este proyecto contiene un conjunto de pruebas automatizadas end-to-end para la aplicación web **Urban Routes**, un servicio de solicitud de viajes tipo taxi/rideshare. La prueba simula el flujo completo de un usuario real: desde el ingreso de una ruta (origen y destino), la selección de una tarifa, la confirmación del número de teléfono vía código SMS, el registro de un método de pago, hasta la personalización del pedido (mensaje para el conductor y solicitud de artículos adicionales como manta y pañuelos).

El objetivo es validar que cada paso del flujo de reserva funcione correctamente y que los datos ingresados por el usuario se reflejen fielmente en la interfaz, mediante aserciones (`assert`) en cada etapa clave del proceso.

## Flujo cubierto por la prueba

1. Ingreso de dirección de origen y destino.
2. Solicitud de taxi y selección de la tarifa "Comfort".
3. Ingreso y confirmación del número de teléfono mediante código SMS.
4. Registro de método de pago (número de tarjeta y código de seguridad).
5. Mensaje personalizado para el conductor.
6. Activación de artículos adicionales (manta y pañuelos).
7. Verificación del contador de helados (ítem adicional del pedido).

## Tecnologías y técnicas utilizadas

- **Python 3** — lenguaje base del proyecto.
- **Selenium WebDriver** — automatización del navegador (Google Chrome).
- **pytest** — framework de ejecución y aserciones de pruebas.
- **Page Object Model (POM)** — patrón de diseño que separa la lógica de interacción con la página (`UrbanRoutesPage`) de la lógica de la prueba (`TestUrbanRoutes`), facilitando el mantenimiento y la reutilización de código.
- **WebDriverWait / Expected Conditions (EC)** — esperas explícitas (`visibility_of_element_located`, `element_to_be_clickable`, `presence_of_element_located`) para manejar la carga asíncrona de una aplicación web dinámica (React), evitando fallos por *timing*.
- **Chrome DevTools Protocol (CDP) / Performance Logging** — captura de logs de red del navegador para interceptar la respuesta de la API que contiene el código de confirmación telefónico (`retrieve_phone_code`), ya que dicho código no es visible directamente en la interfaz.
- **`switch_to.active_element`** — técnica utilizada para interactuar con campos de entrada que reciben el foco del teclado pero no cumplen los criterios de visibilidad estándar de Selenium (elementos con dimensiones de 0px controlados por CSS).
- **`execute_script` (JavaScript Executor)** — mecanismo de respaldo para interactuar con elementos ocultos visualmente pero presentes y funcionales en el DOM (por ejemplo, checkboxes de un componente tipo *toggle switch*).
- **`Keys.TAB`** — simulación de pérdida de foco (`blur`) para disparar validaciones de formulario que dependen de ese evento, en lugar de depender de clics en elementos no relacionados.

## Requisitos previos

- Python 3.10 o superior.
- Google Chrome instalado.
- Dependencias del proyecto instaladas (ver más abajo).

## Instalación

1. Clona o descarga este repositorio.
2. (Opcional pero recomendado) Crea un entorno virtual:

   ```bash
   python -m venv .venv
   ```

   Actívalo:

   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. Instala las dependencias:

   ```bash
   pip install selenium pytest
   ```

4. Verifica que `data.py` contenga las variables necesarias para la prueba (URL de la aplicación, direcciones, número de teléfono, datos de tarjeta, mensaje para el conductor, etc.).

## Cómo ejecutar las pruebas

Desde la raíz del proyecto, ejecuta:

```bash
pytest main.py -v
```

Para ver la salida detallada de cada paso (incluyendo prints de depuración, si los hubiera) y evitar que pytest capture la salida estándar:

```bash
pytest main.py -v -s
```

Para ejecutar únicamente la prueba principal:

```bash
pytest main.py::TestUrbanRoutes::test_set_route -v
```

## Notas importantes

- La función `retrieve_phone_code` **no debe modificarse**: depende de que los logs de rendimiento (`performance logging`) del navegador estén habilitados (configurado en `setup_class`) y solo funciona **después** de haber solicitado el código de confirmación dentro del flujo de la aplicación.
- El navegador se abre y se cierra automáticamente en cada ejecución (`setup_class` / `teardown_class`); no es necesario gestionar el ciclo de vida del driver manualmente.
- Si una prueba falla, revisa primero la línea marcada con `>` en el traceback de pytest y el mensaje `Expected` / `Actual` (o `AssertionError`) para identificar rápidamente si el fallo es de lógica (valor incorrecto) o de interacción con el elemento (excepción de Selenium).
