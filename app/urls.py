from django.urls import path, re_path, include
from app import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'residences', views.ResidenceViewSet)
router.register(r'visitortypes', views.visitorTypeViewSet)
router.register(r'visitorvalidity', views.visitorValidityViewSet)
router.register(r'visitors', views.VisitorViewSet)
router.register(r'residents', views.ResidentViewSet)
router.register(r'statuses', views.StatusViewSet)
router.register(r'inouts', views.InoutsViewSet)

router.register(r'residencesyndics', views.ResidenceSyndicsViewSet)
router.register(r'residenceareas', views.ResidenceAreasViewSet)

router.register(r'appusertype', views.AppUserTypesViewSet)
router.register(r'appuser', views.AppUserViewSet)

router.register(r'residence_type', views.ResidenceTypeViewSet)
router.register(r'access_type', views.visitorAccessTypesViewSet)

router.register(r'user_assigned_areas', views.AppUserAssignedAreasViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/visitor/', views.SearchVisitor.as_view(), name="searchvisitor"),
    path('api/visitorstatus/', views.SearchVisitorStatus.as_view(), name="searchvisitorstatus"),
    path('api/visitorbycode/', views.SearchVisitorByCode.as_view(actions={'get': 'list'})),  
    path('api/loginappuser/', views.LoginAppUserViewSet.as_view(actions={'get': 'list'})),
    path('api/connection_requests/', views.ConnectionRequestsViewSet.as_view(actions={'get': 'list'})),
    path('api/connections/', views.ConnectionsViewSet.as_view(actions={'get': 'list'})),
    path('api/syndicsbyresidence/', views.SyndicsByResidence.as_view(actions={'get': 'list'})),
    path('api/areasbyresidence/', views.AreasByResidence.as_view(actions={'get': 'list'})),
    path('api/appusersbyparent/', views.AppUsersByParent.as_view(actions={'get': 'list'})),
    path('api/residencesbyparent/', views.ResidencesByParent.as_view(actions={'get': 'list'})),
    path('api/residencebyarea/', views.ResidenceByArea.as_view(actions={'get': 'list'})),
    path('api/usertypesbyparent/', views.UserTypesByParent.as_view(actions={'get': 'list'})),
    path('api/areabycode/', views.AreaByCode.as_view(actions={'get': 'list'})),
    path('api/agent/', views.AgentByPasscodeAndArea.as_view(actions={'get': 'list'})),
    path('api/residencesbyuser/', views.ResidencesByUser.as_view(actions={'get': 'list'})),
    path('api/connectionsbyarea/', views.ConnectionsByArea.as_view(actions={'get': 'list'})),
    path('api/residentsbyarea/', views.ResidentsByArea.as_view(actions={'get': 'list'})),
    path('api/residentsbyareaf/', views.ResidentsByAreaF.as_view(actions={'get': 'list'})),
    path('api/residentsbycode/', views.ResidentsByCode.as_view(actions={'get': 'list'})),
    path('api/residentsbyemail/', views.ResidentsByEmail.as_view(actions={'get': 'list'})),
    path('api/residentsbyemailandphone/', views.ResidentsByEmailAndPhone.as_view(actions={'get': 'list'})),
    path('api/appusersbyemail/', views.AppUsersByEmail.as_view(actions={'get': 'list'})),
    path('api/appusersbyparent/', views.AppUsersByParent.as_view(actions={'get': 'list'})),
    path('api/appusersbyarea/', views.AppUsersByArea.as_view(actions={'get': 'list'})),
    path('api/appusersbyareaandtype/', views.AppUsersByAreaAndType.as_view(actions={'get': 'list'})),
    path('api/agentsbyparent/', views.AgentsByParent.as_view(actions={'get': 'list'})),
    path('api/appuserassignedareas/', views.AppUserByAssignedArea.as_view(actions={'get': 'list'})),
    path('api/searchareas/', views.SearchArea.as_view(actions={'get': 'list'})),
    path('api/searchvisitornew/', views.SearchVisitorNew.as_view(actions={'get': 'list'})),
    path('api/visitorsByResident/', views.VisitorsByResident.as_view(actions={'get': 'list'})),
    path('api/searchvisitornewnew/', views.SearchVisitorNewNew.as_view()),
    path('api/checkloginvalidity/', views.CheckLoginValidity.as_view()),
    path('api/searchresident/', views.SearchResidents.as_view(actions={'get': 'list'})),
]
