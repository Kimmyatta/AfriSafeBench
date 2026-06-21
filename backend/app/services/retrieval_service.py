from backend.app.core.config import get_settings


def afrisafe_frameworks_index_available() -> bool:
    index_dir = get_settings().afrisafe_frameworks_index_dir
    return (index_dir / "index.faiss").exists() and (index_dir / "metadata.json").exists()
