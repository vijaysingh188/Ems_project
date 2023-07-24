from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Lift,Floor,LiftDetails
from .serializers import LiftSerializer,FloorSerializer,LiftDetailsSerializer
from rest_framework import viewsets
from django.db.models import Subquery, F, Min, Value
from pprint import pprint

class LiftView(viewsets.ModelViewSet):
    serializer_class = LiftSerializer

    def get_queryset(self):
        return Lift.objects.all()


class FloorView(viewsets.ModelViewSet):
    serializer_class = FloorSerializer

    def get_queryset(self):
        return Floor.objects.all()


class LiftDetailsView(viewsets.ModelViewSet):
    serializer_class = LiftDetailsSerializer

    def get_queryset(self):
        return LiftDetails.objects.all()

    
def get_lift_data(pk):
        ##       first_case:if user is on the same floor and as well as the lift too...###
        if LiftDetails.objects.filter(current_status=pk).values():
            queryset = LiftDetails.objects.filter(current_status=pk)

        ###      second case: nearest_lift should come:.............####

        elif LiftDetails.objects.filter(id__gt=pk).order_by('id').first():
            queryset = LiftDetails.objects.filter(id__gt=pk).order_by('id')

        ###      third case: priority which is near the user:.........###

        elif LiftDetails.objects.annotate(id_diff=Min(F('id') - pk, pk - F('id'))).filter(id_diff__gte=0).order_by('id_diff')[:1]:
            queryset = LiftDetails.objects.annotate(id_diff=Min(F('id') - pk, pk - F('id'))).filter(id_diff__gte=0).order_by('id_diff')[:1]


        else:
            queryset = LiftDetails.objects.all()

        return queryset


def update_obj(pk,data_user,queryset):
    print('================update_obj==========================')
    print('===data_user',data_user)
    print('====pk===',pk)
    print('====queryset==',queryset[0])


    id  = (queryset.values_list('id'))[0][0]
    lift_det_id  = (queryset.values_list('lift_det_id'))[0][0]
    whichfloor_id  = (queryset.values_list('whichfloor_id'))[0][0]

    print(id,lift_det_id,whichfloor_id,type(whichfloor_id))

    print(LiftDetails.objects.values('id','lift_det__liftname','whichfloor__floornumber'),'======qqqqqqqqq')

    obj = LiftDetails.objects.filter(id= id,lift_det_id=lift_det_id,whichfloor_id=whichfloor_id).update(current_status=data_user)

    # print(obj,'===========obj')

    return queryset


class ResourceDetailView(APIView):
        
    def get_object(self, pk):    
        try:          
            return LiftDetails.objects.get(pk=pk)
        except LiftDetails.DoesNotExist:
            raise Http404

    def get_queryset(self): 
        pk = self.kwargs.get('pk') 
    
        queryset = get_lift_data(pk)
        return queryset

    def get(self, request,pk,format=None):
       
        queryset = self.get_queryset()      
        print(queryset[0],'=========queryset',type(queryset))
        serializer = LiftDetailsSerializer(queryset[0])
        
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        pk = self.kwargs.get('pk') 
        queryset = get_lift_data(pk)
        data_user = request.data
        query_update = update_obj(pk,data_user,queryset)
        LiftDetails = self.get_object(pk=pk)
        serializer = LiftDetailsSerializer(LiftDetails)
        return Response(serializer.data)


    
        