import csv
from unittest.mock import Mock, patch
import load


def record(city="Durban"):
    return {key: (city if key == "city" else "sample") for key in load.CSV_COLUMNS}


def test_load_csv_creates_header_and_appends(tmp_path, monkeypatch):
    target = tmp_path / "weather_data.csv"
    monkeypatch.setattr(load, "OUTPUT_FOLDER", str(tmp_path))
    monkeypatch.setattr(load, "OUTPUT_FILE", str(target))
    load.load_to_csv([record()])
    load.load_to_csv([record("Kimberley")])
    with target.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert [row["city"] for row in rows] == ["Durban", "Kimberley"]


def test_load_csv_creates_directory(tmp_path, monkeypatch):
    folder = tmp_path / "new"
    monkeypatch.setattr(load, "OUTPUT_FOLDER", str(folder))
    monkeypatch.setattr(load, "OUTPUT_FILE", str(folder / "data.csv"))
    load.load_to_csv([])
    assert (folder / "data.csv").exists()


def test_load_postgres_success():
    conn = Mock()
    with patch.object(load, "get_connection", return_value=conn):
        assert load.load_to_postgres([record()]) is True
    conn.cursor.return_value.execute.assert_called_once()
    assert conn.cursor.return_value.execute.call_args.args[1]["city"] == "Durban"
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_load_postgres_no_connection():
    with patch.object(load, "get_connection", return_value=None):
        assert load.load_to_postgres([record()]) is False


def test_load_postgres_rolls_back():
    conn = Mock()
    conn.cursor.return_value.execute.side_effect = Exception("insert failed")
    with patch.object(load, "get_connection", return_value=conn):
        assert load.load_to_postgres([record()]) is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


def test_preview_postgres_no_connection():
    with patch.object(load, "get_connection", return_value=None):
        assert load.preview_postgres() is None
