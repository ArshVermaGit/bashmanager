import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_app(tmp_path, monkeypatch):
    monkeypatch.setenv("DEV_SHELL_DATA_DIR", str(tmp_path))
    if "app" in sys.modules:
        app_module = importlib.reload(sys.modules["app"])
    else:
        import app as app_module
    app_module.app.config.update({"TESTING": True})
    return app_module


def test_list_scripts_returns_json(tmp_path, monkeypatch):
    app_module = _load_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    response = client.get("/api/scripts")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)

    for category, scripts in data.items():
        assert isinstance(category, str)
        assert isinstance(scripts, list)
        for script in scripts:
            assert isinstance(script, dict)
            assert "file" in script
            assert "relative_path" in script
            assert "favorite" in script
            assert "locked" in script


def test_workspace_get_returns_success(tmp_path, monkeypatch):
    app_module = _load_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    response = client.get("/api/workspace")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "workspace" in data
