from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComplianceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    COMPLIANT: _ClassVar[ComplianceStatus]
    WARNING: _ClassVar[ComplianceStatus]
    NON_COMPLIANT: _ClassVar[ComplianceStatus]
    UNKNOWN: _ClassVar[ComplianceStatus]
COMPLIANT: ComplianceStatus
WARNING: ComplianceStatus
NON_COMPLIANT: ComplianceStatus
UNKNOWN: ComplianceStatus

class ChartData(_message.Message):
    __slots__ = ["chart_id", "chart_type", "title", "config", "data_series", "metadata"]
    CHART_ID_FIELD_NUMBER: _ClassVar[int]
    CHART_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DATA_SERIES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chart_id: str
    chart_type: str
    title: str
    config: ChartConfig
    data_series: _containers.RepeatedCompositeFieldContainer[DataSeries]
    metadata: ChartMetadata
    def __init__(self, chart_id: _Optional[str] = ..., chart_type: _Optional[str] = ..., title: _Optional[str] = ..., config: _Optional[_Union[ChartConfig, _Mapping]] = ..., data_series: _Optional[_Iterable[_Union[DataSeries, _Mapping]]] = ..., metadata: _Optional[_Union[ChartMetadata, _Mapping]] = ...) -> None: ...

class ChartConfig(_message.Message):
    __slots__ = ["width", "height", "color_scheme", "show_legend", "show_grid", "x_axis", "y_axis"]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    COLOR_SCHEME_FIELD_NUMBER: _ClassVar[int]
    SHOW_LEGEND_FIELD_NUMBER: _ClassVar[int]
    SHOW_GRID_FIELD_NUMBER: _ClassVar[int]
    X_AXIS_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    color_scheme: str
    show_legend: bool
    show_grid: bool
    x_axis: AxisConfig
    y_axis: AxisConfig
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., color_scheme: _Optional[str] = ..., show_legend: bool = ..., show_grid: bool = ..., x_axis: _Optional[_Union[AxisConfig, _Mapping]] = ..., y_axis: _Optional[_Union[AxisConfig, _Mapping]] = ...) -> None: ...

class AxisConfig(_message.Message):
    __slots__ = ["label", "data_type", "min_value", "max_value", "show_ticks"]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
    SHOW_TICKS_FIELD_NUMBER: _ClassVar[int]
    label: str
    data_type: str
    min_value: float
    max_value: float
    show_ticks: bool
    def __init__(self, label: _Optional[str] = ..., data_type: _Optional[str] = ..., min_value: _Optional[float] = ..., max_value: _Optional[float] = ..., show_ticks: bool = ...) -> None: ...

class DataSeries(_message.Message):
    __slots__ = ["series_name", "data_points", "color", "line_style"]
    SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LINE_STYLE_FIELD_NUMBER: _ClassVar[int]
    series_name: str
    data_points: _containers.RepeatedCompositeFieldContainer[DataPoint]
    color: str
    line_style: str
    def __init__(self, series_name: _Optional[str] = ..., data_points: _Optional[_Iterable[_Union[DataPoint, _Mapping]]] = ..., color: _Optional[str] = ..., line_style: _Optional[str] = ...) -> None: ...

class DataPoint(_message.Message):
    __slots__ = ["string_x", "numeric_x", "timestamp_x", "y_value", "label", "metadata"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STRING_X_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_X_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_X_FIELD_NUMBER: _ClassVar[int]
    Y_VALUE_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    string_x: str
    numeric_x: float
    timestamp_x: int
    y_value: float
    label: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, string_x: _Optional[str] = ..., numeric_x: _Optional[float] = ..., timestamp_x: _Optional[int] = ..., y_value: _Optional[float] = ..., label: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ChartMetadata(_message.Message):
    __slots__ = ["data_source", "generated_at", "generated_by", "tags"]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    data_source: str
    generated_at: int
    generated_by: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, data_source: _Optional[str] = ..., generated_at: _Optional[int] = ..., generated_by: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class EnvironmentalMetricsChart(_message.Message):
    __slots__ = ["metric_type", "measurement_unit", "metric_points", "thresholds"]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_UNIT_FIELD_NUMBER: _ClassVar[int]
    METRIC_POINTS_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    metric_type: str
    measurement_unit: str
    metric_points: _containers.RepeatedCompositeFieldContainer[MetricDataPoint]
    thresholds: MetricThresholds
    def __init__(self, metric_type: _Optional[str] = ..., measurement_unit: _Optional[str] = ..., metric_points: _Optional[_Iterable[_Union[MetricDataPoint, _Mapping]]] = ..., thresholds: _Optional[_Union[MetricThresholds, _Mapping]] = ...) -> None: ...

class MetricDataPoint(_message.Message):
    __slots__ = ["timestamp", "value", "location", "measurement_method", "compliance_status"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    COMPLIANCE_STATUS_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    value: float
    location: str
    measurement_method: str
    compliance_status: ComplianceStatus
    def __init__(self, timestamp: _Optional[int] = ..., value: _Optional[float] = ..., location: _Optional[str] = ..., measurement_method: _Optional[str] = ..., compliance_status: _Optional[_Union[ComplianceStatus, str]] = ...) -> None: ...

class MetricThresholds(_message.Message):
    __slots__ = ["warning_threshold", "critical_threshold", "target_value"]
    WARNING_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    TARGET_VALUE_FIELD_NUMBER: _ClassVar[int]
    warning_threshold: float
    critical_threshold: float
    target_value: float
    def __init__(self, warning_threshold: _Optional[float] = ..., critical_threshold: _Optional[float] = ..., target_value: _Optional[float] = ...) -> None: ...
