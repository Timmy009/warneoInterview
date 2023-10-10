class UserExceptionHandler:
    @staticmethod
    def handle_exception(exception):
        # You can customize this method to handle specific exceptions if needed
        return {'message': str(exception)}, 500  # 500 Internal Server Error
