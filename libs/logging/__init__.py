import logging

from libs.logging.adapters import FootprintTraceAdapter


trace_logger = logging.getLogger('trace')


def get_tracer(request):
    return FootprintTraceAdapter(trace_logger, extra=dict(request=request))
