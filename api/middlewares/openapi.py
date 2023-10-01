# from drf_spectacular.extensions import OpenApiAuthenticationExtension
# from api.middlewares.api_middlewares import FirebaseAuthentication


# class FirebaseAuthenticationExtension(OpenApiAuthenticationExtension):
#     target_class = FirebaseAuthentication
#     name = "Firebase JWT Auth"

#     def get_security_definition(self, auto_schema):
#         return {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }

#     def get_security_requirement(self, auto_schema):
#         return [{"Authorization": []}]


# firebase_authentication = FirebaseAuthentication()
# firebase_authentication_extension = FirebaseAuthenticationExtension(
#     target=firebase_authentication
# )
