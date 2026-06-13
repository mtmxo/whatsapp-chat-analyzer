# whatsapp-chat-analyzer

Parser e analisi per chat WhatsApp esportate in formato `.txt`.

## Installazione

```bash
pip install whatsapp-chat-analyzer
```

## Uso base

```python
from whatsapp_analyzer import parse_file

chat = parse_file("export.txt")
for msg in chat:
    print(msg.sender, msg.text)
```
