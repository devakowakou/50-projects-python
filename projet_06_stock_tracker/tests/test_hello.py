def test_get_stock_data_no_data_found():
    from src.core.data_manager import DataManager
    import pytest

    dm = DataManager()

    with pytest.raises(ValueError, match="Aucune donnée trouvée pour AAPL"):
        dm.get_stock_data("AAPL", period="1mo")