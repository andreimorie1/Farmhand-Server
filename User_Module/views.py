from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Farmer

@api_view(['POST'])
def register_farmer(request):
    """
    Registers a farmer with firstname, lastname, and hashed password.
    Ensures duplicate registrations are prevented.
    """
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    password = request.data.get('password')

    # Check if a farmer with the same details already exists
    if Farmer.objects.filter(firstname=firstname).exists():
        return Response(
            {'register': False, 'message': 'User already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create a new farmer entry
    farmer = Farmer(firstname=firstname, lastname=lastname)
    farmer.set_password(password)  # Hash the password before saving
    farmer.save()

    return Response(
        {'register': True, 'message': 'Success'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def login_farmer(request):
    """
    Authenticates a farmer using firstname and password.
    """
    firstname = request.data.get('firstname')
    password = request.data.get('password')

    # Check if a farmer with the given firstname exists
    try:
        farmer = Farmer.objects.get(firstname=firstname)
        if farmer.check_password(password):  # Compare the hashed password
            return Response(
                {'login': True, 'message': 'Success', 'farmerId': farmer.id},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'login': False, 'message': 'Incorrect password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Farmer.DoesNotExist:
        return Response(
            {'login': False, 'message': 'User does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def update_farmer(request):
    """
    Updates a farmer's account details (firstname, lastname, password).
    """
    farmer_id = request.data.get('id')  # Get the farmer ID from the request body

    if not farmer_id:
        return Response(
            {'update': False, 'message': 'Farmer ID is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Ensure that the farmer exists
    try:
        farmer = Farmer.objects.get(id=farmer_id)

        # Update only provided fields
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        password = request.data.get('password')

        if firstname:
            farmer.firstname = firstname
        if lastname:
            farmer.lastname = lastname
        if password:
            farmer.set_password(password)

        farmer.save()

        return Response(
            {'update': True, 'message': 'Success', 'farmerId': farmer.id},
            status=status.HTTP_200_OK
        )

    except Farmer.DoesNotExist:
        return Response(
            {'update': False, 'message': 'Farmer not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
def delete_farmer(request):
    """
    Deletes a farmer's account.
    Requires either the authenticated user or the farmer ID to identify the account to delete.
    """
    farmer_id = request.data.get('id')  # Optional: Pass farmer ID in the request body for flexibility

    try:
        if farmer_id:
            # Find the farmer using the provided ID
            farmer = Farmer.objects.get(id=farmer_id)
        else:
            # If no ID is provided, use the authenticated user
            user = request.user
            farmer = Farmer.objects.get(id=user.id)

        # Delete the farmer account
        farmer.delete()

        return Response(
            {'delete': True, 'message': 'Account successfully deleted'},
            status=status.HTTP_200_OK
        )
    except Farmer.DoesNotExist:
        return Response(
            {'delete': False, 'message': 'Farmer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'delete': False, 'message': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(['POST'])  # Changed to POST
def get_farmer(request):
    """
    Retrieves farmer details by their ID (POST method).
    Expects farmer_id in the request body.
    """
    farmer_id = request.data.get('id')  # Getting farmer_id from the request body

    if not farmer_id:
        return Response(
            {'message': 'Farmer ID is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Get the farmer by their ID
        farmer = Farmer.objects.get(id=farmer_id)

        # Return farmer details
        return Response(
            {
                'farmerId': farmer.id,
                'firstname': farmer.firstname,
                'lastname': farmer.lastname,
                'message': 'Farmer details fetched successfully'
            },
            status=status.HTTP_200_OK
        )
    except Farmer.DoesNotExist:
        return Response(
            {'message': 'Farmer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'message': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )