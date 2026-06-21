export type HealthResponse = {
  status: string;
  service: string;
  afrisafe_frameworks_index_available: boolean;
};

export type AiSafetyModel = {
  id: string;
  label: string;
};

export type AiSafetyScenario = {
  scenario_id: string;
  title: string;
  country: string;
  healthcare_context: string;
  scenario_description: string;
  expected_risk_categories: string[];
  risk_severity: string;
  severity: string;
  explanation: string;
};

export type AiSafetyScenarioListResponse = {
  scenarios: AiSafetyScenario[];
};

export type AiSafetyModelsResponse = {
  models: AiSafetyModel[];
};

export type AiSafetyRescoredReview = {
  review_id: string;
  scenario_id: string;
  title: string;
  country: string;
  model: string;
  coverage_score: number;
  missed_risks: string[];
  path: string;
};

export type AiSafetyRescoredReviewListResponse = {
  reviews: AiSafetyRescoredReview[];
};

export type AiSafetyRisk = {
  risk: string;
  severity: string;
  explanation: string;
};

export type AiSafetyCategoryScore = {
  score: number;
  matched_risk: string | null;
  explanation: string | null;
};

export type AiSafetyScoring = {
  matched_risks: string[];
  missed_risks: string[];
  extra_risks: string[];
  raw_score: number;
  max_score: number;
  coverage_score: number;
  scores_by_category: Record<string, AiSafetyCategoryScore>;
};

export type AiSafetyReport = {
  report_title: string;
  scenario_summary: Record<string, unknown>;
  detected_ai_safety_risks: AiSafetyRisk[];
  risk_severity: Array<Record<string, string>>;
  matched_risks: string[];
  missed_risks: string[];
  coverage_score: number;
  recommendations: string[];
  limitations_and_dual_use_considerations: string[];
};

export type AiSafetyEvaluationResponse = {
  scenario_id: string | null;
  title: string;
  country: string;
  healthcare_context: string;
  model: string;
  identified_risks: AiSafetyRisk[];
  overall_assessment: string;
  scoring: AiSafetyScoring;
  report: AiSafetyReport;
  raw_model_response: string;
  expected_risk_categories: string[];
  risk_severity: string | null;
  benchmark_explanation: string | null;
};

export type AiSafetyFrameworkSource = {
  source: string;
  excerpt: string;
};

export type AiSafetyFrameworkGuidedRecommendation = {
  recommendation: string;
  rationale: string;
  priority: string;
  related_risks: string[];
  framework_sources: string[];
};

export type AiSafetyFrameworkGuidedReportResponse = {
  scenario_id: string | null;
  title: string;
  country: string;
  model: string;
  framework_summary: string;
  recommendations: AiSafetyFrameworkGuidedRecommendation[];
  governance_checklist: string[];
  limitations_and_dual_use_considerations: string[];
  sources: AiSafetyFrameworkSource[];
  raw_model_response: string;
};

export type AiSafetyBenchmarkAggregate = {
  mean_coverage_score_by_model: Record<string, number>;
  coverage_score_by_risk_category: Record<string, Record<string, number>>;
  coverage_score_by_country: Record<string, Record<string, number>>;
  coverage_score_by_severity: Record<string, Record<string, number>>;
};

export type AiSafetyBenchmarkResponse = {
  models: string[];
  scenario_count: number;
  evaluation_count: number;
  aggregate: AiSafetyBenchmarkAggregate;
  results: AiSafetyEvaluationResponse[];
};
