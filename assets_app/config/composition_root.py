"""Application configuration, dependency setup, and bootstrap utilities.

This module centralizes:
    1) Configuration loading via environment variables and/or defaults.
    2) Creation of a simple dependency container (repositories and managers).
    3) A lightweight bootstrap function that exposes a process-wide singleton
       container instance.

Environment variables
---------------------
- INV_DATA_DIR
    Base directory where JSON data files are stored.
    Default: ``./data`` (relative to the current working directory).

- INV_PRODUCTS_FILE
    Filename for the products JSON file.
    Default: ``products.json``

- INV_CHANGES_FILE
    Filename for the product changes (history) JSON file.
    Default: ``product_changes.json``

Files and directories
---------------------
On first bootstrap, the module ensures that the expected JSON files exist.
If missing, a new file is created with the content ``[]`` (an empty list) to
represent an empty dataset.

Layering (DDD-inspired)
-----------------------
UI / CLI / API  →  Managers  →  Repositories  →  Storage (JSON files)

Notes
-----
- The singleton behavior in :func:`bootstrap` is intentionally minimal.
  It is not thread-safe. If you need thread/process safety, add appropriate
  synchronization or use a more robust application container framework.
- The container is created eagerly on the first bootstrap call and reused
  thereafter for the life of the process.
"""
from config.filenames import PRODUCT_FILENAME, HISTORY_FILENAME
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Mapping
import os

from history.manager.product_changes_manager import ProductChangesManager
from history.repository.product_changes_repository import ProductChangesRepository
from products.manager.product_manager import ProductManager
from products.repository.product_repository import ProductRepository


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration for file-based storage.

    Attributes:
        data_dir: Base directory for data files.
        products_file: Filename for the products JSON file.
        changes_file: Filename for the product changes (history) JSON file.

    Derived Paths:
        The :pyattr:`products_path` and :pyattr:`changes_path` properties
        combine :pyattr:`data_dir` with the respective filenames.
    """

    data_dir: Path
    products_file: str = PRODUCT_FILENAME
    changes_file: str = HISTORY_FILENAME

    @property
    def products_path(self) -> Path:
        """Absolute path to the products TXT file."""
        return self.data_dir / self.products_file

    @property
    def changes_path(self) -> Path:
        """Absolute path to the product-changes TXT file."""
        return self.data_dir / self.changes_file


def load_config(env: Optional[Mapping[str, str]] = None,
                base_dir: Optional[Path] = None) -> AppConfig:
    """Load application configuration from environment variables with fallbacks.

        Resolution order:
            1. Values provided via ``env`` mapping (if given).
            2. OS environment variables (:pydata:`os.environ`).
            3. Fallback defaults as documented below.

        Args:
            env: Optional mapping to read configuration from. If ``None``,
                :pydata:`os.environ` is used.
            base_dir: Base path used when ``INV_DATA_DIR`` is not set. If omitted,
                defaults to ``Path("./data")``.

        Environment variables:
            INV_DATA_DIR: Base directory for data files. Default: ``./data`` or
                the value of ``base_dir`` if provided.
            INV_PRODUCTS_FILE: Products filename. Default: ``products.json``.
            INV_CHANGES_FILE: Changes filename. Default: ``product_changes.json``.

        Returns:
            A populated :class:`AppConfig` instance.
        """
    env = env or os.environ
    data_dir = Path(env.get("INV_DATA_DIR", str(base_dir or Path("./data")))).expanduser()
    products_file = env.get("INV_PRODUCTS_FILE", PRODUCT_FILENAME)
    changes_file = env.get("INV_CHANGES_FILE", HISTORY_FILENAME)
    return AppConfig(data_dir=data_dir, products_file=products_file, changes_file=changes_file)


def _ensure_json_file(path: Path) -> None:
    """Create a JSON file with an empty list (``[]``) if it does not already exist.

    Side effects:
        - Ensures the parent directory exists (``parents=True, exist_ok=True``).
        - Writes ``[]`` as UTF-8 text if the file is missing.

    Args:
        path: Target JSON file path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")

@dataclass
class Container:
    """Lightweight dependency container for repositories and managers.

    Attributes:
        product_repository: Repository for :class:`products.entity.product.Product`.
        product_changes_repository: Repository for
            :class:`history.entity.product_changes.ProductChanges`.

        product_manager: Manager that orchestrates product use cases.
        product_changes_manager: Manager that orchestrates product change history use cases.
    """
    product_repository: ProductRepository
    product_changes_repository: ProductChangesRepository

    product_manager: ProductManager
    product_changes_manager: ProductChangesManager


def build_container(config: AppConfig) -> Container:
    """Construct a :class:`Container` wired with repositories and managers.

    Behavior:
        - Ensures the products and changes JSON files exist (creates empty ones if needed).
        - Instantiates file-backed repositories using the configured paths.
        - Constructs managers and preloads their in-memory caches.

    Args:
        config: Application configuration with data directory and filenames.

    Returns:
        A fully initialized :class:`Container`.
    """
    _ensure_json_file(config.products_path)
    _ensure_json_file(config.changes_path)

    product_repo = ProductRepository(str(config.products_path))
    changes_repo = ProductChangesRepository(str(config.changes_path))

    # Managers
    product_mgr = ProductManager(product_repo)
    changes_mgr = ProductChangesManager(changes_repo)

    return Container(
        product_repository=product_repo,
        product_changes_repository=changes_repo,
        product_manager=product_mgr,
        product_changes_manager=changes_mgr,
    )


_container_singleton: Optional[Container] = None

def bootstrap(env: Optional[Mapping[str, str]] = None,
              base_dir: Optional[Path] = None) -> Container:
    """Initialize (once) and return the process-wide dependency container.

    This function lazily constructs a :class:`Container` on first invocation
    and returns the same instance on subsequent calls.

    Args:
        env: Optional environment mapping for configuration resolution.
        base_dir: Optional base directory used if ``INV_DATA_DIR`` is absent.

    Returns:
        The singleton :class:`Container` instance.

    Warning:
        Not thread-safe. If multiple threads may call this concurrently during
        startup, add synchronization (e.g., a lock) around the initialization.
    """
    global _container_singleton
    if _container_singleton is None:
        cfg = load_config(env=env, base_dir=base_dir)
        _container_singleton = build_container(cfg)
    return _container_singleton
