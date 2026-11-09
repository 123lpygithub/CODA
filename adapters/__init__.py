from adapters.base import (
    ArtifactRecord,
    DatasetAdapter,
    DatasetMetadata,
    ReferenceAnnotation,
    ReferenceData,
    ReferenceLabel,
    SourceRef,
    TextLocator,
)
from adapters.common_sense_bug import CommonSenseViolatingBugAdapter
from adapters.cpp_oop import CppOopRelatedFeatureAdapter
from adapters.defects4codellm import (
    Defects4CodeLLMSemanticAdapter,
    Defects4CodeLLMSyntacticAdapter,
)
from adapters.dockerfile_flakiness import DockerfileFlakinessAdapter
from adapters.fairness_api_issue_topic import FairnessApiIssueTopicAdapter
from adapters.ml_satd_23_shades import MLSATD23ShadesAdapter
from adapters.personal_data_protection_github import PersonalDataProtectionGitHubAdapter
from adapters.quantum_classical import QuantumClassicalIssueAdapter
from adapters.static_analysis import StaticAnalysisNondeterminismAdapter

__all__ = [
    "ArtifactRecord",
    "CommonSenseViolatingBugAdapter",
    "CppOopRelatedFeatureAdapter",
    "DatasetAdapter",
    "DatasetMetadata",
    "Defects4CodeLLMSemanticAdapter",
    "Defects4CodeLLMSyntacticAdapter",
    "DockerfileFlakinessAdapter",
    "FairnessApiIssueTopicAdapter",
    "MLSATD23ShadesAdapter",
    "PersonalDataProtectionGitHubAdapter",
    "QuantumClassicalIssueAdapter",
    "ReferenceAnnotation",
    "ReferenceData",
    "ReferenceLabel",
    "SourceRef",
    "StaticAnalysisNondeterminismAdapter",
    "TextLocator",
]
