"""
Research Tools / 科研工具

Scientific computing and research-oriented tools.
科学计算和面向研究的工具。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
import numpy as np
from scipy import stats, optimize, integrate
from core.tool import Tool


class ScientificComputeTool(Tool):
    """
    Scientific computing tool using NumPy and SciPy.
    使用NumPy和SciPy的科学计算工具。

    Provides access to numerical operations, statistics, and optimization.
    提供数值运算、统计和优化功能。
    """

    def __init__(self):
        super().__init__(
            name="scientific_compute",
            description="Perform scientific computations: statistics, linear algebra, optimization, integration",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'stats', 'linalg', 'optimize', 'integrate', 'fft'"
                    },
                    "data": {
                        "type": "array",
                        "description": "Input data array"
                    },
                    "params": {
                        "type": "object",
                        "description": "Additional parameters"
                    }
                },
                "required": ["operation"]
            }
        )

    def execute(
        self,
        operation: str,
        data: List = None,
        params: Dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform scientific computation.
        执行科学计算。

        Args:
            operation: Type of operation / 操作类型
            data: Input data / 输入数据
            params: Additional parameters / 额外参数

        Returns:
            Computation result / 计算结果
        """
        try:
            params = params or {}

            if operation == "stats":
                return self._compute_stats(data)
            elif operation == "linalg":
                return self._linear_algebra(data, params)
            elif operation == "optimize":
                return self._optimize(data, params)
            elif operation == "integrate":
                return self._integrate(params)
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "operation": operation
            }

    def _compute_stats(self, data: List) -> Dict[str, Any]:
        """Compute statistical measures. / 计算统计度量。"""
        arr = np.array(data)

        return {
            "success": True,
            "stats": {
                "mean": float(np.mean(arr)),
                "median": float(np.median(arr)),
                "std": float(np.std(arr)),
                "var": float(np.var(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "q25": float(np.percentile(arr, 25)),
                "q75": float(np.percentile(arr, 75))
            }
        }

    def _linear_algebra(self, data: List, params: Dict) -> Dict[str, Any]:
        """Linear algebra operations. / 线性代数运算。"""
        matrix = np.array(data)

        op = params.get("linalg_op", "eigenvalues")

        if op == "eigenvalues":
            eigenvalues, eigenvectors = np.linalg.eig(matrix)
            return {
                "success": True,
                "eigenvalues": eigenvalues.tolist(),
                "eigenvectors": eigenvectors.tolist()
            }
        elif op == "inverse":
            inv = np.linalg.inv(matrix)
            return {
                "success": True,
                "inverse": inv.tolist()
            }
        elif op == "det":
            det = np.linalg.det(matrix)
            return {
                "success": True,
                "determinant": float(det)
            }
        else:
            return {
                "success": False,
                "error": f"Unknown linear algebra operation: {op}"
            }

    def _optimize(self, data: List, params: Dict) -> Dict[str, Any]:
        """Optimization operations. / 优化运算。"""

        def target_func(x):
            return x**2 + 10*np.sin(x)

        result = optimize.minimize(target_func, x0=0)

        return {
            "success": True,
            "optimization": {
                "x": float(result.x[0]),
                "fun": float(result.fun),
                "success": bool(result.success)
            }
        }

    def _integrate(self, params: Dict) -> Dict[str, Any]:
        """Numerical integration. / 数值积分。"""

        def integrand(x):
            return np.exp(-x**2)

        result, error = integrate.quad(integrand, 0, 1)

        return {
            "success": True,
            "integral": float(result),
            "error": float(error)
        }


class StatisticalTestTool(Tool):
    """
    Statistical hypothesis testing tool.
    统计假设检验工具。

    Perform common statistical tests.
    执行常见的统计检验。
    """

    def __init__(self):
        super().__init__(
            name="statistical_test",
            description="Perform statistical hypothesis tests: t-test, ANOVA, chi-square, etc.",
            parameters={
                "type": "object",
                "properties": {
                    "test_type": {
                        "type": "string",
                        "description": "Test type: 'ttest', 'anova', 'chi2', 'correlation'"
                    },
                    "data1": {
                        "type": "array",
                        "description": "First dataset"
                    },
                    "data2": {
                        "type": "array",
                        "description": "Second dataset (if needed)"
                    }
                },
                "required": ["test_type", "data1"]
            }
        )

    def execute(
        self,
        test_type: str,
        data1: List,
        data2: List = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform statistical test.
        执行统计检验。

        Args:
            test_type: Type of test / 检验类型
            data1: First dataset / 第一个数据集
            data2: Second dataset / 第二个数据集

        Returns:
            Test result / 检验结果
        """
        try:
            arr1 = np.array(data1)
            arr2 = np.array(data2) if data2 else None

            if test_type == "ttest":
                if arr2 is None:
                    statistic, pvalue = stats.ttest_1samp(arr1, 0)
                else:
                    statistic, pvalue = stats.ttest_ind(arr1, arr2)

                return {
                    "success": True,
                    "test": "t-test",
                    "statistic": float(statistic),
                    "p_value": float(pvalue),
                    "significant": pvalue < 0.05
                }

            elif test_type == "correlation":
                if arr2 is None:
                    return {
                        "success": False,
                        "error": "Correlation requires two datasets"
                    }
                correlation, pvalue = stats.pearsonr(arr1, arr2)

                return {
                    "success": True,
                    "test": "Pearson correlation",
                    "correlation": float(correlation),
                    "p_value": float(pvalue),
                    "significant": pvalue < 0.05
                }

            elif test_type == "normality":
                statistic, pvalue = stats.shapiro(arr1)

                return {
                    "success": True,
                    "test": "Shapiro-Wilk normality test",
                    "statistic": float(statistic),
                    "p_value": float(pvalue),
                    "is_normal": pvalue > 0.05
                }

            else:
                return {
                    "success": False,
                    "error": f"Unknown test type: {test_type}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "test_type": test_type
            }


class LiteratureSearchTool(Tool):
    """
    Scientific literature search tool.
    科学文献检索工具。

    Search scientific papers and publications.
    搜索科学论文和出版物。

    Note: This is a placeholder. Integrate with real APIs like:
    注意：这是一个占位符。与真实的API集成，如：
    - arXiv API
    - PubMed API
    - Semantic Scholar API
    - CrossRef API
    """

    def __init__(self, api_key: str = None):
        super().__init__(
            name="literature_search",
            description="Search scientific literature and papers",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "source": {
                        "type": "string",
                        "description": "Source: 'arxiv', 'pubmed', 'scholar'"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                },
                "required": ["query"]
            }
        )
        self.api_key = api_key

    def execute(
        self,
        query: str,
        source: str = "arxiv",
        max_results: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search scientific literature.
        搜索科学文献。

        Args:
            query: Search query / 搜索查询
            source: Literature source / 文献来源
            max_results: Max results / 最大结果数

        Returns:
            Search results / 搜索结果
        """
        return {
            "success": True,
            "query": query,
            "source": source,
            "results": [
                {
                    "title": "Example Paper Title (API Integration Needed)",
                    "authors": ["Author 1", "Author 2"],
                    "abstract": "This is a placeholder result. Integrate with arXiv, PubMed, or Semantic Scholar APIs for real literature search.",
                    "year": 2024,
                    "url": "https://arxiv.org/example"
                }
            ],
            "message": "Literature search requires API integration. See documentation for setup."
        }


class UnitConverterTool(Tool):
    """
    Scientific unit conversion tool.
    科学单位转换工具。

    Convert between different scientific units.
    在不同科学单位之间转换。
    """

    def __init__(self):
        super().__init__(
            name="unit_converter",
            description="Convert between scientific units: length, mass, temperature, energy, etc.",
            parameters={
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "Value to convert"
                    },
                    "from_unit": {
                        "type": "string",
                        "description": "Source unit"
                    },
                    "to_unit": {
                        "type": "string",
                        "description": "Target unit"
                    }
                },
                "required": ["value", "from_unit", "to_unit"]
            }
        )

        self.conversions = {
            ("m", "km"): 0.001,
            ("km", "m"): 1000,
            ("m", "cm"): 100,
            ("cm", "m"): 0.01,
            ("kg", "g"): 1000,
            ("g", "kg"): 0.001,
            ("celsius", "kelvin"): lambda x: x + 273.15,
            ("kelvin", "celsius"): lambda x: x - 273.15,
            ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        }

    def execute(
        self,
        value: float,
        from_unit: str,
        to_unit: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convert units.
        转换单位。

        Args:
            value: Value to convert / 要转换的值
            from_unit: Source unit / 源单位
            to_unit: Target unit / 目标单位

        Returns:
            Conversion result / 转换结果
        """
        try:
            key = (from_unit.lower(), to_unit.lower())

            if key in self.conversions:
                conversion = self.conversions[key]
                if callable(conversion):
                    result = conversion(value)
                else:
                    result = value * conversion

                return {
                    "success": True,
                    "value": value,
                    "from_unit": from_unit,
                    "to_unit": to_unit,
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": f"Conversion from {from_unit} to {to_unit} not supported"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
