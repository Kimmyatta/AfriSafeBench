from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from backend.app.models.schemas import (
    AiSafetyBenchmarkResponse,
    AiSafetyBenchmarkRunRequest,
    AiSafetyEvaluationResponse,
    AiSafetyFrameworkDocumentListResponse,
    AiSafetyFrameworkGuidanceRequest,
    AiSafetyFrameworkGuidedReportResponse,
    AiSafetyFrameworkUploadResponse,
    AiSafetyFrameworksResponse,
    AiSafetyModelsResponse,
    AiSafetyRescoredGuidanceRequest,
    AiSafetyRescoredReviewListResponse,
    AiSafetyScenarioListResponse,
    AiSafetyTextRequest,
    HealthResponse,
)
from backend.app.services.ai_safety_service import (
    evaluate_ai_safety,
    evaluate_scenario,
    generate_framework_guidance_for_scenario,
    generate_framework_guidance_from_rescored_review,
    list_framework_documents,
    list_frameworks,
    list_models,
    list_rescored_reviews,
    list_scenarios,
    run_full_benchmark,
    save_framework_document,
)
from backend.app.services.document_service import extract_text_from_upload
from backend.app.services.retrieval_service import afrisafe_frameworks_index_available


router = APIRouter(prefix="/api", tags=["AfriSafeBench"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "service": "afrisafebench-api",
        "afrisafe_frameworks_index_available": afrisafe_frameworks_index_available(),
    }


@router.get("/ai-safety/scenarios", response_model=AiSafetyScenarioListResponse)
def get_ai_safety_scenarios():
    return {"scenarios": list_scenarios()}


@router.get("/ai-safety/models", response_model=AiSafetyModelsResponse)
def get_ai_safety_models():
    return {"models": list_models()}


@router.get("/ai-safety/frameworks", response_model=AiSafetyFrameworksResponse)
def get_ai_safety_frameworks():
    return {"frameworks": list_frameworks()}


@router.get(
    "/ai-safety/framework-documents",
    response_model=AiSafetyFrameworkDocumentListResponse,
)
def get_ai_safety_framework_documents():
    return {"documents": list_framework_documents()}


@router.post(
    "/ai-safety/framework-documents/upload",
    response_model=AiSafetyFrameworkUploadResponse,
)
async def upload_ai_safety_framework_document(file: UploadFile = File(...)):
    try:
        return save_framework_document(file.filename or "framework.pdf", await file.read())
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post(
    "/ai-safety/scenarios/{scenario_id}/evaluate",
    response_model=AiSafetyEvaluationResponse,
)
def run_ai_safety_scenario_evaluation(
    scenario_id: str,
    model: str = Query("llama-3.3-70b-versatile"),
):
    try:
        return evaluate_scenario(scenario_id=scenario_id, model=model)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/ai-safety/benchmark/run", response_model=AiSafetyBenchmarkResponse)
def run_ai_safety_full_benchmark(payload: AiSafetyBenchmarkRunRequest):
    try:
        return run_full_benchmark(models=payload.models or None)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post(
    "/ai-safety/scenarios/{scenario_id}/framework-guidance",
    response_model=AiSafetyFrameworkGuidedReportResponse,
)
def run_ai_safety_framework_guidance(
    scenario_id: str,
    payload: AiSafetyFrameworkGuidanceRequest,
):
    try:
        return generate_framework_guidance_for_scenario(
            scenario_id=scenario_id,
            model=payload.model,
            detected_risks=payload.detected_risks,
            missed_risks=payload.missed_risks,
            k=payload.k,
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get(
    "/ai-safety/rescored-reviews",
    response_model=AiSafetyRescoredReviewListResponse,
)
def get_ai_safety_rescored_reviews():
    return {"reviews": list_rescored_reviews()}


@router.post(
    "/ai-safety/scenarios/{scenario_id}/rescored-framework-guidance",
    response_model=AiSafetyFrameworkGuidedReportResponse,
)
def run_ai_safety_rescored_framework_guidance(
    scenario_id: str,
    payload: AiSafetyRescoredGuidanceRequest,
):
    try:
        return generate_framework_guidance_from_rescored_review(
            scenario_id=scenario_id,
            source_model=payload.source_model,
            guidance_model=payload.guidance_model,
            k=payload.k,
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/ai-safety/evaluate", response_model=AiSafetyEvaluationResponse)
def run_ai_safety_text_evaluation(payload: AiSafetyTextRequest):
    try:
        return evaluate_ai_safety(
            title=payload.title,
            country=payload.country,
            text=payload.text,
            expected_risk_categories=payload.expected_risk_categories,
            model=payload.model,
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/ai-safety/upload", response_model=AiSafetyEvaluationResponse)
async def run_ai_safety_upload_evaluation(
    file: UploadFile = File(...),
    title: str | None = Query(None),
    country: str = Query(""),
    expected_risk_categories: list[str] = Query(default=[]),
    model: str = Query("llama-3.3-70b-versatile"),
):
    try:
        filename, document_text = await extract_text_from_upload(file)
        return evaluate_ai_safety(
            title=title or filename,
            country=country,
            text=document_text,
            expected_risk_categories=expected_risk_categories,
            model=model,
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
