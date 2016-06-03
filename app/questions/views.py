from rest_framework import permissions, status, views
from rest_framework.response import Response
from topics.models import Topic
from topics.serializers import SimpleTopicSerializer
from questions.models import Question
from questions.serializers import QuestionSerializer, SimpleQuestionSerializer
from posts.models import Post
import difflib


class QuestionView(views.APIView):
    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get questions related to keyword provided
        if request.GET.get('keyword') is not None:
            questions = [elem.question for elem in Question.objects.all()]
            question_names = difflib.get_close_matches(
                request.GET.get('keyword'),
                questions,
                10,
                0.2
            )
            result = Question.objects.all().filter(name__in=question_names)
            serializer = SimpleQuestionSerializer(result, many=True)
            return Response(serializer.data)


class QuestionDetailView(views.APIView):
    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get a specific question
        if request.GET.get('questionID') is not None:
            question = Question.objects.get(pk=request.GET.get('questionID'))
            serializer = QuestionSerializer(question)
            return Response(serializer.data)

    def post(self, request, format=None):
        # Post new question
        post = Post.objects.create(
            content=request.data.get('content'),
            created_by=request.user.a2ausers
        )
        question = Question.objects.create(
            question=request.data.get('question'),
            post=post
        )
        serializer = SimpleTopicSerializer(
            request.data.get('topics'),
            many=True
        )
        for elem in serializer.data:
            topic = Topic.objects.get(elem.id)
            question.add(topic)
        question.save()

    def put(self, request, format=None):
        # Update a question
        if request.GET.get('questionID') is not None:
            id = request.GET.get('questionID')
            question = Question.objects.get(pk=id)
            question.question = request.data.get('question')
            question.post.content = request.data.get('content')
            question.save()
            return Response(status=status.HTTP_200_OK)


class QuestionTopicView(views.APIView):

    def get_permissions(self):
        if self.request.method in 'GET':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def get(self, request, format=None):
        # Get all topics for question with id specified
        if request.GET.get('questionID') is not None:
            questionID = request.GET.get('questionID')
            question = Question.objects.get(pk=questionID)
            serializer = SimpleTopicSerializer(
                question.topics.all(),
                many=True
            )
            return Response(serializer.data)

    def post(self, request, format=None):
        # Add new topic to question with id specified
        new_topic = Topic.objects.get(pk=request.data.get('id'))
        question = Question.objects.get(pk=request.GET.get('questionID'))
        topics = [topic.id for topic in question.topics.all()]
        if new_topic.id in topics:
            return Response({
                'message': 'Topic existed in question'
            }, status=status.HTTP_400_BAD_REQUEST)
        question.topics.add(topic)
        question.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        # Remove a topic from question with id specified
        if request.GET.get('questionID') is not None:
            delete_topic = Topic.objects.get(pk=request.data.get('id'))
            question = Question.objects.get(
                pk=request.GET.get('questionID')
            )
            topics = [topic.id for topic in question.topics.all()]
            if delete_topic.id not in topics:
                return Response({
                    'message': 'Topic not available in question'
                }, status=status.HTTP_400_BAD_REQUEST)
            question.topics.remove(topic)
            question.save()
        return Response(status=status.HTTP_200_OK)
