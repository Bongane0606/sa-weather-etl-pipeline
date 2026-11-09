from unittest.mock import Mock, patch
import db


def test_get_connection_success():
    conn = Mock()
    with patch.object(db.psycopg2, "connect", return_value=conn) as connect:
        assert db.get_connection() is conn
    assert "dbname" in connect.call_args.kwargs


def test_get_connection_failure():
    with patch.object(db.psycopg2, "connect", side_effect=Exception("offline")):
        assert db.get_connection() is None


def test_create_table_success():
    conn = Mock()
    with patch.object(db, "get_connection", return_value=conn):
        assert db.create_table() is True
    assert conn.cursor.return_value.execute.call_count == 2
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_create_table_no_connection():
    with patch.object(db, "get_connection", return_value=None):
        assert db.create_table() is False


def test_create_table_rolls_back_on_error():
    conn = Mock()
    conn.cursor.return_value.execute.side_effect = Exception("sql error")
    with patch.object(db, "get_connection", return_value=conn):
        assert db.create_table() is False
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()


def test_connection_check_success_and_failure():
    conn = Mock()
    with patch.object(db, "get_connection", return_value=conn):
        assert db.test_connection() is True
    conn.close.assert_called_once()
    with patch.object(db, "get_connection", return_value=None):
        assert db.test_connection() is False
