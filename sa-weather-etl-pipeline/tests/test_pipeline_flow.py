from unittest.mock import patch
import pipeline


def test_pipeline_successful_flow():
    raw = [{"name": "Durban"}]
    transformed = [{"city": "Durban"}]
    validated = [{"city": "Durban"}]
    with patch.object(pipeline, "extract_all_cities", return_value=raw) as extract, \
         patch.object(pipeline, "transform_all", return_value=transformed) as transform, \
         patch.object(pipeline, "validate_all", return_value=validated) as validate, \
         patch.object(pipeline, "create_table") as create, \
         patch.object(pipeline, "load_to_csv") as csv_load, \
         patch.object(pipeline, "load_to_postgres") as db_load, \
         patch.object(pipeline, "preview_postgres") as preview:
        pipeline.run_pipeline()
    extract.assert_called_once_with()
    transform.assert_called_once_with(raw)
    validate.assert_called_once_with(transformed)
    create.assert_called_once_with()
    csv_load.assert_called_once_with(validated)
    db_load.assert_called_once_with(validated)
    preview.assert_called_once_with()


def test_pipeline_stops_if_no_extraction():
    with patch.object(pipeline, "extract_all_cities", return_value=[]), \
         patch.object(pipeline, "transform_all") as transform, \
         patch.object(pipeline, "load_to_postgres") as load_db:
        pipeline.run_pipeline()
    transform.assert_not_called()
    load_db.assert_not_called()


def test_pipeline_stops_if_validation_empty():
    with patch.object(pipeline, "extract_all_cities", return_value=[{"name": "Durban"}]), \
         patch.object(pipeline, "transform_all", return_value=[{"city": "Durban"}]), \
         patch.object(pipeline, "validate_all", return_value=[]), \
         patch.object(pipeline, "create_table") as create, \
         patch.object(pipeline, "load_to_csv") as csv_load:
        pipeline.run_pipeline()
    create.assert_not_called()
    csv_load.assert_not_called()
