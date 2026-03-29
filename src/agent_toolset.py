from typing import Any
import pandas as pd
from io import StringIO
import json


class DatasetAnalyzerToolset:
    """Dataset Analyzer Toolset"""

    def __init__(self):
        pass

    async def analyze_dataset(self, data: str) -> dict:
        """
        Analyze dataset (CSV or JSON string) and return insights
        """

        try:
            # 🔍 Detect input type
            if data.strip().startswith("{") or data.strip().startswith("["):
                # JSON input
                df = pd.DataFrame(json.loads(data))
            else:
                # CSV input
                df = pd.read_csv(StringIO(data))

            result = {
                "rows": int(df.shape[0]),
                "columns": int(df.shape[1]),
                "column_names": list(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
            }

            # 📊 Numeric insights
            insights = []
            for col in df.select_dtypes(include="number").columns:
                insights.append({
                    "column": col,
                    "mean": round(df[col].mean(), 2),
                    "max": df[col].max(),
                    "min": df[col].min()
                })

            result["insights"] = insights

            return result

        except Exception as e:
            return {"error": str(e)}

    def get_tools(self) -> dict[str, Any]:
        return {
            "analyze_dataset": self.analyze_dataset
        }