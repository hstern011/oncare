from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import RevisionSerializer, VisitSerializer
from .models import Revision, Visit

# Create your views here.

# Returns the most recent schedule/revision
class LatestRevisionAPIView(views.APIView):
    def get(self, request):
        revision = Revision.objects.order_by("-create_date_time").first() # Get the most recent schedule/revision
        if revision is None:
            return Response([], status=status.HTTP_200_OK)

        serializer = RevisionSerializer(revision)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Returns all revisions
class AllRevisionsAPIView(views.APIView):
    def get(self, request):
        revisions = Revision.objects.order_by("-create_date_time")
        serializer = RevisionSerializer(revisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Returns a specific revision
class GetRevisionAPIView(views.APIView):
    def get(self, request, revision_id):
            try:
                revision = Revision.objects.get(id=revision_id)
            except Revision.DoesNotExist:
                return Response([], status=status.HTTP_200_OK)
            serializer = RevisionSerializer(revision)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Create a new revision based on the old one, possibly removing a visit with a given ID
def new_revision(remove_id = None):

    # Retrieve the stored visits from the latest revision, possibly excluding the given visit id
    try:
        prev_visit_set = Revision.objects.latest('create_date_time').visit_set.all().exclude(public_id=remove_id)
    except Revision.DoesNotExist: # If there are no revisions yet
        prev_visit_set = []
    
    revision = Revision()
    revision.save()

    # Add the previous visit set
    revision.visit_set.set(prev_visit_set)

    return revision

# Provides a POST endpoint for adding a new visit
class AddVisitAPIView(views.APIView):
    def post(self, request):

        data = {
            'start_date_time': request.data.get('start_date_time'),
            'end_date_time': request.data.get('end_date_time'),
            'client': request.data.get('client'), 
            'carer': request.data.get('carer')
        }

        # Deserialize data 
        serializer = VisitSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new revision with the contents of the previous one
        revision = new_revision()

        # Save the new visit and instantiate visit object
        visit = serializer.save()

        # Now add the new visit to the new revision
        revision.visit_set.add(visit)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Provides PUT and DELETE endpoints for 'updating' and 'removing' visits
class UpdateDeleteVisitAPIView(views.APIView):
    # To 'update' a given visit id
    def put(self, request, public_id):
        # Attempt to retrieve visit with the given id
        try:
            visit_instance = Visit.objects.filter(public_id=public_id)
        except ValidationError: #Raised when a non-valid UUID is provided
            return Response(
                {"res": "Not a valid id"}, 
                status=status.HTTP_400_BAD_3REQUEST
            )
        if not visit_instance:
            return Response(
                {"res": "Object with given id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'start_date_time': request.data.get('start_date_time'),
            'end_date_time': request.data.get('end_date_time'),
            'client': request.data.get('client'), 
            'carer': request.data.get('carer'),
            'public_id': public_id 
        }

        # Deserialize data
        serializer = VisitSerializer(data=data)
        if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new revision without the previous version of the visit
        revision = new_revision(remove_id=public_id)
        
        # Save the new visit
        visit = serializer.save()

        # Then add the updated visit details
        revision.visit_set.add(visit)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # To 'delete' a given visit id
    def delete(self, request, public_id):
        # Attempt to retrieve visit with the given id
        visit_instance = Visit.objects.filter(public_id=public_id)
        if not visit_instance:
            return Response(
                {"res": "Object with given id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new revision without the given visit
        new_revision = new_revision(remove_id=public_id)
        
        return Response(status=status.HTTP_200_OK)

        