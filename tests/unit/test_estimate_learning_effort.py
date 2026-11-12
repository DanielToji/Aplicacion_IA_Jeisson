import pytest
from pydantic import ValidationError

from app.schemas.tools import (
    Difficulty,
    EstimateLearningEffortRequest,
)
from app.tools.estimate_learning_effort import estimate_learning_effort


# ---------- Casos válidos ----------

def test_valid_estimate_media():
    req = EstimateLearningEffortRequest(
        activity="Curso de FastAPI",
        difficulty=Difficulty.MEDIA,
        topics_count=10,
        weekly_hours_available=10.0,
    )
    res = estimate_learning_effort(req)

    assert res.total_hours == 22.5          # 10 * 1.5 * 1.5
    assert res.estimated_weeks == 2.25      # 22.5 / 10
    assert res.estimated_days == 16         # ceil(2.25 * 7)
    assert res.recommendation.startswith("Plan mensual")


def test_valid_estimate_baja():
    req = EstimateLearningEffortRequest(
        activity="Intro",
        difficulty=Difficulty.BAJA,
        topics_count=2,
        weekly_hours_available=5.0,
    )
    res = estimate_learning_effort(req)
    assert res.total_hours == 3.0
    assert res.estimated_days == 5          # ceil(0.6 * 7)


def test_valid_estimate_alta():
    req = EstimateLearningEffortRequest(
        activity="Deep dive",
        difficulty=Difficulty.ALTA,
        topics_count=4,
        weekly_hours_available=8.0,
    )
    res = estimate_learning_effort(req)
    assert res.total_hours == 12.0          # 4 * 1.5 * 2.0
    assert res.estimated_weeks == 1.5
    assert res.estimated_days == 11         # ceil(10.5)


# ---------- Casos inválidos (validación Pydantic) ----------

def test_rejects_topics_count_zero():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="Curso",
            difficulty=Difficulty.MEDIA,
            topics_count=0,
            weekly_hours_available=10.0,
        )


def test_rejects_topics_count_negative():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="Curso",
            difficulty=Difficulty.MEDIA,
            topics_count=-3,
            weekly_hours_available=10.0,
        )


def test_rejects_unknown_difficulty():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="Curso",
            difficulty="extrema",           # no está en el Enum
            topics_count=5,
            weekly_hours_available=10.0,
        )


def test_rejects_zero_weekly_hours():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="Curso",
            difficulty=Difficulty.MEDIA,
            topics_count=5,
            weekly_hours_available=0.0,
        )


def test_rejects_short_activity():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="ab",                  # min_length=3
            difficulty=Difficulty.MEDIA,
            topics_count=5,
            weekly_hours_available=10.0,
        )


# ---------- Valores límite ----------

def test_accepts_min_topics_count():
    req = EstimateLearningEffortRequest(
        activity="Curso",
        difficulty=Difficulty.MEDIA,
        topics_count=1,                     # ge=1
        weekly_hours_available=10.0,
    )
    res = estimate_learning_effort(req)
    assert res.total_hours == 2.25
    assert res.estimated_days >= 1


def test_accepts_max_topics_count():
    req = EstimateLearningEffortRequest(
        activity="Curso",
        difficulty=Difficulty.MEDIA,
        topics_count=50,                    # le=50
        weekly_hours_available=10.0,
    )
    res = estimate_learning_effort(req)
    assert res.total_hours == 112.5


def test_rejects_topics_count_above_max():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="Curso",
            difficulty=Difficulty.MEDIA,
            topics_count=51,
            weekly_hours_available=10.0,
        )


def test_accepts_max_weekly_hours():
    req = EstimateLearningEffortRequest(
        activity="Curso",
        difficulty=Difficulty.BAJA,
        topics_count=5,
        weekly_hours_available=40.0,        # le=40
    )
    res = estimate_learning_effort(req)
    assert res.estimated_days >= 1          # nunca 0


def test_rejects_weekly_hours_above_max():
    with pytest.raises(ValidationError):
        EstimateLearningEffortRequest(
            activity="Curso",
            difficulty=Difficulty.MEDIA,
            topics_count=5,
            weekly_hours_available=40.01,
        )


def test_accepts_min_activity_length():
    req = EstimateLearningEffortRequest(
        activity="abc",                     # justo 3 caracteres
        difficulty=Difficulty.MEDIA,
        topics_count=3,
        weekly_hours_available=5.0,
    )
    assert req.activity == "abc"


def test_accepts_max_activity_length():
    long_name = "a" * 200
    req = EstimateLearningEffortRequest(
        activity=long_name,
        difficulty=Difficulty.MEDIA,
        topics_count=3,
        weekly_hours_available=5.0,
    )
    assert len(req.activity) == 200