from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
from io import StringIO
from .serializers import UserSerializer
from .models import User

def csv_upload_view(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        if not file.name.endswith('.csv'):
            return render(request, 'upload_csv.html', {"error": "Invalid file type. Only .csv files are allowed."})

        try:
            data = StringIO(file.read().decode('utf-8'))
            reader = csv.DictReader(data)
        except Exception:
            return render(request, 'upload_csv.html', {"error": "Failed to read the CSV file."})

        total_records = 0
        valid_records = 0
        invalid_records = 0
        errors = []

        for row_num, row in enumerate(reader, start=1):
            total_records += 1
            serializer = UserSerializer(data=row)

            if serializer.is_valid():
                serializer.save()
                valid_records += 1
            else:
                invalid_records += 1
                errors.append({"row": row_num, "errors": serializer.errors})

        response_data = {
            "total_records": total_records,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "errors": errors
        }

        return render(request, 'upload_csv.html', {"response_data": response_data})

    return render(request, 'upload_csv.html')
