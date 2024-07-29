from rest_framework import serializers

class CustomModelSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)
        if not is_valid and not raise_exception:
            self._errors = self.format_errors(self.errors)
        return is_valid

    def format_errors(self, errors):
        formatted_errors = {}
        for field, field_errors in errors.items():
            if isinstance(field_errors, list):
                formatted_errors[field] = ' '.join(field_errors)
            else:
                formatted_errors[field] = str(field_errors)
        return formatted_errors