import csv
import io
from pathlib import Path

from whatsapp_analyzer.cli import main

FIXTURE = Path(__file__).parent / "fixtures" / "android_it.txt"


def test_cli_json_to_stdout(capsys):
    code = main([str(FIXTURE), "--to", "json"])
    out = capsys.readouterr().out
    assert code == 0
    assert "Mario" in out
    assert "2024-06-12T21:35:00" in out


def test_cli_writes_output_file(tmp_path):
    out_file = tmp_path / "chat.json"
    code = main([str(FIXTURE), "--to", "json", "--out", str(out_file)])
    assert code == 0
    assert out_file.exists()
    assert "Mario" in out_file.read_text(encoding="utf-8")


def test_cli_anonymize_and_no_system(capsys):
    main([str(FIXTURE), "--to", "csv", "--anonymize", "--no-system"])
    out = capsys.readouterr().out
    rows = [row for row in csv.reader(io.StringIO(out)) if row]
    # l'anonimizzazione tocca solo la colonna sender, non il testo
    senders = {row[1] for row in rows[1:]}
    assert senders == {"User1", "User2"}
    assert "crittografat" not in out  # messaggio di sistema rimosso
