from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from match_event.views import MatchEventListAPIView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Api
    path("acb-api/pbp-lean/<int:game_id>", MatchEventListAPIView.as_view(), name="match_event_list"),
]
