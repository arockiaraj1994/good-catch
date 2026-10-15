import pytest

from pipeline.adapters.inbound.cli import main


def test_monday_must_be_a_monday() -> None:
    with pytest.raises(SystemExit):
        main(["check", "--monday", "2026-10-20", "--offline"])
