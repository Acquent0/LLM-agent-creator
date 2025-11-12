"""
Data Analysis and Visualization Tools / 数据分析和可视化工具

Tools for data processing, analysis, and visualization.
用于数据处理、分析和可视化的工具。

Author: LLM Agent Framework
License: MIT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from core.tool import Tool


class DataAnalysisTool(Tool):
    """
    Data analysis tool using Pandas.
    使用Pandas的数据分析工具。

    Analyze datasets with statistical and data manipulation operations.
    使用统计和数据操作对数据集进行分析。
    """

    def __init__(self):
        super().__init__(
            name="data_analysis",
            description="Analyze datasets: load, filter, aggregate, summarize data",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'describe', 'filter', 'aggregate', 'correlation'"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data as dict or list of dicts"
                    },
                    "params": {
                        "type": "object",
                        "description": "Operation parameters"
                    }
                },
                "required": ["operation", "data"]
            }
        )

    def execute(
        self,
        operation: str,
        data: Any,
        params: Dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform data analysis operation.
        执行数据分析操作。

        Args:
            operation: Analysis operation / 分析操作
            data: Input data / 输入数据
            params: Additional parameters / 额外参数

        Returns:
            Analysis result / 分析结果
        """
        try:
            df = pd.DataFrame(data)
            params = params or {}

            if operation == "describe":
                return self._describe(df)
            elif operation == "filter":
                return self._filter(df, params)
            elif operation == "aggregate":
                return self._aggregate(df, params)
            elif operation == "correlation":
                return self._correlation(df)
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

    def _describe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate descriptive statistics. / 生成描述性统计。"""
        description = df.describe().to_dict()

        return {
            "success": True,
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "statistics": description,
            "missing_values": df.isnull().sum().to_dict()
        }

    def _filter(self, df: pd.DataFrame, params: Dict) -> Dict[str, Any]:
        """Filter dataframe. / 过滤数据框。"""
        column = params.get("column")
        condition = params.get("condition", "==")
        value = params.get("value")

        if condition == "==":
            filtered = df[df[column] == value]
        elif condition == ">":
            filtered = df[df[column] > value]
        elif condition == "<":
            filtered = df[df[column] < value]
        elif condition == ">=":
            filtered = df[df[column] >= value]
        elif condition == "<=":
            filtered = df[df[column] <= value]
        else:
            return {
                "success": False,
                "error": f"Unknown condition: {condition}"
            }

        return {
            "success": True,
            "filtered_count": len(filtered),
            "data": filtered.to_dict(orient="records")
        }

    def _aggregate(self, df: pd.DataFrame, params: Dict) -> Dict[str, Any]:
        """Aggregate data. / 聚合数据。"""
        group_by = params.get("group_by")
        agg_func = params.get("function", "mean")

        if group_by:
            grouped = df.groupby(group_by)

            if agg_func == "mean":
                result = grouped.mean()
            elif agg_func == "sum":
                result = grouped.sum()
            elif agg_func == "count":
                result = grouped.count()
            else:
                return {
                    "success": False,
                    "error": f"Unknown aggregation function: {agg_func}"
                }

            return {
                "success": True,
                "aggregation": result.to_dict()
            }
        else:
            return {
                "success": False,
                "error": "group_by parameter required"
            }

    def _correlation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlation matrix. / 计算相关矩阵。"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) < 2:
            return {
                "success": False,
                "error": "Need at least 2 numeric columns for correlation"
            }

        corr = df[numeric_cols].corr()

        return {
            "success": True,
            "correlation_matrix": corr.to_dict()
        }


class VisualizationTool(Tool):
    """
    Data visualization tool.
    数据可视化工具。

    Create charts and plots using Matplotlib and Plotly.
    使用Matplotlib和Plotly创建图表和绘图。
    """

    def __init__(self, output_dir: str = "./outputs"):
        super().__init__(
            name="visualization",
            description="Create data visualizations: line plots, bar charts, scatter plots, histograms",
            parameters={
                "type": "object",
                "properties": {
                    "chart_type": {
                        "type": "string",
                        "description": "Chart type: 'line', 'bar', 'scatter', 'histogram', 'box'"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to visualize"
                    },
                    "params": {
                        "type": "object",
                        "description": "Chart parameters (title, labels, etc.)"
                    }
                },
                "required": ["chart_type", "data"]
            }
        )
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def execute(
        self,
        chart_type: str,
        data: Any,
        params: Dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create visualization.
        创建可视化。

        Args:
            chart_type: Type of chart / 图表类型
            data: Data to visualize / 要可视化的数据
            params: Chart parameters / 图表参数

        Returns:
            Visualization result / 可视化结果
        """
        try:
            df = pd.DataFrame(data)
            params = params or {}

            title = params.get("title", "Chart")
            x_col = params.get("x_column")
            y_col = params.get("y_column")

            if chart_type == "line":
                return self._line_plot(df, x_col, y_col, title)
            elif chart_type == "bar":
                return self._bar_chart(df, x_col, y_col, title)
            elif chart_type == "scatter":
                return self._scatter_plot(df, x_col, y_col, title)
            elif chart_type == "histogram":
                return self._histogram(df, x_col, title)
            elif chart_type == "box":
                return self._box_plot(df, y_col, title)
            else:
                return {
                    "success": False,
                    "error": f"Unknown chart type: {chart_type}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart_type": chart_type
            }

    def _line_plot(self, df: pd.DataFrame, x: str, y: str, title: str) -> Dict[str, Any]:
        """Create line plot. / 创建折线图。"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x] if x else df.index,
            y=df[y],
            mode='lines+markers',
            name=y
        ))
        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y)

        output_path = os.path.join(self.output_dir, f"line_plot_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html")
        fig.write_html(output_path)

        return {
            "success": True,
            "chart_type": "line",
            "output_path": output_path,
            "message": f"Line plot saved to {output_path}"
        }

    def _bar_chart(self, df: pd.DataFrame, x: str, y: str, title: str) -> Dict[str, Any]:
        """Create bar chart. / 创建条形图。"""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df[x] if x else df.index,
            y=df[y],
            name=y
        ))
        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y)

        output_path = os.path.join(self.output_dir, f"bar_chart_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html")
        fig.write_html(output_path)

        return {
            "success": True,
            "chart_type": "bar",
            "output_path": output_path,
            "message": f"Bar chart saved to {output_path}"
        }

    def _scatter_plot(self, df: pd.DataFrame, x: str, y: str, title: str) -> Dict[str, Any]:
        """Create scatter plot. / 创建散点图。"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y],
            mode='markers',
            name=f"{x} vs {y}"
        ))
        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y)

        output_path = os.path.join(self.output_dir, f"scatter_plot_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html")
        fig.write_html(output_path)

        return {
            "success": True,
            "chart_type": "scatter",
            "output_path": output_path,
            "message": f"Scatter plot saved to {output_path}"
        }

    def _histogram(self, df: pd.DataFrame, column: str, title: str) -> Dict[str, Any]:
        """Create histogram. / 创建直方图。"""
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df[column], name=column))
        fig.update_layout(title=title, xaxis_title=column, yaxis_title="Frequency")

        output_path = os.path.join(self.output_dir, f"histogram_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html")
        fig.write_html(output_path)

        return {
            "success": True,
            "chart_type": "histogram",
            "output_path": output_path,
            "message": f"Histogram saved to {output_path}"
        }

    def _box_plot(self, df: pd.DataFrame, column: str, title: str) -> Dict[str, Any]:
        """Create box plot. / 创建箱线图。"""
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[column], name=column))
        fig.update_layout(title=title, yaxis_title=column)

        output_path = os.path.join(self.output_dir, f"box_plot_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html")
        fig.write_html(output_path)

        return {
            "success": True,
            "chart_type": "box",
            "output_path": output_path,
            "message": f"Box plot saved to {output_path}"
        }


class DataCleaningTool(Tool):
    """
    Data cleaning and preprocessing tool.
    数据清洗和预处理工具。

    Handle missing values, outliers, and data transformations.
    处理缺失值、异常值和数据转换。
    """

    def __init__(self):
        super().__init__(
            name="data_cleaning",
            description="Clean and preprocess data: handle missing values, remove duplicates, normalize",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation: 'remove_duplicates', 'fill_missing', 'remove_outliers', 'normalize'"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to clean"
                    },
                    "params": {
                        "type": "object",
                        "description": "Operation parameters"
                    }
                },
                "required": ["operation", "data"]
            }
        )

    def execute(
        self,
        operation: str,
        data: Any,
        params: Dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Clean data.
        清洗数据。

        Args:
            operation: Cleaning operation / 清洗操作
            data: Input data / 输入数据
            params: Operation parameters / 操作参数

        Returns:
            Cleaned data / 清洗后的数据
        """
        try:
            df = pd.DataFrame(data)
            params = params or {}

            if operation == "remove_duplicates":
                cleaned = df.drop_duplicates()
            elif operation == "fill_missing":
                method = params.get("method", "mean")
                if method == "mean":
                    cleaned = df.fillna(df.mean())
                elif method == "median":
                    cleaned = df.fillna(df.median())
                elif method == "forward":
                    cleaned = df.fillna(method='ffill')
                else:
                    cleaned = df.fillna(0)
            elif operation == "remove_outliers":
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())
                cleaned = df[(z_scores < 3).all(axis=1)]
            elif operation == "normalize":
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                cleaned = df.copy()
                cleaned[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }

            return {
                "success": True,
                "operation": operation,
                "original_shape": df.shape,
                "cleaned_shape": cleaned.shape,
                "data": cleaned.to_dict(orient="records")
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "operation": operation
            }
