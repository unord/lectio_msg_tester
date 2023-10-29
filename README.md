# Lectio Besked Tester

## Introduktion

Dette projekt indeholder Python-scripts til at sende beskeder via Lectio's hjemmeside. Scriptet benytter sig af Playwright til web-scraping og automatisering af browserhandlingerne. 

## Krav

- Python 3.6 eller nyere
- Playwright

## Installation

1. **Klon projektet til din lokale maskine**

    ```bash
    git clone https://github.com/unord/lectio_msg_tester
    ```

2. **Naviger ind i projektets mappe**

    ```bash
    cd <project-folder>
    ```

3. **Installer de nødvendige Python-biblioteker**

    ```bash
    pip install -r requirements.txt
    ```

4. **Installér Playwright og dens browser-binære**

    For at installere Playwright, kør følgende kommando:

    ```bash
    playwright install
    ```
    
    Dette vil downloade alle nødvendige browser-binærer.

## Hvordan man bruger

Her er nogle korte beskrivelser af de primære funktioner i scriptet:

- `lectio_send_msg(...) -> dict`: Sender en besked via Lectio.
- `push_health_check(...) -> dict`: Sender en push health check-besked via uptime-kuma.

For at sende en besked, kan du bruge `lectio_send_msg` funktionen som vist nedenfor:

```python
result = lectio_send_msg(
    school_id='123',
    lectio_user='username',
    lectio_password='password',
    send_to='recipient',
    subject='Test Subject',
    msg='Hello, World!'
)
print(result)
```

Hvis beskeden sendes korrekt, returnerer `lectio_send_msg` en dictionary med `'success': True`.

## Fejlfinding

1. Hvis du oplever problemer med at køre scriptet, sørg for, at du har alle de nødvendige pakker installeret.

2. Kontroller at Playwright er korrekt installeret. Du kan teste dette ved at køre `playwright --version` i terminalen.


## Licens

Dette projekt er licenseret under MIT-licensen.
