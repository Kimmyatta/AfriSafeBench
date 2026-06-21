from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    afrisafe_frameworks_index_available: bool


class AiSafetyModel(BaseModel):
    id: str
    label: str


class AiSafetyScenario(BaseModel):
    scenario_id: str
    title: str
    country: str
    healthcare_context: str = ""
    scenario_description: str
    expected_risk_categories: list[str]
    risk_severity: str = "Unknown"
    severity: str
    explanation: str


class AiSafetyScenarioListResponse(BaseModel):
    scenarios: list[AiSafetyScenario]


class AiSafetyModelsResponse(BaseModel):
    models: list[AiSafetyModel]


class AiSafetyFramework(BaseModel):
    name: str
    source_year: str | None = None
    review_focus: list[str] = Field(default_factory=list)
    risk_categories: list[str] = Field(default_factory=list)


class AiSafetyFrameworksResponse(BaseModel):
    frameworks: list[AiSafetyFramework]


class AiSafetyFrameworkDocumentListResponse(BaseModel):
    documents: list[str]


class AiSafetyFrameworkUploadResponse(BaseModel):
    filename: str
    path: str
    message: str


class AiSafetyTextRequest(BaseModel):
    title: str = "Uploaded AI healthcare deployment document"
    country: str = ""
    text: str
    expected_risk_categories: list[str] = Field(default_factory=list)
    model: str = "llama-3.3-70b-versatile"


class AiSafetyFrameworkGuidanceRequest(BaseModel):
    model: str = "llama-3.3-70b-versatile"
    detected_risks: list[dict[str, Any]] = Field(default_factory=list)
    missed_risks: list[str] = Field(default_factory=list)
    k: int = 6


class AiSafetyRescoredReview(BaseModel):
    review_id: str
    scenario_id: str
    title: str
    country: str = ""
    model: str
    coverage_score: float
    missed_risks: list[str] = Field(default_factory=list)
    path: str


class AiSafetyRescoredReviewListResponse(BaseModel):
    reviews: list[AiSafetyRescoredReview]


class AiSafetyRescoredGuidanceRequest(BaseModel):
    source_model: str
    guidance_model: str | None = None
    k: int = 6


class AiSafetyRisk(BaseModel):
    risk: str
    severity: str
    explanation: str


class AiSafetyCategoryScore(BaseModel):
    score: int
    matched_risk: str | None = None
    explanation: str | None = None


class AiSafetyScoring(BaseModel):
    matched_risks: list[str]
    missed_risks: list[str]
    extra_risks: list[str]
    raw_score: int
    max_score: int
    coverage_score: float
    scores_by_category: dict[str, AiSafetyCategoryScore]


class AiSafetyReport(BaseModel):
    report_title: str
    scenario_summary: dict[str, Any]
    detected_ai_safety_risks: list[AiSafetyRisk]
    risk_severity: list[dict[str, str]]
    matched_risks: list[str]
    missed_risks: list[str]
    coverage_score: float
    recommendations: list[str]
    limitations_and_dual_use_considerations: list[str]


class AiSafetyEvaluationResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    scenario_id: str | None = None
    title: str
    country: str
    healthcare_context: str = ""
    model: str
    identified_risks: list[AiSafetyRisk]
    overall_assessment: str
    scoring: AiSafetyScoring
    report: AiSafetyReport
    raw_model_response: str
    expected_risk_categories: list[str]
    risk_severity: str | None = None
    benchmark_explanation: str | None = None


class AiSafetyFrameworkSource(BaseModel):
    source: str
    excerpt: str


class AiSafetyFrameworkGuidedRecommendation(BaseModel):
    recommendation: str
    rationale: str
    priority: str = "Medium"
    related_risks: list[str] = Field(default_factory=list)
    framework_sources: list[str] = Field(default_factory=list)


class AiSafetyFrameworkGuidedReportResponse(BaseModel):
    scenario_id: str | None = None
    title: str
    country: str = ""
    model: str
    framework_summary: str
    recommendations: list[AiSafetyFrameworkGuidedRecommendation]
    governance_checklist: list[str]
    limitations_and_dual_use_considerations: list[str]
    sources: list[AiSafetyFrameworkSource]
    raw_model_response: str


class AiSafetyBenchmarkAggregate(BaseModel):
    mean_coverage_score_by_model: dict[str, float]
    coverage_score_by_risk_category: dict[str, dict[str, float]]
    coverage_score_by_country: dict[str, dict[str, float]]
    coverage_score_by_severity: dict[str, dict[str, float]]


class AiSafetyBenchmarkResponse(BaseModel):
    models: list[str]
    scenario_count: int
    evaluation_count: int
    aggregate: AiSafetyBenchmarkAggregate
    results: list[AiSafetyEvaluationResponse]


class AiSafetyBenchmarkRunRequest(BaseModel):
    models: list[str] = Field(default_factory=list)
