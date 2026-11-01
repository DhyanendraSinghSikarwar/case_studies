from dataclasses import dataclass


@dataclass(frozen=True)
class TrainConfig:
    data_path: str
    out_path: str = "model.joblib"
    features: tuple[str, ...] = ("tenure", "monthly_spend", "support_calls")
    target: str = "churned"
    test_size: float = 0.2
    seed: int = 42
