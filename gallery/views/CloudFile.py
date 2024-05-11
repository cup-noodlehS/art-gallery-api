from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from faso.utils import upload_to_cloudinary, delete_from_cloudinary


class CloudFile(APIView):
    def post(self, request):
        file = request.data.get('file', None)
        width = request.data.get('width', 600)
        height = request.data.get('height', 800)
        crop = request.data.get('crop', 'fill')
        folder = request.data.get('folder', 'default')
        if file is not None:
            try:
                print(file, 'file')
                url = upload_to_cloudinary(file, folder, width, height, crop)
                return Response({'url': url})
            except:
                return Response({'error': 'Error uploading file'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        file_url = request.data.get('url', None)
        folder = request.data.get('folder', None)
        print(request.data, 'request')
        if file_url is not None and folder is not None:
            print('heree')
            try:
                res = delete_from_cloudinary(file_url, folder)
                return Response(res)
            except:
                return Response({'error': 'Delete Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)