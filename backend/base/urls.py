from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from match_event.views import GameBiggestLeadAPIView, GameLeadersAPIView, PBPLeanAPIView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Api
    path("acb-api/pbp-lean/<int:game_id>", PBPLeanAPIView.as_view(), name="pbp_lean"),
    path(
        "acb-api/game-leaders/<int:game_id>",
        GameLeadersAPIView.as_view(),
        name="game_leaders",
    ),
    path(
        "acb-api/game-biggest_lead/<int:game_id>",
        GameBiggestLeadAPIView.as_view(),
        name="game_biggest_lead",
    ),
]
