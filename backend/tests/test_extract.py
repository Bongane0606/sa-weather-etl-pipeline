from unittest.mock import Mock, patch
import requests
import extract


def test_extract_success():
    response = Mock(status_code=200)
    response.json.return_value = {"name": "Durban"}
    with patch.object(extract.requests, "get", return_value=response) as get:
        assert extract.extract_weather("Durban") == {"name": "Durban"}
    assert get.call_args.kwargs["params"]["q"] == "Durban,ZA"
    assert get.call_args.kwargs["timeout"] == 10


def test_extract_http_error():
    with patch.object(extract.requests, "get", return_value=Mock(status_code=401)):
        assert extract.extract_weather("Durban") is None


def test_extract_timeout():
    with patch.object(extract.requests, "get", side_effect=requests.exceptions.Timeout):
        assert extract.extract_weather("Durban") is None


def test_extract_connection_error():
    with patch.object(extract.requests, "get", side_effect=requests.exceptions.ConnectionError):
        assert extract.extract_weather("Durban") is None


def test_extract_all_cities_filters_failures_and_attaches_province():
    cities = [{"city": "Durban", "province": "KwaZulu-Natal"}, {"city": "Kimberley", "province": "Northern Cape"}]
    with patch.object(extract, "CITIES", cities), patch.object(extract, "extract_weather", side_effect=[{"name": "Durban"}, None]) as fn:
        result = extract.extract_all_cities()
    assert result == [{"name": "Durban", "province": "KwaZulu-Natal"}]
    assert fn.call_count == 2
