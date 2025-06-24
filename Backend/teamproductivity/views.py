from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .Serializers import *
import pandas as pd
from .chatbot import query_db_view



class TeamsView (APIView):

    def get(self,request):
        teams = Teams.objects.all()
        teams_serialize = TeamsSerializer(teams,many = True)

        team_names = [team["name"] for team in teams_serialize.data]
        response = {"teams":team_names}

        return Response(response)
    

class SprintView (APIView) : 

    def get(self,request):
        sprints = Sprint.objects.all()
        sprint_serialize = SprintSerializer(sprints,many = True)

        sprint_names = [sprint["name"] for sprint in sprint_serialize.data]
        response = {"sprints":sprint_names}

        return Response(response)


class metricsView (APIView):
  
    def get (self ,request,team_name,sprint_name):

        team = Teams.objects.get(name = team_name)
        team_id = team.id
        sprint = Sprint.objects.get(name = sprint_name)
        sprint_id = sprint.id
        
        issues = Issue.objects.filter(sprint = sprint,team = team )
        print("Request Received") 
        if not issues.exists():
            return Response({"message": "No issues found for the given sprint and team."},status =404)
        
        issue_serialize = IssueSerializer(issues ,many=True)
        issue_df = pd.DataFrame(issue_serialize.data)

        if 'created_at' not in issue_df.columns or 'resolved_at' not in issue_df.columns:
            return Response({"message": "Missing necessary timestamps in issue data."}, status=400)
        
        issue_df['created_at'] = pd.to_datetime(issue_df['created_at'])
        issue_df['resolved_at'] = pd.to_datetime(issue_df['resolved_at'])

        issue_df['resolution_time'] = (issue_df['resolved_at'] - issue_df['created_at']).dt.days
        mttr =issue_df['resolution_time'].mean()
 
        velocity = len(issue_df)

        return Response({
            "sprint_id": sprint_name,
            "velocity": velocity,
            "mttr": round(mttr, 2) if mttr is not None else None
        }) 

class ChatbotView(APIView):

    def post(self,request):
        print("QUERY REQUEST RECEIVED")
        query = request.data.get('user_query')
        print("Query:",query)
        
        response = query_db_view(query)
        print("RESPONSE:",response)

        return Response({"response":response})


