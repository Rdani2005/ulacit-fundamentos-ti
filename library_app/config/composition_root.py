from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Mapping

from config.filenames import STUDENT_FILENAME, BOOK_FILENAME, LOAN_FILENAME
from student.student_repository import StudentRepository
from student.student_manager import StudentManager

from book.book_repository import BookRepository
from book.book_manager import BookManager

from loan.loan_repository import LoanRepository
from loan.loan_manager import LoanManager


@dataclass(frozen=True)
class AppConfig:
    data_dir: Path
    students_file: str = STUDENT_FILENAME
    books_file: str = BOOK_FILENAME
    loans_file: str = LOAN_FILENAME

    @property
    def students_path(self) -> Path:
        return self.data_dir / self.students_file

    @property
    def books_path(self) -> Path:
        return self.data_dir / self.books_file

    @property
    def loans_path(self) -> Path:
        return self.data_dir / self.loans_file


def load_config(env: Optional[Mapping[str, str]] = None,
                base_dir: Optional[Path] = None) -> AppConfig:
    env = env or os.environ
    data_dir = Path(env.get("LIB_DATA_DIR", str(base_dir or Path("./data")))).expanduser()
    students_file = env.get("LIB_STUDENTS_FILE", STUDENT_FILENAME)
    books_file = env.get("LIB_BOOKS_FILE", BOOK_FILENAME)
    loans_file = env.get("LIB_LOANS_FILE", LOAN_FILENAME)
    return AppConfig(
        data_dir=data_dir,
        students_file=students_file,
        books_file=books_file,
        loans_file=loans_file,
    )


def _ensure_json_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


@dataclass
class Container:
    # Repos
    student_repository: StudentRepository
    book_repository: BookRepository
    loan_repository: LoanRepository

    # Managers
    student_manager: StudentManager
    book_manager: BookManager
    loan_manager: LoanManager


def build_container(config: AppConfig) -> Container:
    _ensure_json_file(config.students_path)
    _ensure_json_file(config.books_path)
    _ensure_json_file(config.loans_path)

    student_repo = StudentRepository(str(config.students_path))
    book_repo = BookRepository(str(config.books_path))
    loan_repo = LoanRepository(str(config.loans_path))

    student_mgr = StudentManager(student_repo)

    book_mgr = BookManager(book_repo)
    try:
        getattr(book_mgr, "_BookManager__load_data")()
    except Exception:
        pass

    loan_mgr = LoanManager(loan_repo, book_mgr, student_mgr)

    return Container(
        student_repository=student_repo,
        book_repository=book_repo,
        loan_repository=loan_repo,
        student_manager=student_mgr,
        book_manager=book_mgr,
        loan_manager=loan_mgr,
    )

_container_singleton: Optional[Container] = None

def bootstrap(env: Optional[Mapping[str, str]] = None,
              base_dir: Optional[Path] = None) -> Container:
    """Crea (o reutiliza) un contenedor listo para usarse."""
    global _container_singleton
    if _container_singleton is None:
        cfg = load_config(env=env, base_dir=base_dir)
        _container_singleton = build_container(cfg)
    return _container_singleton