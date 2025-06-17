from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.renderers import JSONRenderer

class SpectacularJSONAPIView(SpectacularAPIView):
    """
    OpenAPI JSON view for API documentation
    """
    renderer_classes = [JSONRenderer]


class SpectacularSwaggerViewTopBar(SpectacularSwaggerView):
    """
    Custom swagger UI adding topbar
    """
    template_name = 'drf_spectacular_mod/swagger_ui.html'