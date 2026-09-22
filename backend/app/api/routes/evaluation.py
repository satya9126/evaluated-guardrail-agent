import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.get("/results")
def get_evaluation_results():
    results_path = (
        Path(__file__).resolve().parents[3]
        / "evaluations"
        / "results.json"
    )

    if not results_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Evaluation results not found."
        )

    with open(results_path, "r") as file:
        results = json.load(file)

    return results